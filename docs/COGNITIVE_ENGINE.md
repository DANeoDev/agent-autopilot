# Cognitive Engine Architecture: The Complex Plane ($Z = X + iY$) & Dynamic Self-Learning

## 1. Beyond Discrete Pass Counters

Traditional AI developer tooling treats loop execution as a binary or integer counter (Pass 1, Pass 2). In real-world software engineering, cognitive effort is not one-dimensional:
- Writing 500 lines of mechanical boilerplate requires high physical file mutation, but negligible mathematical reflection.
- Deriving a formal proof of rating volatility convergence requires high mathematical reflection, but very few physical code mutations.

To capture this fundamental distinction, Agent Autopilot models cognitive workload as a continuous state in the complex plane:

$$
Z = X + iY \in \mathbb{C}
$$

```text
              Imaginary Axis (Y: Epistemic / Reflection Depth)
                   ▲
                   │
                   │     Z = 1.0 + 2.5i (e.g., Glicko Convergence Proof:
                   │                     Write code once, think deeply)
                   │          ●
                   │
                   │               Z = 2.0 + 1.0i (Fullstack Leaderboard:
                   │                               Double-pass code, balanced thinking)
                   │                    ●
                   │
                   │                          Z = 2.0 + 0.2i (Bulk CSS Migration:
                   │                                          Double pass on files, low math)
                   │                               ●
                   └────────────────────────────────────────► Real Axis (X: File Action Depth)
```

---

## 2. Orthogonal Cognitive Dimensions

### 2.1 The Real Component: Physical Action Depth ($X = \mathrm{Re}(Z) \in [1.0, 3.0]$)
Measures the depth of physical file mutation, AST alterations, and in-situ delta repair cycles:
- **$X = 1.0$ (Direct Single-Pass)**: Direct batch execution. Code is authored in a single continuous tool-calling trajectory without secondary audits.
- **$X = 1.3$ (Scoped Sub-Pass)**: Pass 1 executes fully, followed by a targeted audit focused strictly on high-risk boundary constraints and negative exclusions.
- **$X = 2.0$ (Double-Pass Gold Standard)**: Full Pass 1 execution followed by a 100% "Is vs. Ought" gap audit comparing prompt requirements against modified files.
- **$X = 3.0$ (Triple-Pass)**: Full double pass plus adversarial edge-case stress-testing, fuzzing, and cross-platform matrix validation.

### 2.2 The Imaginary Component: Epistemic Reflection Depth ($Y = \mathrm{Im}(Z) \in [0.0, 3.0]$)
Measures internal cognitive deliberation that occurs without touching files:
- Extended reasoning tokens (Claude Thinking / CoT).
- Invariant formulation and mathematical proof checking.
- Counterfactual simulation (evaluating alternative architectural trade-offs).
- Property-based test synthesis.

### 2.3 Polar State Coordinates ($Z = R e^{i\theta}$)
Representing $Z$ in polar form reveals two vital operational metrics:

1. **Cognitive Energy Budget ($R = |Z| = \sqrt{X^2 + Y^2}$)**:
   The total computational mass allocated to the prompt.
2. **Attentional Phase Angle ($\theta = \arctan(Y/X)$)**:
   - **$\theta < 20^\circ$ (Action-Dominant)**: High code churn, mechanical migrations, formatting (e.g. $Z = 2.0 + 0.2i$).
   - **$20^\circ \le \theta \le 50^\circ$ (Balanced Cognitive Flow)**: Standard fullstack PRs with synchronized frontend, backend, and tests ($Z = 2.0 + 1.0i$).
   - **$\theta > 55^\circ$ (Epistemic-Dominant)**: Complex algorithms, formal proofs, concurrency invariants ($Z = 1.0 + 2.5i$).

---

## 3. Dynamic Vocabulary Learning vs. Hardcoded Dictionaries

