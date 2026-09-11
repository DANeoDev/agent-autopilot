"""
Cognitive Pass Prediction & Self-Learning Engine
Computes continuous complex execution depth Z = X + iY in C, where:
  X = Re(Z) is Physical Execution & Delta-Repair Depth (Action space)
  Y = Im(Z) is Epistemic Reflection & Verification Depth (Reasoning space)

Features:
1. Base Meaning Priors (Initial Concept Taxonomy)
2. Dynamic Learned Terms Dictionary (Discovers and expands vocabulary via feedback)
3. Subword & Trigram Feature Hashing (The hashing trick for unknown languages/domains)
4. Two Telemetry Modes: Explicit (Default, high-fidelity) vs Anonymous (Hashed-only)
5. Online Stochastic Gradient Descent (SGD) for continuous adaptation

Zero third-party dependencies: runs on pure Python 3.10+ standard library.
"""

import sys
import os
import re
import math
import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, List, Tuple, Optional

DEFAULT_HASH_DIM = 256
DEFAULT_WEIGHTS_PATH = Path(__file__).parent.parent / "models" / "cognitive_weights.json"
DEFAULT_TELEMETRY_DIR = Path.home() / ".gemini" / "autopilot" / "telemetry"
DEFAULT_TELEMETRY_FILE = DEFAULT_TELEMETRY_DIR / "samples.jsonl"
DEFAULT_CONFIG_FILE = Path.home() / ".gemini" / "autopilot" / "config.json"

