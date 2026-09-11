# Security & Permission Model

> [!WARNING]
> **DISCLAIMER & EXPERIMENTAL STATUS: USE AT YOUR OWN RISK!**
> **Antigravity Autopilot is experimental software and has not been extensively tested across all environments, operating systems, and edge cases.**
> By using this software or enabling autopilot modes, you acknowledge that AI agents may execute arbitrary shell commands, install packages, and read/write local files without manual step-by-step review. **You assume full responsibility for any actions, changes, or data loss that may occur on your machine.**

---

## 1. Antigravity Security Tiers

Google Antigravity enforces strict permission boundaries to protect your system:

| Setting Key | Possible Values | Default | Autopilot Value |
|---|---|---|---|
| `autoExecutionPolicy` | `CASCADE_COMMANDS_AUTO_EXECUTION_NEVER`<br>`CASCADE_COMMANDS_AUTO_EXECUTION_EAGER` | `NEVER` | `EAGER` |
| `fileAccessPolicy` | `AGENT_SETTING_POLICY_ALLOW`<br>`AGENT_SETTING_POLICY_ASK` | `ASK` | `ALLOW` |
| `sandboxMode` | `true` / `false` | `false` | `false` |

---

## 2. Why Autopilot Requires Elevated Permissions

When running in **Autopilot Mode**, the agent is tasked with building, testing, fixing, and verifying complete feature suites without pausing to ask:
- *"May I run `git status`?"*
- *"May I run `pytest`?"*
- *"May I write this file?"*

If permissions remain on strict manual prompt, fully autonomous multi-hour or overnight execution is impossible because execution halts at the very first command.

---

## 3. The Security Handshake

Before any project configuration is updated, `agy-autopilot` strictly enforces the **Security Handshake**:

1. **Target Inspection**: The manager inspects `~/.gemini/config/projects/<project_id>.json` to locate the active project.
2. **Explicit Notice**: The user is displayed a prominent security warning detailing exactly which permissions will be granted and reminding them of experimental risks.
3. **Confirmation Gate**: The changes are only committed if the user explicitly approves via interactive prompt (`y/N`) or passes `--yes`.
4. **Instant Reversibility**: The user can revoke autonomous permissions at any time with:
   ```bash
   agy-autopilot --disable-autopilot
   ```

---

## 4. Potential Risks & Threat Surface

Because Autopilot operates on the local machine, users should be aware of the following concrete risks:

- **Unsandboxed Host Shell Execution**: In standard environments (including Windows), commands run with the privileges of the active local user account. An unintended command or agent hallucination can alter files, run system processes, or affect other files accessible to the user.
- **Supply Chain & Arbitrary Code via Tests/Scripts**: Permitting `npm test`, `pytest`, or `python` execution grants the agent the ability to trigger third-party scripts specified in project manifests (`package.json`, `setup.py`). Malicious or buggy dependencies can execute arbitrary code.
- **Indirect Prompt Injection**: If the agent reads untrusted third-party repositories, issues, or web data, adversarial prompts could theoretically attempt to guide the agent to perform unauthorized actions. Eager execution removes the human checkpoint.
- **Data Deletion / Destructive Git Actions**: Self-healing loops trying to resolve test or build errors might run destructive operations (e.g. `git checkout -f`, `git clean -fd`, or deleting code files) if not monitored.
- **Direct Configuration File Mutation**: Modifying Antigravity's internal `projects/<id>.json` files directly could conflict with future Antigravity updates or corrupt project metadata if manually disrupted.
- **Quota & API Cost Spikes**: Long-running or looped autonomous sessions utilizing high-tier models (Claude Opus 4.6) can quickly consume token quotas and increase API usage.

---

## 5. Safe Usage Guidelines

To minimize risk when using Antigravity Autopilot:

1. **Work in Dedicated Git Branches**: Never run autopilot on `main` or uncommitted work. Ensure your repository is committed and clean before enabling autopilot so any unwanted changes can be reverted with `git checkout`.
2. **Never Run Near Sensitive Data**: Do not run autopilot in directories containing `.env` files, production API keys, personal documents, or sensitive corporate intellectual property.
3. **Do Not Run with Administrative / Root Privileges**: Ensure your shell runs as a normal non-elevated user.
4. **Supervise Periodic Check-ins**: While designed for autonomous execution, check the terminal transcript periodically to verify the agent remains on course.
5. **Disable Autopilot When Done**: Revert permissions to strict prompt mode once your autonomous task completes:
   ```bash
   agy-autopilot --disable-autopilot
   ```

