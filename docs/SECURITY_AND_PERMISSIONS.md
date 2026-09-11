# Security & Permission Model

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
2. **Explicit Notice**: The user is displayed a prominent security warning detailing exactly which permissions will be granted.
3. **Confirmation Gate**: The changes are only committed if the user explicitly approves via interactive prompt (`y/N`) or passes `--yes`.
4. **Instant Reversibility**: The user can revoke autonomous permissions at any time with:
   ```bash
   agy-autopilot --disable-autopilot
   ```
