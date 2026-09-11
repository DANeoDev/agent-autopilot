"""
Cognitive Pass Prediction & Self-Learning Engine
Computes continuous complex execution depth Z = X + iY in C, where:
  X = Re(Z) is Physical Execution & Delta-Repair Depth (Action space)
  Y = Im(Z) is Epistemic Reflection & Verification Depth (Reasoning space)

Uses feature hashing (the hashing trick) and online Stochastic Gradient Descent
to learn dynamically from execution outcomes without hardcoded dictionaries.
Zero third-party dependencies: runs on pure Python 3.10+ standard library.
"""

import sys
import os
import re
import math
import json
import hashlib
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional

DEFAULT_HASH_DIM = 256
DEFAULT_WEIGHTS_PATH = Path(__file__).parent.parent / "models" / "cognitive_weights.json"
DEFAULT_TELEMETRY_DIR = Path.home() / ".gemini" / "autopilot" / "telemetry"
DEFAULT_TELEMETRY_FILE = DEFAULT_TELEMETRY_DIR / "samples.jsonl"


def tokenize_and_hash(text: str, dim: int = DEFAULT_HASH_DIM) -> List[float]:
    """
    Extracts word tokens and character 3-grams, projecting them into a normalized
    sparse vector via feature hashing (the hashing trick).
    Zero fixed dictionary; learns arbitrary vocabularies across any programming language.
    """
    vec = [0.0] * dim
    clean_text = text.lower()
    words = re.findall(r"\b[a-z0-9_-]+\b", clean_text)

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


class CognitiveEngine:
    def __init__(self, weights_path: Path = DEFAULT_WEIGHTS_PATH, dim: int = DEFAULT_HASH_DIM):
        self.weights_path = Path(weights_path)
        self.dim = dim
        self.w_x = [0.0] * dim
        self.w_y = [0.0] * dim
        self.b_x = 2.0  # Prior: default X = 2.0 (Double-Pass)
        self.b_y = 1.0  # Prior: default Y = 1.0 (Standard reflection)
        self.samples_seen = 0
        self.load_weights()

    def load_weights(self):
        if self.weights_path.exists():
            try:
                with open(self.weights_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.w_x = data.get("w_x", [0.0] * self.dim)
                    self.w_y = data.get("w_y", [0.0] * self.dim)
                    self.b_x = data.get("b_x", 2.0)
                    self.b_y = data.get("b_y", 1.0)
                    self.samples_seen = data.get("samples_seen", 0)
            except Exception:
                pass

    def save_weights(self):
        self.weights_path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "version": "1.0",
            "dim": self.dim,
            "samples_seen": self.samples_seen,
            "b_x": self.b_x,
            "b_y": self.b_y,
            "w_x": self.w_x,
            "w_y": self.w_y,
        }
        with open(self.weights_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def predict(self, prompt: str) -> Dict[str, Any]:
        feats = tokenize_and_hash(prompt, self.dim)

        raw_x = sum(w * x for w, x in zip(self.w_x, feats)) + self.b_x
        raw_y = sum(w * x for w, x in zip(self.w_y, feats)) + self.b_y

        X = max(1.0, min(3.0, raw_x))
        Y = max(0.0, min(3.0, raw_y))

        R = math.sqrt(X * X + Y * Y)
        theta_rad = math.atan2(Y, X)
        theta_deg = math.degrees(theta_rad)

        if X < 1.4:
            discrete_x = 1
            x_desc = "Single-Pass (Direct Batch Execution)"
        elif X <= 2.3:
            discrete_x = 2
            x_desc = "Double-Pass (Gold Standard: In-Situ Gap Audit)"
        else:
            discrete_x = 3
            x_desc = "Triple-Pass (Deep Edge-Case & Regression Matrix)"

        if theta_deg < 20.0:
            orientation = "Action-Dominant (Heavy Code Mutex, Low Reflection)"
        elif theta_deg > 55.0:
            orientation = "Epistemic-Dominant (Heavy Mathematical & Conceptual Reasoning)"
        else:
            orientation = "Balanced Cognitive Flow (Equal Execution & Self-Audit)"

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
        }

    def record_and_update(self, prompt: str, actual_x_star: float, actual_y_star: float, lr: float = 0.05):
        feats = tokenize_and_hash(prompt, self.dim)

        pred_x = sum(w * x for w, x in zip(self.w_x, feats)) + self.b_x
        pred_y = sum(w * x for w, x in zip(self.w_y, feats)) + self.b_y

        err_x = pred_x - actual_x_star
        err_y = pred_y - actual_y_star

        for i in range(self.dim):
            self.w_x[i] -= lr * err_x * feats[i]
            self.w_y[i] -= lr * err_y * feats[i]

        self.b_x -= lr * err_x
        self.b_y -= lr * err_y
        self.samples_seen += 1

        self.save_weights()

        try:
            DEFAULT_TELEMETRY_DIR.mkdir(parents=True, exist_ok=True)
            entry = {
                "features_hash": hashlib.sha256(json.dumps(feats).encode()).hexdigest()[:16],
                "dim": self.dim,
                "pred_x": round(pred_x, 3),
                "pred_y": round(pred_y, 3),
                "actual_x": round(actual_x_star, 3),
                "actual_y": round(actual_y_star, 3),
                "samples_seen": self.samples_seen,
            }
            with open(DEFAULT_TELEMETRY_FILE, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception:
            pass


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Autopilot Cognitive Pass Prediction & Self-Learning Engine")
    parser.add_argument("--prompt", type=str, help="Prompt text to analyze and predict pass parameters")
    parser.add_argument("--learn", nargs=2, metavar=("X_STAR", "Y_STAR"), type=float, help="Record ground-truth outcome and perform online SGD update")
    parser.add_argument("--json", action="store_true", help="Output prediction in raw JSON format")
    args = parser.parse_args()

    engine = CognitiveEngine()

    if args.prompt:
        if args.learn:
            x_star, y_star = args.learn
            engine.record_and_update(args.prompt, x_star, y_star)
            print(f"[SUCCESS] Updated cognitive model with outcome: X*={x_star}, Y*={y_star}")

        result = engine.predict(args.prompt)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print("\n========================================================")
            print("  AUTOPILOT COGNITIVE COMPLEX STATE ENGINE (Z = X + iY)")
            print("========================================================")
            print(f"Complex State (Z)   : {result['Z']} in C")
            print(f"Physical Depth (X)  : {result['X_continuous']} -> {result['X_description']}")
            print(f"Epistemic Depth (Y) : {result['Y_continuous']} (Internal reflection & reasoning)")
            print(f"Cognitive Budget (R): {result['R_magnitude']} (Total attentional energy)")
            print(f"Phase Angle (theta) : {result['theta_degrees']} deg -> {result['orientation']}")
            print(f"Samples Trained     : {result['samples_trained']}")
            print("========================================================\n")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
