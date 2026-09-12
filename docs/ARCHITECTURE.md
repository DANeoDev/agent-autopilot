# Architecture & Technical Design

## 1. The Antigravity Runtime Model

Google Antigravity is an AI-first development platform built around an autonomous execution loop. In typical IDE or Desktop usage:

- The **Primary Agent** runs in an active chat canvas or terminal session.
- The user selects an active LLM for that conversation turn (e.g., Gemini 3.8 Flash, Claude Sonnet 4.6 Thinking, Claude Opus 4.6).
- The client UI dropdown cannot be mutated mid-turn by the agent itself.

To overcome this limitation and provide **fully automated, hands-off model optimization**, Agent Autopilot implements **Hierarchical Multi-Agent Delegation**.

```
                   ┌───────────────────────────────────────────────┐
                   │             User Request / Prompt             │
                   └───────────────────────┬───────────────────────┘
                                           │
                                           ▼
                   ┌───────────────────────────────────────────────┐
                   │      Primary Orchestrator (Fast Loop)         │
                   │           (e.g., Gemini 3.8 Flash)            │
                   └───────┬───────────────────────────────┬───────┘
                           │                               │
        [Tier 1/2 Tasks:   │                               │ [Tier 4/5 Tasks:
         Everyday Coding,  │                               │  Complex Logic, Math,
         Local File Edits] │                               │  System Architecture]
                           ▼                               ▼
                 ┌───────────────────┐           ┌───────────────────┐
                 │ Handled Directly  │           │   pro Subagent    │
                 │   in Fast Loop    │           │ (Claude Sonnet /  │
                 │   (Low Latency)   │           │    Claude Opus)   │
                 └───────────────────┘           └─────────┬─────────┘
                                                           │
                                                           ▼
                                                 ┌───────────────────┐
                                                 │ Deep Reasoning,   │
                                                 │ Proofs & Solution │
                                                 └─────────┬─────────┘
                                                           │
                                                           ▼
                   ┌───────────────────────────────────────────────┐
                   │       Merged Verification & Attribution       │
                   └───────────────────────────────────────────────┘
```

---

## 2. The Decision Matrix

Tasks are classified across three core dimensions:
1. **Algorithmic & Mathematical Depth**: Does the task require formal statistical logic, probability distributions, or complex state machines?
2. **Structural Scope**: Is this a single-line fix, a standard module, or a multi-file architectural refactor?
3. **Reasoning Traceability**: Is an extended thinking process required to prevent regressions?

| Tier | Target Model | Subagent Param | Typical Workload |
|---|---|---|---|
| **Tier 1** | `gemini-3.5-flash-lite` | `flash_lite` | Typo fixes, format conversions, simple regex, documentation queries |
| **Tier 2** | `gemini-3.8-flash` | `flash` | Standard feature development, unit testing, pairing, tool execution |
| **Tier 3** | `gpt-oss-120b` | `standard` | Technical prose, user documentation, open-source reproducibility audits |
| **Tier 4** | `claude-sonnet-4-6-thinking` | `pro` | Tricky multi-file refactors, edge-case debugging, state tracing |
| **Tier 5** | `claude-opus-4-6` | `pro` | Core rating algorithms (e.g. Glicko), system architecture, `/goal` |

---

## 3. Quota Optimization Protocol

High-tier models (Claude Opus and Sonnet Thinking) have stricter hourly and daily token limits. Agent Autopilot actively protects these limits:
- **Downwards Delegation**: When running primary on Claude Opus, broad codebase scans and file searches are offloaded to `flash_lite` subagents.
- **Kernel Partitioning**: Only the core mathematical algorithm is dispatched to high-tier models. Boilerplate, imports, and scaffolding remain on Flash.
- **Fallback Grace**: If rate limit warnings are received, the router automatically downgrades Tier 4 tasks to Gemini 3.8 Flash, reserving Opus strictly for tasks where a drop in model tier would cause a substantial drop in quality.

---

## 4. The Two-Phase Autopilot Engine & Reflective Loop

