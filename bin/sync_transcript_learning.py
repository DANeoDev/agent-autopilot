#!/usr/bin/env python3
"""
Autonomous Conversation Transcript Learning Sync (Closed-Loop Ingestion)

Bridges active agent conversation transcripts directly into the Autopilot Cognitive
Engine by:
1. Locating the active conversation transcript (or specified conversation ID).
2. Extracting authentic user requests, stripping system wrappers and meta-tokens.
3. Tracking processed step indices in a persistent state file to prevent duplicate training.
4. Computing objective empirical ground truth (X*, Y*) based on:
   - Affective/correction feedback cues ("sadly", "still", "wasnt there", "fix" -> X* >= 2.6)
   - Punch-list complexity and technical domain density (X* = 2.2 - 2.5)
   - Prompt viability score Q for confidence-weighted SGD (eff_lr = lr * Q^2)
5. Updating local cognitive weights and appending to telemetry history.
"""

import sys
import os
import re
import json
import glob
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Tuple

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from bin.cognitive_engine import CognitiveEngine, evaluate_prompt_viability, tokenize_words

DEFAULT_BRAIN_DIR = Path.home() / ".gemini" / "antigravity" / "brain"
DEFAULT_STATE_FILE = Path.home() / ".gemini" / "autopilot" / "telemetry" / "ingested_steps.json"


def find_latest_transcript() -> Optional[Path]:
    """Finds the most recently modified transcript.jsonl across all brain conversation dirs."""
    if not DEFAULT_BRAIN_DIR.exists():
        return None

    transcripts = list(DEFAULT_BRAIN_DIR.glob("*/.system_generated/logs/transcript.jsonl"))
    if not transcripts:
        # Fallback to alternate log structure if present
        transcripts = list(DEFAULT_BRAIN_DIR.glob("*/logs/transcript.jsonl"))

    if not transcripts:
        return None

    # Sort by modification time descending
    transcripts.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return transcripts[0]


def clean_user_prompt(raw_text: str) -> Optional[str]:
    """
    Strips XML wrappers (<USER_REQUEST>, <CONTEXT_SUMMARY>, etc.) and extracts
    the authentic user prompt text. Returns None if prompt is purely synthetic.
    """
    if not raw_text:
        return None

    # Skip internal system notifications or context summaries
    if "<CONTEXT_SUMMARY>" in raw_text or "<system>" in raw_text:
        return None

    text = raw_text
    # Extract inside <USER_REQUEST> if present
    match = re.search(r"<USER_REQUEST>(.*?)</USER_REQUEST>", text, re.DOTALL)
    if match:
        text = match.group(1)

    # Strip any stray XML tags
    text = re.sub(r"<[^>]+>", "", text).strip()

    # Skip empty or trivial approvals (like single-word approvals without instructions)
    if not text or len(text.split()) < 2:
        return None

    return text


def compute_ground_truth(prompt: str, viability: Dict[str, Any]) -> Tuple[float, float, List[str]]:
    """
    Computes empirical ground-truth target (X*, Y*) based on task attributes:
    - High-regression signals ("sadly", "still", "not there yet", "wasnt there") -> X* >= 2.6
    - Punch-list requests with 5+ items or dense architecture -> X* = 2.2 - 2.5
    - Mathematical / algorithm / formal proof terms -> Y* = 1.8 - 2.5
    - Standard routine turn -> X* = 1.8 - 2.2, Y* = 0.8 - 1.2
    """
    clean = prompt.lower()
    words = tokenize_words(clean)
    num_words = len(words)

    delta_reasons = []

    # 1. Regression & Correction Signals
    regression_cues = ["sadly", "still", "again", "forgot", "missed", "broken", "revert", "wasnt", "not yet"]
    has_regression = any(c in clean for c in regression_cues)

    # 2. Punch-list item counts
    item_matches = len(re.findall(r"(?:^|\n)\s*(?:\d+[\.\)]|[-*])\s+", prompt))

    # 3. Algorithmic / Mathematical density
    math_cues = ["glicko", "rating", "algorithm", "proof", "matrix", "convergence", "stochastic", "sgd", "variance"]
    math_count = sum(1 for m in math_cues if m in clean)

    # Base ground truth
    if has_regression:
        x_star = 2.75
        y_star = 1.60
        delta_reasons.append("detected user correction / regression signal")
    elif item_matches >= 4 or num_words > 120:
        x_star = 2.40
        y_star = 1.30
        delta_reasons.append(f"dense multi-item punchlist ({item_matches} items)")
    elif math_count >= 2:
        x_star = 2.20
        y_star = 2.10
        delta_reasons.append("algorithmic / statistical reasoning requirements")
    else:
        x_star = 2.20
        y_star = 1.00
        delta_reasons.append("standard resilient double-pass baseline")

    return x_star, y_star, delta_reasons


