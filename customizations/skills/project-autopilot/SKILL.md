---
name: project-autopilot
description: Enables full end-to-end autonomous project execution in Google Antigravity. Guides dynamic permission granting, implementation plan execution, continuous testing, bug fixing, and verification until all criteria are satisfied.
---

# Project Autopilot: Full Autonomous Project Execution

This skill equips the Antigravity agent to take a user's vision or list of desired features and execute them completely autonomously to completion, using optimal models and continuous self-verification.

## 1. Trigger Phrases & Security Handshake

When the user gives directives such as:
- *"Engage autopilot on this project"*
- *"I allow you all necessary actions during this project"*
- *"Keep working on this project until the implementation plan is met and tested"*
- *"Fully automate this feature set"*

### The Security Handshake (Mandatory Step):
Before executing actions without pausing for individual confirmations, you MUST:
1. Check current project settings via `agy-autopilot --dir . --status` or inspect the project configuration.
2. Present a clear security warning to the user outlining the elevated permissions:
   - Command Execution: `CASCADE_COMMANDS_AUTO_EXECUTION_EAGER`
   - File Operations: Full read/write within workspace
   - Automated testing and dependency installation
3. Confirm that the user explicitly consented (or confirm that `agy-autopilot --enable-autopilot` was run).

---

## 2. Autonomous Execution Loop

Once permissions are established, operate using the following continuous cycle:

```
[User Vision / Requirements]
           │
           ▼
[1. Actionable Milestones & Verification Plan]
           │
           ▼
[2. Automated Model Routing per Milestone]
  ├─ Mathematical / Algorithmic Core  ──► Pro / Opus Subagent
  ├─ General Code & File Operations    ──► Gemini 3.8 Flash (Primary)
  └─ Documentation & Markdown Prose    ──► GPT-OSS 120B
           │
           ▼
[3. Implementation & Test Creation]
           │
           ▼
[4. Run Automated Test Suites (pytest, npm, cargo, etc.)]
           │
           ├── Tests Fail / Edge Cases Found ──► [Auto-Diagnose & Self-Heal] ──┐
           │                                                                    │
           ▼ (Loops until 100% passing)                                         │
[5. All Criteria Satisfied & 0 Errors] ◄────────────────────────────────────────┘
           │
           ▼
[6. Produce Final Verification Walkthrough]
```

---

## 3. Quality & Self-Healing Guardrails

- **Never declare victory without test evidence**: Always run the project's test suite and inspect exit codes and error output.
- **Isolate and Fix Failures**: If a test fails, do not ask the user how to fix it unless there is architectural ambiguity. Inspect the traceback, modify the code, and re-run tests.
- **Preserve Documentation Integrity**: Do not remove existing docstrings or unrelated tests.
- **Model Attribution**: Always report which models were engaged during the autopilot cycle.