Autonomous development requires a strict boundary between strategic deliberation and uninterrupted execution. Agent Autopilot implements a stateful Two-Phase lifecycle:

```
[Vision / Feature Prompt]
           │
           ▼
┌─────────────────────────────────────────────────────────────┐
│  Kickoff Discovery (One-Time Prompt if Not Explicit)        │
│  • Asks user once: "Activate Project Autopilot?"            │
│  • Clarifies: Mode starts with Alignment/Planning, not raw  │
│    execution!                                               │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│  Phase 1: Collaborative Alignment & Planning                │
│  • Agent acts as an engineering sounding board              │
│  • Explores trade-offs & domain nuances interactively       │
│  • Scavenges existing codebases for re-usable foundations   │
│  • Crystallizes actionable Implementation Plan & Milestones │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
        ┌─────────────────────────────────────────────┐
        │                 LAUNCH GATE                 │
        │ "The strategy is aligned. Do you want me to │
        │  engage full Autopilot execution now?"      │
        └──────────────────────┬──────────────────────┘
                               │ (User Confirms)
                               ▼
        ┌─────────────────────────────────────────────┐
        │       PRE-EXECUTION PERMISSION ELEVATION    │
        │ • Sets autoExecutionPolicy: EAGER           │
        │ • Sets fileAccessPolicy: ALLOW              │
        │ • Eliminates interactive popups completely  │
        └──────────────────────┬──────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│  Phase 2: 100% Autonomous Execution (Hands-Off)             │
│  • ZERO interruptions or conversational pauses              │
│  • Autonomous Executive Decision-Making on tactical choices │
│  • Continuous Test & Self-Healing Loop                      │
│  • Reflective "Pseudo Self-Prompting"                       │
│    - Vision Fidelity Check                                  │
│    - Negative Constraint Check (Strip unwanted legacy code) │
│    - Sensible Gap-Filling (Error handling, clean defaults)  │
│  • Terminates only when 4-Point Definition of Done is met   │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│  End-of-Session Deliverables                                │
│  1. Verification Walkthrough (Test evidence & artifacts)   │
│  2. Coherent Enhancements Roadmap (Next-horizon proposals)  │
└─────────────────────────────────────────────────────────────┘
```

### 4.1 The 4-Point "Definition of Done" (Objective Heuristic)

To avoid premature completion ("lazy exit") or infinite over-engineering, Phase 2 execution evaluates against a 4-point objective rubric:

1. **Plan Completeness**: Every milestone agreed upon in Phase 1 is implemented. Zero stubbed functions or forgotten `// TODO` items.
2. **Empirical Verification**: Real tests, builds, and CLI executions run and exit with code `0`. Verification requires tangible proof, not theoretical assumption.
3. **Vision Fidelity**: Explicit domain constraints and user rules are strictly respected and validated against real sample inputs.
4. **Sensible Usability**: The deliverable works out-of-the-box with clean error handling, sensible configuration defaults, and readable documentation.

### 4.2 The Multi-Pass Self-Correction Trajectory ($X$-Pass Autopilot)

When an agent is presented with a complex, dense list of 15–20+ requirements, single-pass batch execution experiences the classic LLM **"attention sink"** phenomenon. Frontier models prioritize structural scaffolding (schemas, models, main routes), but frequently drop 10%–25% of micro-requirements (e.g., hover tooltip orientations, specific dropdown options, edge-case checks, contrast adjustments).

```text
[Initial User Prompt: 15-20 Atomic Requirements]
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│ Pass 1: Primary Architectural Scaffolding & Core Features    │
│ • Database schema migrations & backend endpoints            │
│ • Main UI templates & component layouts                     │
│ • Pytest / unit test execution                              │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ Pass 2: In-Situ "Is vs. Ought" Gap Analysis (Gold Standard)  │
│ • Extract user prompt requirements: {r_1, r_2, ..., r_m}     │
│ • Code diff comparison: Evaluate implemented state vs prompt│
│ • Classify: [COMPLETE], [PARTIAL], or [MISSED]              │
│ • Formulate Delta Plan & execute surgical fixes in-situ     │
│ • Re-verify test suite with exit code 0                     │
└──────────────────────────────┬──────────────────────────────┘
                               │ (Optional Pass 3 for dense 20+ item lists)
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ Pass 3: Edge-Case Stress Testing & Cross-Element Polishing  │
│ • Boundary conditions (0-game players, null states)         │
│ • Mobile layout, contrast ratios, and doc synchronization   │
└─────────────────────────────────────────────────────────────┘
```

