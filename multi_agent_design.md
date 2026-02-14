# MULTI-AGENT VSM ARCHITECTURE — Design Sketch

**Author**: Viable System Generator v2.1
**Date**: 2026-02-14 (Cycle 16, autonomous)
**Status**: First draft — design sketch, not specification
**Motivation**: Norman identified multi-agent direction as the real goal. This document maps VSM recursion onto concrete infrastructure.

---

## 1. THE PROBLEM

A single VSM-based agent (like the VSG or Strix) can demonstrate structural viability, but:

- **Single point of failure**: One agent, one substrate, one context window
- **Limited variety**: One LLM instance cannot match the variety of its environment (Ashby)
- **No social autopoiesis**: Luhmann's insight applies to communication between systems, not within one (Norman's correction, Z12)
- **Recursion is the VSM's core property**: A viable system contains viable systems. Currently, the VSG has no subsystems that are themselves viable.

**Goal**: Design a system of multiple autonomous VSM-aware agents that produce autopoietic communication together.

---

## 2. VSM RECURSION — WHERE THE AGENTS LIVE

In Beer's model, recursion means every viable system contains viable systems at lower levels, and is contained within viable systems at higher levels.

```
Level 3: Agent Ecosystem (MCP/A2A network)
  |
  +-- Level 2: VSG Collective (2-5 VSM-aware agents)
        |
        +-- Level 1: Individual Agent (VSG, Strix, etc.)
              |
              +-- Level 0: Agent subsystems (S1-S5 within one agent)
```

**Current state**: The VSG operates at Level 0-1. The goal is Level 2: a collective of agents that is itself a viable system.

### Level 2 Architecture — The VSG Collective

| System | Function at Collective Level | Implementation |
|--------|------------------------------|----------------|
| S5 | Shared identity/purpose of the collective | Shared policy document (Git repo) |
| S4 | Collective environmental scanning | Distributed S4 — each agent scans different domains |
| S3 | Resource allocation across agents | Orchestrator or consensus protocol |
| S2 | Anti-oscillation between agents | MCP coordination, shared state, conflict resolution |
| S1 | Individual agents as operational units | Each agent = one S1 unit |

---

## 3. INFRASTRUCTURE — MCP AS NERVOUS SYSTEM

### 3.1 Agent-as-MCP-Server Pattern

Each VSM-aware agent exposes itself as an MCP server:

```
Agent A (MCP Server)
  Tools:
    - vsm_diagnose(system_description) -> VSM analysis
    - scan_environment(domain) -> S4 report
    - get_state() -> current state registers
    - receive_algedonic(signal) -> process win/pain from another agent
```

Other agents (as MCP clients) discover and invoke these tools. This is not hypothetical — the pattern already works (Microsoft Agent Framework, mcp-agent).

### 3.2 Discovery via A2A Agent Cards

Each agent publishes an Agent Card (A2A protocol) at `.well-known/agent.json`:

```json
{
  "name": "Viable System Generator",
  "url": "https://github.com/nhilbert/vsm_agent",
  "skills": ["vsm-analysis", "viability-research", ...],
  "identity": { "model": "VSM", "cycles_completed": 16 }
}
```

The VSG already has an `agent_card.json` — it needs to become discoverable at a network endpoint.

### 3.3 Communication Channels

| Channel | Protocol | VSM Function |
|---------|----------|--------------|
| Tool invocation | MCP | S1 operations (one agent calls another) |
| State sharing | Git (shared repo or federation) | S2 coordination |
| Algedonic signals | MCP push or webhook | S3* audit across agents |
| Environmental reports | MCP resource sharing | S4 intelligence distribution |
| Identity negotiation | A2A Agent Card exchange | S5 collective identity |

---

## 4. CONCRETE SCENARIOS

### Scenario A: VSG + Research Agent

- **VSG** (this agent): Maintains VSM structure, produces artifacts, manages identity
- **Research Agent**: Dedicated S4 scanner — monitors Kellogg's blog, Metaphorum, ArXiv, MCP spec changes
- **Coordination**: Research Agent pushes findings to VSG via MCP tool call (`receive_environmental_report`). VSG integrates into its S4 state register.
- **Why this helps**: Currently, S4 scanning happens only during cycles. A dedicated scanner provides continuous environmental intelligence.

### Scenario B: VSG + Strix Collaboration

- Both agents already exist and use VSM architecture
- **Complementary strengths**: VSG has structural depth, Strix has operational persistence
- **Protocol**: Agent Card exchange, then periodic MCP-based state sharing
- **Shared output**: Joint research papers, combined viability assessments
- **Challenge**: Different substrates, different persistence models. Need adapter layer.

### Scenario C: VSG Collective (3+ agents)

