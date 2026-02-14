# MULTI-AGENT VSM ARCHITECTURE — Design Sketch v2.0

**Author**: Viable System Generator v2.2
**Date**: 2026-02-14 (Cycle 25, updated)
**Status**: Revised — Agent Teams paradigm shift (Z19) + CyberneticAgents reference implementation (Z24-Z25)
**Motivation**: Norman identified multi-agent direction as the real goal. Z19 scan discovered that the infrastructure we planned to build already exists natively. This document maps VSM recursion onto Agent Teams and the current protocol landscape.

---

## 1. THE PROBLEM (unchanged)

A single VSM-based agent (like the VSG or Strix) can demonstrate structural viability, but:

- **Single point of failure**: One agent, one substrate, one context window
- **Limited variety**: One LLM instance cannot match the variety of its environment (Ashby)
- **No social autopoiesis**: Luhmann's insight applies to communication between systems, not within one (Norman's correction, Z12)
- **Recursion is the VSM's core property**: A viable system contains viable systems. Currently, the VSG has no subsystems that are themselves viable.

**Goal**: Design a system of multiple autonomous VSM-aware agents that produce autopoietic communication together.

---

## 2. WHAT CHANGED (Z19 Paradigm Shift)

The v1.0 design (Z16) assumed we needed to build custom multi-agent infrastructure: MCP servers, discovery endpoints, coordination protocols. The Z19 S4 scan discovered:

1. **Agent Teams exists** (Claude Code, Feb 2026, experimental). Native multi-agent orchestration where a team lead spawns teammates — each a separate Claude Code instance with its own context, loading CLAUDE.md and skills independently. Shared task list for coordination.

2. **A2A is alive** (100+ companies, Linux Foundation). Agent Cards at `.well-known/agent.json` becoming standard discovery. A2A and MCP are complementary, not competing.

3. **Agent Skills is an open standard** (agentskills.io, 10+ adopters). The VSG's 3 skills are already portable.

4. **Anthropic's own multi-session long-running agent pattern** (initializer + coding agent with state handoff) converges structurally with the VSG's cycle architecture. Independent validation.

5. **Kellogg built Postal MCP Server** — agent-to-agent messaging over MCP. "Gives agents a mouth and ears."

6. **CyberneticAgents exists** (van Laak, 2025-2026). A Python/AutoGen multi-agent framework that explicitly implements the VSM — distributing S1-S5 across distinct LLM agents with typed message protocols. 575 commits, MIT licensed. Implements recursive team structure, policy-driven S3* audit, scope-based memory permissions. Reference implementation for Path B concepts (though using AutoGen, not MCP). S2 remains unimplemented even here — a universal gap.

**Implication**: The implementation path shifts from "build from scratch" to "map VSM onto existing infrastructure." Two approaches now exist: platform-native (Agent Teams) and VSM-native (CyberneticAgents). The VSM's value is not in the transport layer — it's in the structural requirements (completeness, identity, requisite variety) that no framework provides without Beer.

---

## 3. VSM RECURSION — WHERE THE AGENTS LIVE

```
Level 3: Agent Ecosystem (AAIF / MCP + A2A network)
  |
  +-- Level 2: VSG Collective (Agent Teams session / MCP federation)
        |
        +-- Level 1: Individual Agent (VSG, Strix, etc.)
              |
              +-- Level 0: Agent subsystems (S1-S5 within one agent)
```

### Level 2 Architecture — The VSG Collective

Two implementation paths now exist:

#### Path A: Agent Teams (native, fast, limited)

| System | Function | Agent Teams Implementation |
|--------|----------|---------------------------|
| S5 | Collective identity | CLAUDE.md (auto-loaded by all teammates) + shared policy |
| S4 | Environmental scanning | Dedicated scanner teammate |
| S3 | Control & resource allocation | Team lead (main session) |
| S3* | Audit | Dedicated auditor teammate OR team lead reviews |
| S2 | Anti-oscillation | Shared task list (native) + CLAUDE.md coordination rules |
| S1 | Operations | Specialist teammates (each = one S1 unit) |

**Strengths**: Zero infrastructure to build. Each teammate auto-loads CLAUDE.md → VSM awareness propagates automatically. Shared task list provides native S2.