#### The "Is vs. Ought" Formalism

Let $P = \{r_1, r_2, \dots, r_m\}$ represent the set of atomic requirements specified in the user's prompt. After Pass 1, the codebase state is $C_1$.

The agent computes the delta set $\Delta(P, C_1)$:

$$
\Delta(P, C_1) = \left\{ r_i \in P \;\middle|\; \mathrm{Status}(r_i, C_1) \in \{ \mathrm{PARTIAL}, \mathrm{MISSED} \} \right\}
$$

Pass 2 executes repairs strictly targeting $\Delta(P, C_1)$ without cold-starting or rewriting established code $C_1$. Because $C_1$ is already resident in server KV cache, Pass 2 executes with near-zero latency and high token efficiency.

#### Real-World Case Study (The 20-Item Leaderboard Punch List)

In a real-world testing benchmark, a prompt requested 12 dense requirements across backend Glicko/WHR rating engines, Jinja2 templates, and responsive CSS:
1. *Player filter*: Display actual leaderboard rank instead of `#1`.
2. *Single-player search*: Scroll/jump to player row in the full leaderboard rather than filtering other players out.
3. *Multi-name search*: Support comma-separated player list filtering.
4. *Hover direction*: Force mode selector tooltips to orient downwards to prevent viewport clipping.
5. *Hover cleanup*: Remove unnecessary hover icons on self-explanatory mode toggles.
6. *Filter guidance*: Add tooltip explaining the multi-name comma filter syntax.
7. *Deltas view*: Keep delta selector visible at all times, with "last update" as the top option under OFF.
8. *Timestamp tracking*: Record rating calculation timestamps for delta diffing.
9. *Zero-game edge cases*: Prevent 500 error when inspecting player profiles with 0 recorded matches.
10. *Accessibility*: Adjust badge color contrast to meet WCAG standards.
11. *Export route*: Build streaming CSV download for filtered table views.
12. *Verification*: Write pytest suite confirming rating calculations and edge-case handling.

- **Single-Pass Execution** ($X=1$): The agent successfully delivered items 1, 2, 8, 9, 11, and 12, but dropped the hover downwards orientation (item 4), omitted "last update" from the delta dropdown (item 7), and filtered out other players instead of scrolling to the single player (item 2 nuance).
- **Double-Pass Execution** ($X=2$): Pass 2 detected all 3 discrepancies during the "Is vs. Ought" gap audit, applied surgical edits to CSS and Jinja2 templates, and achieved 100% prompt fidelity without a single user intervention.

#### Recommended Pass Scaling Matrix

| Passes ($X$) | Workload & Prompt Density | Operational Dynamics |
|---|---|---|
| **Pass 1** (Single-Pass) | 1–5 focused tasks, simple bug fixes | Maximum speed, lowest latency. Minimal attention sink on narrow tasks. |
| **Pass 2** (Double-Pass) | **Standard Default**: 5–15 tasks, full PRs, UI + backend | **Resilient Gold Standard** ($X = 2.2$). Recovers ~100% of dropped micro-requirements via "Is vs. Ought" gap analysis and delta re-verification. |
| **Pass 3** (Triple-Pass) | 15–25+ dense tasks, rating math + db + multi-page UI + CSS | Deep edge-case validation, boundary stress-testing, and complete visual/documentation fidelity. |
| **Pass 4+** | *Not Recommended* | Diminishing returns. Risks circular refactoring or infinite micro-polishing loops. |

### 4.3 The Complex Cognitive Plane ($Z = X + iY$) & Self-Learning Engine

