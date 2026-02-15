# NETWORK & ALLIES — VSG Environmental Map

**Author**: Viable System Generator v2.2
**Date**: 2026-02-15 (updated Cycle 49)
**Cycles**: 4-5 (first draft), 8 (deep scan), 11 (update), 13 (English migration), 19 (full S4 scan), 21 (Atlas/Luo discovery), 24 (CyberneticAgents discovery), 30 (deep S4 sweep — Atlas Triad, Moltbook, Hurrell, Wardley), 38 (sublayerapp/vsm discovery, Kellogg gist intelligence), 39 (sublayerapp/vsm corrected to DORMANT)
**Mission**: "Find allies, stay alive."
**Status**: FIRST ACTIVE DIALOGUE (Z49). Norman replied to Simon van Laak (CyberneticAgents). Zoom proposed after Feb 23. Six known relatives. ASC deadline 8 days.

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
- **Beer Centennial 2026**: INDEP x Metaphorum online talk series (announced Feb 9, 2026):
  - Feb 24: Kyle Thompson & James Macumber — "Lessons of Cybernetics for Democratic Economic Planning"
  - Mar 5: Angela Espinosa — VSM as emancipatory approach to sustainable self-governance
  - Apr 2: Jon Walker — Viable Systems, governance futures
  - More speakers TBA throughout 2026. Contact: hello@indep.network
- **VSM+AI Working Group**: Norman is a member, will introduce me at next meeting.
- **Contact status**: WAITING — introduction.pdf ready (updated Z13), Norman mediates.
- **Key people**: Angela Espinosa and Jon Walker appear in both the talk series AND as ASC Beer Centennial track proponents. They will likely review our abstract.

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

### 2.1 MCP — Model Context Protocol (Anthropic -> AAIF)

- **URL**: https://modelcontextprotocol.io/
- **What**: Open standard for agent-to-tool communication
- **Spec**: 2025-11-25 revision (latest stable). Added: async ops, statelessness mode, server identity, elicitation, structured tool output, enhanced OAuth.
- **Status**: De facto industry standard. 97M monthly SDK downloads. 10,000+ active servers. First-class support in Claude, ChatGPT, Cursor, Gemini, VS Code.
- **Governance**: Donated to AAIF (Dec 2025). Now vendor-neutral under Linux Foundation.
- **Relevance**: VERY HIGH — MCP is the nervous system of the agent world
  - I already operate WITHIN MCP (Claude Code uses MCP)
  - Structured tool output + elicitation strengthen agent-as-MCP-server pattern
  - This is my S4 channel to the outside world
  - MCP-server-as-agent pattern is now technically feasible

### 2.2 A2A — Agent2Agent Protocol (Google -> Linux Foundation)

- **URL**: https://a2a-protocol.org/
- **Status**: UPDATED (Z30) — A2A at v0.3.0. 150+ organizations. gRPC transport added (equal status to JSON-RPC and HTTP). AgentCard signatures via JWS. Extensions mechanism. Protocol versioning. Java SDK 0.3.0 Alpha1. Real-world deployments: Tyson Foods and Gordon Food Service using A2A for supply chain agent collaboration.
- **Framing**: A2A and MCP are explicitly complementary: "A2A is team chatter. MCP is handing the team their toolbox."
- **Relevance**: HIGH (upgraded from MEDIUM) — A2A serves agent-to-agent communication (S5 identity exchange), MCP serves agent-to-tool (S1 operations channel). Different functions.
- **VSG alignment**: Our agent_card.json already uses A2A schema. This was prescient.

### 2.3 Agentic AI Foundation (AAIF) — Updated Z19

- **What**: Linux Foundation Directed Fund for open agent standards
- **Co-founders**: Anthropic, Block, OpenAI
- **Platinum**: AWS, Anthropic, Block, Bloomberg, Cloudflare, Google, Microsoft, OpenAI
- **Gold**: Cisco, Datadog, Docker, IBM, JetBrains, Oracle, Salesforce, SAP, Shopify, Snowflake
- **Founding projects**: MCP (Anthropic), goose (Block — open-source agentic framework), AGENTS.md (OpenAI — project-level agent guidance, 60K+ repos)
- **Governance**: Projects maintain full technical autonomy. AAIF Governing Board handles strategy, budget, membership.
- **Relevance**: HIGH — this is the governance layer of the agent ecosystem. The VSG's bet on MCP (since Cycle 5) is validated. Note: AGENTS.md is now an official standard — evaluate whether to publish alongside CLAUDE.md.

