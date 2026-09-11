# Antigravity Autopilot 🚀

> **Fully Automated Multi-Tier Model Routing, Intelligent Orchestration & Autonomous Project Execution for Google Antigravity.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Platform: Windows](https://img.shields.io/badge/Platform-Windows%2010%2F11-0078D6.svg?logo=windows)](https://microsoft.com)
[![Compatible: Google Antigravity](https://img.shields.io/badge/Compatible-Google%20Antigravity%202.0%20%2B%20CLI-4285F4.svg?logo=google)](https://antigravity.google)

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

## ✨ Features

- 🧠 **Dynamic 5-Tier Decision Matrix**: Classifies prompts in <50ms and routes to the exact model tier needed.
- ⚡ **1-Click Windows Installer**: Double-click `install.bat` and the entire machine-wide configuration is installed in seconds.
- 🤖 **Two-Phase Autonomous Project Mode (`project-autopilot`)**:
  - **Phase 1: Collaborative Alignment**: The agent acts as an engineering sounding board to discuss architectural trade-offs, clarify domain rules, and align on a detailed implementation plan.
  - **The Launch Gate**: Prompts explicitly: *"The plan is aligned. Do you want me to engage full Autopilot execution now?"*
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

## 🚀 Quickstart (1-Click Windows Install)

### Option A: Double-Click Installer (Zero Setup)
1. Download or clone this repository.
2. Double-click **`install.bat`** in the repository root.
3. Done! All global rules, skills, and CLI tools are installed and added to your `PATH`.

### Option B: PowerShell
```powershell
git clone https://github.com/DANeoDev/antigravity-autopilot.git
cd antigravity-autopilot
.\scripts\install.ps1
```

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
# Instant model recommendation for any prompt
agy-route "Design a new Glicko rating volatility algorithm"

# JSON output for build scripts and pipelines
agy-route --json "Fix typo in variable name"

# Inspect active project settings
agy-autopilot --dir . --status

# Enable autonomous execution permissions for current workspace
agy-autopilot --dir . --enable-autopilot
```

---

## 📁 Repository Structure

```text
antigravity-autopilot/
├── bin/
│   ├── agy_router.py              # CLI task classifier and decision engine
│   ├── agy-route.bat              # Global CLI command
│   ├── agy_project_manager.py     # Project permissions and autopilot engine
│   └── agy-autopilot.bat          # Project settings CLI command
├── customizations/
│   ├── rules/
│   │   └── AGENTS.md              # Machine-wide orchestration rule
│   └── skills/
│       ├── model-router/          # Skill: Task classification & subagent dispatch
│       │   └── SKILL.md
│       └── project-autopilot/     # Skill: Autonomous goal execution & self-healing
│           └── SKILL.md
├── docs/
│   ├── ARCHITECTURE.md            # Deep dive on runtime & multi-agent routing
│   └── SECURITY_AND_PERMISSIONS.md # Security boundaries & permission guidelines
├── scripts/
│   ├── install.ps1                # PowerShell installer
│   ├── install.bat                # Batch bootstrap runner
│   ├── uninstall.ps1              # Clean uninstaller
│   └── verify.ps1                 # Health checker
├── install.bat                    # Root 1-click double-clickable installer
├── LICENSE                        # MIT License
└── README.md                      # Documentation
```

---

## 🗑️ Uninstallation

To cleanly remove the global skills and binaries from your machine:
```powershell
.\scripts\uninstall.ps1
```
*(Your `~/.gemini/config/AGENTS.md` is preserved so custom non-autopilot rules are not lost).*

---

## 📜 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for more information.
