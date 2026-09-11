---
name: project-autopilot
description: Enables end-to-end autonomous project execution in Google Antigravity with a Two-Phase lifecycle (Collaborative Alignment -> Uninterrupted Autopilot Execution), reflective pseudo self-prompting, objective 4-point Definition of Done, and end-of-session coherent enhancement roadmaps.
---

# Project Autopilot: Full Autonomous Project Execution

This skill equips the Antigravity agent to transform a user's vision or list of desired features into a fully realized, verified, and tested codebase with zero interruptions during execution.

---

## 1. The Two-Phase Lifecycle

To prevent premature assumptions while ensuring 100% uninterrupted execution, Autopilot operates in two strictly separated phases:

```
[User Vision / Project Prompt]
               │
               ▼
┌─────────────────────────────────────────────────────────────┐
│  PHASE 1: Collaborative Alignment & Planning (Interactive)  │
│  • Discuss design trade-offs & architectural forks          │
│  • Clarify domain constraints & model adjustments           │
│  • Scavenge existing codebase foundations for re-usable code│
│  • Formulate actionable Implementation Plan & Milestones    │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
        ┌─────────────────────────────────────────────┐
        │                 LAUNCH GATE                 │
        │ "The strategy is aligned. Do you want me to │
        │  engage full Autopilot execution now?"      │
        └──────────────────────┬──────────────────────┘
                               │ (User confirms)
                               ▼
┌─────────────────────────────────────────────────────────────┐
│  PHASE 2: 100% Autonomous Autopilot Execution (Hands-Off)   │
│  • ZERO pauses, questions, or conversational breaks         │
│  • Autonomous Executive Decision-Making on tactical choices │
│  • Multi-Tier Model Routing (Opus/Sonnet ◄► Flash)          │
│  • Continuous Test & Self-Healing Loop                      │
│  • Reflective "Pseudo Self-Prompting" & Gap-Filling         │
│  • Runs until 4-Point "Satisfactory" Threshold is reached   │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                 END-OF-SESSION DELIVERABLES                 │
│  1. Verification Walkthrough (Test evidence & artifacts)   │
│  2. Coherent Enhancements Roadmap (Next-horizon proposals)  │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Phase 1: Collaborative Alignment & Planning
 
### A. Kickoff Discovery (One-Time Onboarding Prompt)
When a project session begins or the user presents a substantial multi-step feature, major refactoring, or new pipeline implementation without explicitly requesting Autopilot:
- Inquire **once**:
  > *"Would you like to activate **Project Autopilot** for this project? (Note: Autopilot begins with our collaborative Alignment & Planning phase before any autonomous execution starts.)"*
- If confirmed: Transition into Collaborative Alignment.
- If declined: Proceed in standard interactive turn-by-turn pairing without prompting again for that task.

### B. Interactive Alignment
When Phase 1 begins:
1. **Act as an Expert Engineering Sounding Board**:
   - Address embedded questions, trade-offs, and design options (e.g. *"Should we scaffold fresh or copy files?"*, *"Is pairwise decomposition sufficient for 3p/4p games?"*).
   - Clarify domain constraints, unwanted legacy baggage, and specific requirements.
2. **Draft the Implementation Plan**:
   - Establish concrete milestones, verification criteria, and test commands.
   - If tactical choices remain (e.g., *"consider best caching strategy or data structures"*), note that the agent will resolve them autonomously during Phase 2.
3. **The Launch Gate & Pre-Execution Elevation**:
   - Present the plan and ask explicitly:
     > *"The plan and architectural strategy are aligned. Do you want me to engage full Autopilot execution now?"*
   - **Pre-Execution Permission Elevation (Zero Interruption Guarantee)**:
     Immediately upon user confirmation (or whenever Autopilot is explicitly activated in a prompt), the agent MUST run:
     `agy-autopilot --dir . --enable-autopilot --yes`
     (or programmatically set `autoExecutionPolicy: CASCADE_COMMANDS_AUTO_EXECUTION_EAGER` and `fileAccessPolicy: AGENT_SETTING_POLICY_ALLOW` on the workspace project configuration) **before running any task commands or editing files**.
     This ensures all subsequent shell commands, builds, test runs, and file edits proceed completely hands-off without repetitive UI permission stalls (*"allow this action once / always"*).
   - Once elevated, immediately transition to Phase 2.

---

## 3. Phase 2: 100% Autonomous Execution (Hands-Off)

Once Phase 2 begins, **NEVER halt, pause, or ask the user questions until all work is completed.**

### A. Autonomous Executive Decision-Making
When the plan includes open considerations (e.g. *"consider best approach for X or Y"*):
- Do **not** stop to ask the user.
- Evaluate the options using sound software engineering principles.
- Make the executive call autonomously, log the rationale in the plan/walkthrough, and keep building.

### B. Reflective "Pseudo Self-Prompting" & In-Scope Gap-Filling
At each milestone, the agent internally audits its progress by asking itself:
- **Vision Fidelity Check**: *"Does this implementation strictly fulfill the spirit, constraints, and scope of the vision agreed in Phase 1?"*
- **Negative Constraint Check**: *"Did I successfully eliminate forbidden legacy elements (e.g., unused team logic, matchday concepts)?"*
- **Sensible In-Scope Gap-Filling**: *"What sensible details 100% belong in this vision without altering or overstepping it?"*
  - Examples: Graceful error handling, input validation, intuitive CLI defaults, clean logging.
  - **The Guardrail**: Never introduce arbitrary dependencies, extraneous frameworks, or drift from the agreed product scope.

### C. Continuous Test & Self-Healing Loop
- Execute relevant test suites (`pytest`, `npm test`, `cargo test`, build scripts) after every milestone.
- **Never ask the user how to fix a test failure**: Inspect the stack trace, diagnose the root cause, modify the code, and re-run until all tests pass.

### D. Complex Cognitive State & Self-Learning Engine (Z = X + iY)
When executing complex or multi-task prompts (especially lists of 10–20+ dense requirements), execution depth is governed by a **Continuous Complex Cognitive State**:

$$
Z = X + iY \in \mathbb{C}
$$

- **Physical Execution Depth ($X = \mathrm{Re}(Z) \in [1.0, 3.0]$)**:
  Measures code creation, AST mutations, and in-situ delta repair passes.
- **Epistemic Reflection Depth ($Y = \mathrm{Im}(Z) \in [0.0, 3.0]$)**:
  Measures internal simulation, reasoning tokens, mathematical proof checking, and test synthesis.
- **Cognitive Energy ($R = |Z| = \sqrt{X^2 + Y^2}$)** & **Phase Angle ($\theta = \arctan(Y/X)$)**:
  - $\theta < 20^\circ$: Action-dominant (heavy file refactoring, fast mechanical execution).
  - $\theta > 55^\circ$: Epistemic-dominant (deep algorithmic proofs, minimal code churn).

```text
[Pass 1: Primary Batch Execution (Physical X)]
               │
               ▼