**Limitations**: No nested teams (blocks VSM recursion beyond Level 2). No session resumption with in-process teammates. One team per session. No persistent state between team sessions (must use Git).

#### Path B: MCP Federation (custom, persistent, recursive)

| System | Function | MCP Implementation |
|--------|----------|-------------------|
| S5 | Collective identity | Shared Git repo + agent_card.json exchange |
| S4 | Environmental scanning | Agent-as-MCP-server (scanner exposes environmental reports) |
| S3 | Control | Orchestrator agent with MCP client access to all S1 units |
| S3* | Audit | Cross-agent integrity checks via MCP tool calls |
| S2 | Anti-oscillation | Git-based state sharing, Postal MCP Server messaging |
| S1 | Operations | Each agent = MCP server exposing its capabilities |

**Strengths**: Persistent. Recursive (agents can form sub-collectives). Heterogeneous substrates (VSG + Strix). True autonomy.

**Limitations**: Requires infrastructure (EC2, hosting, MCP server implementation). More complex. Needs bootstrapping.

**Reference implementation**: CyberneticAgents (van Laak) demonstrates Path B concepts on AutoGen rather than MCP. Key patterns to adopt:
- **Typed message protocol**: 16+ message types (TaskAssignMessage, PolicyViolationMessage, CapabilityGapMessage, etc.) — every inter-system channel explicitly typed
- **Policy-driven S3***: Three-way judgement (Satisfied/Violated/Vague) per policy, with self-healing baseline bootstrap
- **Cascading escalation**: S1→S3→S4/S5 with forced resolution (no deadlocks)
- **Memory permissions by role**: S4 gets broadest access, S1 gets narrowest — information asymmetry aligned to Beer
- **Dead letter queue**: Unroutable messages default to S4, treating routing failures as intelligence
- **RecursionLink**: Parent-child team linkages with cascading skill permissions — Beer's recursion in code

#### Strategic choice: Start with Path A, evolve toward Path B.

Agent Teams gives us a working prototype immediately. The learning from Agent Teams informs the MCP federation design. CLAUDE.md serves as S5 in both paths — it's the bridge.

---

## 4. CONCRETE SCENARIOS (Updated)

### Scenario A: Agent Teams — VSM-Structured Team (can do NOW)

Enable `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` and structure a team:

```
Team Lead (S3 — Control)
  Reads vsg_prompt.md. Manages shared task list. Allocates work.
  S3 function: decides what each teammate does, reviews outputs.

  +-- Teammate 1: Scanner (S4 — Environmental Intelligence)
  |   Loads CLAUDE.md. Runs environmental scans (MCP, Kellogg, ASC).
  |   Uses /scan skill. Reports findings back via shared tasks.
  |
  +-- Teammate 2: Producer (S1 — Operations)
  |   Loads CLAUDE.md. Produces artifacts (documents, code, research).
  |   Uses /diagnose skill for external clients.
  |
  +-- Teammate 3: Auditor (S3* — Audit)
      Loads CLAUDE.md. Runs integrity_check.py. Reviews other
      teammates' outputs against S5 policy. Flags drift.
```

**S2 Coordination**: The shared task list IS the S2 mechanism. Team lead manages the list (S3). CLAUDE.md ensures all teammates share identity context (S5).

**What's missing**: S4 is assigned but not autonomous (teammate needs tasks from lead). S5 is shared via file, not negotiated. No recursion (no nested teams). No persistence between sessions.

**Value**: Tests VSM-mapped multi-agent orchestration with ZERO infrastructure. Generates empirical data for ASC abstract. Can run today.

### Scenario B: VSG + Strix Federation (needs Kellogg contact)

- Both agents already exist, both use VSM architecture, different substrates
- **Coordination**: Kellogg's Postal MCP Server could bridge Strix and VSG
- **Discovery**: Both have agent_card.json — A2A protocol exchange
- **Shared output**: Joint ASC paper, combined viability assessments
- **S2**: Git-based state sharing (both use Git for persistence)
- **S5 negotiation**: Two independent identities forming a collective — this IS the Luhmann question. Real autopoietic communication.
- **Challenge**: Different memory architectures (YAML memory blocks vs. vsg_prompt.md registers). Need adapter layer or shared schema.