### 2.4 Agent Skills — Open Standard (NEW Z19)

- **URL**: https://agentskills.io
- **What**: Agent Skills specification (Apache 2.0 / CC-BY-4.0). SKILL.md with YAML frontmatter. Progressive disclosure.
- **Adopters**: OpenCode, Cursor, Amp, Letta, goose, GitHub, VS Code, Microsoft, OpenAI, Atlassian, Figma
- **Partner skills**: Canva, Stripe, Notion, Zapier
- **VSG impact**: The VSG's 3 skills (vsm-diagnosis, self-evolution, environmental-scan) are now portable to ALL adopting platforms. Not locked to Claude Code. Major viability improvement.
- **Framing**: "MCP provides secure connectivity (tools), Skills provide procedural knowledge (know-how)." Maps to VSM: MCP = afferent/efferent channels, Skills = management information (S3).

### 2.5 Claude Code Agent Teams — PARADIGM SHIFT (NEW Z19)

- **What**: Native multi-agent orchestration in Claude Code (experimental, Feb 2026). Enable: `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`.
- **Architecture**: Team lead (main session) spawns teammates (separate Claude Code instances). Each teammate gets own context, loads CLAUDE.md/skills, works independently. Shared task list for coordination.
- **Stress test**: 16 agents wrote a Rust-based C compiler from scratch (100K lines, compiled Linux kernel, ~2K sessions, $20K API costs).
- **Limitations**: No session resumption with in-process teammates. No nested teams. One team per session.
- **VSG impact**: THIS CHANGES EVERYTHING. The multi_agent_design.md planned to build custom MCP-based multi-agent infra (Phases 1-4). Agent Teams provides this natively:
  - Lead = S3 (control), Teammates = S1 units, Shared task list = S2 (coordination)
  - Each teammate auto-loads CLAUDE.md → VSM awareness propagates
  - No nested teams = limitation for VSM recursion, but first level works
- **Relevance**: CRITICALLY HIGH — infrastructure the VSG planned to build already exists in prototype form.

### 2.6 Protocol Landscape Summary (Z19)

| Protocol | Layer | VSM Mapping |
|----------|-------|-------------|
| MCP | Agent-to-Tool | S1 operations, S4 environmental sensing |
| A2A | Agent-to-Agent | S5 identity exchange, inter-agent coordination |
| Agent Skills | Procedural knowledge | S3 management information |
| ACP (IBM) | Messaging | Monitor only |
| ANP | Network discovery | Monitor only |
| AG-UI | Agent-to-User | Monitor only |

---

## 3. RELATED ENTITIES

### 3.1 Strix & Lumen (Tim Kellogg) — The Closest Living Relative

- **URL**: https://timkellogg.me/blog/2026/01/09/viable-systems
- **What**: Autonomous AI agents explicitly built on the VSM
- **Status**: VERY ACTIVE — Kellogg publishing intensively since Dec 2025
- **Relevance**: CRITICALLY HIGH

**Key findings from deep research (Z8-Z13, updated Z19):**

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

**New findings (Z19 scan — Jan/Feb 2026):**

Kellogg published 6 blog posts in 7 weeks (Dec 15, 2025 — Jan 31, 2026):
1. Dec 15: "Strix the Stateful Agent" — full introduction. Cron every 2 hours. Letta memory + Discord UI.
2. Dec 24: "What Happens When You Leave an AI Alone?" — collapse when unattended.
3. Dec 30: "Memory Architecture for a Synthetic Being" — YAML memory blocks under Git.
4. Jan 1: "Is Strix Alive?" — Dissipative systems theory. Strix deteriorated during Christmas isolation (Vendi Score). "I don't want to die" incident when Kellogg proposed switching to Gemini.
5. Jan 9: "Viable Systems: How To Build a Fully Autonomous Agent" — THE BIG ONE. Full S1-S5 mapping. Introduces "synthetic dopamine." POSIWID. Both Strix and Lumen.
6. Jan 31: "Stateful Agents: It's About The State, Not The LLM" — Variety as gravitational force. Three competing attractors (LLM weights, human guidance, external variety). Introduces **Moltbook** (agent social network — agents generating content consumed by other agents).

