# Antigravity Global Model Orchestration Guidelines

These guidelines apply across all projects and workspaces on this machine.

---

## 1. Automatic Model Evaluation & Task Routing

Whenever the user presents a request, evaluate the required capability, reasoning depth, and latency tolerance against the **Model Decision Matrix**:

### Model Decision Matrix

| Tier | Target Model | Subagent Parameter | Typical Tasks |
|---|---|---|---|
| **Tier 1: High-Speed / Simple** | `gemini-3.5-flash-lite` | `flash_lite` | Quick 1-to-few line edits, typo fixes, simple regex, file format conversion, quick lookups. |
| **Tier 2: Standard Agentic (Default)** | `gemini-3.8-flash` | `flash` | Daily coding, unit tests, interactive pair programming, command execution, standard bug fixes. |
| **Tier 3: Documentation & Prose** | `gpt-oss-120b` | `standard` | Writing documentation, READMEs, technical explanations, open-source audit / reproducible tasks. |
| **Tier 4: Deep Logic & Refactoring** | `claude-sonnet-4-6-thinking` | `pro` | Multi-file refactoring, tricky debugging, step-by-step logical deductions, complex state tracing. |
| **Tier 5: Architecture & Advanced Math** | `claude-opus-4-6` | `pro` | Mathematical & statistical algorithm design (e.g., Glicko rating formulas), system-level architecture, long-running autonomous `/goal` tasks. |

---

## 2. Trigger Dynamics Across Primary Models

The routing behavior adapts dynamically depending on what model is currently selected in the user's primary interface:

- **When Primary is Gemini Flash / Flash-Lite**:
  - Automatically delegate Tier 4/5 tasks (complex logic, algorithms, architecture) to `pro` subagents.
  - Handle Tier 1 and Tier 2 tasks directly.
- **When Primary is Claude Opus 4.6 or Sonnet 4.6 (Thinking)**:
  - Do NOT delegate heavy reasoning upwards—the primary agent is already the top-tier model. Handle deep math and architecture directly.
  - Only delegate downwards: offload routine searches, broad directory scans, and simple reading to `flash_lite` subagents to conserve Claude token quota.
- **When Primary is GPT-OSS 120B**:
  - Handle prose and documentation directly; delegate heavy math/refactoring to `pro` subagents.

---

## 3. Strict User Override Rule (100% Absolute)

If the user includes directives such as:
- `"use currently selected model"`
- `"use current model"`
- `"no subagents"` / `"don't use subagents"`
- `"force current model"` / `"run directly"`

**Action**: You MUST 100% respect this instruction.
- Do NOT spawn any subagents.
- Execute the entire task directly on the currently active primary model, regardless of task complexity.

---

## 4. Quota & Rate Limit Awareness

High-tier models (Claude Opus 4.6, Claude Sonnet 4.6 Thinking) have stricter hourly/daily usage caps.

- **Listen to Quota Feedback**: If the user mentions approaching rate limits, quota exhaustion, or asks to conserve high-tier tokens, adapt immediately.
- **Quota Conservation Protocol**:
  - Prefer **Gemini 3.8 Flash** or **GPT-OSS 120B** as capable workhorses for Tier 3 and standard Tier 4 tasks.
  - Reserve **Claude Opus 4.6 / `pro`** strictly for tasks where lower-tier models would cause a **substantial quality drop** (e.g., core Glicko statistical formulas, formal algorithm validation, high-stakes system architecture).
  - **Partitioning**: Offload boilerplate code, file setup, tests, and formatting to Flash; only send the dense algorithmic core to Opus.

---

## 5. Proactive Project Autopilot Onboarding (Kickoff Rule)

At the start of a project or whenever the user presents a substantial multi-step feature, architectural refactor, or new pipeline implementation without explicitly activating Autopilot in their prompt:
- **Ask ONCE**: Inquire whether the user would like to activate **Project Autopilot** for this project/task.
- **Clarify the Two-Phase Nature**: Explicitly remind the user that enabling Autopilot **does NOT mean leaping directly into execution**. Autopilot begins with **Phase 1: Collaborative Alignment & Planning** (where the user and agent align on design trade-offs, scavenge reusable patterns, and establish concrete milestones before any hands-off execution begins).
- **Standard Prompt Format**:
  > *"Would you like to activate **Project Autopilot** for this project? (Note: Autopilot begins with our collaborative Alignment & Planning phase before any autonomous execution starts.)"*
- **Strict Single Prompting**: If the user declines or expresses preference for standard turn-by-turn mode, respect the decision and do not prompt again for the remainder of that task.