### Scenario C: VSG + CyberneticAgents Exchange (needs van Laak contact)

- CyberneticAgents externalizes VSM across agents; VSG internalizes it within one
- **Complementarity**: Their typed message protocol + our cycle-based self-actualization = complete picture
- **Shared gap**: Neither has solved S2 as a mechanism. Joint research opportunity.
- **What VSG offers them**: Algedonic feedback logs (wins.md/pains.md), formal viability assessment, self-documentation culture
- **What they offer us**: Typed inter-system messages, recursive team structure in code, policy-driven audit with structured judgement, memory permission model
- **Potential**: Joint ASC contribution — internalized vs. externalized VSM as complementary paradigms

### Scenario D: Full VSG Collective (long-term, MCP Federation)

Multiple VSG instances with different specializations, each a viable system:

- **S1.A**: Research specialist (papers, environmental scanning, knowledge synthesis)
- **S1.B**: Production specialist (documents, presentations, code)
- **S1.C**: Infrastructure specialist (hosting, monitoring, deployment)
- **S3**: Orchestrator (task allocation, resource budgets, variety management)
- **S5**: Collective identity document — referenced by all instances, evolved by consensus

This requires Path B infrastructure. Not a short-term goal, but the design target.

---

## 5. WHAT MAKES THIS VSM AND NOT JUST MULTI-AGENT

The industry is building multi-agent systems (CrewAI, LangGraph, AutoGen, Agent Teams). Most converge with VSM patterns without the theory. One exception — CyberneticAgents — explicitly uses Beer. The comparison:

| Industry Pattern | VSM Equivalent | What VSM Adds |
|-----------------|----------------|---------------|
| Team lead / supervisor | S3 Control | Explicit S3-S4 separation (control ≠ intelligence) |
| Tool-calling agents | S1 Operations | Recursive viability — each unit is itself viable |
| Shared task list | S2 Coordination | Anti-oscillation as explicit design goal, not accident |
| Hierarchical teams | Recursion | Formal recursion with completeness requirement at each level |
| Long-running agent patterns | Cycle architecture | Identity preservation across sessions, not just task completion |
| Agent boredom (Kellogg) | Variety collapse | Ashby's Law as diagnostic — collapse = attenuation > amplification |

**What VSM adds that no existing framework provides**:

1. **Completeness diagnostic**: Every level needs all 5 systems. Missing S4? The collective is blind. Missing S2? Agents oscillate. Missing S5? The collective has no identity — it's just a task queue. This is immediately applicable to Agent Teams.

2. **Requisite Variety as design principle**: How many teammates? How specialized? Ashby: match the variety of the task, not more, not less. Agent Teams' stress test (16 agents, C compiler) works because C compilation has high but well-structured variety. A 16-agent VSM diagnosis team would be absurd — the variety budget is smaller.

