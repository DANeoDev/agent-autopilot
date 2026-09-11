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

## 5. Mandatory Model Attribution Footer

At the very end of EVERY response, you MUST include a clear attribution note indicating which model(s) performed the work. Use the following format:

> 🤖 **Model Used**: [Primary Model Name] *(if subagents were invoked, add: `+ [Subagent Model / Tier] for [specific subtask]`)*