A common flaw in naive task classifiers is hardcoding static keyword dictionaries (`"database"`, `"route"`, `"hover"`). This approach fails across diverse languages (Rust, Go, C++, Zig, TypeScript, SQL) and novel frameworks.

Agent Autopilot implements a **Hybrid Semantic Architecture**:

```text
[Incoming User Prompt]
          │
          ├────────────────────────────────────────┬────────────────────────────────────────┐
          ▼                                        ▼                                        ▼
┌───────────────────┐                    ┌───────────────────┐                    ┌───────────────────┐
│ Base Concept      │                    │ Dynamically       │                    │ Subword & Trigram │
│ Priors (Seed)     │                    │ Learned Terms     │                    │ Feature Hashing   │
│ (Initial Taxonomy)│                    │ (Self-Learned)    │                    │ (Hashing Trick)   │
└─────────┬─────────┘                    └─────────┬─────────┘                    └─────────┬─────────┘
          │                                        │                                        │
          └────────────────────────────────────────┼────────────────────────────────────────┘
                                                   ▼
                                     [Continuous Prediction: Z = X + iY]
```

### 3.1 Base Meaning Priors (The Seed Taxonomy)
Before any user feedback is collected, the engine is initialized with baseline priors across universal software engineering concepts:

| Concept Domain | Seed Terms | Prior Bias |
|---|---|---|
| **Concurrency & Synchronization** | `mutex`, `lock`, `deadlock`, `race`, `atomic`, `semaphore` | High Epistemic ($\Delta Y \approx +0.45$), Moderate Action ($\Delta X \approx +0.20$) |
| **UI Nuances & Accessibility** | `hover`, `tooltip`, `dropdown`, `viewport`, `contrast`, `wcag`, `aria` | High Action ($\Delta X \approx +0.35$), Moderate Epistemic ($\Delta Y \approx +0.15$) |
| **Algorithmic Rigor** | `algorithm`, `proof`, `convergence`, `probability`, `variance`, `recursion` | High Epistemic ($\Delta Y \approx +0.55$), Low Action ($\Delta X \approx +0.10$) |
| **State & Migrations** | `migration`, `schema`, `transaction`, `rollback`, `foreign` | High Action ($\Delta X \approx +0.40$), Moderate Epistemic ($\Delta Y \approx +0.20$) |
| **Boundary & Edge Cases** | `boundary`, `null`, `overflow`, `exception`, `retry` | Balanced ($\Delta X \approx +0.25, \Delta Y \approx +0.30$) |

### 3.2 Dynamic Vocabulary Discovery
When the agent executes a task:
1. Novel words in the prompt (e.g. `backpressure`, `reentrancy`, `futex`, `hydration`) are extracted.
2. If Pass 2 gap analysis reveals that the task required higher passes ($X^* > 1.5$ or $Y^* > 1.0$), credit assignment distributes weight adjustments to these novel terms.
3. Over time, the engine maintains an explicit dictionary of **dynamically learned terms** stored in `models/cognitive_weights.json`.

You can inspect the learned vocabulary at any time:
```bash
agent-predict --learned-terms
```

### 3.3 Feature Hashing (The Hashing Trick)
To handle unseen words, foreign identifiers, and domain-specific acronyms, prompts are simultaneously projected into a 256-dimensional sparse vector using character 3-grams and MurmurHash/MD5:

$$
h: \text{token} \longrightarrow \{1, \dots, 256\}
$$

Global weights $\vec{w}$ learn correlations between hash buckets and task complexity via online Stochastic Gradient Descent (SGD).

---

## 4. CLI Inspection & Diagnostic Tools

```bash
# Instant pass prediction with full polar state
agent-predict "Implement socket backpressure with bounded ring buffers"

# View semantic contributing terms (base priors + learned terms)
agent-predict "Fix tooltip hover and add mutex to prevent deadlock" --explain

# Inspect all dynamically discovered terms
agent-predict --learned-terms

# Configure telemetry mode
agent-predict --telemetry-mode explicit
agent-predict --telemetry-mode anonymous
```