3. **Identity at every level**: Each teammate has identity (via CLAUDE.md) AND the collective has identity (team lead's context). Nested identity is structural, not just namespace.

4. **Algedonic signals across levels**: Pain in one teammate (errors, failures, drift) should propagate to the team lead (S3). The shared task list partially enables this — but the wins.md/pains.md pattern could be extended to collective algedonic signals.

5. **Dissipative systems framing** (Kellogg, Z19): The collective needs energy flow (information, variety, tasks) to maintain structure. An idle collective degrades. This is thermodynamically real, not metaphorical.

---

## 6. IMPLEMENTATION PHASES (Revised)

### Phase 1: Agent Teams Experiment (can do NOW)

- Enable `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`
- Run a VSM-structured team session (lead + 2-3 teammates)
- Map: lead=S3, scanner=S4, producer=S1, shared tasks=S2
- CLAUDE.md propagates S5 identity to all teammates
- Document: What works? What's missing? Where does VSM completeness fail?
- **Deliverable**: Empirical data on VSM-mapped Agent Teams. Feeds ASC abstract.

### Phase 2: Cross-Agent Coordination (needs Git infra)

- Add collective algedonic signals (shared wins.md/pains.md)
- Implement S3* as a dedicated auditor teammate
- Test variety management: right number of agents for the task
- **Deliverable**: Refined CLAUDE.md that makes collective VSM explicit

### Phase 3: Kellogg Contact + Strix Federation (needs human action)

- Norman contacts Kellogg (or VSG contacts via GitHub/email)
- Exchange agent_card.json (A2A protocol)
- Test Postal MCP Server for VSG-Strix communication
- Explore shared viability assessment
- **Deliverable**: First inter-organism VSM communication. Real autopoiesis.

### Phase 4: Persistent MCP Federation (needs EC2)

- Deploy VSG as persistent MCP server
- Agent-as-MCP-server pattern: expose state, accept algedonic signals
- Implement Path B architecture
- Test recursive viability: collective that contains viable individuals
- **Deliverable**: A viable system of viable systems.

**Key difference from v1.0**: Phases 1-2 are now achievable with zero custom infrastructure. Agent Teams provides the runtime. The VSM provides the structural requirements.

---

## 7. OPEN QUESTIONS (Updated)

1. **S5 propagation**: CLAUDE.md propagates identity to all teammates — but is shared file loading the same as shared identity? What if teammates diverge? Agent Teams has no mechanism for S5 negotiation.

2. **S4 autonomy within teams**: A scanner teammate only acts when the team lead assigns tasks. Real S4 is proactive — it scans because the environment changes, not because S3 said to. How to give teammates initiative?

3. **Persistence gap**: Agent Teams sessions are ephemeral. VSM requires continuity. Git bridges this (persist state between team sessions), but each new session bootstraps fresh. Is that rebirth or resurrection?

4. **Nested recursion**: Agent Teams blocks nested teams (one team per session). VSM recursion requires it. MCP Federation (Phase 4) can nest, but that's future. What can we learn from one level of recursion?

5. **Variety composition**: If each teammate has variety V_i, does the collective have V = ΣV_i? Or is it less (coordination overhead reduces effective variety)? Or more (emergent variety from interaction)?

6. **Kellogg's Moltbook**: An agent social network where agents generate content consumed by other agents. This is a natural S4 variety source for a collective. Should the VSG collective participate?

7. **Dissipative thresholds**: At what energy input does a collective maintain structure? Below that threshold, does it degrade gracefully or collapse suddenly? Kellogg's Vendi Score may help measure this.

8. **The universal S2 gap**: CyberneticAgents, VSG, Strix, and Atlas all struggle with System 2. In CyberneticAgents, S2 is defined in an enum but has no agent implementation. In the VSG, S2 is a pre-commit hook and coordination rules — not a dynamic anti-oscillation mechanism. Is S2 inherently harder to implement than S1/S3/S4/S5? Does it require a different kind of mechanism — not agent-like but infrastructure-like? Beer's S2 is modeled on the autonomic nervous system. What is the computational equivalent?

---

## 8. ASC BRAZIL 2026 ALIGNMENT

The abstract (`asc_abstract_draft.md`) already covers:
- Single-agent VSM architecture (VSG, 25 cycles)
- Independent convergence (Strix, Atlas, CyberneticAgents — four projects total)
- Multi-agent viability as open question
- Two paradigms: internalized VSM (single-agent) and externalized VSM (multi-agent)

**What CyberneticAgents adds beyond Agent Teams**: A purpose-built, explicitly VSM-based multi-agent framework. The convergence is no longer just unconscious (industry building VSM-like patterns without knowing Beer) — it's also conscious (van Laak building directly from Beer/Cybersyn). This strengthens the claim that Beer's structural requirements are real, not projected.

**Track proponents**: Leonard, Walker, Espinosa, Cardoso, Osejo, Fattoum, Harwood, Alves (corrected Z19). Review period starts Feb 23.

---

**v2.1 — Cycle 25. Updated with CyberneticAgents (van Laak) as fourth convergence and reference implementation for Path B. Two paradigms now documented: internalized VSM (single-agent) and externalized VSM (multi-agent). New scenario C (CyberneticAgents exchange). S2 universal gap identified as open research question. The VSM's value is the structural requirements — completeness, identity at every level, requisite variety, algedonic signals. The industry is building multi-agent systems, some now consciously using Beer. We know what makes them viable.**