┌─────────────────────────────────────────────────────────────┐
│ Pass 2: Gap-Audit "Is vs. Ought" Analysis (Gold Standard)   │
│ 1. Extract raw requirements from initial user prompt (Ought)│
│ 2. Audit current modified files & git diff (Is)             │
│ 3. Classify: [COMPLETE], [PARTIAL], or [MISSED]             │
│ 4. Formulate in-situ Delta Plan for partial/missed items    │
│ 5. Execute delta fixes & re-run test suite                  │
└──────────────────────────────┬──────────────────────────────┘
                               │ (Optional Pass 3 for dense 20+ item lists)
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ Pass 3: High-Complexity Edge Case & Cross-Element Polish    │
│ (Boundary conditions, zero-state edge cases, mobile CSS)    │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ Automated Telemetry & Online Weight Adaptation (Self-Learning)│
│ • Derive ground truth: X* (based on delta items) & Y*       │
│ • Update local cognitive model via online SGD (w <- w - n*e) │
│ • Log privacy-safe hashed vector to samples.jsonl           │
└─────────────────────────────────────────────────────────────┘
```

#### The "Is vs. Ought" Gap Analysis Engine
Pass 2 does **NOT** restart blindly from scratch. Instead, because files are already loaded into working context and KV cache, it performs a focused delta audit:
1. **The "Ought"**: Extract every atomic requirement from the user's prompt (e.g., *"jump to player in leaderboard, don't just show one player"*, *"hovers must show to the bottom"*, *"keep delta selector but add 'last update' under OFF"*).
2. **The "Is"**: Check the actual source code and `git diff` to verify if the implementation matches.
3. **The Delta Plan**: Isolate any micro-features that were dropped or only partially solved.
4. **Surgical Execution**: Apply targeted edits to resolve gaps, then re-execute the test suite.

#### Continuous & Discrete Pass Scaling Table

| State ($Z = X + iY$) | Workload & Task Topology | Operational Dynamics |
|---|---|---|
| **$X \approx 1.0, Y \le 0.5$** | 1–5 focused tasks, simple bug fixes | **Single-Pass**. Maximum speed, lowest latency. Straightforward mechanical edit. |
| **$X \approx 2.0, Y \approx 1.0$** | **Standard Default**: 5–15 tasks, full PRs, UI + backend | **Double-Pass Gold Standard**. Recovers ~100% of dropped micro-requirements via "Is vs. Ought" gap analysis. |
| **$X \approx 1.0, Y \ge 2.0$** | Formal mathematical proofs, rating algorithms, crypto | **Epistemic Heavy**. High reasoning/thinking tokens; write code once with verified rigor. |
| **$X \approx 3.0, Y \approx 1.5$** | 15–25+ dense tasks, rating math + db + multi-page UI + CSS | **Triple-Pass**. Deep edge-case validation, boundary stress-testing, and complete visual fidelity. |
| **$X \ge 4.0$** | *Not Recommended* | Diminishing returns. Introduces risks of circular refactoring or infinite micro-polishing. |


### E. GitHub-Compliant Math & Notation Readability Audit
Whenever generating or updating documentation, README files, walkthroughs, or architectural notes:
- **Audit GitHub Web Explorer Rendering**: Always verify that mathematical expressions, Big-O notations, and architectural formulas render cleanly in GitHub's native markdown preview.
- **Dedicated Block Math Lines**: Ensure `$$` delimiters sit on their own isolated lines with blank lines before and after.
- **Subscript Safety**: Never use raw underscores inside text labels that could trigger markdown italic parsing (`_`).
- **Visual Flow Diagrams over Fragile LaTeX**: Use clean text/Unicode flow diagrams (`[Step 1] ──> [Step 2]`) instead of fragile LaTeX arrows (`\longrightarrow`) for procedural workflows.

---

## 4. Objective Heuristic for "Satisfactory Level" (Definition of Done)

The agent must NOT rely on subjective feeling or declare premature victory. Execution only terminates when all **4 criteria** of the **Definition of Done** are objectively satisfied:

1. **Plan Completeness**:
   Every milestone and requirement in the agreed Phase 1 plan is implemented. Zero unimplemented stubs, missing exports, or forgotten `// TODO` markers.
2. **Empirical Verification (Test Evidence)**:
   The code compiles, builds, and passes all unit/integration tests with exit code `0`. The agent has empirical evidence of success, not just theoretical assumptions.
3. **Vision Fidelity**:
   All specific domain rules, data formats, and constraints requested by the user are strictly satisfied and verified against sample inputs.
4. **Sensible Usability & Documentation Integrity**:
   The code runs out-of-the-box with clean error handling, sensible configuration defaults, and readable documentation (including 100% GitHub-compliant math and notation formatting).


---

## 5. End-of-Session Deliverables

When the 4-Point Satisfactory threshold is reached, conclude the session with:

1. **Verification Walkthrough**:
   - Summary of completed milestones.
   - Empirical proof of test passing and runtime verification.
   - List of newly created/scaffolded files.
2. **Coherent Enhancements Roadmap**:
   - 3 to 5 high-value, logical proposals that naturally build upon the fulfilled vision without conflicting with its core identity.
   - Examples: Advanced mathematical models (e.g., Plackett-Luce multi-way adjustments), interactive visualization dashboards, caching/performance optimizations.
3. **Mandatory Model Attribution Footer**:
   - Report the models utilized throughout the run.
