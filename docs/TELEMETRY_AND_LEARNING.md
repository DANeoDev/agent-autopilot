# Telemetry & Self-Learning Architecture

## 1. The Closed-Loop Ground Truth Engine

A machine learning model is only as good as its feedback signal. Traditional AI assistants rely on human thumbs-up/thumbs-down buttons, which are subjective, noisy, and rarely provided.

Agent Autopilot generates **objective, empirical ground truth $(X^*, Y^*)$ automatically** at the conclusion of every execution:

```text
[Pass 1 Execution] ──> [Test Suite Execution] ──> [Pass 2 "Is vs. Ought" Gap Analysis]
                                                               │
                                                               ▼
                                       ┌────────────────────────────────────────────────┐
                                       │ Objective Ground-Truth Derivation:             │
                                       │ • N_delta = count([PARTIAL] + [MISSED] items)  │
                                       │ • N_regressions = count(Test failures)         │
                                       │ • Cost = token volume & wall-clock time        │
                                       └───────────────────────┬────────────────────────┘
                                                               │
                                                               ▼
                                             (X*, Y*) Ground Truth Computed
                                                               │
                                                               ▼
                                       [Online SGD Update & Local Telemetry Buffer]
```

### The Ground Truth Formula:
- **$X^* = 1.0$**: All requirements implemented in Pass 1, 0 test failures, and 0 delta items found during the gap audit. Running secondary passes was unnecessary.
- **$X^* = 2.0$**: Pass 1 dropped $\ge 1$ micro-requirements, and Pass 2 successfully resolved them. Double-pass was optimal.
- **$X^* = 3.0$**: Pass 2 required deep secondary edge-case refinement or resolved regressions caught during secondary testing.
- **$Y^*$**: Scaled proportionally to internal reasoning token depth and complexity of invariant checking.

---

## 2. Dual Telemetry Modes: Explicit (Default) vs. Anonymous

Autopilot supports two telemetry modes configured machine-wide or per-project:

```bash
# Set telemetry mode via CLI
agent-autopilot --telemetry explicit     # Standard Default
agent-autopilot --telemetry anonymous    # Privacy-Hashed Mode
```

### 2.1 Explicit Mode (The Standard Default)

> **Why is Explicit Mode the Standard Default?**  
> Raw prompt text and exact Pass 2 delta items carry orders of magnitude more information than opaque numerical vectors. Storing the prompt text locally enables:
> 1. **Dynamic Vocabulary Discovery**: The engine can parse exact subwords, terms, and multi-word phrases (e.g., *"socket backpressure"*, *"reentrant lock"*) and correlate them with pass difficulty.
> 2. **Contextual Error Analysis**: Allows inspecting exactly which prompt phrasing patterns lead frontier models into attention sinks.
> 3. **High-Fidelity Model Retraining**: Enables local retraining of embedding models and future fine-tuning of agent decision policies.

#### Sample Explicit Telemetry Entry (`~/.gemini/autopilot/telemetry/samples.jsonl`):
```json
{
  "mode": "explicit",
  "timestamp": "2026-09-12T01:05:00.123456+00:00",
  "prompt": "Fix hover dropdown and add mutex synchronization to avoid deadlock",
  "token_count": 10,
  "pred_Z": {"X": 2.67, "Y": 1.23},
  "actual_outcome": {"X_star": 2.5, "Y_star": 2.0},
  "delta_items_detected": ["mutex lock contention test", "dropdown hover offset"],
  "test_exit_code": 0,
  "terms_updated_count": 6,
  "samples_seen": 3
}
```

---

### 2.2 Anonymous Mode (Privacy-Hashed Mode)

For sensitive commercial codebases, private infrastructure projects, or compliance-restricted enterprise environments, **Anonymous Mode** completely strips prompt text and filenames:

- Replaces raw prompt text with a non-reversible SHA-256 hash of the feature vector.
- Records only normalized numerical metrics ($D=256$), token length, and $(X^*, Y^*)$ outcomes.
- Zero intellectual property, prompt text, or code ever touches the telemetry file.

#### Sample Anonymous Telemetry Entry:
```json
{
  "mode": "anonymous",
  "timestamp": "2026-09-12T01:05:00.123456+00:00",
  "features_hash": "e207de1031d6bea1",
  "token_count": 10,
  "dim": 256,
  "pred_x": 2.67,
  "pred_y": 1.23,
  "actual_x": 2.5,
  "actual_y": 2.0,
  "samples_seen": 3
}
```

---

## 3. Online Stochastic Gradient Descent (SGD) Updates

At the conclusion of each session, the engine executes an in-situ gradient descent update:

### 3.1 Weight Vector Adjustment
Let $\vec{x} = \vec{\phi}(\text{prompt}) \in \mathbb{R}^{256}$ be the normalized feature vector:

$$
e_x = \hat{X} - X^*, \quad e_y = \hat{Y} - Y^*
$$

$$
\vec{w}_x \leftarrow \vec{w}_x - \eta \cdot e_x \cdot \vec{x}
$$

$$
\vec{w}_y \leftarrow \vec{w}_y - \eta \cdot e_y \cdot \vec{x}
$$

$$
b_x \leftarrow b_x - \frac{1}{2}\eta \cdot e_x, \quad b_y \leftarrow b_y - \frac{1}{2}\eta \cdot e_y
$$

### 3.2 Dynamic Term Credit Assignment
For every meaningful word $w \in \text{prompt}$:
- If $w$ already exists in `learned_terms`:
  - $\Delta X(w) \leftarrow \Delta X(w) - \frac{1}{2}\eta \cdot e_x$
  - $\Delta Y(w) \leftarrow \Delta Y(w) - \frac{1}{2}\eta \cdot e_y$
  - Increments occurrence counter $\mathrm{count}(w) \leftarrow \mathrm{count}(w) + 1$.
- If $w$ is a novel word and $|e_x| > 0.1$ or $|e_y| > 0.1$:
  - Inserts $w$ into `learned_terms` with initial weights proportional to the error gradient.

---

## 4. Local File Storage Locations

| Artifact | Path | Description |
|---|---|---|
| **Model Weights** | `models/cognitive_weights.json` | Calibrated baseline priors and dynamically learned vocabulary |
| **Telemetry Log** | `~/.gemini/autopilot/telemetry/samples.jsonl` | Append-only training samples buffer |
| **Configuration** | `~/.gemini/autopilot/config.json` | Global telemetry mode setting (`explicit` vs `anonymous`) |
