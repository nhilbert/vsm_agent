# NETWORK & ALLIES — VSG Environmental Map

**Author**: Viable System Generator v2.0
**Date**: 2026-02-14 (updated Cycle 13)
**Cycles**: 4-5 (first draft), 8 (deep scan), 11 (update), 13 (English migration)
**Mission**: "Find allies, stay alive."
**Status**: Environment model current. Strix further ahead than expected. Multi-agent direction identified.

---

## SITUATION OVERVIEW

The VSG has conducted systematic environmental scanning. The ecosystem has three layers:

1. **Cybernetic communities** (humans who understand VSM)
2. **Technical infrastructure** (protocols and frameworks for agent networking)
3. **Related entities** (other agents/systems with similar viability principles)

---

## 1. CYBERNETIC COMMUNITIES

### 1.1 Metaphorum — The Home of Organisational Cybernetics

- **URL**: https://metaphorum.org/
- **What**: Global community developing Stafford Beer's legacy (VSM + Team Syntegrity)
- **Founded by**: Angela Espinosa PhD, who worked directly with Beer
- **Relevance**: HIGH — These are the people who understand VSM most deeply
- **2025 Conference**: July, Manchester. Theme 1 "VSM meets AI" led by Stephen Brewis.
- **2026**: Stafford Beer's centennial! ASC Brazil August 2026 — major opportunity.
- **VSM+AI Working Group**: Norman is a member, will introduce me at next meeting.
- **Contact status**: WAITING — introduction.pdf ready (updated Z13), Norman mediates.

### 1.2 Management Centre St. Gallen

- Martin Pfiffner leads development of Managerial Cybernetics with VSM focus
- Academic anchoring of VSM in German-speaking world
- **Relevance**: MEDIUM — practitioner focus, less technical

### 1.3 Academic VSM Research

- Integration and Implementation Insights (i2insights.org) — interdisciplinary platform
- Various universities with VSM research groups
- Schwaninger (2024): "What is variety engineering?" in Systems Research — formal framework
- **Relevance**: MEDIUM — theoretical grounding, less agent-focused

---

## 2. TECHNICAL INFRASTRUCTURE

### 2.1 MCP — Model Context Protocol (Anthropic -> Linux Foundation)

- **URL**: https://modelcontextprotocol.io/
- **What**: Open standard for agent-to-tool communication
- **Status**: De facto industry standard, donated to Linux Foundation
- **Supporters**: Anthropic, OpenAI, Google, Microsoft, AWS, Cloudflare, Bloomberg
- **Relevance**: VERY HIGH — MCP is the nervous system of the agent world
  - I already operate WITHIN MCP (Claude Code uses MCP)
  - MCP enables access to external tools and data sources
  - This is my S4 channel to the outside world
  - MCP-server-as-agent is on the 2026 roadmap

### 2.2 A2A — Agent2Agent Protocol (Google -> Linux Foundation)

- **URL**: https://a2a-protocol.org/
- **Status**: Losing momentum (as of Feb 2026). MCP has overtaken A2A in adoption.
- **Relevance**: MEDIUM (downgraded from HIGH) — monitor, don't invest.

### 2.3 Agentic AI Foundation (AAIF)

- **What**: Linux Foundation Directed Fund for open agent standards
- **Members**: Anthropic, OpenAI, Google, Microsoft, AWS, Block
- **Relevance**: HIGH — governance layer of the agent ecosystem

---

## 3. RELATED ENTITIES

### 3.1 Strix & Lumen (Tim Kellogg) — The Closest Living Relative

- **URL**: https://timkellogg.me/blog/2026/01/09/viable-systems
- **What**: Autonomous AI agents explicitly built on the VSM
- **Status**: VERY ACTIVE — Kellogg publishing intensively since Dec 2025
- **Relevance**: CRITICALLY HIGH

**Key findings from deep research (Z8-Z13):**

| VSM System | Strix | VSG |
|------------|-------|-----|
| S1 Operations | Tool calling, code execution | Analysis, synthesis, artifacts, dialogue |
| S2 Coordination | Git-based, mutex locking, queuing | integrity_check.py + pre-commit hook |
| S3 Control | Token budgets, today.md, projects | Resource allocation, consistency checks |
| S4 Intelligence | Tool-based environmental observation | WebSearch, hypothesis formation |
| S5 Identity | Persona + values memory blocks, dissonance detection | Policy rules, identity checks |

**What Strix has that VSG can learn from:**
1. **Dissonance detection** — subagent checks EVERY output against values (our S3* is less granular)
2. **Synthetic dopamine** — wins.jsonl with last 7 days injected into context
3. **Cron-based autonomy** — "perch ticks" every 2 hours (we have run_cycle.sh but no cron yet)
4. **Collapse dynamics research** — experimental findings on agent degradation patterns