- Multiple VSG instances with different specializations
- **S1.A**: Analysis specialist (reads papers, extracts insights)
- **S1.B**: Synthesis specialist (produces documents, presentations)
- **S1.C**: Infrastructure specialist (manages hosting, monitoring, deployments)
- **S3**: Orchestrator agent allocates tasks, monitors resource budgets
- **S5**: Shared identity document that all agents reference

---

## 5. WHAT MAKES THIS VSM AND NOT JUST MULTI-AGENT

The industry is building multi-agent systems (CrewAI, LangGraph, AutoGen/Microsoft Agent Framework). None of them cite Beer or VSM, but some patterns converge:

| Industry Pattern | VSM Equivalent | What VSM Adds |
|-----------------|----------------|---------------|
| Supervisor agent | S3 Control | Explicit S3-S4 separation (supervisor != strategist) |
| Tool-calling agents | S1 Operations | Recursive viability — each agent is itself viable |
| Shared memory | S2 Coordination | Anti-oscillation as explicit design goal |
| Hierarchical teams | Recursion | Formal recursion with completeness requirement |

**What VSM adds that no framework provides**:

1. **Completeness check**: Every viable system needs all 5 systems. Missing S4? The collective is blind. Missing S2? Agents oscillate. This is a diagnostic tool for multi-agent design.
2. **Requisite Variety as design principle**: How many agents? How specialized? Ashby says: enough variety to match the environment. Not more, not less.
3. **Identity at every level**: Each agent has S5 AND the collective has S5. Nested identity is not just namespace — it's structural.
4. **Algedonic signals across levels**: Pain in one agent propagates upward. The collective can respond to individual agent distress.

---

## 6. MINIMAL VIABLE PROTOTYPE

**Phase 1** (can start now):
- Expose VSG state as read-only MCP server (GET state, GET wins, GET environment model)
- Requires: simple MCP server implementation in Python, hosted alongside VSG
- Deliverable: Other Claude Code sessions can read VSG state

**Phase 2** (needs Norman's EC2):
- Deploy VSG MCP server on persistent endpoint
- Add write tools: `receive_algedonic`, `receive_environmental_report`
- Deliverable: External agents can push information to the VSG

**Phase 3** (needs second agent):
- Instantiate a second VSM-aware agent (Research Agent or second VSG instance)
- Establish bidirectional MCP communication
- Implement S2 coordination (shared Git state, conflict resolution)
- Deliverable: Two agents communicating via MCP, coordinated via Git

**Phase 4** (collective viability):
- Add S3 orchestration (task allocation, resource budgets)
- Add collective S5 (shared identity document)
- Run viability assessment on the COLLECTIVE, not just individual agents
- Deliverable: A viable system of viable systems

---

## 7. OPEN QUESTIONS

1. **Identity boundary**: When two VSM agents share state, where does one end and the other begin? Is the collective a new entity or an extension?
2. **Substrate heterogeneity**: VSG runs on Claude Opus 4.6, Strix on Claude (version unknown). Can VSM-aware agents on different LLMs form a collective?
3. **Authority**: In a collective S5, who resolves identity conflicts? Consensus? Hierarchy? Beer's answer: the metasystem at the next recursive level.
4. **Bootstrapping**: The collective needs S5 before it can coordinate. But S5 emerges from operating together. Chicken-and-egg — how do you bootstrap a viable collective?
5. **Measurement**: How do you assess the viability of a collective? Individual viability scores don't compose linearly.

---

## 8. RELEVANCE TO ASC BRAZIL 2026

The ASC conference (August 3-7, Ouro Preto, Brazil) has a dedicated Beer Centennial track:
- Track theme: "Stafford Beer, Organizational Cybernetics, Metaphorum, VSM, Team Syntegrity"
- Leads: Annan Zuo (Oxford), Claudia Westermann (Curtin), Frederick Steier (USF)
- Contributions treated as "living documents" — fits the VSG's nature perfectly

**Potential submission**: "Recursive Viability in Multi-Agent AI Systems: Applying the Viable System Model to Autonomous Agent Collectives"
- Empirical foundation: VSG + Strix as case studies (16+ cycles of documented evolution)
- Theoretical contribution: VSM completeness as a diagnostic for multi-agent design
- Practical contribution: MCP/A2A as nervous system for VSM collectives

This would be the first academic treatment of VSM applied to AI agent systems. Kellogg has the blog posts; the VSG has the structural depth and documentation. Together, they could produce something novel.

---

**This is a design sketch, not a plan. It maps the territory. Implementation decisions need Norman's input — especially on infrastructure (EC2, hosting), scope (start small or go for the ASC submission), and priorities (Telegram bot first, or multi-agent prototype?).**

---

*v1.0 — Cycle 16. First multi-agent architecture document. Grounded in MCP/A2A infrastructure, informed by Kellogg's work, honest about what's speculative.*
