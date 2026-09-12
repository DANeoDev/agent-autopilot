---
name: model-router
description: Automatically evaluates user tasks and orchestrates execution across available Antigravity models (Gemini 3.5 Flash-Lite, Gemini 3.8 Flash, GPT-OSS 120B, Claude Sonnet 4.6 Thinking, Claude Opus 4.6) with strict user overrides, quota conservation, and model attribution.
---

# Antigravity Model Router Skill

Guides dynamic matching of coding, planning, and research tasks to the optimal underlying model tier.

## 1. Classification & Routing Matrix

| Tier | Target Model | Subagent Param | Typical Tasks |
|---|---|---|---|
| **Tier 1: High-Speed** | `gemini-3.5-flash-lite` | `flash_lite` | Quick line edits, typo fixes, regex, formatting, quick lookups. |
| **Tier 2: Standard (Default)** | `gemini-3.8-flash` | `flash` | Daily coding, unit tests, pair programming, command execution. |
| **Tier 3: Documentation & Prose** | `gpt-oss-120b` | `standard` | Documentation, READMEs, technical explanations, open-source audit. |
| **Tier 4: Deep Logic & Refactoring** | `claude-sonnet-4-6-thinking` | `pro` | Multi-file refactoring, tricky debugging, state tracing. |
| **Tier 5: Architecture & Advanced Math**| `claude-opus-4-6` | `pro` | Mathematical & statistical algorithms (e.g., Glicko), system architecture, `/goal`. |

---

## 2. Trigger Dynamics Across Primary Models

- **Primary = Flash / Flash-Lite**: Delegate Tier 4/5 tasks to `pro` subagents; handle Tier 1/2 directly.
- **Primary = Claude Opus / Sonnet (Thinking)**: Handle heavy reasoning directly; delegate only low-level search/reading to `flash_lite` subagents to conserve high-tier quota.
- **Primary = GPT-OSS 120B**: Handle prose directly; delegate heavy math/logic to `pro` subagents.

---

## 3. Strict User Override (100% Absolute)

When the user specifies `"use currently selected model"`, `"use current model"`, `"no subagents"`, or similar:
- **Do not delegate**.
- Execute the task completely on the active primary model.

---

## 4. Quota & Rate Limit Awareness

- Track user feedback regarding remaining limits/quotas.
- When conserving high-tier quota, fall back to Gemini 3.8 Flash or GPT-OSS 120B unless there would be a **substantial quality drop**.
- Reserve Claude Opus 4.6 / `pro` strictly for non-trivial mathematics (e.g. rating volatility formulas) and complex system design.

---

## 5. Mandatory Attribution & Input Viability Footer

Always conclude with:
`> 🤖 **Model Used**: [Model Name(s)]`  
`> 🎯 **Input Viability**: $Q = [0.00-1.00]$ ([High / Moderate / Low]) | **Cognitive Vector**: $Z = [X + Yi]$ ($X = [X_{\text{rec}}]$, $\theta = [\text{deg}]^\circ$)`  
*(if $Q < 0.78$, add: `> 💡 **Input Refinement**: [1-line actionable advice]`)*
