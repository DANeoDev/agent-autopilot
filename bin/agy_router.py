"""
Antigravity Intelligent Model Router (CLI & Programmatic)
Analyzes task prompts and automatically selects the optimal AI model
based on complexity, domain, reasoning depth, latency/cost, and quota limits.
"""

import sys
import re
import json
import argparse
from typing import Tuple

MODELS = {
    "flash_lite": {
        "id": "gemini-3.5-flash-lite",
        "name": "Gemini 3.5 Flash-Lite",
        "provider": "Google",
        "tier": 1,
        "desc": "Ultra-fast, lowest latency, cost-effective for single edits and quick lookups."
    },
    "flash": {
        "id": "gemini-3.8-flash",
        "name": "Gemini 3.8 Flash (Default)",
        "provider": "Google",
        "tier": 2,
        "desc": "Balanced workhorse for everyday coding, unit tests, and general agentic workflows."
    },
    "gpt_oss": {
        "id": "gpt-oss-120b",
        "name": "GPT-OSS 120B",
        "provider": "Open Source",
        "tier": 3,
        "desc": "Strong at clear documentation, README prose, and open-source reproducibility."
    },
    "sonnet_thinking": {
        "id": "claude-sonnet-4-6-thinking",
        "name": "Claude Sonnet 4.6 (Thinking)",
        "provider": "Anthropic",
        "tier": 4,
        "desc": "Extended step-by-step reasoning for multi-file refactoring and deep debugging."
    },
    "opus": {
        "id": "claude-opus-4-6",
        "name": "Claude Opus 4.6",
        "provider": "Anthropic",
        "tier": 5,
        "desc": "Maximum intelligence for advanced math/statistics (Glicko), architecture, and /goal."
    }
}

PATTERNS_OPUS = [
    r"\b(glicko|rating system|elo|bayesian|stochastic|markov|mathematical proof|algorithm design)\b",
    r"\b(system architecture|architectural overhaul|monolith to microservices|high-level design)\b",
    r"\b(/goal|overnight|autonomous goal|unsupervised)\b"
]

PATTERNS_SONNET = [
    r"\b(refactor across|multi-file|deep debug|memory leak|deadlock|race condition)\b",
    r"\b(trace execution|step by step reasoning|complex logic|subtle bug)\b",
    r"\b(migration plan|state machine|complex types)\b"
]

PATTERNS_GPT_OSS = [
    r"\b(write docs|write readme|documentation|explain in plain english|tutorial)\b",
    r"\b(open source|reproducibility|audit weights|license compliance)\b",
    r"\b(user manual|api documentation|markdown guide)\b"
]

PATTERNS_FLASH_LITE = [
    r"\b(fix typo|rename variable|simple regex|format json|quick lookup|one-liner)\b",
    r"\b(what is the command|convert to lowercase|sort list|simple syntax)\b"
]

OVERRIDE_PATTERNS = [
    r"use currently selected model",
    r"use current model",
    r"no subagents?",
    r"don't use subagents?",
    r"force current model",
    r"run directly"
]


def classify_task(prompt: str, conserve_quota: bool = False) -> Tuple[str, str, bool]:
    """
    Classifies a task prompt and returns (model_key, rationale, is_user_override).
    """
    lower = prompt.lower()

    # Check for explicit user override
    for pat in OVERRIDE_PATTERNS:
        if re.search(pat, lower):
            return "flash", "Strict user override detected: executing directly on currently selected model.", True

    # Tier 5 (Opus)
    for pat in PATTERNS_OPUS:
        if re.search(pat, lower):
            return "opus", "Requires maximum reasoning, mathematical/statistical rigour, or deep architecture (Tier 5).", False

    # Tier 4 (Sonnet Thinking)
    for pat in PATTERNS_SONNET:
        if re.search(pat, lower):
            if conserve_quota:
                return "flash", "Quota conservation active: falling back to Gemini 3.8 Flash to preserve Claude limits.", False
            return "sonnet_thinking", "Requires extended step-by-step reasoning and multi-file code tracing (Tier 4).", False

    # Tier 3 (GPT-OSS 120B)
    for pat in PATTERNS_GPT_OSS:
        if re.search(pat, lower):
            return "gpt_oss", "Documentation, prose writing, or open-source reproducibility task (Tier 3).", False

    # Tier 1 (Flash-Lite)
    for pat in PATTERNS_FLASH_LITE:
        if re.search(pat, lower):
            return "flash_lite", "Low-complexity, routine single-file task; best served with lowest latency (Tier 1).", False

    # Default to Tier 2 (Gemini 3.8 Flash)
    return "flash", "Standard development/agentic workflow; optimal balance of speed and capability (Tier 2).", False


def main():
    parser = argparse.ArgumentParser(description="Antigravity Intelligent Model Router")
    parser.add_argument("prompt", nargs="*", help="The task prompt to evaluate")
    parser.add_argument("--json", action="store_true", help="Output result in JSON format")
    parser.add_argument("--conserve-quota", action="store_true", help="Conserve high-tier model quota where feasible")
    args = parser.parse_args()

    prompt_text = " ".join(args.prompt).strip()
    if not prompt_text:
        if not sys.stdin.isatty():
            prompt_text = sys.stdin.read().strip()
        else:
            print("Error: No prompt provided. Usage: agy-route <prompt>", file=sys.stderr)
            sys.exit(1)

    key, rationale, is_override = classify_task(prompt_text, conserve_quota=args.conserve_quota)
    selected = MODELS[key]

    subagent_param = "none (direct)" if is_override else (
        "pro" if key in ["opus", "sonnet_thinking"] else ("flash_lite" if key == "flash_lite" else "flash")
    )

    if args.json:
        result = {
            "model_key": key,
            "model_id": selected["id"],
            "model_name": selected["name"],
            "provider": selected["provider"],
            "tier": selected["tier"],
            "rationale": rationale,
            "is_user_override": is_override,
            "subagent_param": subagent_param,
            "prompt": prompt_text
        }
        print(json.dumps(result, indent=2))
    else:
        print("\n========================================================")
        print("  GOOGLE ANTIGRAVITY - AUTOMATED MODEL ROUTER")
        print("========================================================")
        print(f"Task: {prompt_text[:80]}{'...' if len(prompt_text) > 80 else ''}")
        print("--------------------------------------------------------")
        print(f"Selected Model : {selected['name']}")
        print(f"Model ID       : {selected['id']}")
        print(f"Provider       : {selected['provider']} (Tier {selected['tier']})")
        print(f"User Override  : {'YES (100% direct)' if is_override else 'No'}")
        print(f"Rationale      : {rationale}")
        print("--------------------------------------------------------")
        print(f"Subagent Param : Model: '{subagent_param}'")
        print("========================================================\n")


if __name__ == "__main__":
    main()
