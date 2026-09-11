# Agent Autopilot 🚀

> **Universal Multi-Tier Model Routing, Intelligent Orchestration & Autonomous Project Execution for Google Antigravity, Claude Code, Cursor, Windsurf & Codex.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Platform: Windows | macOS | Linux](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-0078D6.svg)](https://github.com/DANeoDev/agent-autopilot)
[![Compatible: Antigravity | Claude Code | Cursor | Codex](https://img.shields.io/badge/Compatible-Antigravity%20%7C%20Claude%20Code%20%7C%20Cursor%20%7C%20Codex-4285F4.svg)](https://github.com/DANeoDev/agent-autopilot)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B%20(Tested%203.13.5)-3776AB.svg?logo=python)](https://python.org)


> [!WARNING]
> **DISCLAIMER & EXPERIMENTAL STATUS: USE AT YOUR OWN RISK!**
> **Antigravity Autopilot is experimental software and has not been extensively tested across all operating environments.**
> Autonomous execution (`project-autopilot`) elevates command and file permissions (`CASCADE_COMMANDS_AUTO_EXECUTION_EAGER`), allowing the agent to execute shell commands and modify code without per-step human review.
> - **Use strictly at your own risk.** You are solely responsible for actions taken on your system.
> - Always work on dedicated, isolated Git branches with clean commits and backups.
> - Never run in directories containing sensitive production credentials, unbacked-up data, or untrusted code.
> - Review [docs/SECURITY_AND_PERMISSIONS.md](docs/SECURITY_AND_PERMISSIONS.md) before enabling autonomous mode.

---

## 💡 Why Antigravity Autopilot?

Google Antigravity is a groundbreaking agentic development environment, but choosing between models presents constant trade-offs:
- **Fast models** (Gemini 3.8 Flash) are lightning quick for daily coding, but struggle with complex mathematical algorithm design (e.g. Glicko rating formulas) and intricate multi-file architectural refactoring.
- **Top-tier reasoning models** (Claude Opus 4.6, Claude Sonnet 4.6 Thinking) have the deepest intelligence, but are slower and carry strict hourly rate limits that you don't want to waste on simple file edits or reading logs.
- **Client UI Limitation**: In Antigravity Desktop, the model selector dropdown cannot switch itself automatically on a per-prompt basis.
- **Interactive Stalls**: Running long autonomous feature implementations (`/goal`) often halts repeatedly waiting for user permissions on every `git`, `pytest`, or file edit step.

**Antigravity Autopilot solves all of this.** It turns your agent into an **Intelligent Orchestrator**: your primary loop stays fast and responsive on Gemini 3.8 Flash, while hard reasoning, mathematical proofs, and deep refactoring are autonomously dispatched to `pro` subagents (Claude Opus / Sonnet Thinking) in the background — and with **Autopilot Mode**, entire feature lists can be implemented, tested, and self-healed hands-off.

---

## 📖 How to Use Autopilot: From a 20-Task Dump to Finished Code

You don't need to micro-manage your assistant step-by-step or spoon-feed functions one-by-one. With Antigravity Autopilot, you can dump an entire PR punch list or **15–20 substantive tasks in a single prompt**.

```
┌────────────────────────────────────────────────────────────────────────┐
│ 1. THE KICKOFF PROMPT                                                  │
│    Dump 10-20 tasks or high-level vision in a single prompt            │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ 2. PHASE 1: COLLABORATIVE ALIGNMENT & PLANNING (Interactive)           │
│    • Explores domain trade-offs & re-uses existing codebase patterns   │
│    • Structures the 20 tasks into a dependency-ordered milestone plan  │
│    • Prompts the Launch Gate: "Strategy aligned. Engage Autopilot?"    │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ (User says "yes")
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ 3. PRE-EXECUTION PERMISSION ELEVATION                                  │
│    Instantly applies eager mode; zero "allow action" UI interruptions  │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ 4. PHASE 2: AUTONOMOUS HIGH-VELOCITY EXECUTION (Hands-Off)             │
│    • Batch-executes all 20 tasks with Cognitive Momentum               │
│    • Immediate Self-Healing: Diagnoses & fixes test failures on-the-fly│
│    • Reflective Auditing: Verifies vision fidelity & strips legacy     │
│    • Terminates only when 4-Point Definition of Done is fully met      │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ 5. END-OF-SESSION DELIVERABLES                                         │
│    Verification Walkthrough (with test proof) + Future Horizon Roadmap │
└────────────────────────────────────────────────────────────────────────┘
```

### The 4-Step Prompting Walkthrough

#### Step 1: Dump Your Tasks in One Go
Paste your entire feature list into the chat:
```text
"Full Dashboard & Rating Engine Overhaul:
Enable autopilot and implement these 14 requirements:
1. Parse tournament JSON match results decomposed into pairwise matchups.
2. Update Glicko-2 backend parameters (tau=0.5, default rating=1500).
3. Create migration script for SQLite player_ratings table.
4. Build FastAPI route /api/leaderboard with min_matches filtering.
5. Add Jinja2 template leaderboard.html with sorting and delta badges.
6. Refactor CSS with clean responsive flexbox/grid layout.
7. Add streaming CSV export route for leaderboard data.
8. Build player profile view with rating history table.
9. Fix edge case where players with 0 games throw 500 error.
10. Remove deprecated RB48 delta tab and clean unused routes.
11. Write comprehensive pytest suite covering rating calculations.
12. Ensure all tests pass with code 0 and verify CLI commands."
```
> 💡 **Kickoff Discovery**: If you forget to write *"enable autopilot"* on a new project or large task, the agent proactively asks **once**:  
> *"Would you like to activate **Project Autopilot** for this project? (Note: Autopilot begins with our collaborative Alignment & Planning phase before any autonomous execution starts.)"*

#### Step 2: Phase 1 — Collaborative Alignment & Planning
The agent does **not** leap blindly into editing files. Instead, it acts as your senior engineering peer:
- It checks existing code to reuse schemas and utilities.
- It highlights any trade-offs or ambiguous choices.
- It formats all 14 tasks into an actionable Implementation Plan with clear test commands.
- It halts at the **Launch Gate**:
  > *"The strategy is aligned and the plan is ready. Do you want me to engage full Autopilot execution now?"*

#### Step 3: Pre-Execution Permission Elevation
The moment you confirm (*"yes"*, *"go ahead"*), the agent immediately elevates project permissions (`agy-autopilot --dir . --enable-autopilot --yes`).  
**Zero interruptions**: Subsequent commands, file writes, package installs, and test runs proceed hands-off without repetitive *"allow this action once / always"* UI popups.

#### Step 4: Phase 2 — Autonomous High-Velocity Execution
The agent executes the entire plan in an unbroken chain:
- **Cognitive Momentum**: Routes, templates, CSS, and tests are authored in direct alignment.
- **Immediate Self-Healing**: It runs tests immediately. If a test fails, it diagnoses the discrepancy, updates code or assertions, and re-tests until 100% passing without stopping to ask *"what should I do?"*.
- **4-Point Definition of Done**: Plan completeness, tangible test evidence (code 0), strict vision fidelity, and clean out-of-the-box usability.

---

## 🔄 Multi-Pass Self-Correction Trajectory: Why $X=2$ (Double-Pass) is the Gold Standard

When managing dense, multi-faceted prompt requests (15–20+ requirements spanning backend math, database schemas, responsive CSS, and subtle UX interactions), single-pass execution faces a universal frontier model limitation: **the LLM "attention sink" effect**.

### 1. The Real-World Prompt Challenge (The 20-Item Punch List)

Consider this real-world prompt dump from a tournament leaderboard & rating system overhaul:

```text
"Leaderboard & Rating Overhaul:
1. When using player filter, don't show 'rank #1' - show the player's ACTUAL leaderboard rank.
2. If filtering for a single player, jump/scroll to their spot in the full leaderboard rather than hiding everyone else.
3. If multiple names are provided (comma-separated), filter the table to show only those players.
4. Fix mode selector hovers (Glicko-2 / WHR) to orient downwards so they aren't clipped by the viewport.
5. Remove redundant hover icon from mode selector; keep it self-explanatory.
6. Add tooltip on the player filter explaining how the comma-separated multi-player search works.
7. Always display deltas: keep delta selector, but add 'last update' as first option under OFF.
8. Implement backend rating update timestamp tracking for leaderboard delta calculations.
9. Fix edge case where players with 0 recorded games crash profile view with 500 error.
10. Refactor leaderboard CSS: improve contrast ratio on secondary badges for WCAG accessibility.
11. Add streaming CSV export route for filtered leaderboard view.
12. Write comprehensive pytest assertions verifying ranking logic, deltas, and edge cases."
```

In a traditional single-pass execution:
- The agent builds the primary backend routes, Glicko calculations, and Jinja2 templates (Pass 1).
- But subtle micro-requirements (e.g. tooltip orientation to the bottom, the "last update" dropdown option, comma-separated name parsing) easily get lost in the attention sink.
- In turn-by-turn development, the developer must inspect every file, notice what was dropped, and manually re-prompt: *"Hey, you forgot to orient the hovers downwards and didn't add 'last update' to the selector."*

### 2. The Solution: In-Situ "Is vs. Ought" Gap Analysis

Instead of requiring human proofreading, Autopilot introduces an **autonomous self-correction trajectory** with a default depth of **Double-Pass** ($X=2$):

```text
[User Prompt: 15-20 Tasks]
             │
             ▼
┌────────────────────────────────────────────────────────┐
│ PASS 1: Primary Batch Execution                        │
│ • Builds schemas, routes, templates, CSS, and tests    │
│ • Runs test suite & resolves primary errors            │
└────────────────────────────┬───────────────────────────┘
                             │
                             ▼
┌────────────────────────────────────────────────────────┐
│ PASS 2: "Is vs. Ought" Gap Analysis (Gold Standard)    │
│ 1. Extract raw requirements line-by-line (Ought)       │
│ 2. Inspect git diff & modified files (Is)              │
│ 3. Classify: [COMPLETE], [PARTIAL], or [MISSED]        │
│ 4. Formulate in-situ Delta Plan for gaps               │
│ 5. Execute delta repairs & re-verify test suite        │
└────────────────────────────┬───────────────────────────┘
                             │ (Definition of Done satisfied)
                             ▼
┌────────────────────────────────────────────────────────┐
│ Complete, Verified Codebase with 100% Feature Fidelity │
└────────────────────────────────────────────────────────┘
```

#### Why Pass 2 is Lightning Fast & Token-Efficient:
- **Zero Cold Starts**: The agent does **not** restart from scratch or wipe existing work.
- **Warm KV-Cache**: All modified files and schemas are already loaded in working memory and server KV cache.
- **Surgical Delta Execution**: Pass 2 only writes the missing pieces (e.g., adding the dropdown option and adjusting the CSS tooltip offset).

### 3. Recommended Pass Depth Scaling Matrix

| Passes ($X$) | Workload & Prompt Density | Operational Dynamics |
|---|---|---|
| **Pass 1** (Single-Pass) | 1–5 focused tasks, simple bug fixes | Maximum velocity, minimal latency. Low probability of attention drop on narrow scopes. |
| **Pass 2** (Double-Pass) | **Standard Default**: 5–15 tasks, full PRs, UI + backend | **Gold Standard**. Recovers ~100% of dropped micro-requirements via "Is vs. Ought" delta audit. |
| **Pass 3** (Triple-Pass) | 15–25+ dense tasks, rating math + db + multi-page UI + CSS | Deep edge-case validation, boundary condition stress-testing (e.g. 0-game players), full WCAG styling audit. |
| **Pass 4+** | *Not Recommended* | Diminishing returns. Risks circular refactoring or infinite micro-polishing. |

### 4. Configuring Pass Depth via CLI

You can inspect or configure the pass depth for any workspace using `agent-autopilot`:

```bash
# View active project status and pass configuration
agent-autopilot --dir . --status

# Configure workspace to Double-Pass (Gold Standard Default)
agent-autopilot --dir . --passes 2

# Configure workspace to Triple-Pass for massive multi-tier projects
agent-autopilot --dir . --passes 3
```

---

## 🧠 Complex Cognitive State ($Z = X + iY$) & Self-Learning Engine

Autopilot does not treat pass execution as a rigid integer loop counter. In agentic software engineering, cognitive effort spans two orthogonal dimensions: **Physical Execution Depth** (mutating code) and **Epistemic Reflection Depth** (reasoning, simulating, and verifying without editing files).

Autopilot models execution depth as a continuous state in the complex plane:

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

### 1. The Two Orthogonal Dimensions of Agent Work

| Component | Dimension | Physical Meaning in Agent Runtime |
|---|---|---|
| **Real Component** ($X = \mathrm{Re}(Z) \in [1.0, 3.0]$) | **Action / Physical Mutation** | File creation, AST edits, refactoring passes, and in-situ delta repair loops. |
| **Imaginary Component** ($Y = \mathrm{Im}(Z) \in [0.0, 3.0]$) | **Epistemic / Cognitive Reflection** | Reasoning tokens, proof checking, counterfactual simulation, and test synthesis. |

#### Polar Coordinates: Energy and Phase
In polar form $Z = R e^{i\theta}$:
1. **Cognitive Energy Budget** $R = |Z| = \sqrt{X^2 + Y^2}$:
   The total computational mass allocated to the prompt.
2. **Attentional Phase Angle** $\theta = \arctan(Y/X)$:
   - $\theta < 20^\circ$ **(Action-Dominant)**: High code churn, mechanical migrations, formatting (e.g. $Z = 2.0 + 0.2i$).
   - $20^\circ \le \theta \le 50^\circ$ **(Balanced Cognitive Flow)**: Standard fullstack PRs with synchronized frontend, backend, and tests ($Z = 2.0 + 1.0i$).
   - $\theta > 55^\circ$ **(Epistemic-Dominant)**: Complex algorithms, formal proofs, concurrency invariants ($Z = 1.0 + 2.5i$).

### 2. Continuous & Fractional Pass Execution ($X \in \mathbb{R}^+$)

Pass depth is continuous rather than all-or-nothing:
- $X = 1.0$ **(Direct Pass)**: Direct batch implementation without secondary audits.
- $X = 1.3$ **(Scoped Sub-Pass)**: Pass 1 executes fully, followed by a targeted audit focused strictly on high-risk boundary constraints and negative exclusions.
- $X = 2.0$ **(Gold Standard Double-Pass)**: Full 100% "Is vs. Ought" gap audit across every prompt requirement against modified files.
- $X = 3.0$ **(Triple-Pass)**: Full double pass plus adversarial edge-case generation and cross-platform regression matrices.

### 3. Self-Learning Vocabulary via Feature Hashing (Zero Hardcoded Dictionaries)

Traditional tools rely on brittle keyword dictionaries (*"database"*, *"route"*, *"hover"*). Agent Autopilot replaces hardcoded lists with **unsupervised subword feature hashing (the hashing trick)**:

$$
h: \text{token} \longrightarrow \{1, \dots, D\} \quad (D = 256)
$$

1. **Dynamic Character 3-Gram & Token Projections**: The prompt is projected into a 256-dimensional sparse vector $\vec{\phi}(\text{prompt})$.
2. **Online Stochastic Gradient Descent (SGD)**:
   At the end of every Autopilot run, the agent evaluates ground truth $(X^*, Y^*)$ (did Pass 2 find missed items? did tests pass?) and performs an online weight update:

   $$
   \vec{w} \leftarrow \vec{w} - \eta \cdot \nabla \mathcal{L}(\vec{w}^T \vec{\phi}(\text{prompt}), X^*)
   $$

3. **Autonomous Correlation Discovery**:
   If prompts containing terms like *"mutex"*, *"debounce"*, or *"WCAG"* consistently drop requirements in Pass 1, the model **automatically increases the weights** of those hash buckets without requiring manual dictionary updates.

### 4. Privacy-First Local & Federated Telemetry

- **Zero Prompt Leaks**: Raw prompts, code, filenames, and project directories **never** leave your machine.
- **Telemetry Buffer**: Local samples are recorded as anonymized feature hashes to `~/.gemini/autopilot/telemetry/samples.jsonl`:
  ```json
  {"features_hash": "e207de1031d6bea1", "dim": 256, "pred_x": 2.0, "pred_y": 1.0, "actual_x": 1.0, "actual_y": 0.2, "samples_seen": 1}
  ```

### 5. CLI Usage: Instant Cognitive Pass Prediction

You can inspect the predicted complex state $Z = X + iY$ for any prompt before executing:

```bash
# Using agent-predict (or agy-predict)
agent-predict "Build Glicko rating volatility convergence proof and unit tests"

# Output:
# ========================================================
#   AUTOPILOT COGNITIVE COMPLEX STATE ENGINE (Z = X + iY)
# ========================================================
# Complex State (Z)   : 1.94 + 0.95i in C
# Physical Depth (X)  : 1.943 -> Double-Pass (Gold Standard)
# Epistemic Depth (Y) : 0.955 (Internal reflection & reasoning)
# Cognitive Budget (R): 2.165 (Total attentional energy)
# Phase Angle (θ)     : 26.2° -> Balanced Cognitive Flow
# Samples Trained     : 1
# ========================================================

# Or via agent-autopilot
agent-autopilot --predict "Migrate 12 Jinja templates to React"
```

---


## ⚡ The Autopilot Advantage: Velocity & Token Economics

Why does running tasks under **Antigravity Autopilot** feel orders of magnitude faster, cleaner, and more responsive?

It is not an illusion—it is a **measurable compounding effect** driven by runtime execution mechanics, cognitive context persistence, and fundamental LLM token economics.

### 1. Eliminating the "Human Ping-Pong" Latency (The Flow State)
In standard conversational pair-programming, execution is severely fragmented:

```text
[Step 1] ──> [Pause & Explain] ──> [Human Reads] ──> [User Types "OK"] ──> [Model Resumes] ──> [Step 2] ...
```

Even if each model response takes only 15–20 seconds, human context switching, reading pauses, and conversational round-trips easily stretch a **3-minute coding task into a 45-minute interactive slog**.

Under Autopilot, all 10–20 steps (reading schemas, modifying routes, adjusting templates, styling CSS, updating test suites) happen back-to-back in an **unbroken execution chain**. The assistant acts as an autonomous senior engineer executing an entire PR checklist rather than an autocomplete engine waiting for keystrokes.

### 2. Cognitive Momentum & "Hot Cache" Working Memory
When an agent is forced to stop and wait between turns, subtle state drift occurs: variable names get slightly mismatched, CSS selectors diverge, and codebase assumptions reset.

Under Autopilot, zero cold-start re-evaluation is needed:
- The full mental model of the codebase (how backend queries link with templates, variable names, query parameters, CSS utility classes, and test fixtures) stays **actively primed in working context**.
- All changes across backend, frontend, and test files are authored in direct, simultaneous alignment.

### 3. Immediate Autonomous Feedback Loops (Self-Healing in Real Time)
In traditional development, an unexpected test failure halts everything:
> *"Hey, 2 unit tests failed because default parameters changed. How should I proceed?"*

This burns two full conversational round-trips. In Autopilot:
- The test suite is triggered **immediately** after multi-file changes.
- Test failures or regressions are diagnosed on the spot, code and assertions are aligned to match project specifications, and tests are re-run until passing at 100%—**zero human pauses required**.

### 4. Systemic Batching vs. Fragmented Tweaks
In fragmented development, fixing a UI bug often exposes a route issue, which reveals a database schema oversight. Tackling them as a cohesive, batch-compiled system means touching each file **once** with complete contextual clarity, rather than patching the same file 5 times across an hour.

### 5. Extreme Token Efficiency: Defeating `O(N^2)` Inflation
From an LLM architectural perspective, Autopilot is significantly more token-efficient than turn-by-turn chat:

#### A. Eliminating the "Conversation History Tax" (`O(N^2)` Growth)
Every time a new message is sent in a traditional chat session, the **entire past conversation history** must be re-sent to the model as input tokens for that turn:

$$
\text{Input Tokens}_{\text{Turn-by-Turn}} \approx \sum_{k=1}^{N} \left( \text{Initial Context} + \sum_{i=1}^{k} \text{Turn}_i \right) \propto \mathcal{O}(N^2)
$$

Every intermediate status check, conversational transition, and "Please proceed" becomes permanent conversational weight re-processed and billed on every subsequent step.
- **Autopilot Flow**: Operates in a single continuous tool-calling trajectory. Zero redundant conversational turns re-ingesting back-and-forth history.


#### B. Zero "Politeness & Transition" Token Bloat
Standard turn-by-turn chat generates 200–500 tokens *per micro-step* of conversational filler:
> *"I have successfully modified user_service.py. Here is a summary of what changed: [...]. Now I will move on to user_profile.html. Would you like me to proceed?"*

Across 8 micro-steps, that alone generates **2,000–4,000 output tokens of pure fluff** that serves zero functional purpose and burdens subsequent turns. Autopilot strips this away entirely: it executes tool calls directly until the Definition of Done is met.

#### C. Drastic Reduction in Redundant File Inspection
When an agent halts between turns, it loses certainty and repeatedly re-runs `view_file` and `grep_search` on the same files. In a continuous Autopilot flow, a single inspection informs the routes, templates, and unit tests in one pass—no redundant re-reading.

#### D. Maximized KV-Cache Hit Rates
Modern inference backends (Gemini and Claude) rely heavily on Prompt/KV Caching. Rapid, unblocked tool sequences keep prompt prefixes warm in server memory. Long idle periods between human prompts cause cache eviction, requiring expensive re-computation of the context window.

---


## ✨ Features

- 🧠 **Dynamic 5-Tier Decision Matrix**: Classifies prompts in <50ms and routes to the exact model tier needed.
- 🧬 **Complex Cognitive State Engine** ($Z = X + iY \in \mathbb{C}$): Models execution on a continuous complex spectrum: physical file mutation ($X = \mathrm{Re}(Z) \in [1.0, 3.0]$) and epistemic reflection ($Y = \mathrm{Im}(Z) \in [0.0, 3.0]$) with polar energy and attentional phase metrics.
- 🎓 **Self-Learning Vocabulary via Feature Hashing**: Zero static keyword dictionaries. Uses character 3-gram feature hashing and online Stochastic Gradient Descent (SGD) to automatically learn which terms correlate with attention drops over time.
- 📡 **Privacy-Preserving Telemetry & Local Buffer**: Stores purely anonymized numeric vectors and empirical outcomes locally (`samples.jsonl`) with zero prompt text, code, or filename exposure.
- 🚀 **Proactive Autopilot Onboarding (Kickoff Discovery)**: When initiating a major feature or new project without explicitly requesting Autopilot, the agent proactively asks *once* if you want to activate Project Autopilot (starting cleanly with Collaborative Alignment & Planning before any execution).
- 🤖 **Two-Phase Autonomous Project Mode (`project-autopilot`)**:
  - **Phase 1: Collaborative Alignment**: The agent acts as an engineering sounding board to discuss architectural trade-offs, clarify domain rules, and align on a detailed implementation plan.
  - **The Launch Gate**: Prompts explicitly: *"The plan is aligned. Do you want me to engage full Autopilot execution now?"*
  - **Pre-Execution Elevation**: Automatically configures the workspace project settings to eager mode *prior* to task execution, guaranteeing zero interactive "allow this action" permission stalls.
  - **Phase 2: Uninterrupted Hands-Off Execution**: ZERO stops or questions. Tactical choices ("consider approach X or Y") are decided autonomously via executive decision-making.
- 🔍 **Reflective "Pseudo Self-Prompting"**: The agent continuously audits itself during execution:
  - *"Does this fulfill the original vision and constraints?"*
  - *"What sensible features belong 100% in this vision without overstepping?"* (graceful error handling, input validation, clean CLI defaults).
- 🎯 **Objective 4-Point Definition of Done ("Satisfactory" Threshold)**:
  1. *Plan Completeness*: All agreed milestones implemented (zero `TODO` stubs).
  2. *Empirical Verification*: Real tests and builds pass with exit code `0`.
  3. *Vision Fidelity*: Strict adherence to domain constraints.
  4. *Sensible Usability*: Clean error handling, sensible defaults, ready out-of-the-box.
- 🔮 **End-of-Session Coherent Enhancements Roadmap**: Concludes with test verification evidence and 3–5 high-value, logical next-step proposals that naturally expand the completed vision.
- 🛡️ **Explicit Security Handshake**: Never elevates project permissions silently. Shows clear warnings and requires explicit user consent before enabling eager execution.
- 🔒 **100% Strict User Override**: Say `"use currently selected model"` or `"no subagents"`, and the agent strictly executes directly without delegating.
- 📉 **Quota & Rate Limit Awareness**: Actively protects Claude Opus and Sonnet token caps. Partitions tasks and falls back to capable models when quota pressure is detected.
- 📐 **GitHub-Compliant Math & Notation Auditing**: Autopilot actively audits generated documentation, architecture notes, and walkthroughs so that all mathematical formulas, Big-O notations, and technical diagrams adhere to GitHub Flavored Markdown (GFM) and render flawlessly in GitHub's web repository explorer.
- 🏷️ **Transparent Model Attribution**: Concludes every response with an attribution footer detailing which model(s) performed the work.

---

## 📊 Model Decision Matrix

| Tier | Target Model | Provider | Typical Tasks | Subagent Tier |
|---|---|---|---|---|
| **Tier 1** | `gemini-3.5-flash-lite` | Google | Typos, quick regex, format conversions, simple lookups | `flash_lite` |
| **Tier 2** | `gemini-3.8-flash` *(Default)* | Google | Daily coding, unit tests, pair programming, tool calls | `flash` (direct) |
| **Tier 3** | `gpt-oss-120b` | Open Source | Documentation, READMEs, technical prose, audits | `standard` |
| **Tier 4** | `claude-sonnet-4-6-thinking` | Anthropic | Multi-file refactors, deep debugging, state tracing | `pro` |
| **Tier 5** | `claude-opus-4-6` | Anthropic | Glicko/Elo rating math, system architecture, `/goal` | `pro` |

---

## 💻 System & Platform Compatibility

Antigravity Autopilot is engineered as a **Universal Multi-Agent Orchestration Layer**. It integrates cleanly into Google Antigravity as well as prominent CLI and IDE agent terminals:

### 🤖 Supported Agent Terminals & Environments

| Terminal / Agent | Configuration Path | How Autopilot Integrates |
|---|---|---|
| **Google Antigravity** | `~/.gemini/config/AGENTS.md` + `skills/` | Full two-phase autopilot skill, model router, and permission manager. |
| **Anthropic Claude Code (`claude`)** | `~/.claude/CLAUDE.md` | Machine-wide user memory for unbroken PR checklists & reflective loops. |
| **Cursor AI Agent** | `~/.cursorrules` | System-wide agent rules and 4-point Definition of Done heuristics. |
| **Windsurf Cascade** | `~/.windsurfrules` | Cascade global autonomous rules & cognitive momentum protocol. |
| **OpenAI Codex & Universal Agents** | `~/AGENTS.md` & `~/.config/agents/AGENTS.md` | Universal agent convention (Aider, OpenHands, Cline, Roo Code). |

### 🖥️ Operating Systems & Runtimes

| Component | Target / Verified Specification | Status |
|---|---|---|
| **Antigravity Engine** | **Google Antigravity v2.12.2+** (ProductVersion 2.12.2.0; Antigravity 2.0+ architecture) | ✅ Primary Reference Target |
| **Primary OS** | **Windows 11** (Build 10.0.26200+, AMD64 64-bit) & **Windows 10** (1809+) | ✅ Native 1-Click Installer (`install.bat`) |
| **macOS Support** | macOS 13+ (Ventura, Sonoma, Sequoia - Apple Silicon & Intel) | ✅ Supported via `./scripts/install.sh` |
| **Linux / WSL** | Ubuntu 22.04+, Debian 12+, Fedora 38+, Arch, WSL2 | ✅ Supported via `./scripts/install.sh` |
| **Python Runtime** | **Python 3.10+** (Verified on Python 3.13.5 64-bit) | ✅ Required for CLI tools & router |

---

## 🚀 Quickstart & Universal Installation

The installer automatically detects installed agent environments (`.gemini`, `.claude`, `.cursor`, `.codeium`) and installs the appropriate configuration across all of them in a single step.

### 🪟 Windows (1-Click Multi-Agent Install)

#### Option A: Double-Click Installer (Zero Command Line)
1. Clone or download this repository.
2. Double-click **`install.bat`** in the repository root.
3. Done! Machine-wide rules, skills, and CLI binaries are instantly deployed to Antigravity, Claude Code, and your User `PATH`.

#### Option B: PowerShell
```powershell
git clone https://github.com/DANeoDev/agent-autopilot.git
cd agent-autopilot

# Auto-detect and install to all active agents
.\scripts\install.ps1

# Or target specific agents:
.\scripts\install.ps1 -Target all           # Install to Antigravity, Claude, Cursor, Windsurf, Codex
.\scripts\install.ps1 -Target claude        # Install strictly for Claude Code
.\scripts\install.ps1 -Target antigravity   # Install strictly for Antigravity
```

### 🍎 macOS & 🐧 Linux (1-Line Shell Install)

Run the native POSIX installer:
```bash
git clone https://github.com/DANeoDev/agent-autopilot.git
cd agent-autopilot
chmod +x scripts/install.sh
./scripts/install.sh
```

*This auto-detects installed agent directories, installs rules to `~/.gemini`, `~/.claude`, and `~/AGENTS.md`, deploys executable wrappers (`agent-route`, `agent-autopilot`, `agy-route`, `agy-autopilot`) to `~/.gemini/antigravity/bin`, and adds the bin directory to your `~/.zshrc` / `~/.bashrc`.*


---

## 🛠️ How to Use It Day-to-Day

### 1. In Antigravity Chat (Standard Usage)
Keep your primary model set to **Gemini 3.8 Flash (Medium)**.
- For everyday tasks: The agent responds instantly.
- For deep tasks: *"Design a Glicko rating volatility formula"* ➔ The agent automatically detects Tier 5 complexity and delegates the algorithmic design to a `pro` subagent in the background.

### 2. Full Project Autopilot (Two-Phase Execution)
Paste your project vision, requirements, or discussion points:
```text
"TTA - New Project pipeline
I added a folder with tournament match results. Matches in 3p/4p games are handled as individual 1on1s.
Discuss if it is possible to adjust this model. Build a clean stats page, player profiles, and model analysis.
Re-use our existing foundation, but use standard time-based Glicko/WHR (no matchday, no team logic)."
```
1. **Phase 1 (Collaborative Alignment)**:
   - The agent discusses architectural forks with you (e.g. scaffolding fresh vs copying files).
   - Explores domain nuances and agrees on scope.
   - Formulates the Implementation Plan with verification milestones.
   - Triggers the **Launch Gate**: *"The strategy is aligned. Do you want me to engage full Autopilot execution now?"*
2. **Phase 2 (100% Autonomous Hands-Off Execution)**:
   - Evaluates tactical choices autonomously without pausing.
   - Executes implementation, tests, and self-heals code until the **4-point Definition of Done** is satisfied.
   - Performs reflective "pseudo self-prompting" to ensure vision fidelity and sensible gap-filling (clean error handling, sensible defaults).
   - Concludes with a **Verification Walkthrough** and a **Coherent Enhancements Roadmap** for future iterations.

### 3. User Overrides & Quota Conservation
- **Force current model**: *"Refactor the auth controller, use currently selected model"* ➔ Skips all subagents.
- **Quota conservation**: *"Conserve Claude tokens for now"* ➔ Diverts Tier 4 tasks to Flash/GPT-OSS.

### 4. From Any Command Line (CLI Tools)
```bash
# Instant model recommendation for any prompt (use agent-route or agy-route)
agent-route "Design a new Glicko rating volatility algorithm"

# JSON output for automated agent pipelines and scripts
agent-route --json "Fix typo in variable name"

# Inspect active project settings
agent-autopilot --dir . --status

# Enable autonomous execution permissions for current workspace
agent-autopilot --dir . --enable-autopilot
```

---

## 📚 Documentation Deep Dives

For exhaustive technical breakdowns of specific subsystems:

- 🧠 **[docs/COGNITIVE_ENGINE.md](docs/COGNITIVE_ENGINE.md)**: Deep dive on the complex plane ($Z = X + iY$), polar energy & phase metrics, base concept priors, and unsupervised vocabulary learning.
- 🔄 **[docs/MULTI_PASS_AUTOPILOT.md](docs/MULTI_PASS_AUTOPILOT.md)**: The Double-Pass ($X=2$) Gold Standard, the "Is vs. Ought" Gap Analysis Engine, and the 20-item tournament prompt benchmark.
- 📡 **[docs/TELEMETRY_AND_LEARNING.md](docs/TELEMETRY_AND_LEARNING.md)**: Explicit (Default) vs. Anonymous telemetry modes, local sample buffers, and online Stochastic Gradient Descent (SGD) mechanics.
- 🏗️ **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)**: Overall system runtime architecture, velocity dynamics, and mathematical proofs defeating quadratic token inflation.
- 🛡️ **[docs/SECURITY_AND_PERMISSIONS.md](docs/SECURITY_AND_PERMISSIONS.md)**: Permission elevation guidelines, experimental disclaimers, and security boundaries.

---

## 📁 Repository Structure

```text
agent-autopilot/
├── bin/
│   ├── agy_router.py              # Cross-platform CLI task classifier & decision engine
│   ├── agy_project_manager.py     # Cross-platform project permissions & autopilot manager
│   ├── cognitive_engine.py        # Self-learning continuous complex pass predictor (Z = X + iY)
│   ├── agy-route.bat / agy-route  # Route launchers
│   ├── agy-autopilot.bat / agy-autopilot # Autopilot launchers
│   ├── agy-predict.bat / agy-predict # Cognitive state predictor launchers
│   ├── agent-route.bat / agent-route # Universal route launchers
│   ├── agent-autopilot.bat / agent-autopilot # Universal autopilot launchers
│   └── agent-predict.bat / agent-predict # Universal cognitive state predictor launchers
├── customizations/
│   ├── rules/
│   │   └── AGENTS.md              # Machine-wide model orchestration & complex cognitive rules
│   └── skills/
│       ├── model-router/          # Skill: Task classification & subagent dispatch
│       │   └── SKILL.md
│       └── project-autopilot/     # Skill: Complex cognitive state execution & online learning
│           └── SKILL.md
├── docs/
│   ├── ARCHITECTURE.md            # Overall system architecture, runtime dynamics & token economics
│   ├── COGNITIVE_ENGINE.md        # Complex plane Z=X+iY, polar metrics & dynamic vocabulary learning
│   ├── MULTI_PASS_AUTOPILOT.md    # Double-Pass (X=2) Gold Standard, "Is vs. Ought" gap analysis & case study
│   ├── TELEMETRY_AND_LEARNING.md  # Explicit (Default) vs Anonymous modes, telemetry buffers & online SGD
│   └── SECURITY_AND_PERMISSIONS.md # Security boundaries & permission guidelines
├── models/
│   └── cognitive_weights.json     # Calibrated baseline & locally learned neural feature weights
├── scripts/
│   ├── install.bat                # Windows batch bootstrap runner
│   ├── install.ps1                # Multi-agent Windows PowerShell installer
│   ├── install.sh                 # Multi-agent macOS & Linux Bash installer
│   ├── uninstall.ps1              # Windows uninstaller
│   ├── uninstall.sh               # macOS & Linux uninstaller
│   └── verify.ps1                 # Windows health check script
├── install.bat                    # Root 1-click double-clickable Windows installer
├── LICENSE                        # MIT License
└── README.md                      # Documentation
```

---

## 🗑️ Uninstallation

To cleanly remove the global skills and binaries from your machine:

**Windows (PowerShell):**
```powershell
.\scripts\uninstall.ps1
```

**macOS & Linux (Bash):**
```bash
./scripts/uninstall.sh
```

*(Your `~/.gemini/config/AGENTS.md` is preserved so custom non-autopilot rules are not lost).*

---

## 📜 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for more information.