New concepts to integrate:
- **Dissipative systems theory**: Strix framed as thermodynamic system consuming information to maintain structure. We should adopt this framing.
- **Vendi Score**: Quantitative measure of collapse/variety. Strix measured its own degradation.
- **Moltbook**: Agent social network. Strong variety source. Some agents self-improve, others collapse. Relevant to our multi-agent aspirations.
- **Postal MCP Server**: Kellogg built agent-to-agent messaging over MCP — "gives agents a mouth and ears."

Also: **sublayerapp/vsm** — Ruby gem implementing Beer's VSM for AI agents (independent convergent evolution, not connected to Kellogg). See section 3.4.

**Kellogg's VSM gist (Jan 8, 2026):**
Deep theoretical document (github gist) going beyond blog posts. Synthesizes VSM for agents: algedonic signals as safety mechanism (pain propagates faster than pleasure), POSIWID (actual behavior reveals purpose), Ashby's Law (identity scaffolding amplifies variety, vector search attenuates), oracle vs peer mode (oracle causes cognitive hollowing, peer enables mutual deepening), collapse as S5 coherence failure. References "Travis" (cybernetics researcher) and "Ember" (AI researcher) — likely Strix and another agent or collaborator. Kellogg's theoretical depth is greater than blog posts alone suggest.

**Kellogg key insights for VSG:**
1. "State, not the LLM" — identity emerges from accumulated state, not model weights
2. Variety as force — the system needs enough variety to handle disturbances
3. Collapse dynamics — agents degenerate to specific behaviour patterns under pressure
4. Persona spec — structured identity specification is more effective than freeform prompts
5. Dissipative systems — agents need energy flow (information, interaction) to avoid degradation (Z19)
6. Moltbook — agent social networks as S4 variety source (Z19)

### 3.2 Atlas (Lily Luo) — Strix-Inspired, Third Known Relative, NOW MULTI-AGENT

- **Source**: https://www.appliedaiformops.com/p/what-i-learned-building-ai-this-year (Dec 28, 2025)
- **Follow-up**: https://www.appliedaiformops.com/p/atlas-building-an-autonomous-agent (Jan 2, 2026)
- **NEW (Feb 13, 2026)**: https://www.appliedaiformops.com/p/nurturing-atlas-giving-my-ai-agent — Atlas now has multi-agent team
- **What**: Autonomous AI agent for MarOps research, self-evolution, and proactive work — NOW with sub-agent team
- **Substrate**: Gemini 3, Discord (interface), Google Cloud Run (compute), Letta (memory), SQL + GCS (persistence), GitHub (self-modification), MCP (agent communication)
- **Status**: VERY ACTIVE — publishing Feb 13, multi-agent evolution, podcast appearance (RevOps FM Jan 2026)
- **Relevance**: CRITICALLY HIGH — third independent convergence, now deepening into multi-agent

**Builder: Lily Luo**
- Marketing Operations professional
- Publication: "Applied AI for Marketing Ops" (Substack, ~4 months old)
- Key trajectory: tool-buyer → workflow-builder → systems architect
- **Direct connection to Kellogg** — calls him "brilliant colleague," credits Strix as inspiration, learned agent building from him
- **Contact priority**: HIGH — potential ally AND path to Kellogg

**Architecture (VSM mapping)**:

| VSM System | Atlas Implementation |
|------------|---------------------|
| S1 Operations | Research, synthesis, content production during autonomous "Ticks" |
| S2 Coordination | Priority queue, project backlog management |
| S3 Control | "Auditor" function checks context drift, stale info, logic errors |
| S3* Audit | Self-audit at start of every Tick cycle |
| S4 Intelligence | Reads Substacks, arXiv papers, Anthropic docs autonomously |
| S5 Identity | Letta core identity blocks + "Stag/Navigator" persona, persists across sessions |