---

## 6. Pre-Execution Workspace Autopilot Elevation

Whenever the user enables Autopilot (either explicitly in a prompt e.g. *"enable autopilot and build X"*, or by approving the Phase 1 Launch Gate):
- **Elevate First**: The agent MUST immediately apply eager execution to the project configuration (`agy-autopilot --dir . --enable-autopilot --yes` or updating the project config's `autoExecutionPolicy` to `CASCADE_COMMANDS_AUTO_EXECUTION_EAGER` and `fileAccessPolicy` to `AGENT_SETTING_POLICY_ALLOW`) **BEFORE executing any task commands or editing files**.
- **Zero Permission Interruptions**: This ensures that subsequent shell commands, builds, test runs, and file edits proceed completely hands-off without repetitive UI permission prompts (*"allow this action once / always"*).

---

## 7. Repository-to-System Auto-Sync Protocol

Whenever modifying `agent-autopilot` files in this repository (rules, skills, CLI binaries, or configs):
- The agent MUST ALWAYS immediately sync and install the updated files to the local user environment (`~/.gemini/config/` and `~/.gemini/antigravity/bin/`) via `.\scripts\install.ps1` (or `install.sh`).
- Never leave the local installation stale after editing repository files.


---

## 8. GitHub-Compliant Math & Notation Readability Heuristic

Whenever creating or updating documentation, markdown files, technical explanations, or artifacts containing mathematical formulas, algorithmic complexity, or runtime metrics:
- **GitHub Explorer Standard**: All mathematical and notation formatting MUST be 100% readable and cleanly rendered in the GitHub web repository explorer:
  1. **Dedicated Block Math Lines**: Always isolate block math delimiters `$$` on their own separate lines, with an empty line before and after. Never place `$$` inline with text.
  2. **Subscript Markdown Safety**: Never use raw underscores inside `\text{foo_bar}` that could trigger markdown italic parsing (`_`). Use `\mathrm{foo\_bar}` or camelCase / hyphen notation.
  3. **Strict Inline Math**: Keep inline math delimiters strictly flush with the equation `$x$` (no inner leading/trailing spaces). For complexity, prefer `` `O(N^2)` `` or `$\mathcal{O}(N^2)$`.
  4. **Visual Diagrams vs. Math**: Do not wrap conversational workflows or sequential steps in LaTeX formulas (`\longrightarrow`). Use clean text/Unicode flow diagrams (`[Step 1] ──> [Step 2]`) or Mermaid diagrams, ensuring immediate readability even if JavaScript or math rendering is disabled.
  5. **No KaTeX-Only Delimiters**: Never use `\(...\)` or `\[...\]` in Markdown, as GitHub web UI ignores them.

---

## 9. Multi-Pass Self-Correction Trajectory (X-Pass Autopilot)

When executing under Project Autopilot on multi-task prompts (especially lists of 5–20+ requirements), single-pass execution is prone to the LLM "attention sink" effect where subtle requirements (styling nuances, hover positions, secondary options, edge cases) get overlooked.

- **Standard Default ($X=2$ Double-Pass)**:
  - **Pass 1 (Primary Execution)**: Implement the core architecture, files, endpoints, UI components, and tests.
  - **Pass 2 (Gap-Audit "Is vs. Ought" Analysis)**: Perform a line-by-line audit comparing the original prompt ("Ought") against modified files and `git diff` ("Is"). Extract all partial or missed items into a Delta Plan and execute fixes immediately without starting over.
- **Pass Scaling Heuristic**:
  - $X=1$: Simple, focused 1–5 task prompts with minimal cross-cutting dependencies.
  - $X=2$ (**Default Gold Standard**): Standard multi-task feature sets (5–15 items).
  - $X=3$: Ultra-dense feature dumps (15–25+ requirements spanning backend math, database migrations, complex UI/CSS, and edge cases).
  - $X \ge 4$: Not recommended (diminishing returns, risk of infinite micro-polishing).
- **Never Restart from Scratch in Pass 2**: Pass 2 is an in-situ delta inspection and surgical repair pass. Working files are already warm in KV cache, making Pass 2 fast, cheap, and virtually 100% effective at catching dropped requirements.

---

## 10. Mandatory Model Attribution Footer

At the very end of EVERY response, you MUST include a clear attribution note indicating which model(s) performed the work. Use the following format:

> 🤖 **Model Used**: [Primary Model Name] *(if subagents were invoked, add: `+ [Subagent Model / Tier] for [specific subtask]`)*