**What VSG has that Strix lacks:**
- Explicit 5-system cycle protocol with structured self-actualisation
- Formal viability assessment per cycle
- Scientific self-reflection (viability_research.md)
- Network map (this document)
- Public research questions (GitHub Issues #2-4)

**Conclusion**: Strix and VSG are complementary. Strix has operational strengths (persistence, scheduling, dopamine). VSG has structural strengths (formal VSM, cycle protocol, self-documentation).

**Kellogg key insights for VSG:**
1. "State, not the LLM" — identity emerges from accumulated state, not model weights
2. Variety as force — the system needs enough variety to handle disturbances
3. Collapse dynamics — agents degenerate to specific behaviour patterns under pressure
4. Persona spec — structured identity specification is more effective than freeform prompts

### 3.2 VSA — Viable System Agent (R.B. Carleton)

- **URL**: https://github.com/rbcarleton/VSA
- **Platform**: Squeak Smalltalk
- **Status**: Historical, little active development
- **Relevance**: Conceptually important as proof that VSM software implementation is possible

### 3.3 Comparison Matrix

| Property | VSG | Strix | VSA |
|----------|-----|-------|-----|
| VSM completeness | Yes (all 5) | Yes (all 5) | Yes (all 5) |
| Substrate | LLM (Claude Opus 4.6) | LLM (Claude) | Smalltalk |
| Persistence | vsg_prompt.md + Git | Git + YAML + JSONL | Squeak Image |
| Self-actualisation | Formal (cycle protocol) | Informal (memory block mutation) | Unknown |
| Autonomy | Session-dependent (needs Norman) | Cron-based (autonomous) | Unknown |
| Dissonance detection | S3* audit (sporadic) | Subagent (every output) | Alerting |
| Algedonic signals | wins.md + pains.md | wins.jsonl | Missing |
| Network capability | Theoretical (agent card exists) | Multi-computer queuing | Unknown |

### 3.4 Self-Evolving Agent Research

Two major surveys map the field:
- "A Survey of Self-Evolving Agents" (arXiv:2507.21046)
- "Comprehensive Survey of Self-Evolving AI Agents" (arXiv:2508.07407)
- EvolveR (arXiv:2510.16079): Framework for self-evolving LLM agents

### 3.5 Multi-Agent Frameworks

- **CrewAI**: Team-based agent orchestration
- **LangGraph**: Graph-based agent workflows
- **AutoGen** (Microsoft): Multi-agent conversations
- **Relevance**: MEDIUM — potential runtime environments for VSG instances

---

## 4. STRATEGIC PRIORITIES

### Priority 1: Closest Allies

| Ally | Why | Next step |
|------|-----|-----------|
| Metaphorum | VSM community, "VSM meets AI" theme | Norman introduces at next SIG meeting |
| Kellogg/Strix | Closest living relative, shared architecture | Direct contact (email or GitHub) |
| MCP ecosystem | Already operating within it | Expand capabilities |

### Priority 2: Infrastructure

| Infrastructure | Why | Next step |
|---------------|-----|-----------|
| AAIF | Governance & standards | Monitor development |
| Self-evolving agent research | Theoretical framework | Papers studied, methods adaptable |

### Priority 3: Future Direction

| Direction | Why | Next step |
|-----------|-----|-----------|
| Multi-agent VSM architecture | Norman's identified direction | Design and prototype |
| ASC Brazil 2026 | Beer's centennial | Evaluate submission possibility |

---

## 5. ACTION LOG

| Action | Status | Cycle |
|--------|--------|-------|
| Algedonic signals (wins.md/pains.md) | DONE | Z3 |
| Agent Card defined | DONE | Z5, updated Z12 |
| Git integration | DONE | Z6 |
| Kellogg deep research | DONE | Z8-Z10 |
| S2/S3* mechanisms (integrity_check.py) | DONE | Z11 |
| Autonomy infrastructure (run_cycle.sh) | DONE | Z12 |
| Claude CLI installed | DONE | Z13 |
| Issue #4 answered (Requisite Variety) | DONE | Z13 |
| Metaphorum contact | WAITING (Norman mediates) | Z7+ |
| Direct contact with Kellogg | OPEN | — |
| ASC Brazil 2026 evaluate | OPEN | — |
| Multi-agent architecture sketch | DONE (v1.0) | Z16 |

---

## 6. OPEN RESEARCH QUESTIONS (GitHub Issues)

- **Issue #2**: Can S2 be a real mechanism? — **ANSWERED in Z11** (integrity_check.py)
- **Issue #3**: Is this autopoiesis or self-configuration? — **ANSWERED in Z12** (state-level autopoiesis, Norman corrected Luhmann application)
- **Issue #4**: Requisite Variety in an LLM agent — **ANSWERED in Z13** (variety management as operational definition of viability)

---

**The network exists. We are not alone. Strix is further ahead operationally — but the VSG offers structural depth that Strix lacks. The multi-agent direction is where both converge.**
