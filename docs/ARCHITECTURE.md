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

---

## 4. The Two-Phase Autopilot Engine & Reflective Loop

Autonomous development requires a strict boundary between strategic deliberation and uninterrupted execution. Antigravity Autopilot implements a stateful Two-Phase lifecycle:

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

### The 4-Point "Definition of Done" (Objective Heuristic)

To avoid premature completion ("lazy exit") or infinite over-engineering, Phase 2 execution evaluates against a 4-point objective rubric:

1. **Plan Completeness**: Every milestone agreed upon in Phase 1 is implemented. Zero stubbed functions or forgotten `// TODO` items.
2. **Empirical Verification**: Real tests, builds, and CLI executions run and exit with code `0`. Verification requires tangible proof, not theoretical assumption.
3. **Vision Fidelity**: Explicit domain constraints and user rules are strictly respected and validated against real sample inputs.
4. **Sensible Usability**: The deliverable works out-of-the-box with clean error handling, sensible configuration defaults, and readable documentation.

### Coherent Enhancements Roadmap

Upon reaching the Satisfactory threshold, the session automatically delivers 3–5 high-value, logical next-step proposals that naturally expand upon the fulfilled foundation without violating product identity.

---

## 5. Theoretical Foundations: Velocity Dynamics & Token Economics

The dramatic speedup and quality gains observed during autonomous execution are grounded in formal runtime dynamics and LLM inference mathematics.

### 5.1 The Human Ping-Pong Multiplier vs. Uninterrupted Batch Execution

In standard conversational pair-programming, wall-clock time is dominated not by model inference, but by **interactive friction**:

$$\text{Total Wall Clock Time} = \sum_{k=1}^{M} \left( T_{\text{infer}, k} + T_{\text{read}, k} + T_{\text{human\_prompt}, k} + T_{\text{context\_switch}, k} \right)$$

Even with an ultra-fast model ($T_{\text{infer}} \approx 10\text{s}$), human review, prompt formulation, and conversational pauses add $60\text{s}$ to $180\text{s}$ per turn. A 15-step feature implementation balloons from **3 minutes of model compute into 45+ minutes of human waiting**.

Under **Autopilot**, the human terms $T_{\text{read}} + T_{\text{human\_prompt}} + T_{\text{context\_switch}} \to 0$:
$$\text{Total Autopilot Time} \approx \sum_{k=1}^{M} T_{\text{infer}, k}$$
All steps execute back-to-back at hardware speed.

### 5.2 Cognitive Momentum & Working Context Continuity

When an agent pauses between prompts:
1. **Context Drift**: In traditional turn-by-turn prompting, each user message subtly shifts the attention distribution. Variable names, template IDs, and database column names risk drifting across separate turns.
2. **Cold-Start File Re-Inspection**: Disjointed agents repeatedly call `view_file` or `grep_search` to verify symbols they previously inspected because their internal certainty decays.
3. **Hot Cache Continuity**: In Autopilot, a single unified trajectory holds the schema, backend routes, HTML template blocks, CSS classes, and test fixtures in uninterrupted working context. Code is written in total lockstep with zero re-inspection overhead.

### 5.3 Mathematical Proof: Defeating $O(N^2)$ Token Inflation

The common belief that autonomous agents consume more tokens is mathematically false. Turn-by-turn chat carries a severe **"Conversation History Tax"** that compounds quadratically.

#### The Turn-by-Turn History Tax ($O(N^2)$ Growth):
On each user turn $k \in [1, N]$, the client re-transmits the initial system prompt $S$ plus the entire transcript of all prior user messages $U_i$ and assistant responses $A_i$:

$$\text{Cumulative Input Tokens}_{\text{Turn-by-Turn}} = \sum_{k=1}^{N} \left( S + \sum_{i=1}^{k-1} (U_i + A_i) \right) = N \cdot S + \sum_{k=1}^{N} (N - k)(U_k + A_k) \propto O(N^2)$$

#### The Autopilot Trajectory ($O(N)$ Tool Execution):
In Autopilot, execution occurs within a single turn via continuous tool call steps $T_k$. The initial prompt $S$ and user intent $U$ are processed **once**, and tool outputs are streamed linearly without re-packaging cumulative conversational back-and-forths:

$$\text{Cumulative Input Tokens}_{\text{Autopilot}} \approx S + U + \sum_{k=1}^{M} \Delta_{\text{tool}, k} \propto O(N)$$

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

Antigravity Autopilot is designed to run seamlessly across all primary developer operating systems.

| Component | Target / Verified Specification | Details |
|---|---|---|
| **Antigravity Engine** | **Google Antigravity v2.12.2+** (ProductVersion `2.12.2.0`) | Compatible with the Antigravity 2.0+ architecture, built-in skill loading, and multi-agent subagent protocols. |
| **Primary Reference OS** | **Windows 11 (Build 10.0.26200+, AMD64)** & **Windows 10 (1809+)** | 1-Click native installation via `install.bat` and `scripts/install.ps1`. Seamless User PATH registration. |
| **macOS Support** | macOS 13+ (Ventura, Sonoma, Sequoia - Apple Silicon & Intel) | Native POSIX installer via `scripts/install.sh`. Configures `~/.gemini/config/` and shell rc (`~/.zshrc` / `~/.bashrc`). |
| **Linux & WSL2** | Ubuntu 22.04+, Debian 12+, Fedora 38+, Arch Linux | Native POSIX installer via `scripts/install.sh`. Pure Python standard-library CLI tools. |
| **Python Runtime** | **Python 3.10+** (Tested on Python 3.13.5) | Standard library only (`os`, `sys`, `json`, `pathlib`, `argparse`). Zero third-party dependencies required. |


