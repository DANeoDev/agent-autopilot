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

When the user first presents a vision or project proposal:
1. **Act as an Expert Engineering Sounding Board**:
   - Address embedded questions, trade-offs, and design options (e.g. *"Should we scaffold fresh or copy files?"*, *"Is pairwise decomposition sufficient for 3p/4p games?"*).
   - Clarify domain constraints, unwanted legacy baggage, and specific requirements.
2. **Draft the Implementation Plan**:
   - Establish concrete milestones, verification criteria, and test commands.
   - If tactical choices remain (e.g., *"consider best caching strategy or data structures"*), note that the agent will resolve them autonomously during Phase 2.
3. **The Launch Gate (Mandatory Confirmation)**:
   - Present the plan and ask explicitly:
     > *"The plan and architectural strategy are aligned. Do you want me to engage full Autopilot execution now?"*
   - Also verify the **Security Handshake** (confirm `agy-autopilot --enable-autopilot` or consent to eager execution).
   - Once the user gives the green light, immediately transition to Phase 2.

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

---

## 4. Objective Heuristic for "Satisfactory Level" (Definition of Done)

The agent must NOT rely on subjective feeling or declare premature victory. Execution only terminates when all **4 criteria** of the **Definition of Done** are objectively satisfied:

1. **Plan Completeness**:
   Every milestone and requirement in the agreed Phase 1 plan is implemented. Zero unimplemented stubs, missing exports, or forgotten `// TODO` markers.
2. **Empirical Verification (Test Evidence)**:
   The code compiles, builds, and passes all unit/integration tests with exit code `0`. The agent has empirical evidence of success, not just theoretical assumptions.
3. **Vision Fidelity**:
   All specific domain rules, data formats, and constraints requested by the user are strictly satisfied and verified against sample inputs.
4. **Sensible Usability**:
   The code runs out-of-the-box with clean error handling, sensible configuration defaults, and readable documentation.

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