def load_ingested_state() -> Dict[str, Any]:
    """Loads state tracking which transcript steps have already been ingested."""
    if DEFAULT_STATE_FILE.exists():
        try:
            with open(DEFAULT_STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"ingested_keys": []}


def save_ingested_state(state: Dict[str, Any]):
    """Saves updated ingestion state."""
    DEFAULT_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DEFAULT_STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def sync_transcript(transcript_path: Path, dry_run: bool = False, verbose: bool = True) -> int:
    """
    Parses transcript and feeds new user turns into the Cognitive Engine.
    Returns the count of newly ingested samples.
    """
    if not transcript_path.exists():
        print(f"[ERROR] Transcript not found: {transcript_path}")
        return 0

    state = load_ingested_state()
    ingested_keys = set(state.get("ingested_keys", []))

    engine = CognitiveEngine()
    newly_ingested = 0

    with open(transcript_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue

            try:
                step = json.loads(line)
            except Exception:
                continue

            # Ingest steps of type USER_INPUT
            if step.get("type") != "USER_INPUT":
                continue

            step_idx = step.get("step_index", line_num)
            created_at = step.get("created_at", f"step_{step_idx}")
            unique_key = f"{transcript_path.parent.parent.name}:{step_idx}:{created_at}"

            if unique_key in ingested_keys:
                continue

            raw_content = step.get("content", "")
            prompt = clean_user_prompt(raw_content)
            if not prompt:
                ingested_keys.add(unique_key)
                continue

            viability = evaluate_prompt_viability(prompt)
            x_star, y_star, reasons = compute_ground_truth(prompt, viability)

            if verbose:
                snippet = prompt[:65].replace("\n", " ")
                print(f"[{newly_ingested+1}] Ingesting: \"{snippet}...\"")
                print(f"    Viability : Q = {viability['Q']:.2f} ({viability['classification']})")
                print(f"    Target    : X* = {x_star:.2f}, Y* = {y_star:.2f} ({', '.join(reasons)})")

            if not dry_run:
                engine.record_and_update(
                    prompt=prompt,
                    actual_x_star=x_star,
                    actual_y_star=y_star,
                    delta_items=reasons,
                    test_exit_code=0
                )

            ingested_keys.add(unique_key)
            newly_ingested += 1

    if not dry_run:
        state["ingested_keys"] = list(ingested_keys)
        state["last_sync_timestamp"] = datetime.now(timezone.utc).isoformat()
        save_ingested_state(state)

    return newly_ingested


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Autonomous Transcript Learning Sync for Agent Autopilot")
    parser.add_argument("--transcript", type=str, help="Path to transcript.jsonl file")
    parser.add_argument("--conversation-id", type=str, help="Conversation ID to locate transcript for")
    parser.add_argument("--dry-run", action="store_true", help="Inspect prompts and targets without updating weights")
    parser.add_argument("--quiet", action="store_true", help="Suppress per-step details")
    args = parser.parse_args()

    transcript_file: Optional[Path] = None

    if args.transcript:
        transcript_file = Path(args.transcript)
    elif args.conversation_id:
        target = DEFAULT_BRAIN_DIR / args.conversation_id / ".system_generated" / "logs" / "transcript.jsonl"
        if not target.exists():
            target = DEFAULT_BRAIN_DIR / args.conversation_id / "logs" / "transcript.jsonl"
        transcript_file = target
    else:
        transcript_file = find_latest_transcript()

    if not transcript_file or not transcript_file.exists():
        print("[ERROR] Could not find a valid transcript.jsonl file.")
        print(f"  Searched in: {DEFAULT_BRAIN_DIR}")
        sys.exit(1)

    print("========================================================")
    print("  AUTOPILOT CLOSED-LOOP TRANSCRIPT LEARNING INGESTION")
    print("========================================================")
    print(f"Transcript : {transcript_file}")
    print(f"Mode       : {'DRY RUN' if args.dry_run else 'LIVE WEIGHT UPDATE'}")
    print("--------------------------------------------------------")

    count = sync_transcript(transcript_file, dry_run=args.dry_run, verbose=not args.quiet)

    print("--------------------------------------------------------")
    if args.dry_run:
        print(f"[DRY RUN COMPLETE] {count} new user prompts evaluated.")
    else:
        print(f"[SUCCESS] Ingested and trained on {count} new user prompts!")
        print("  Global model weights and local telemetry history updated.")
    print("========================================================\n")


if __name__ == "__main__":
    main()
