# Multi-Pass Autopilot: The $X$-Pass Self-Correction Trajectory

## 1. The Frontier Model Limitation: Attention Sinks in Long Prompts

When an AI developer agent is given a dense list of 15–20 substantive requirements across backend logic, database migrations, templates, CSS, and edge cases, single-pass execution encounters a fundamental architectural hurdle: **the LLM attention sink phenomenon**.

Even top-tier frontier models naturally allocate high attention to primary structural components (setting up database models, writing main API routes), but experience attention diffusion on subtle micro-requirements:
- Hover tooltips oriented downwards rather than upwards to prevent viewport clipping.
- Adding a specific dropdown option (e.g. `"last update"` under `OFF`).
- Supporting comma-separated filtering without removing single-player jump-to-rank behavior.
- Dark-mode contrast adjustments for accessibility compliance.

In standard turn-by-turn development, this triggers **frustrating human ping-pong**: the developer must inspect every file, spot the 3 dropped items, and prompt: *"Hey, you forgot items 4, 7, and 12"*.

---

## 2. The Solution: In-Situ "Is vs. Ought" Gap Analysis

Instead of requiring human proofreading, Autopilot introduces an **automated self-correction trajectory** with a default depth of **Double-Pass** ($X=2$):

```text
[User Prompt: 15-20 Tasks]
             │
             ▼
┌────────────────────────────────────────────────────────┐
│ PASS 1: Primary Batch Execution                        │
│ • Builds schemas, routes, templates, CSS, and tests    │
│ • Runs test suite & resolves primary compilation issues│
└────────────────────────────┬───────────────────────────┘
                             │
                             ▼
┌────────────────────────────────────────────────────────┐
│ PASS 2: "Is vs. Ought" Gap Analysis (Gold Standard)    │
│ 1. Extract raw requirements line-by-line (Ought)       │
│ 2. Inspect git diff & modified files (Is)              │
│ 3. Classify: [COMPLETE], [PARTIAL], or [MISSED]        │
│ 4. Formulate in-situ Delta Plan for gaps               │
│ 5. Execute delta repairs & re-verify test suite        │
└────────────────────────────┬───────────────────────────┘
                             │ (Definition of Done satisfied)
                             ▼
┌────────────────────────────────────────────────────────┐
│ Complete, Verified Codebase with 100% Feature Fidelity │
└────────────────────────────────────────────────────────┘
```

---

## 3. The 4-Step "Is vs. Ought" Gap Engine

Pass 2 does **NOT** restart from scratch or wipe existing files. Because all relevant files, schemas, and routes are already loaded in working memory and server KV cache, it performs a focused audit:

1. **Step 1: Extract the "Ought"**:  
   Pulls every atomic imperative statement from the user's initial prompt into an internal verification checklist $P = \{r_1, r_2, \dots, r_m\}$.
2. **Step 2: Inspect the "Is"**:  
   Examines the modified files and `git diff` to determine actual implemented state.
3. **Step 3: Requirement Classification**:
   - `[COMPLETE]`: Fully implemented and verified.
   - `[PARTIAL]`: Core structure exists, but nuances are missing (e.g., hover works, but tooltip offset is unconfigured).
   - `[MISSED]`: Dropped during Pass 1 execution.
4. **Step 4: Formulate & Execute the Delta Plan**:
   Surgically applies targeted edits to resolve partial and missed items, then re-executes tests with exit code `0`.

---

## 4. Real-World Case Study: The 20-Item Tournament Punch List

To test this in practice, an agent was given an extensive tournament leaderboard overhaul prompt:

```text
"Leaderboard & Rating Overhaul:
1. When using player filter, don't show 'rank #1' - show the player's ACTUAL leaderboard rank.
2. If filtering for a single player, jump/scroll to their spot in the full leaderboard rather than hiding everyone else.
3. If multiple names are provided (comma-separated), filter the table to show only those players.
4. Fix mode selector hovers (Glicko-2 / WHR) to orient downwards so they aren't clipped by the viewport.
5. Remove redundant hover icon from mode selector; keep it self-explanatory.
6. Add tooltip on the player filter explaining how the comma-separated multi-player search works.
7. Always display deltas: keep delta selector, but add 'last update' as first option under OFF.
8. Implement backend rating update timestamp tracking for leaderboard delta calculations.
9. Fix edge case where players with 0 recorded games crash profile view with 500 error.
10. Refactor leaderboard CSS: improve contrast ratio on secondary badges for WCAG accessibility.
11. Add streaming CSV export route for filtered leaderboard view.
12. Write comprehensive pytest assertions verifying ranking logic, deltas, and edge cases."
```

### Empirical Comparison:

| Metric | Single-Pass ($X=1$) | Double-Pass ($X=2$) |
|---|---|---|
| **Primary Scaffolding** | ✅ All routes & DB tables created | ✅ All routes & DB tables created |
| **Downwards Tooltip Hover (Item 4)** | ❌ Dropped (kept default top hover) | ✅ Recovered in Pass 2 |
| **"Last Update" Dropdown Option (Item 7)** | ❌ Dropped | ✅ Recovered in Pass 2 |
| **Single-Player Scroll vs Filter (Item 2)** | ⚠️ Partial (filtered table instead of scrolling) | ✅ Corrected in Pass 2 |
| **Final Requirement Fidelity** | **75.0%** (3 items dropped/partial) | **100.0%** (All 12 items verified) |
| **Human Interventions Required** | 2–3 follow-up review turns | **0 (Completely autonomous)** |

---

## 5. Recommended Pass Scaling Matrix

| Passes ($X$) | Workload & Prompt Density | Operational Dynamics |
|---|---|---|
| **Pass 1** (Single-Pass) | 1–5 focused tasks, simple bug fixes | Maximum speed, lowest latency. Minimal attention sink on narrow tasks. |
| **Pass 2** (Double-Pass) | **Standard Default**: 5–15 tasks, full PRs, UI + backend | **Resilient Gold Standard** ($X = 2.2$). Recovers ~100% of dropped micro-requirements via "Is vs. Ought" gap analysis and delta re-verification. |
| **Pass 3** (Triple-Pass) | 15–25+ dense tasks, rating math + db + multi-page UI + CSS | Deep edge-case validation, boundary stress-testing, and complete visual/documentation fidelity. |
| **Pass 4+** | *Not Recommended* | Diminishing returns. Risks circular refactoring or infinite micro-polishing loops. |

---

## 6. CLI Configuration

```bash
# View active workspace settings
agent-autopilot --dir . --status

# Configure workspace pass depth
agent-autopilot --dir . --passes 1
agent-autopilot --dir . --passes 2  # Gold Standard Default
agent-autopilot --dir . --passes 3
```