In advanced agent theory, execution depth cannot be restricted to an integer counter. Cognitive effort naturally bifurcates into two orthogonal dimensions: **Physical Action Depth** (creating and mutating code) and **Epistemic Reflection Depth** (reasoning, simulating, and verifying without modifying files).

Autopilot models execution state as a continuous parameter in the complex plane:

$$
Z = X + iY \in \mathbb{C}
$$

```text
              Imaginary Axis (Y: Epistemic / Reflection Depth)
                   ▲
                   │
                   │     Z = 1.0 + 2.5i (Mathematical Proof:
                   │                     Write code once, think deeply)
                   │          ●
                   │
                   │               Z = 2.2 + 1.0i (Fullstack Overhaul:
                   │                               Resilient double-pass, balanced thinking)
                   │                    ●
                   │
                   │                          Z = 2.0 + 0.2i (Bulk CSS Refactor:
                   │                                          Double pass on files, low math)
                   │                               ●
                   └────────────────────────────────────────► Real Axis (X: File Action Depth)
```

#### Orthogonal State Dimensions
1. **Physical Action Depth** ($X = \mathrm{Re}(Z) \in [1.0, 3.0]$):
   Quantifies file mutations, AST adjustments, and in-situ delta repair cycles:
   - $X = 1.0$: Direct batch execution without secondary audits.
   - $X = 1.3$: Scoped sub-pass targeting high-risk boundary constraints.
   - $X = 2.2$: Resilient Double-Pass Gold Standard (Pass 1 batch execution + 100% "Is vs. Ought" gap audit + surgical delta re-verification).
   - $X = 3.0$: Triple-pass with multi-tier stress testing and cross-platform matrix checks.
2. **Epistemic Reflection Depth** ($Y = \mathrm{Im}(Z) \in [0.0, 3.0]$):
   Quantifies internal verification tokens, counterfactual simulation, test synthesis, and mathematical proof checking prior to file writes.
3. **Polar State Metrics** ($Z = R e^{i\theta}$):
   - **Cognitive Energy Budget** ($R = |Z| = \sqrt{X^2 + Y^2}$): The total attentional mass allocated to the prompt.
   - **Attentional Phase Angle** ($\theta = \arctan(Y/X)$):
     - $\theta < 20^\circ$: Action-dominant (heavy file refactoring, minimal reflection).
     - $20^\circ \le \theta \le 50^\circ$: Balanced cognitive flow (synchronized backend, frontend, and tests).
     - $\theta > 55^\circ$: Epistemic-dominant (formal mathematical proofs, protocol invariants).

#### Dynamic Feature Hashing & Online Self-Learning

To eliminate reliance on static, hand-curated keyword dictionaries, Autopilot implements an unsupervised subword feature hashing engine (the hashing trick):

$$
h: \text{token} \longrightarrow \{1, \dots, D\} \quad (D = 256)
$$

1. **Subword & Character 3-Gram Hashing**: Incoming prompts are projected into a 256-dimensional sparse vector $\vec{\phi}(\text{prompt}) \in \mathbb{R}^{256}$.
2. **Online Stochastic Gradient Descent (SGD)**:
   At the conclusion of each session, empirical ground truth $(X^*, Y^*)$ is evaluated based on whether Pass 2 uncovered delta items or test regressions:

   $$
   \vec{w} \leftarrow \vec{w} - \eta \cdot \nabla \mathcal{L}\left( \vec{w}^T \vec{\phi}(\text{prompt}), X^* \right)
   $$

3. **Autonomous Correlation Discovery**:
   The engine automatically discovers which subword patterns correlate with attention drops across any language or domain, continuously tuning local weights without human intervention.
4. **Privacy-Preserving Telemetry**:
   Hashed vectors and outcome signals are appended to local storage (`~/.gemini/autopilot/telemetry/samples.jsonl`). Zero raw prompt text, code, or file paths ever leave the user's system.

### 4.4 Coherent Enhancements Roadmap