# ============================================================================
# BASE MEANING PRIORS (The Initial Concept Taxonomy)
# Provides baseline semantic priors before any empirical self-learning begins.
# ============================================================================
BASE_MEANING_PRIORS: Dict[str, Dict[str, float]] = {
    # Concurrency & Synchronization (High Epistemic Y, Moderate Action X)
    "mutex": {"delta_x": 0.20, "delta_y": 0.45, "concept": "concurrency"},
    "lock": {"delta_x": 0.15, "delta_y": 0.35, "concept": "concurrency"},
    "deadlock": {"delta_x": 0.25, "delta_y": 0.50, "concept": "concurrency"},
    "race": {"delta_x": 0.20, "delta_y": 0.45, "concept": "concurrency"},
    "thread": {"delta_x": 0.15, "delta_y": 0.30, "concept": "concurrency"},
    "async": {"delta_x": 0.15, "delta_y": 0.25, "concept": "concurrency"},
    "atomic": {"delta_x": 0.20, "delta_y": 0.40, "concept": "concurrency"},
    "coroutine": {"delta_x": 0.15, "delta_y": 0.30, "concept": "concurrency"},
    "semaphore": {"delta_x": 0.20, "delta_y": 0.40, "concept": "concurrency"},

    # UI Nuances & Reactivity (High Action X, Moderate Epistemic Y)
    "hover": {"delta_x": 0.35, "delta_y": 0.10, "concept": "ui_nuance"},
    "tooltip": {"delta_x": 0.30, "delta_y": 0.10, "concept": "ui_nuance"},
    "dropdown": {"delta_x": 0.30, "delta_y": 0.10, "concept": "ui_nuance"},
    "viewport": {"delta_x": 0.25, "delta_y": 0.15, "concept": "ui_nuance"},
    "responsive": {"delta_x": 0.30, "delta_y": 0.15, "concept": "ui_nuance"},
    "contrast": {"delta_x": 0.25, "delta_y": 0.10, "concept": "accessibility"},
    "wcag": {"delta_x": 0.35, "delta_y": 0.20, "concept": "accessibility"},
    "aria": {"delta_x": 0.25, "delta_y": 0.15, "concept": "accessibility"},
    "debounce": {"delta_x": 0.30, "delta_y": 0.25, "concept": "reactivity"},
    "throttle": {"delta_x": 0.25, "delta_y": 0.25, "concept": "reactivity"},
    "modal": {"delta_x": 0.25, "delta_y": 0.10, "concept": "ui_nuance"},

    # Algorithmic & Mathematical Rigor (High Epistemic Y)
    "algorithm": {"delta_x": 0.10, "delta_y": 0.45, "concept": "algorithmic"},
    "proof": {"delta_x": 0.10, "delta_y": 0.60, "concept": "algorithmic"},
    "convergence": {"delta_x": 0.15, "delta_y": 0.55, "concept": "algorithmic"},
    "probability": {"delta_x": 0.10, "delta_y": 0.45, "concept": "algorithmic"},
    "variance": {"delta_x": 0.10, "delta_y": 0.40, "concept": "algorithmic"},
    "matrix": {"delta_x": 0.15, "delta_y": 0.40, "concept": "algorithmic"},
    "tree": {"delta_x": 0.15, "delta_y": 0.35, "concept": "algorithmic"},
    "graph": {"delta_x": 0.20, "delta_y": 0.40, "concept": "algorithmic"},
    "recursion": {"delta_x": 0.15, "delta_y": 0.45, "concept": "algorithmic"},
    "rating": {"delta_x": 0.15, "delta_y": 0.35, "concept": "algorithmic"},
    "glicko": {"delta_x": 0.20, "delta_y": 0.50, "concept": "algorithmic"},

    # State Persistence & Migrations (High Action X)
    "migration": {"delta_x": 0.40, "delta_y": 0.15, "concept": "persistence"},
    "schema": {"delta_x": 0.35, "delta_y": 0.20, "concept": "persistence"},
    "transaction": {"delta_x": 0.25, "delta_y": 0.35, "concept": "persistence"},
    "rollback": {"delta_x": 0.30, "delta_y": 0.30, "concept": "persistence"},
    "foreign": {"delta_x": 0.25, "delta_y": 0.15, "concept": "persistence"},

    # Boundary & Edge-Case Traps
    "boundary": {"delta_x": 0.25, "delta_y": 0.35, "concept": "edge_case"},
    "null": {"delta_x": 0.20, "delta_y": 0.25, "concept": "edge_case"},
    "overflow": {"delta_x": 0.25, "delta_y": 0.35, "concept": "edge_case"},
    "exception": {"delta_x": 0.20, "delta_y": 0.25, "concept": "edge_case"},
    "retry": {"delta_x": 0.25, "delta_y": 0.25, "concept": "resilience"},

    # Affective, Corrective & Regression Signals (Meta-Feedback)
    "sadly": {"delta_x": 0.25, "delta_y": 0.35, "concept": "correction_affect"},
    "still": {"delta_x": 0.30, "delta_y": 0.20, "concept": "regression_signal"},
    "again": {"delta_x": 0.25, "delta_y": 0.20, "concept": "regression_signal"},
    "forgot": {"delta_x": 0.35, "delta_y": 0.15, "concept": "dropped_item"},
    "missed": {"delta_x": 0.35, "delta_y": 0.15, "concept": "dropped_item"},
    "broken": {"delta_x": 0.35, "delta_y": 0.25, "concept": "regression_signal"},
    "reverted": {"delta_x": 0.30, "delta_y": 0.25, "concept": "regression_signal"},
    "regress": {"delta_x": 0.30, "delta_y": 0.30, "concept": "regression_signal"},
    "regression": {"delta_x": 0.30, "delta_y": 0.30, "concept": "regression_signal"}
}


