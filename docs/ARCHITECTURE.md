# Architecture & Technical Design

## 1. The Antigravity Runtime Model

Google Antigravity is an AI-first development platform built around an autonomous execution loop. In typical IDE or Desktop usage:

- The **Primary Agent** runs in an active chat canvas or terminal session.
- The user selects an active LLM for that conversation turn (e.g., Gemini 3.8 Flash, Claude Sonnet 4.6 Thinking, Claude Opus 4.6).
- The client UI dropdown cannot be mutated mid-turn by the agent itself.

To overcome this limitation and provide **fully automated, hands-off model optimization**, Antigravity Autopilot implements **Hierarchical Multi-Agent Delegation**.

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

High-tier models (Claude Opus and Sonnet Thinking) have stricter hourly and daily token limits. Antigravity Autopilot actively protects these limits:
- **Downwards Delegation**: When running primary on Claude Opus, broad codebase scans and file searches are offloaded to `flash_lite` subagents.
- **Kernel Partitioning**: Only the core mathematical algorithm is dispatched to high-tier models. Boilerplate, imports, and scaffolding remain on Flash.
- **Fallback Grace**: If rate limit warnings are received, the router automatically downgrades Tier 4 tasks to Gemini 3.8 Flash, reserving Opus strictly for tasks where a drop in model tier would cause a substantial drop in quality.