Upon reaching the Satisfactory threshold, the session automatically delivers 3–5 high-value, logical next-step proposals that naturally expand upon the fulfilled foundation without violating product identity.

---

## 5. Theoretical Foundations: Velocity Dynamics & Token Economics

The dramatic speedup and quality gains observed during autonomous execution are grounded in formal runtime dynamics and LLM inference mathematics.

### 5.1 The Human Ping-Pong Multiplier vs. Uninterrupted Batch Execution

In standard conversational pair-programming, wall-clock time is dominated not by model inference, but by **interactive friction**:

$$
\text{Total Wall Clock Time} = \sum_{k=1}^{M} \left( T_{\mathrm{infer}, k} + T_{\mathrm{read}, k} + T_{\mathrm{prompt}, k} + T_{\mathrm{switch}, k} \right)
$$

Even with an ultra-fast model ($T_{\mathrm{infer}} \approx 10\text{s}$), human review, prompt formulation, and conversational pauses add $60\text{s}$ to $180\text{s}$ per turn. A 15-step feature implementation balloons from **3 minutes of model compute into 45+ minutes of human waiting**.

Under **Autopilot**, the human friction terms $T_{\mathrm{read}} + T_{\mathrm{prompt}} + T_{\mathrm{switch}} \to 0$:

$$
\text{Total Autopilot Time} \approx \sum_{k=1}^{M} T_{\mathrm{infer}, k}
$$

All steps execute back-to-back at hardware speed.

### 5.2 Cognitive Momentum & Working Context Continuity

When an agent pauses between prompts:
1. **Context Drift**: In traditional turn-by-turn prompting, each user message subtly shifts the attention distribution. Variable names, template IDs, and database column names risk drifting across separate turns.
2. **Cold-Start File Re-Inspection**: Disjointed agents repeatedly call `view_file` or `grep_search` to verify symbols they previously inspected because their internal certainty decays.
3. **Hot Cache Continuity**: In Autopilot, a single unified trajectory holds the schema, backend routes, HTML template blocks, CSS classes, and test fixtures in uninterrupted working context. Code is written in total lockstep with zero re-inspection overhead.

### 5.3 Mathematical Proof: Defeating `O(N^2)` Token Inflation

The common belief that autonomous agents consume more tokens is mathematically false. Turn-by-turn chat carries a severe **"Conversation History Tax"** that compounds quadratically.

#### The Turn-by-Turn History Tax (`O(N^2)` Growth):
On each user turn $k \in [1, N]$, the client re-transmits the initial system prompt $S$ plus the entire transcript of all prior user messages $U_i$ and assistant responses $A_i$:

$$
\text{Cumulative Input Tokens}_{\text{Turn-by-Turn}} = \sum_{k=1}^{N} \left( S + \sum_{i=1}^{k-1} (U_i + A_i) \right) = N \cdot S + \sum_{k=1}^{N} (N - k)(U_k + A_k) \propto \mathcal{O}(N^2)
$$

#### The Autopilot Trajectory (`O(N)` Tool Execution):
In Autopilot, execution occurs within a single turn via continuous tool call steps $T_k$. The initial prompt $S$ and user intent $U$ are processed **once**, and tool outputs are streamed linearly without re-packaging cumulative conversational back-and-forths:

$$
\text{Cumulative Input Tokens}_{\text{Autopilot}} \approx S + U + \sum_{k=1}^{M} \Delta_{\mathrm{tool}, k} \propto \mathcal{O}(N)
$$


#### Elimination of "Conversational Fluff":
Standard interactive turns generate 200–500 tokens *per turn* of polite transitions:
> *"I have modified `app/routes.py`. Here is a breakdown: [...]. Would you like me to proceed with the unit tests now?"*

Over a 12-turn task, this produces **2,500–5,000 output tokens of pure filler** that permanently bloats the conversation history. Autopilot eliminates this overhead entirely.

