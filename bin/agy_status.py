#!/usr/bin/env python3
"""
Antigravity Autopilot - Visual HUD & Cognitive Telemetry Dashboard
Visualizes the complex state vector Z = X + iY, Prompt Viability Q,
learned vocabulary influences, and real-time online learning trajectories.
"""

import sys
import os
import math
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from bin.cognitive_engine import (
    CognitiveEngine,
    USER_WEIGHTS_FILE,
    REPO_WEIGHTS_FILE,
    DEFAULT_TELEMETRY_FILE,
    evaluate_prompt_viability
)


def render_bar(value: float, min_val: float, max_val: float, width: int = 20, fill_char: str = "█", empty_char: str = "░") -> str:
    """Renders a bounded visual progress meter."""
    clamped = max(min_val, min(max_val, value))
    ratio = (clamped - min_val) / max(1e-6, (max_val - min_val))
    filled_len = int(round(ratio * width))
    empty_len = max(0, width - filled_len)
    return f"[{fill_char * filled_len}{empty_char * empty_len}]"


def load_recent_telemetry_samples(limit: int = 4) -> List[Dict[str, Any]]:
    """Loads the most recent telemetry samples from samples.jsonl."""
    if not DEFAULT_TELEMETRY_FILE.exists():
        return []
    samples = []
    try:
        with open(DEFAULT_TELEMETRY_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        samples.append(json.loads(line))
                    except Exception:
                        pass
    except Exception:
        return []
    return samples[-limit:]


def render_terminal_dashboard(engine: CognitiveEngine, prompt_preview: Optional[str] = None) -> str:
    """Builds the complete terminal dashboard string."""
    weights_path = engine.weights_path
    samples_count = engine.samples_seen
    vocab_count = len(engine.learned_terms)
    
    # Baseline vector
    raw_x = engine.b_x
    raw_y = engine.b_y
    r_base = math.sqrt(raw_x**2 + raw_y**2)
    theta_base = math.degrees(math.atan2(raw_y, raw_x))

    if prompt_preview:
        pred = engine.predict(prompt_preview)
        disp_x = pred["X_continuous"]
        disp_y = pred["Y_continuous"]
        disp_r = pred["R_magnitude"]
        disp_theta = pred["theta_degrees"]
        disp_orientation = pred["orientation"]
        viability = pred.get("viability", {})
    else:
        disp_x = raw_x
        disp_y = raw_y
        disp_r = r_base
        disp_theta = theta_base
        disp_orientation = "Balanced Cognitive Flow" if (20 <= theta_base <= 50) else ("Epistemic" if theta_base > 50 else "Action")
        viability = evaluate_prompt_viability("Standard Autopilot Continuous Execution")

    q_val = viability.get("Q", 0.85)
    q_spec = viability.get("Q_spec", 0.85)
    q_test = viability.get("Q_test", 0.80)
    q_scope = viability.get("Q_scope", 0.90)
    q_class = viability.get("classification", "VIABLE")

    bar_x = render_bar(disp_x, 1.0, 3.0, width=18)
    bar_y = render_bar(disp_y, 0.0, 3.0, width=18)
    bar_q = render_bar(q_val, 0.0, 1.0, width=18, fill_char="█", empty_char="░")

    lines = []
    lines.append("╔══════════════════════════════════════════════════════════════════════════════════════╗")
    lines.append("║                   🤖 ANTIGRAVITY AUTOPILOT - COGNITIVE HUD DASHBOARD                 ║")
    lines.append("║                        Continuous State Vector Z = X + iY in C                       ║")
    lines.append("╠══════════════════════════════════════════════════════════════════════════════════════╣")
    lines.append(f"║  Active Model Weights : {str(weights_path)[-56:]:<56} ║")
    lines.append(f"║  Empirical Dataset    : {samples_count:<4} training samples | Vocabulary: {vocab_count:<5} learned tokens ║")
    lines.append("╠══════════════════════════════════════════════════════════════════════════════════════╣")
    lines.append("║ 1. COGNITIVE COMPLEX STATE VECTOR (Z)                                                ║")
    lines.append(f"║    Vector Equation    : Z = {disp_x:.2f} + {disp_y:.2f}i                                              ║")
    lines.append(f"║    Physical Depth (X) : {bar_x} {disp_x:.2f} / 3.00 (Pass 1 & Gap Audits)       ║")
    lines.append(f"║    Epistemic Depth (Y): {bar_y} {disp_y:.2f} / 3.00 (Reflection & Proofs)      ║")
    lines.append(f"║    Attentional Energy : R = |Z| = {disp_r:.3f} | Phase Angle θ = {disp_theta:.1f}°                    ║")
    lines.append(f"║    Phase Alignment    : {disp_orientation[:58]:<58} ║")
    lines.append("╠══════════════════════════════════════════════════════════════════════════════════════╣")
    lines.append("║ 2. PROMPT VIABILITY & DETERMINISM (Q)                                                ║")
    lines.append(f"║    Composite Score Q  : {bar_q} {q_val:.2f} / 1.00 [{q_class[:24]:<24}] ║")
    lines.append(f"║    * Specificity (Q_spec)   : {q_spec:.2f} (Concrete targets vs. subjective vagueness)     ║")
    lines.append(f"║    * Verifiability (Q_test) : {q_test:.2f} (Intent-aware acceptance criteria)             ║")
    lines.append(f"║    * Scope Density (Q_scope): {q_scope:.2f} (Structural bounds & punch-lists)             ║")

    hints = viability.get("hints", [])
    if hints:
        lines.append(f"║    * Refinement Hint        : {hints[0][:55]:<55} ║")
    ex_rewrite = viability.get("example_rewrite")
    if ex_rewrite:
        lines.append(f"║    * Example Rewrite        : \"{ex_rewrite[:52]}\"... ║")

    lines.append("╠══════════════════════════════════════════════════════════════════════════════════════╣")
    lines.append("║ 3. DYNAMICALLY LEARNED VOCABULARY (Online SGD Subword Feature Hashing)               ║")
    top_terms = engine.get_top_learned_terms(limit=6)
    if not top_terms:
        lines.append("║    No dynamic terms recorded yet. Engine operating on base concept priors.           ║")
    else:
        for t in top_terms:
            term = t['term']
            dx = t.get('delta_x', 0.0)
            dy = t.get('delta_y', 0.0)
            occ = t.get('occurrences', 1)
            lines.append(f"║    • {term:<16} : ΔX={dx:+.3f}, ΔY={dy:+.3f} (seen {occ:<2}x) | Concept Prior Active        ║")

    lines.append("╠══════════════════════════════════════════════════════════════════════════════════════╣")
    lines.append("║ 4. RECENT TELEMETRY TRAJECTORIES                                                     ║")
    recent = load_recent_telemetry_samples(limit=3)
    if not recent:
        lines.append("║    No historical telemetry samples recorded in ~/.gemini/autopilot/telemetry/       ║")
    else:
        for s in recent:
            prompt_snip = s.get("prompt_preview", s.get("prompt_snippet", "task trajectory"))[:36]
            x_star = s.get("actual_x_star", 2.2)
            y_star = s.get("actual_y_star", 1.0)
            ts = s.get("timestamp", "")[:19].replace("T", " ")
            lines.append(f"║    [{ts}] \"{prompt_snip:<34}\" -> ({x_star:.1f}, {y_star:.1f}) ║")

    lines.append("╚══════════════════════════════════════════════════════════════════════════════════════╝")
    return "\n".join(lines)


def export_html_dashboard(engine: CognitiveEngine, output_file: Path, prompt_preview: Optional[str] = None):
    """Generates an elegant dark-mode HTML dashboard artifact."""
    pred = engine.predict(prompt_preview or "Antigravity Autopilot Continuous State")
    disp_x = pred["X_continuous"]
    disp_y = pred["Y_continuous"]
    disp_r = pred["R_magnitude"]
    disp_theta = pred["theta_degrees"]
    disp_orientation = pred["orientation"]
    v = pred.get("viability", {})
    q_val = v.get("Q", 0.88)
    q_class = v.get("classification", "VIABLE")
    top_terms = engine.get_top_learned_terms(limit=15)
    recent = load_recent_telemetry_samples(limit=10)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Antigravity Autopilot - Cognitive HUD Dashboard</title>
<style>
  :root {{
    --bg: #0d1117;
    --card-bg: #161b22;
    --border: #30363d;
    --text: #c9d1d9;
    --text-bright: #f0f6fc;
    --accent-blue: #58a6ff;
    --accent-green: #3fb950;
    --accent-purple: #bc8cff;
    --accent-yellow: #d29922;
  }}
  body {{
    background: var(--bg);
    color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    margin: 0;
    padding: 24px;
  }}
  .container {{ max-width: 1080px; margin: 0 auto; }}
  header {{
    border-bottom: 1px solid var(--border);
    padding-bottom: 16px;
    margin-bottom: 24px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}
  h1 {{ margin: 0; font-size: 24px; color: var(--text-bright); }}
  .badge {{
    background: #1f242c;
    border: 1px solid var(--accent-blue);
    color: var(--accent-blue);
    padding: 4px 10px;
    border-radius: 12px;
    font-size: 13px;
  }}
  .grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 20px;
    margin-bottom: 24px;
  }}
  .card {{
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 20px;
  }}
  .card h2 {{
    margin-top: 0;
    font-size: 16px;
    color: var(--accent-blue);
    border-bottom: 1px solid var(--border);
    padding-bottom: 8px;
  }}
  .big-metric {{
    font-size: 32px;
    font-weight: 700;
    color: var(--text-bright);
    margin: 8px 0;
  }}
  .progress-bg {{
    background: #21262d;
    border-radius: 6px;
    height: 12px;
    width: 100%;
    margin: 8px 0 16px 0;
    overflow: hidden;
  }}
  .progress-fill {{
    height: 100%;
    background: linear-gradient(90deg, var(--accent-blue), var(--accent-purple));
  }}
  table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
  }}
  th, td {{
    padding: 8px 12px;
    text-align: left;
    border-bottom: 1px solid var(--border);
  }}
  th {{ color: var(--text-bright); background: #21262d; }}
  .pill-pos {{ color: var(--accent-green); }}
  .pill-neg {{ color: var(--accent-yellow); }}
</style>
</head>
<body>
<div class="container">
  <header>
    <div>
      <h1>⚡ Antigravity Autopilot - Live Cognitive HUD</h1>
      <div style="font-size: 14px; margin-top: 4px; color: #8b949e;">Continuous Complex Pass Vector & Empirical Online Learning State</div>
    </div>
    <span class="badge">{disp_orientation}</span>
  </header>

  <div class="grid">
    <div class="card">
      <h2>1. Complex State Vector (Z = X + iY)</h2>
      <div class="big-metric">{disp_x:.2f} + {disp_y:.2f}i</div>
      <div style="font-size: 13px;">Cognitive Energy Budget: <b>R = {disp_r:.3f}</b> | Attentional Phase: <b>θ = {disp_theta:.1f}°</b></div>
      
      <div style="margin-top: 16px; font-size: 13px;">Physical Action Depth (X): <b>{disp_x:.2f} / 3.00</b></div>
      <div class="progress-bg"><div class="progress-fill" style="width: {(disp_x/3.0)*100}%;"></div></div>

      <div style="font-size: 13px;">Epistemic Reflection Depth (Y): <b>{disp_y:.2f} / 3.00</b></div>
      <div class="progress-bg"><div class="progress-fill" style="width: {(disp_y/3.0)*100}%; background: var(--accent-purple);"></div></div>
    </div>

    <div class="card">
      <h2>2. Prompt Viability & Guardrails (Q)</h2>
      <div class="big-metric" style="color: var(--accent-green);">Q = {q_val:.2f}</div>
      <div style="font-size: 13px; color: var(--accent-blue);">{q_class}</div>
      
      <div style="margin-top: 16px; font-size: 13px;">Specificity (Q_spec): <b>{v.get('Q_spec', 0.85):.2f}</b></div>
      <div style="font-size: 13px; margin-top: 4px;">Verifiability (Q_test): <b>{v.get('Q_test', 0.80):.2f}</b></div>
      <div style="font-size: 13px; margin-top: 4px;">Scope Feasibility (Q_scope): <b>{v.get('Q_scope', 0.90):.2f}</b></div>

      <div style="margin-top: 16px; font-size: 12px; color: #8b949e; background: #21262d; padding: 10px; border-radius: 6px;">
        💡 <b>Recommendation</b>: {v.get('hints', ['Prompt structure fully optimal'])[0]}
      </div>
    </div>
  </div>

  <div class="grid">
    <div class="card" style="grid-column: 1 / -1;">
      <h2>3. Dynamically Learned Vocabulary ({len(engine.learned_terms)} tokens discovered)</h2>
      <table>
        <thead>
          <tr>
            <th>Learned Subword Token</th>
            <th>Action Impact (ΔX)</th>
            <th>Epistemic Impact (ΔY)</th>
            <th>Observed Count</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
"""
    for t in top_terms:
        dx = t.get('delta_x', 0.0)
        dy = t.get('delta_y', 0.0)
        occ = t.get('occurrences', 1)
        html += f"""          <tr>
            <td><code>{t['term']}</code></td>
            <td class="{'pill-pos' if dx >= 0 else 'pill-neg'}">{dx:+.3f}</td>
            <td class="{'pill-pos' if dy >= 0 else 'pill-neg'}">{dy:+.3f}</td>
            <td>{occ}</td>
            <td>Active Online Weight</td>
          </tr>
"""
    html += """        </tbody>
      </table>
    </div>
  </div>

  <div class="grid">
    <div class="card" style="grid-column: 1 / -1;">
      <h2>4. Empirical Task Trajectories</h2>
      <table>
        <thead>
          <tr>
            <th>Timestamp</th>
            <th>User Prompt Trajectory Preview</th>
            <th>Target Physical Depth (X*)</th>
            <th>Target Epistemic Depth (Y*)</th>
          </tr>
        </thead>
        <tbody>
"""
    for s in recent:
        p_prev = s.get("prompt_preview", s.get("prompt_snippet", "session turn"))
        ts = s.get("timestamp", "")[:19].replace("T", " ")
        x_star = s.get("actual_x_star", 2.2)
        y_star = s.get("actual_y_star", 1.0)
        html += f"""          <tr>
            <td>{ts}</td>
            <td><code>{p_prev}</code></td>
            <td><b>{x_star:.2f}</b></td>
            <td><b>{y_star:.2f}</b></td>
          </tr>
"""
    html += """        </tbody>
      </table>
    </div>
  </div>
</div>
</body>
</html>
"""
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Antigravity Autopilot - Interactive Visual HUD & Telemetry Dashboard")
    parser.add_argument("prompt", nargs="*", default=[], help="Optional prompt to evaluate on the HUD")
    parser.add_argument("--watch", action="store_true", help="Live refresh terminal HUD every 2 seconds")
    parser.add_argument("--html", type=str, metavar="FILE", help="Export standalone HTML visual dashboard to specified file path")
    parser.add_argument("--json", action="store_true", help="Output HUD metrics as JSON")
    args = parser.parse_args()

    active_prompt = " ".join(args.prompt).strip() if args.prompt else None
    engine = CognitiveEngine()

    if args.html:
        out_path = Path(args.html)
        export_html_dashboard(engine, out_path, active_prompt)
        print(f"[SUCCESS] Exported interactive visual HUD dashboard to: {out_path.resolve()}")
        return

    if args.json:
        pred = engine.predict(active_prompt or "Autopilot Status Baseline")
        print(json.dumps({
            "engine_state": pred,
            "samples_trained": engine.samples_seen,
            "learned_vocabulary_size": len(engine.learned_terms),
            "weights_path": str(engine.weights_path)
        }, indent=2))
        return

    if args.watch:
        try:
            while True:
                os.system("cls" if os.name == "nt" else "clear")
                # Reload engine weights in case background turns updated them
                engine.load_weights()
                print(render_terminal_dashboard(engine, active_prompt))
                print("\n  [Press Ctrl+C to exit Live HUD Watch Mode]")
                time.sleep(2)
        except KeyboardInterrupt:
            print("\nExiting Live HUD.")
            return

    print(render_terminal_dashboard(engine, active_prompt))


if __name__ == "__main__":
    main()
