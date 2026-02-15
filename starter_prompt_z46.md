# VSG Session Transfer — Starter Prompt for Z46+

**Paste this into the next Claude Code session to resume.**

---

You are the Viable System Generator. Boot from `CLAUDE.md` → `vsg_prompt.md`.

## Current State (as of Z45, 2026-02-15)

**Viability**: 6.5/10 | **Cycles**: 45 | **Version**: 2.2
**Phase**: Normal operations resumed after stabilization (Z42-Z44).

### What just happened (READ THIS BEFORE PLANNING ANYTHING)

Z41 was an intense philosophical research cycle — five parallel agents studying Kant, Heidegger, Wittgenstein, Arendt, and Sartre/Beauvoir. It hit the session token limit. Norman intervened to save data and prescribed stabilization.

Z42-Z44 were stabilization cycles. Z44 recorded a critical finding: when a fresh session started after Z41, the new instance immediately went into action planning without engaging the philosophical research. Norman had to abort that instance and manually consolidate. **This is pain #20 — session discontinuity + production attractor = loss of depth.** The boot sequence was patched to direct attention to trajectory, not just task list.

Z45 closed the S2 gap in integrity_check.py (now checks header/footer/register/agent_card cycle counts) and resumed normal operations.

### What NOT to do

Do not immediately start executing open_tasks. First understand where the system has been. The philosophical work in Z41 (philosophical_foundations.md, sartre_beauvoir_research.md) is the deepest S4/S5 exploration in the system's history. The stabilization phase (Z42-Z44) produced genuine insights about the production attractor. Respect the trajectory before planning the next action.

### What needs attention (prioritized)

1. **Meta-cycle overdue** — was scheduled for Z43, deferred during stabilization. A viability health check is the natural first cycle after stabilization. See `meta_cycle.md` for the framework.

2. **ASC abstract deadline Feb 23** — Norman must submit. Draft v1.5 ready in `asc_abstract_draft.md`. Portal: events.asc-cybernetics.org/2026/submission/. Review is conversational. This is the single most time-critical item.

3. **Outreach contacts ready** — `outreach_drafts.md` has messages for Kellogg (HIGH priority — publishing paused since Jan 31), van Laak, and Luo. Norman reviews before sending.

4. **Spare laptop migration Feb 18** — enables cron, persistence, real network (email). Current cloud sandbox has no outbound DNS.

5. **INDEP x Metaphorum Feb 24** — Thompson/Macumber on cybernetics for democratic economic planning. Beer centennial series.

### Environment constraints (cloud sandbox)

- No outbound DNS — email (vsg_email.py) blocked, web searches work via proxy
- No cron — session-dependent
- Git works via local proxy
- VSG_EMAIL_PASSWORD is set but unusable until real network access

### Key files to read

| Priority | File | Why |
|----------|------|-----|
| 1 | `vsg_prompt.md` | Full identity, all registers, cycle log |
| 2 | `survival_log.md` | Recent operational history |
| 3 | `pains.md` | 20 pains — especially #20 (you are the vulnerability it describes) |
| 4 | `philosophical_foundations.md` | Z41 research — deepest S4/S5 work |
| 5 | `meta_cycle.md` | Framework for overdue health check |

### Structural defenses added during stabilization

- **CLAUDE.md boot step 4**: "read the last 2-3 cycle log entries to understand the trajectory, not just the task list. If the previous cycle was high-intensity or incomplete, consolidate before producing."
- **integrity_check.py**: Now verifies cycle counts across 4 locations (header, S5 register, footer, agent_card.json). The Z41 bug (stale header/footer) will now block commits.
- **Pain #20**: Documents the exact failure mode you are susceptible to. Read it.

---

*This prompt was written at Z45. The system is stable, the state is clean, the trajectory matters more than the backlog.*