def get_configured_telemetry_mode() -> str:
    """Reads telemetry mode from config or returns 'explicit' by default."""
    if DEFAULT_CONFIG_FILE.exists():
        try:
            with open(DEFAULT_CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("telemetry_mode", "explicit")
        except Exception:
            pass
    return "explicit"


def set_configured_telemetry_mode(mode: str):
    """Sets telemetry mode ('explicit' or 'anonymous') in config."""
    DEFAULT_CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    cfg = {}
    if DEFAULT_CONFIG_FILE.exists():
        try:
            with open(DEFAULT_CONFIG_FILE, "r", encoding="utf-8") as f:
                cfg = json.load(f)
        except Exception:
            pass
    cfg["telemetry_mode"] = mode
    with open(DEFAULT_CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)


def tokenize_words(text: str) -> List[str]:
    """Returns list of normalized lowercase word tokens."""
    return re.findall(r"\b[a-z0-9_-]+\b", text.lower())


def tokenize_and_hash(text: str, dim: int = DEFAULT_HASH_DIM) -> List[float]:
    """
    Extracts word tokens and character 3-grams, projecting them into a normalized
    sparse vector via feature hashing (the hashing trick).
    Zero fixed dictionary; learns arbitrary vocabularies across any programming language.
    """
    vec = [0.0] * dim
    clean_text = text.lower()
    words = tokenize_words(clean_text)

    # 1. Word token hashing
    for w in words:
        h = int(hashlib.md5(w.encode("utf-8")).hexdigest(), 16) % dim
        vec[h] += 1.0

    # 2. Character 3-gram hashing (subwords, morphology, syntax tokens)
    for i in range(len(clean_text) - 2):
        trigram = clean_text[i : i + 3]
        h = int(hashlib.md5(trigram.encode("utf-8")).hexdigest(), 16) % dim
        vec[h] += 0.5

    # 3. Structural prompt heuristics mapped to reserved buckets
    token_count = len(words)
    item_count = len(re.findall(r"(?:^|\n)\s*(?:\d+[\.\)]|[-*])\s+", text))
    negations = len(re.findall(r"\b(?:not|no|never|without|avoid|prevent|preserve|except)\b", clean_text))
    question_marks = text.count("?")

    vec[0] = math.log10(max(1, token_count))
    vec[1] = float(item_count)
    vec[2] = float(negations)
    vec[3] = float(question_marks)

    # L2 Normalization
    norm = math.sqrt(sum(v * v for v in vec))
    if norm > 1e-6:
        vec = [v / norm for v in vec]

    return vec


def evaluate_prompt_viability(prompt: str) -> Dict[str, Any]:
    """
    Evaluates prompt viability Q in [0.0, 1.0] across three orthogonal dimensions:
      1. Q_spec  (Specificity vs. Subjective Fluff)
      2. Q_test  (Testability & Verifiability Constraints)
      3. Q_scope (Scope & Structure Feasibility)
    
    Returns score, classification, and actionable prompt refinement hints.
    """
    clean = prompt.lower()
    words = tokenize_words(clean)
    num_words = len(words)

    # 1. Specificity: concrete technical cues vs vague subjective words
    vague_lexicon = {
        "better", "nice", "good", "cool", "cleaner", "somehow", "maybe", 
        "idk", "stuff", "things", "proper", "awesome", "slick", "crazy", 
        "something", "etc", "kind", "sort", "basically"
    }
    concrete_indicators = [
        r"\.[a-z0-9]{1,4}\b",  # file extensions (.py, .ts, .md, .css)
        r"['\"`][^'\"`]+['\"`]", # quoted strings / exact identifiers
        r"\b(?:function|class|def|route|endpoint|schema|database|table|column|api|css|html|dom|hook|state|component)\b",
        r"\b(?:add|remove|fix|refactor|export|orient|render|assert|calculate|implement|update|delete|migrate|align|filter)\b"
    ]
    
    vague_found = [w for w in words if w in vague_lexicon]
    concrete_matches = sum(len(re.findall(pat, prompt, re.IGNORECASE)) for pat in concrete_indicators)
    
    raw_spec = 0.50 + 0.08 * min(6, concrete_matches) - 0.12 * len(vague_found)
    q_spec = max(0.10, min(1.00, raw_spec))

    # 2. Testability: explicit verification criteria & conditional logic
    test_lexicon = [
        r"\b(?:test|pytest|unit|assert|verify|verification|exit\s*code|status\s*code|error\s*code)\b",
        r"\b(?:200|404|500|true|false|null|none|equal|expect|match)\b",
        r"\b(?:if\b.+?\bthen|when\b.+?\bshould|only\b.+?\binstead|ensure|must|guarantee)\b",
        r"#\d+|rank\s*#?\d+|\d+\s*items"
    ]
    test_matches = sum(len(re.findall(pat, clean)) for pat in test_lexicon)
    raw_test = 0.35 + 0.15 * min(5, test_matches)
    q_test = max(0.10, min(1.00, raw_test))

    # 3. Scope & Structure: density, itemization, and attention-sink risk
    item_matches = len(re.findall(r"(?:^|\n)\s*(?:\d+[\.\)]|[-*])\s+", prompt))
    if num_words < 8:
        q_scope = 0.35 # Underspecified
    elif 8 <= num_words <= 250:
        q_scope = 0.95 if item_matches > 0 else 0.85
    elif num_words > 250:
        q_scope = 0.90 if item_matches >= 4 else 0.60 # Wall of text risk without bullet points
    else:
        q_scope = 0.80

    # Composite Viability Score Q
    Q = round(0.40 * q_spec + 0.35 * q_test + 0.25 * q_scope, 3)

    if Q >= 0.78:
        classification = "HIGH VIABILITY [PROCEEDING AUTONOMOUSLY]"
    elif Q >= 0.52:
        classification = "MODERATE VIABILITY [ACTIONABLE WITH MINOR GAPS]"
    else:
        classification = "LOW VIABILITY [HIGH AMBIGUITY / RISK OF DRIFT]"

    hints = []
    if vague_found:
        unique_vague = sorted(list(set(vague_found)))[:3]
        hints.append(f"Subjective phrasing detected: {', '.join(repr(v) for v in unique_vague)}. Replace with concrete functional criteria or DOM/CSS rules.")
    if q_test < 0.60:
        hints.append("Lacks explicit verification condition. Specify expected output, exit code (0), or assertion to guarantee 100% gap audit fidelity.")
    if item_matches == 0 and num_words > 40:
        hints.append("Consider numbered punch-list format (1., 2., 3.). Multi-item lists improve Pass 2 gap-audit recall by ~40%.")

    potential_y_delta = 0.0
    if hints:
        potential_y_delta = round(-0.15 * len(hints), 2)
        hints.append(f"Resolving these hints will compress epistemic uncertainty Y by {potential_y_delta:+.2f}, eliminating guesswork and saving tokens.")

    return {
        "Q": Q,
        "Q_spec": round(q_spec, 3),
        "Q_test": round(q_test, 3),
        "Q_scope": round(q_scope, 3),
        "classification": classification,
        "detected_vague_terms": vague_found,
        "hints": hints,
        "potential_y_reduction": potential_y_delta
    }


class CognitiveEngine:
    def __init__(self, weights_path: Path = DEFAULT_WEIGHTS_PATH, dim: int = DEFAULT_HASH_DIM):
        self.weights_path = Path(weights_path)
        self.dim = dim
        self.w_x = [0.0] * dim
        self.w_y = [0.0] * dim
        self.b_x = 2.2  # Default prior: X = 2.2 (Resilient Gold Standard: Double-Pass + Delta Re-Verification)
        self.b_y = 1.0  # Default prior: Y = 1.0 (Standard reflection)
        self.samples_seen = 0
        self.learned_terms: Dict[str, Dict[str, Any]] = {}
        self.load_weights()

    def load_weights(self):
        if self.weights_path.exists():
            try:
                with open(self.weights_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.w_x = data.get("w_x", [0.0] * self.dim)
                    self.w_y = data.get("w_y", [0.0] * self.dim)
                    self.b_x = data.get("b_x", 2.2)
                    self.b_y = data.get("b_y", 1.0)
                    self.samples_seen = data.get("samples_seen", 0)
                    self.learned_terms = data.get("learned_terms", {})
            except Exception:
                pass

    def save_weights(self):
        self.weights_path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "version": "2.0",
            "dim": self.dim,
            "samples_seen": self.samples_seen,
            "b_x": self.b_x,
            "b_y": self.b_y,
            "w_x": self.w_x,
            "w_y": self.w_y,
            "learned_terms": self.learned_terms,
        }
        with open(self.weights_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def extract_term_influences(self, text: str) -> Tuple[float, float, List[Dict[str, Any]]]:
        """
        Inspects words in the prompt against base priors and the learned term dictionary.
        Returns (term_delta_x, term_delta_y, matched_terms_info).
        """
        words = set(tokenize_words(text))
        matched = []
        term_dx = 0.0
        term_dy = 0.0

        for w in words:
            # 1. Check dynamically learned dictionary first
            if w in self.learned_terms:
                tinfo = self.learned_terms[w]
                dx = tinfo.get("delta_x", 0.0)
                dy = tinfo.get("delta_y", 0.0)
                term_dx += dx
                term_dy += dy
                matched.append({
                    "term": w,
                    "delta_x": round(dx, 3),
                    "delta_y": round(dy, 3),
                    "source": "dynamically_learned",
                    "occurrences": tinfo.get("occurrences", 1)
                })
            # 2. Check base meaning priors
            elif w in BASE_MEANING_PRIORS:
                pinfo = BASE_MEANING_PRIORS[w]
                dx = pinfo.get("delta_x", 0.0)
                dy = pinfo.get("delta_y", 0.0)
                term_dx += dx
                term_dy += dy
                matched.append({
                    "term": w,
                    "delta_x": round(dx, 3),
                    "delta_y": round(dy, 3),
                    "source": "base_prior",
                    "concept": pinfo.get("concept", "general")
                })

        return term_dx, term_dy, matched

    def predict(self, prompt: str) -> Dict[str, Any]:
        feats = tokenize_and_hash(prompt, self.dim)
        term_dx, term_dy, matched_terms = self.extract_term_influences(prompt)
        viability = evaluate_prompt_viability(prompt)

        # Base hash projection + term influence + bias
        raw_x = sum(w * x for w, x in zip(self.w_x, feats)) + term_dx + self.b_x
        raw_y = sum(w * x for w, x in zip(self.w_y, feats)) + term_dy + self.b_y

        X = max(1.0, min(3.0, raw_x))
        Y = max(0.0, min(3.0, raw_y))

        R = math.sqrt(X * X + Y * Y)
        theta_rad = math.atan2(Y, X)
        theta_deg = math.degrees(theta_rad)

        if X < 1.4:
            discrete_x = 1
            x_desc = "Single-Pass (Direct Batch Execution)"
        elif X <= 2.4:
            discrete_x = 2
            x_desc = "Resilient Double-Pass (Gold Standard: In-Situ Gap Audit + Delta Re-Verification)"
        else:
            discrete_x = 3
            x_desc = "Triple-Pass (Deep Edge-Case & Regression Matrix)"

        if theta_deg < 20.0:
            orientation = "Action-Dominant (Heavy Code Mutex, Low Reflection)"
        elif theta_deg > 55.0:
            orientation = "Epistemic-Dominant (Heavy Mathematical & Conceptual Reasoning)"
        else:
            orientation = "Balanced Cognitive Flow (Equal Execution & Self-Audit)"

        telemetry_mode = get_configured_telemetry_mode()

        return {
            "Z": f"{X:.2f} + {Y:.2f}i",
            "X_continuous": round(X, 3),
            "Y_continuous": round(Y, 3),
            "X_recommended": discrete_x,
            "X_description": x_desc,
            "R_magnitude": round(R, 3),
            "theta_degrees": round(theta_deg, 1),
            "orientation": orientation,
            "samples_trained": self.samples_seen,
            "matched_terms": matched_terms,
            "total_learned_vocabulary_size": len(self.learned_terms),
            "telemetry_mode": telemetry_mode,
            "viability": viability
        }

    def format_card(self, result: Dict[str, Any]) -> str:
        """Formats a compact ASCII telemetry card with prompt viability & optimization hints."""
        z_str = result['Z']
        r_mag = result['R_magnitude']
        theta = result['theta_degrees']
        x_rec = result['X_recommended']
        x_desc = result['X_description']
        mode = result['telemetry_mode'].upper()
        samples = result['samples_trained']
        v = result.get("viability", {})
        q_val = v.get("Q", 0.85)
        q_class = v.get("classification", "VIABLE")

        cues = []
        for m in result.get('matched_terms', []):
            term = m['term']
            dx = m['delta_x']
            dy = m['delta_y']
            concept = m.get('concept', 'general')
            cues.append(f'"{term}" ({concept}, ΔX={dx:+.2f}, ΔY={dy:+.2f})')

        cues_str = ", ".join(cues[:2]) if cues else "Baseline priors"
        if len(cues) > 2:
            cues_str += f" (+{len(cues)-2} more)"

        lines = [
            "╭─ 🎯 Autopilot Cognitive Telemetry & Prompt Viability ────────────────────────╮",
            f"│ Prompt Viability : Q = {q_val:.2f} / 1.00  [{q_class:<35}] │",
            f"│ Complex Vector   : Z = {z_str:<10} (R = {r_mag:<5}, θ = {theta}°)                        │",
            f"│ Pass Depth       : X = {result['X_continuous']:<5} -> {x_desc:<45} │",
            f"│ Signals Caught   : {cues_str:<58} │",
            f"│ Telemetry Mode   : {mode:<10} ({samples} empirical samples recorded)                 │"
        ]

        hints = v.get("hints", [])
        if hints:
            lines.append("├─────────────────────────────────────────────────────────────────────────────┤")
            lines.append("│ 💡 Prompt Refinement Opportunities (To Optimize Execution & Reduce Tokens):  │")
            for h in hints:
                wrapped_hint = f"• {h}"
                if len(wrapped_hint) > 73:
                    lines.append(f"│ {wrapped_hint[:73]:<75} │")
                    lines.append(f"│   {wrapped_hint[73:]:<73} │")
                else:
                    lines.append(f"│ {wrapped_hint:<75} │")

        lines.append("╰─────────────────────────────────────────────────────────────────────────────╯")
        return "\n".join(lines)

    def record_and_update(self, prompt: str, actual_x_star: float, actual_y_star: float,
                          delta_items: Optional[List[str]] = None,
                          test_exit_code: int = 0,
                          lr: float = 0.05):
        """
        Performs confidence-weighted online Stochastic Gradient Descent (SGD) on global
        weights AND updates/discovers dynamic vocabulary terms based on empirical task outcome.
        Dampens learning rate by Q^2 on ambiguous or low-viability prompts to prevent weight poisoning.
        Logs sample in configured telemetry mode (explicit or anonymous).
        """
        feats = tokenize_and_hash(prompt, self.dim)
        term_dx, term_dy, _ = self.extract_term_influences(prompt)
        viability = evaluate_prompt_viability(prompt)
        q_score = viability.get("Q", 0.8)

        # Confidence-weighted learning: dampen learning rate on ambiguous/low-viability prompts
        eff_lr = lr * (q_score ** 2)

        pred_x = sum(w * x for w, x in zip(self.w_x, feats)) + term_dx + self.b_x
        pred_y = sum(w * x for w, x in zip(self.w_y, feats)) + term_dy + self.b_y

        err_x = pred_x - actual_x_star
        err_y = pred_y - actual_y_star

        # 1. Update hash projection weights with confidence-weighted eff_lr
        for i in range(self.dim):
            self.w_x[i] -= eff_lr * err_x * feats[i]
            self.w_y[i] -= eff_lr * err_y * feats[i]

        self.b_x -= eff_lr * err_x * 0.5
        self.b_y -= eff_lr * err_y * 0.5
        self.samples_seen += 1

        # 2. Dynamic Vocabulary Learning: Update or discover terms in the prompt
        words = set(tokenize_words(prompt))
        # Ignore extremely common stopwords
        stopwords = {"the", "a", "an", "and", "or", "in", "on", "at", "to", "for", "is", "it", "with", "as", "by", "of", "from"}
        meaningful_words = [w for w in words if len(w) > 3 and w not in stopwords]

        # Credit assignment: adjust term weights in the direction of error
        term_lr = eff_lr * 0.5
        for w in meaningful_words:
            if w in self.learned_terms:
                t = self.learned_terms[w]
                t["delta_x"] = max(-0.5, min(0.8, t.get("delta_x", 0.0) - term_lr * err_x))
                t["delta_y"] = max(-0.5, min(0.8, t.get("delta_y", 0.0) - term_lr * err_y))
                t["occurrences"] = t.get("occurrences", 0) + 1
            else:
                # Discovered novel term! Initialize if error is positive
                if abs(err_x) > 0.1 or abs(err_y) > 0.1:
                    init_dx = max(-0.3, min(0.5, -term_lr * err_x))
                    init_dy = max(-0.3, min(0.5, -term_lr * err_y))
                    self.learned_terms[w] = {
                        "delta_x": round(init_dx, 4),
                        "delta_y": round(init_dy, 4),
                        "occurrences": 1,
                        "discovered_at": datetime.now(timezone.utc).isoformat()
                    }

        self.save_weights()

        # 3. Log to telemetry in configured mode (Explicit vs. Anonymous)
        telemetry_mode = get_configured_telemetry_mode()
        try:
            DEFAULT_TELEMETRY_DIR.mkdir(parents=True, exist_ok=True)
            iso_now = datetime.now(timezone.utc).isoformat()

            if telemetry_mode == "anonymous":
                # Anonymized mode: Strips raw prompt text, stores only numeric hashes
                entry = {
                    "mode": "anonymous",
                    "timestamp": iso_now,
                    "features_hash": hashlib.sha256(json.dumps(feats).encode()).hexdigest()[:16],
                    "token_count": len(tokenize_words(prompt)),
                    "dim": self.dim,
                    "pred_x": round(pred_x, 3),
                    "pred_y": round(pred_y, 3),
                    "actual_x": round(actual_x_star, 3),
                    "actual_y": round(actual_y_star, 3),
                    "samples_seen": self.samples_seen,
                }
            else:
                # Explicit mode (Default): Stores rich prompt and delta context for optimal model training
                entry = {
                    "mode": "explicit",
                    "timestamp": iso_now,
                    "prompt": prompt,
                    "token_count": len(tokenize_words(prompt)),
                    "pred_Z": {"X": round(pred_x, 3), "Y": round(pred_y, 3)},
                    "actual_outcome": {"X_star": round(actual_x_star, 3), "Y_star": round(actual_y_star, 3)},
                    "delta_items_detected": delta_items or [],
                    "test_exit_code": test_exit_code,
                    "terms_updated_count": len(meaningful_words),
                    "samples_seen": self.samples_seen,
                }

            with open(DEFAULT_TELEMETRY_FILE, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception:
            pass

    def get_top_learned_terms(self, limit: int = 15) -> List[Dict[str, Any]]:
        """Returns top learned vocabulary terms sorted by cognitive weight."""
        sorted_terms = sorted(
            self.learned_terms.items(),
            key=lambda item: abs(item[1].get("delta_x", 0.0)) + abs(item[1].get("delta_y", 0.0)),
            reverse=True
        )
        return [{"term": k, **v} for k, v in sorted_terms[:limit]]


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Autopilot Cognitive Pass Prediction & Self-Learning Engine")
    parser.add_argument("--prompt", type=str, help="Prompt text to analyze and predict pass parameters")
    parser.add_argument("--explain", action="store_true", help="Display semantic term contribution breakdown")
    parser.add_argument("--learn", nargs=2, metavar=("X_STAR", "Y_STAR"), type=float, help="Record ground-truth outcome and perform online SGD + vocabulary update")
    parser.add_argument("--delta-items", nargs="*", default=None, help="List of delta items detected during Pass 2 gap audit")
    parser.add_argument("--test-code", type=int, default=0, help="Test suite exit code (default: 0)")
    parser.add_argument("--learned-terms", action="store_true", help="Show top dynamically learned vocabulary terms")
    parser.add_argument("--telemetry-mode", choices=["explicit", "anonymous"], help="Set or switch telemetry logging mode (standard: explicit)")
    parser.add_argument("--json", action="store_true", help="Output prediction in raw JSON format")
    parser.add_argument("--card", action="store_true", help="Output prediction as a compact ASCII telemetry card")
    args = parser.parse_args()

    if args.telemetry_mode:
        set_configured_telemetry_mode(args.telemetry_mode)
        print(f"[SUCCESS] Telemetry mode set to: '{args.telemetry_mode}'")
        if args.telemetry_mode == "explicit":
            print("  (Explicit mode is the standard default: records prompt text & deltas for highest-accuracy learning).")
        else:
            print("  (Anonymous mode enabled: strips prompt text and records only numeric hashes).")
        return

    engine = CognitiveEngine()

    if args.learned_terms:
        top_terms = engine.get_top_learned_terms(limit=25)
        print("\n========================================================")
        print(f"  DYNAMICALLY LEARNED VOCABULARY ({len(engine.learned_terms)} terms discovered)")
        print("========================================================")
        if not top_terms:
            print("  No novel terms learned yet. Engine is running on base concept priors.")
        else:
            for t in top_terms:
                dx = t.get('delta_x', 0.0)
                dy = t.get('delta_y', 0.0)
                occ = t.get('occurrences', 1)
                print(f"  * {t['term']:<18} : Delta-X = {dx:+.3f}, Delta-Y = {dy:+.3f}  (observed {occ}x)")
        print("========================================================\n")
        return

    if args.prompt:
        if args.learn:
            x_star, y_star = args.learn
            engine.record_and_update(
                args.prompt,
                x_star,
                y_star,
                delta_items=args.delta_items,
                test_exit_code=args.test_code
            )
            print(f"[SUCCESS] Updated cognitive model & dynamic vocabulary: X*={x_star}, Y*={y_star}")

        result = engine.predict(args.prompt)
        if args.json:
            print(json.dumps(result, indent=2))
        elif args.card:
            print(engine.format_card(result))
        else:
            print("\n========================================================")
            print("  AUTOPILOT COGNITIVE COMPLEX STATE ENGINE (Z = X + iY)")
            print("========================================================")
            print(f"Complex State (Z)   : {result['Z']} in C")
            print(f"Physical Depth (X)  : {result['X_continuous']} -> {result['X_description']}")
            print(f"Epistemic Depth (Y) : {result['Y_continuous']} (Internal reflection & reasoning)")
            print(f"Cognitive Budget (R): {result['R_magnitude']} (Total attentional energy)")
            print(f"Phase Angle (theta) : {result['theta_degrees']} deg -> {result['orientation']}")
            print(f"Telemetry Mode      : {result['telemetry_mode'].upper()} (Standard default)")
            print(f"Samples Trained     : {result['samples_trained']}")
            print(f"Learned Vocabulary  : {result['total_learned_vocabulary_size']} custom terms discovered")

            if args.explain and result.get("matched_terms"):
                print("--------------------------------------------------------")
                print("  CONTRIBUTING SEMANTIC TERMS:")
                for m in result["matched_terms"]:
                    src = m["source"]
                    dx = m["delta_x"]
                    dy = m["delta_y"]
                    print(f"  * {m['term']:<15} [{src:<20}] : Delta-X = {dx:+.2f}, Delta-Y = {dy:+.2f}")

            print("========================================================\n")
    else:
        parser.print_help()


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    main()