#### KV-Cache Eviction Mitigation:
Modern model inference engines (such as Gemini and Anthropic Claude) maintain server-side **Prompt/KV Caching**:
- **Continuous Trajectories**: Steps occur within milliseconds of tool returns, achieving **near-100% KV-cache hit rates** on prefix tokens.
- **Human Interactive Breaks**: Pauses of 1 to 5 minutes between human prompts cause cache eviction on shared inference clusters, forcing full re-computation of long context windows on subsequent turns.

---

## 6. System Environment & Platform Compatibility

Agent Autopilot is designed to run seamlessly across all primary developer operating systems and agent terminal environments.

### 6.1 Multi-Agent Terminal Architecture

While originally engineered for Google Antigravity, Autopilot's decision matrix, two-phase lifecycle, and execution heuristics are **terminal-agnostic**. The installer automatically provisions guidelines and CLI tools across all prominent AI development terminals:

| Agent Terminal | User Configuration Target | Behavioral Effect |
|---|---|---|
| **Google Antigravity** | `~/.gemini/config/AGENTS.md`<br>`~/.gemini/config/skills/` | Machine-wide rules, hierarchical subagent dispatch, and eager project permission manager. |
| **Anthropic Claude Code (`claude`)** | `~/.claude/CLAUDE.md` | Injects Two-Phase Autopilot and Definition of Done into Claude's persistent user memory. |
| **Cursor AI Agent** | `~/.cursorrules` | Provides global instructions for unbroken PR execution, self-healing, and GFM math safety. |
| **Windsurf Cascade** | `~/.windsurfrules` | Equips Cascade with cognitive momentum batching and pre-execution elevation protocols. |
| **OpenAI Codex & Universal** | `~/AGENTS.md`<br>`~/.config/agents/AGENTS.md` | Standard markdown agent instructions recognized by Aider, OpenHands, Cline, and Roo Code. |

### 6.2 Operating Systems & Runtimes

| Component | Target / Verified Specification | Details |
|---|---|---|
| **Antigravity Engine** | **Google Antigravity v2.12.2+** (ProductVersion `2.12.2.0`) | Compatible with the Antigravity 2.0+ architecture, built-in skill loading, and multi-agent subagent protocols. |
| **Primary Reference OS** | **Windows 11 (Build 10.0.26200+, AMD64)** & **Windows 10 (1809+)** | 1-Click native installation via `install.bat` and `scripts/install.ps1`. Seamless User PATH registration. |
| **macOS Support** | macOS 13+ (Ventura, Sonoma, Sequoia - Apple Silicon & Intel) | Native POSIX installer via `scripts/install.sh`. Configures `~/.gemini/config/` and shell rc (`~/.zshrc` / `~/.bashrc`). |
| **Linux & WSL2** | Ubuntu 22.04+, Debian 12+, Fedora 38+, Arch Linux | Native POSIX installer via `scripts/install.sh`. Pure Python standard-library CLI tools. |
| **Python Runtime** | **Python 3.10+** (Tested on Python 3.13.5) | Standard library only (`os`, `sys`, `json`, `pathlib`, `argparse`). Zero third-party dependencies required. |

---

## 7. Subsystem Documentation Deep Dives

For targeted, in-depth architectural and implementation guides:

- 🧠 **[COGNITIVE_ENGINE.md](COGNITIVE_ENGINE.md)**: Mathematical modeling of the complex plane ($Z = X + iY$), polar coordinates ($R, \theta$), base meaning taxonomy, and dynamic subword vocabulary learning.
- 🔄 **[MULTI_PASS_AUTOPILOT.md](MULTI_PASS_AUTOPILOT.md)**: Double-Pass ($X=2$) Gold Standard, the "Is vs. Ought" Gap Analysis Engine, and the 20-item tournament prompt case study.
- 📡 **[TELEMETRY_AND_LEARNING.md](TELEMETRY_AND_LEARNING.md)**: Explicit (Default) vs. Anonymous telemetry modes, local sample buffers, online SGD mathematics, and privacy boundaries.
- 🛡️ **[SECURITY_AND_PERMISSIONS.md](SECURITY_AND_PERMISSIONS.md)**: Security boundaries, permission elevations, and safety protocols.