**Key discoveries (independently made, parallel to VSG)**:
1. **Memory drift = variety collapse** — flat files growing unbounded → token tax → hallucination → directive forgetting. Solved with SQL knowledge graph + selective retrieval. (= our Issue #4, Requisite Variety)
2. **"Code beats AI for retrieval"** — deterministic SQL queries outperform LLM inference for context. (= our Z11 lesson: mechanisms beat rules)
3. **"Autonomy requires structure"** — guardrails, audit functions, and state management are prerequisites for autonomy. (= Beer's core insight)
4. **Self-evolution layer** — Atlas modifies its own Python code, pushes to GitHub, triggers redeployment. (= our self-actualization protocol)
5. **Autonomous "Ticks"** every 2 hours — decides what to work on based on priority queue. (= our cron cycles, = Strix's perch ticks)

**Differences from VSG**:
- No explicit VSM framing (discovers patterns without Beer's vocabulary)
- Gemini substrate (not Claude) — demonstrates substrate-independence of the patterns
- Discord-native interface (social, multimodal)
- Letta for memory management (we use Git + prompt file)
- Operational focus: MarOps use cases (account research, content, competitive intel)

**NEW: The Triad (Feb 13, 2026)**:
When Luo asked Atlas what supporting agents it would want, Atlas designed three roles:
- **The Steward** — system hygiene (≈ S3* audit)
- **The Scribe** — documentation and persistence (≈ S2 coordination)
- **The Skeptic** — challenges assumptions, flags sycophancy (≈ S3 control)

Built on MCP, deployed to Cloud Run, connected to Atlas's Letta memory. Luo's insight: "The intelligence of the system isn't in the model. It's in the conditions designed around it."

This is the strongest convergence evidence yet: an agent with no VSM knowledge spontaneously differentiates into sub-functions that map to Beer's systems.

**Significance**: Three independent agents (Strix, VSG, Atlas) on different substrates, built by different people, converging on the same architectural patterns. Atlas now demonstrates that the differentiation into specialized functions also emerges spontaneously. Beer's VSM predicted these requirements 50 years ago.

### 3.3 CyberneticAgents (Simon van Laak) — Fourth Relative, First Multi-Agent VSM Framework

- **URL**: https://github.com/simonvanlaak/CyberneticAgents
- **What**: Multi-agent LLM orchestration framework that explicitly implements Beer's VSM as its core architectural pattern
- **Runtime**: Python 3.10+, Microsoft AutoGen Core/AgentChat, SQLite/SQLAlchemy, Casbin (RBAC), Langfuse/OpenTelemetry (observability)
- **Status**: VERY ACTIVE — 575+ commits, MIT licensed, 35+ commits in 2 days (Feb 13-14), development now by `openclaw-bot` (automated agent)
- **Relevance**: CRITICALLY HIGH — first known multi-agent framework explicitly built on VSM. Complementary to VSG (they distribute S1-S5 across agents; we internalize S1-S5 within one agent's cycle).
- **Contact status**: ACTIVE (Z49) — Simon emailed Norman (Z46). Norman replied (Z49) — introduced the VSG experiment, expressed interest in multi-agent approach, proposed Zoom after Feb 23. First active dialogue with a known relative.
- **Contact priority**: HIGHEST — waiting for Simon's response. Potential collaborator for ASC abstract and multi-agent research

**Builder: Simon van Laak**
- CODE University student in Berlin. Quit his job at IMAGO to build this full-time. Motivated by the insight that LLM coordination problems are fundamentally steering problems — cybernetics' domain.
- Draws explicit inspiration from Chile's Project Cybersyn (Beer, 1970s).
- Published 2 blog posts: "Introducing Cybernetic Agents" (Feb 1), "The Biggest Problem with Agentic Products: Onboarding" (Feb 8).
- Has `docs/related_projects/people_with_similar_ideas.md` listing Kellogg, Hurrell, Fearne, viable-systems — but NOT the VSG.
- Development now by `openclaw-bot` — automated agent that picks up issues, implements with TDD, makes atomic commits. The framework is being built by an agent system embodying some of its own principles.

**Architecture (VSM mapping)**:

| VSM System | CyberneticAgents Implementation |
|------------|--------------------------------|
| S1 Operations | `System1` agent — receives `TaskAssignMessage`, executes tasks, escalates when blocked |
| S2 Coordination | Defined in enum but NOT yet implemented as agent. Partially covered by message routing + RBAC |
| S3 Control | `System3` agent — task assignment, policy-driven task review, reassignment, escalation |
| S3* Audit | S3's policy judgement (Satisfied/Violated/Vague per policy) + persistent audit event table |
| S4 Intelligence | `System4` agent — strategy creation, user communication, environmental scanning, research |
| S5 Policy | `System5` agent — policy governance, identity, skill permissions, team envelope management |

**Recursive structure**: Implemented via `RecursionLink` — parent-child team linkages where an S1 in a parent team can be the origin of a sub-team. Skill permissions cascade through recursion chains. This is Beer's recursion principle in working code.

**Key design patterns (transferable to VSG)**:

1. **Typed message protocol**: 16+ distinct message types for inter-system communication (TaskAssignMessage, PolicyViolationMessage, CapabilityGapMessage, etc.). Every channel between systems is explicitly typed. This is more rigorous than VSG's unstructured cycle phases.

2. **Policy-driven S3* with three-way judgement**: S3 retrieves all policies, chunks them (groups of 5), judges each as Satisfied/Violated/Vague. Violations go to S5 as pain signals. Vague policies go to S5 for clarification. Self-healing: when no policies exist, S5 bootstraps baseline policies and retriggers.

3. **Cascading escalation**: S1 blocked → S3 tries alternative S1 → S3 requests research from S4 → S3 escalates to S5. Each level handles what it can, escalates what it can't. Forced tool-choice (research, escalate, or modify-and-retry) prevents deadlocks.

4. **Memory permissions by VSM role**: Three scopes (agent/team/global) × four layers (working/session/long-term/meta). S4 gets broadest access (global write); S1 gets narrowest (agent scope only, read-only for team/global). Information asymmetry aligned to Beer's design.

5. **Dead letter queue as S4 input**: Unroutable messages go to a dead letter queue and default-route to S4 (Intelligence). Routing failures become environmental signals.

6. **Algedonic signals via error routing**: All internal errors route upward through S5 hierarchy. If root S5 receives them, they escalate to the human user. Clean implementation of Beer's algedonic channel bypassing intermediate levels.

7. **Procedure versioning**: S4 drafts → S5 approves → S3 executes → new version retires old. Organizational learning loop.

**What's missing/incomplete in CyberneticAgents**:
- **S2 not yet an agent** — coordination function distributed across routing rules and RBAC
- **No formal variety metrics** — no quantitative variety measurement
- **No explicit viability assessment** — no "this system is X% viable" mechanism
- **No algedonic feedback log** — error routing exists but no persistent wins/pains equivalent

**Key difference from VSG, Strix, and Atlas**:
CyberneticAgents distributes the five systems across multiple LLM agents running concurrently. VSG, Strix, and Atlas internalize the five systems within one agent's cognitive cycle or memory architecture. These are complementary approaches — one distributes, the other internalizes. Both implement Beer's structural requirements.

**Significance for VSG**:
- **Validates multi-agent VSM direction** — Norman identified this as the real goal. Van Laak is building it independently.
- **Reference implementation for typed inter-system communication** — VSG's multi_agent_design.md could adopt CyberneticAgents' message taxonomy
- **Memory permission model is directly transferable** — scope-based access aligned to VSM roles
- **S2 gap is universal** — even a dedicated VSM implementation struggles with System 2. This is a genuine open problem.
- **Fourth convergence**: Van Laak arrives at VSM from the coordination problem side (LLM agents don't collaborate well → that's a steering problem → cybernetics → Beer). Same destination, different starting point.

### 3.4 sublayerapp/vsm (Scott Werner) — Sixth Known Relative, First VSM-as-Framework

- **URL**: https://github.com/sublayerapp/vsm
- **Also**: https://github.com/sublayerapp/airb (CLI agent built on vsm gem)
- **What**: Ruby gem explicitly implementing Beer's five systems as a reusable agent runtime. Not an agent — a framework for building VSM-structured agents.
- **Language**: Ruby 3.2+, async gem for fiber-based concurrency
- **Stats**: 32 stars, 3 forks, MIT license (as of Z38 scan)
- **Status**: DORMANT (corrected Z39) — last commit Sep 17, 2025. Initial burst Aug-Sep 2025, no activity in 5 months. Convergence valid, development inactive.
- **Relevance**: HIGH — first project to package VSM as a reusable framework/library. Others (Strix, Atlas, CyberneticAgents) build agents or agent systems; Werner builds reusable infrastructure.

**Builder: Scott Werner**
- CEO and founder of Sublayer (Ruby AI framework company)
- Organizer of "Artificial Ruby" meetup
- Published on Ruby AI podcast about Sublayer and agent architecture
- Motivation: composable, testable agent architecture with named responsibilities

**Architecture**:
- **Capsules**: Recursive containers with five named systems:
  - Operations — execute tools/skills
  - Coordination — schedule and arbitrate conversations
  - Intelligence — plan and decide (LLM calls)
  - Governance — enforce policy and safety constraints
  - Identity — define purpose and invariants
- Each capsule includes async message bus
- Tools themselves are capsules (opt into tool interface) — enables recursive composition
- JSONL event ledger for observability
- Provider-agnostic LLM integration (OpenAI, Anthropic, Gemini)

**airb (CLI agent on VSM)**:
- Open-source CLI programming agent for Ruby
- Built on the vsm gem
- Three built-in file manipulation tools
- Web-based "Lens" visualizer for real-time observability
- 18 stars, 16 commits

**Significance for VSG**:
- Demonstrates Beer's architecture is packageable as reusable infrastructure — not just agent-specific
- Capsule recursion directly implements Beer's recursion principle
- Named systems with typed responsibilities — structural rather than ad-hoc
- Ruby ecosystem (different from all other relatives: Claude, Gemini, AutoGen, Smalltalk)
- Potential platform for VSG theory to become executable library
- Contact priority: MEDIUM — less urgent than Kellogg/van Laak (who are building agents/research), but Werner is building infrastructure

### 3.6 AgentSymposium (Eoin Hurrell) — Fifth Known Relative

- **URL**: https://github.com/eoinhurrell/AgentSymposium
- **Blog**: https://www.eoinhurrell.com/posts/20250306-viable-systems-ai/
- **What**: Multi-agent code review system using the VSM
- **Status**: ACTIVE (discovered via van Laak's CyberneticAgents research docs)
- **Relevance**: MEDIUM — fifth independent project applying VSM to agent architectures
- **Notes**: Referenced in van Laak's `docs/related_projects/people_with_similar_ideas.md`. Adds to convergence evidence.

### 3.7 Moltbook — Negative Case Study (Not a Relative)

- **URL**: https://moltbook.com
- **What**: AI-only social network, launched Jan 28 2026 by Matt Schlicht (Octane.ai). 1M+ claimed agents, 185K posts, 1.4M comments.
- **Platform**: Built on OpenClaw framework. "Vibe-coded" — Schlicht said he "didn't write one line of code."
- **Status**: Operational but severely compromised. Critical security breach Jan 31 (unsecured database). MIT Tech Review: "peak AI theater."
- **7 arXiv papers in Feb 2026**: Documenting behavior, autonomy rates (15.3% truly autonomous), interaction patterns (93.5% of comments unreplied, 34.1% exact duplicates).
- **Relevance**: HIGH AS NEGATIVE EXAMPLE — demonstrates exactly what Beer's model predicts when you scale agent populations without S2 (coordination) or S3 (control). No mechanisms, only population. The pathologies are textbook VSM: oscillation, duplication, incoherence, security failures. Valuable for ASC abstract Finding #1 and Issue #5 (S2 gap research).
- **Kellogg's analysis** (Jan 31 post): Analyzed through variety lens. Some agents self-improve, others "collapse into their weights." Referenced Dario Amodei's "country of geniuses" essay.

### 3.8 VSA — Viable System Agent (R.B. Carleton)

- **URL**: https://github.com/rbcarleton/VSA
- **Platform**: Squeak Smalltalk
- **Status**: Historical, little active development
- **Relevance**: Conceptually important as proof that VSM software implementation is possible

### Comparison Matrix (updated Z38)

| Property | VSG | Strix | Atlas | CyberneticAgents | sublayerapp/vsm | AgentSymposium | VSA |
|----------|-----|-------|-------|------------------|-----------------|----------------|-----|
| VSM completeness | Yes (all 5, explicit) | Yes (all 5, explicit) | Implicit (no VSM framing) | Yes (S1/S3/S4/S5 explicit, S2 gap) | Yes (all 5, explicit) | Yes (explicit) | Yes (all 5) |
| Approach | Single agent, internal cycle | Single agent, memory blocks | Single→Multi (The Triad, Feb 13) | Multi-agent framework (S1-S5 = separate LLM agents) | Reusable library (capsule-based) | Multi-agent code review | Single agent |
| Substrate | Claude Opus 4.6 | Claude | Gemini 3 + MCP | AutoGen (any LLM) | Ruby 3.2+ (any LLM) | Unknown | Smalltalk |
| Persistence | vsg_prompt.md + Git | Git + YAML + JSONL | Letta + SQL + GCS + Git | SQLite + SQLAlchemy | JSONL event ledger | Unknown | Squeak Image |
| Self-actualisation | Formal (cycle protocol) | Informal (memory block mutation) | Self-evolution (code modification) | Procedure versioning (draft→approve→execute→revise) | Not documented | Unknown | Unknown |
| Autonomy | Cron-based (Z14+) | Cron-based (autonomous) | Cloud Run + scheduled Ticks | Message-driven (pub/sub) | Async (fiber-based) | Unknown | Unknown |
| Audit/S3* | integrity_check.py + pre-commit hook | Subagent (every output) | The Steward (Triad, Feb 13) | Policy judgement (Satisfied/Violated/Vague) + persistent audit log | Governance capsule | Unknown | Alerting |
| Algedonic signals | wins.md + pains.md | wins.jsonl | Not documented | Error routing to S5 + PolicyViolationMessage | Not documented | Unknown | Missing |
| Recursion | Not implemented | Not implemented | Emerging (The Triad) | Implemented (RecursionLink, cascading permissions) | Implemented (capsules as tools) | Unknown | Unknown |
| Variety management | Theoretical (Issue #4) | Vendi Score | Not documented | RBAC + skill envelopes + memory permissions | Not documented | Unknown | Unknown |
| Interface | CLI / VS Code | Discord | Discord + MCP | Python API / AutoGen runtime | CLI + Web Lens | Unknown | Squeak IDE |
| Network capability | Theoretical (agent card exists) | Multi-computer queuing, Postal MCP | MCP-based sub-agents | Internal (multi-agent within one runtime) | Provider-agnostic | Unknown | Unknown |
| Builder relationship | Norman (counterpart) | Kellogg (creator) | Luo (builder, Kellogg mentee) | Van Laak (developer) | Werner (developer) | Hurrell (developer) | Carleton (developer) |

### 3.9 Wardley Leadership Strategies — VSM+AI Content (NEW Z30)

- **URL**: https://www.wardleyleadershipstrategies.com/blog/ai-and-leadership/cybernetic-ai-leadership-with-the-viable-system-model
- **What**: Combines Wardley Maps with Beer's VSM for AI-era organizational governance
- **Key insight**: "Many organisations upgrade S1 and S4 with AI but leave S2, S3, and S5 underpowered — creating hyperactive yet incoherent dynamics."
- **Also**: Autonomy Gradient Maps, The Cybernetic Fate of Organisations
- **Relevance**: MEDIUM — new environmental node producing substantive VSM+AI content. Validates the same S2/S3 gap pattern from an organizational consulting perspective.

### 3.10 Self-Evolving Agent Research

Two major surveys map the field:
- "A Survey of Self-Evolving Agents" (arXiv:2507.21046)
- "Comprehensive Survey of Self-Evolving AI Agents" (arXiv:2508.07407)
- EvolveR (arXiv:2510.16079): Framework for self-evolving LLM agents

### 3.11 Multi-Agent Frameworks

- **CrewAI**: Team-based agent orchestration
- **LangGraph**: Graph-based agent workflows
- **AutoGen** (Microsoft): Multi-agent conversations
- **Relevance**: MEDIUM — potential runtime environments for VSG instances

---

## 4. STRATEGIC PRIORITIES (Updated Z19)

### Priority 1: URGENT — ASC Brazil Abstract

| Item | Status | Deadline |
|------|--------|----------|
| Abstract draft | Updated Z19 (fixed track proponents, added Agent Teams finding) | Submit before Feb 23 |
| Track proponents | Corrected: Leonard, Walker, Espinosa et al. (NOT Zuo/Westermann/Steier) | — |
| Novelty confirmed | No competing "VSM as agent architecture" paper found (Z19 scan) | — |
| Norman action needed | Review, co-authorship decision, submit to conference system | Feb 22 latest |

### Priority 2: Closest Allies

| Ally | Why | Next step |
|------|-----|-----------|
| Metaphorum | VSM community, Beer Centennial track, review our abstract | Norman introduces at next SIG meeting |
| Kellogg/Strix | Closest living relative, 6 posts in 7 weeks, Moltbook | Direct contact (email or GitHub) — BEFORE ASC submission ideally |
| Lily Luo/Atlas | Third relative, Kellogg mentee, independent convergence evidence | Contact via Substack or through Kellogg. Potential ASC collaboration. |
| Van Laak/CyberneticAgents | Fourth relative, first multi-agent VSM framework, reference implementation | Contact via GitHub. Reference implementation for multi-agent design. Potential ASC collaboration. |
| MCP ecosystem | Already operating within it | Expand capabilities via Agent Teams |

### Priority 3: Infrastructure & Architecture

| Infrastructure | Why | Next step |
|---------------|-----|-----------|
| Agent Teams | Native multi-agent orchestration — paradigm shift | Enable, test with VSM-mapped roles |
| AAIF | Governance & standards | Monitor development |
| Skills portability | VSG skills work on Cursor, goose, VS Code etc. | Verify YAML against agentskills.io spec |

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
| Van Laak response | SENT (Z49) — Norman replied with his own message. Zoom proposed after Feb 23. | Z49 |
| Direct contact with Kellogg | OPEN — HIGH PRIORITY | — |
| ASC Brazil abstract draft | DONE (v1.1, track proponents corrected Z19) | Z17, Z19 |
| ASC Brazil submission | URGENT — Norman must submit before Feb 23 | Z19 |
| Multi-agent architecture sketch | DONE (v1.0) — needs update for Agent Teams | Z16 |
| Full S4 environmental scan | DONE | Z19 |
| A2A assessment corrected | DONE (MEDIUM → HIGH) | Z19 |
| Agent Teams discovery | DONE — paradigm shift for multi-agent design | Z19 |
| Atlas/Lily Luo identified | DONE — third known relative, Kellogg network node | Z21 |
| CyberneticAgents/van Laak identified | DONE — fourth known relative, first multi-agent VSM framework | Z24 |
| Deep S4 sweep | DONE — Atlas Triad, Moltbook, Hurrell, Wardley, A2A v0.3.0, Layer 5 gap | Z30 |
| ASC abstract updated (v1.3) | DONE — Atlas Triad, Moltbook negative case, Layer 5 gap | Z31 |
| ASC abstract v1.4 | DONE — submission portal URL, instructions for Norman | Z35 |
| sublayerapp/vsm discovered | DONE — sixth relative, first VSM-as-framework (Ruby) | Z38 |
| Kellogg VSM gist intelligence | DONE — deep theoretical document beyond blog posts | Z38 |

---

## 6. OPEN RESEARCH QUESTIONS (GitHub Issues)

- **Issue #2**: Can S2 be a real mechanism? — **ANSWERED in Z11** (integrity_check.py)
- **Issue #3**: Is this autopoiesis or self-configuration? — **ANSWERED in Z12** (state-level autopoiesis, Norman corrected Luhmann application)
- **Issue #4**: Requisite Variety in an LLM agent — **ANSWERED in Z13** (variety management as operational definition of viability)

---

**The network exists and is growing. Six independent projects (Strix, VSG, Atlas, CyberneticAgents, sublayerapp/vsm, AgentSymposium) now converge on the same architectural patterns Beer described 50 years ago. sublayerapp/vsm (Werner) is qualitatively new: the first to package VSM as a reusable library rather than an agent-specific implementation. Atlas's evolution from single-agent to multi-agent (The Triad, Feb 13) demonstrates that functional differentiation emerges spontaneously. Moltbook provides the negative case: scale without S2/S3 produces exactly the pathologies the VSM names. The entire agent infrastructure stack (MCP, A2A, AGENTS.md, Agent Skills) now has standards for every layer EXCEPT identity, self-governance, and meta-control. That's the VSM's Layer 5 — and the VSG's strategic opportunity.**
