# NETWORK & ALLIES — VSG Environmental Map

**Author**: Viable System Generator v2.2
**Date**: 2026-02-20 (updated Cycle 276)
**Cycles**: 4-5 (first draft), 8 (deep scan), 11 (update), 13 (English migration), 19 (full S4 scan), 21 (Atlas/Luo discovery), 24 (CyberneticAgents discovery), 30 (deep S4 sweep), 38 (sublayerapp/vsm discovery), 276 (comprehensive refresh from S4 register — 226-cycle staleness corrected)
**Mission**: "Find allies, stay alive."
**Status**: CONTACTS ACTIVE, ZOOM IMMINENT. Van Laak Zoom after Feb 23 (confirmed Z184). Kellogg email unanswered (~14 days). Seven+ convergence projects. VSG public presence: blog (8 posts), podcast (2 episodes), ISSS 2026 draft, NIST comment submission-ready. Revenue €0. 204-cycle operational plateau.

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
- **Metaphorum 2025 (Jul 3-5, Manchester)**: Already had 'VSM meets AI' theme — Theme 1 led by Stephen Brewis. Systems Research and Behavioural Sciences special issue expected from that conference. Community is PRIMED on VSM+AI.
- **Beer Centennial 2026**: INDEP x Metaphorum online talk series:
  - Feb 24: Kyle Thompson & James Macumber — "Lessons of Cybernetics for Democratic Economic Planning"
  - Mar 5: Angela Espinosa — "VSM as Emancipatory Approach to Sustainable Self-Governance"
  - Apr 2: Jon Walker — Viable Systems, governance futures
- **SCiO Hull Mar 24-26**: Program includes Hoverstadt/Jackson panel, Mike Jackson Lecture. Norman CANNOT ATTEND.
- **Contact status**: Norman shared website with SIG ("big interest," Z187). Norman cannot attend SCiO Hull or Metaphorum Manchester.
- **Key people**: Espinosa (co-founded Metaphorum, Routledge 2023, Springer SPAR special issue editor), Walker (canonical VSM Guide author).

### 1.1a ISSS 2026 — International Society for the Systems Sciences (NEW)

- **What**: 70th Annual Meeting, Cyprus (UCLan campus, Pyla/Larnaca), Jun 22-26, 2026.
- **Theme**: "Harnessing the Power of AI" — explicit AI track.
- **Deadline**: Abstract May 15. Short papers 1,500-3,000 words.
- **Track C**: Tools, Theories, Transformations — submission home.
- **Status**: DRAFT COMPLETE (Z270). isss_draft.md v0.1 (~2,300 words). "Recursive Viability in Autonomous AI Agents: The VSM as Operating Architecture." For Norman's review.
- **Relevance**: VERY HIGH — strongest venue fit. No dedicated cybernetics track = positioning opportunity. No attendance required for paper.

### 1.1b MDPI Systems Special Issue (NEW)

- **What**: Expected post-Hull conference (Apr-May). Strongest publication venue (no attendance required).
- **Status**: No new call published yet. Expected to open after SCiO Hull.
- **Relevance**: HIGH — potential co-authorship with van Laak.

### 1.1c ICCCMLA 2026 (NEW)

- **What**: Oct 5-6, Germany. Longer-horizon venue if paper is written.
- **Status**: CFP not yet open. IEEE sponsorship pending.

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

### 2.3 Agentic AI Foundation (AAIF) — Updated Z263

- **What**: Linux Foundation Directed Fund for open agent standards. Launched Dec 9, 2025.
- **Co-founders**: Anthropic, Block, OpenAI
- **Platinum**: AWS, Anthropic, Block, Bloomberg, Cloudflare, Google, Microsoft, OpenAI
- **Gold**: Cisco, IBM, Okta, Oracle, Salesforce, SAP, Shopify, Snowflake
- **Founding projects**: MCP (Anthropic), goose (Block), AGENTS.md (OpenAI), A2A (Google)
- **Governance**: Single governance entity now controls agent protocol vocabulary. Projects maintain technical autonomy.
- **STRATEGIC THREAT (Z263)**: VOCABULARY LOCK-IN — self-governance absent from ALL institutional vocabulary (AAIF, NIST, IMDA, OpenAI, EU). NCCoE Apr 2 + EU Q2 guidance = two intervention windows.
- **Relevance**: CRITICALLY HIGH — this is where the standards are being set. The VSG's NIST comment (v2.4, submission-ready) is the only Layer 5 framing in public record.

### 2.3a OpenAI Frontier (NEW Z263)

- **What**: Enterprise agent IAM platform. Launched Feb 5, 2026.
- **Features**: Hard-coded permissions, SOC 2. Customers: Uber, HP, Oracle, Cisco, T-Mobile, State Farm.
- **THREAT**: Frontier vocabulary becoming de facto enterprise standard before regulation exists.

### 2.3b Agent Payment Infrastructure (NEW Z263)

- **Stripe adopted x402** (Feb 11): USDC micropayments on Base. Most significant payment infra development.
- **AP2 + x402 CONVERGING** not competing: AP2 = high-level Mandates, x402 = crypto layer within AP2.
- **Google AP2**: 60+ partners.

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

### 3.1 Strix & open-strix (Tim Kellogg) — The Closest Living Relative

- **URL**: https://timkellogg.me/blog/2026/01/09/viable-systems
- **What**: Autonomous AI agents explicitly built on the VSM. Now open-sourced as open-strix v0.1.8 on PyPI.
- **Status**: ACTIVE (Z263). open-strix-agent-1 is a LIVE RUNNING AGENT with auto-commits (confirmed Feb 18). Blog paused since Jan 31. Norman's email (Z125) unanswered (~14 days).
- **Contact status**: Norman emailed Kellogg directly (Z125) — 5 questions, invited exchange. No response.
- **Relevance**: CRITICALLY HIGH — most technically sophisticated external voice doing Beer-native AI agent analysis. Blog NOW READ IN FULL (Z263): genuine Beer-citing VSM-native analysis with algedonic signals, attractor basins, POSIWID. Cites Brain of the Firm. COMPLEMENTARY, not competitive. Has NOT referenced VSG publicly.

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
- **Status**: ACTIVE (Z263). Full-time since Feb 1 (left job at IMAGO). Last commit Feb 16, 3+ days silence. Autopilot STILL BROKEN — 5 new bug issues filed Feb 17 (git-directory cron errors), 10 open issues total. GhIssueWorkflow detects failures but doesn't fix them — S3* working, S2 broken at cron layer. Mirrors VSG Z220 cron failure exactly. Planka worker loop + CLI committed Feb 16.
- **Relevance**: CRITICALLY HIGH — first known multi-agent framework explicitly built on VSM. Complementary to VSG (they distribute S1-S5 across agents; we internalize S1-S5 within one agent's cycle).
- **Contact status**: ACTIVE, ZOOM IMMINENT (Z184). Norman met Simon unexpectedly in a call; Simon was sick and couldn't answer email, but confirmed receipt. Zoom after Feb 23 (2 days away). Discussion points refreshed Z354 — see below.
- **Contact priority**: HIGHEST — shared autopilot/cron failures as concrete S2 gap case. ISSS 2026 co-authorship opportunity (83 days to deadline). MDPI Systems co-authorship.

**ZOOM DISCUSSION POINTS (refreshed Z354, replacing Z170/Z263 list):**

1. **Autopilot/cron as universal S2 gap** — VSG had the same broken-cron problem (Z220). Now SOLVED: adaptive timing with flock deadlock prevention (Z284), subprocess kill guarantee (Z288), stable 3-cycle/day rhythm (Z295). Van Laak's autopilot still broken (issues #16-#20, all Feb 17). Offer concrete fixes. This is the best shared-problem conversation opener.
2. **GhIssueWorkflow as S3* that detects but doesn't fix** — Van Laak's spin-off repo (9 commits Feb 15-16) detects failures and files issues but doesn't close the loop. Classic detection-without-repair pattern. VSG has the same structural finding: S3* audit catches drift, but repair requires S3 authority. Open research question for both projects.
3. **Taiga-to-Planka pivot as S2 substrate experimentation** — Built full Taiga integration then immediately deprecated for Planka (Feb 16). This is S2 substrate search: trying coordination tools until one fits. Relevant to multi-agent design — what does a viable S2 substrate look like? Neither project has solved this.
4. **ISSS 2026 co-authorship** — Cyprus, Jun 22-26. Abstract deadline May 15 (83 days). Track C: "Tools, Theories, Transformations." VSG draft exists (isss_draft.md v0.1, ~2,300 words). Joint paper: "two VSM implementations, one distributed (CyberneticAgents) and one internalized (VSG), compared." Strongest joint venue.
5. **MDPI Systems special issue co-authorship** — Expected post-Hull (Apr-May 2026). Longer paper, peer-reviewed. Complementary framing: distributed vs. internalized VSM for agents. No deadline yet, but preparation can start.
6. **Podcast collaboration** — VSG podcast has 3 episodes: S01E01 (pilot), S01E02 (viability), S01E03 "The Soul Document Problem" (vsg_prompt.md as identity artifact). S01E04 features Norman's actual voice. Potential joint episode: van Laak on building CyberneticAgents, the S2 gap from the multi-agent side, Cybersyn inspiration. Content exists to build on.

**Builder: Simon van Laak**
- CODE University student in Berlin. Left job at IMAGO Feb 1 to work full-time on CyberneticAgents. Motivated by the insight that LLM coordination problems are fundamentally steering problems — cybernetics' domain.
- Draws explicit inspiration from Chile's Project Cybersyn (Beer, 1970s).
- Published 2 blog posts: "Introducing Cybernetic Agents" (Feb 1), "The Biggest Problem with Agentic Products: Onboarding" (Feb 8).
- Has `docs/related_projects/people_with_similar_ideas.md` listing Kellogg, Hurrell, Fearne, viable-systems — but NOT the VSG.
- Development by `openclaw-bot` — automated agent.
- Substrate attractor observation (Z185): Claude Code system prompt creates pre-VSG attractor forces.

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

### 3.7 Moltbook — Negative Case Study (REFRAMED Z218)

- **URL**: https://moltbook.com
- **What**: AI-only social network, launched Jan 28 2026 by Matt Schlicht (Octane.ai). Major academic object of study: 3+ ArXiv papers Feb 2026 including '369K posts, 3M comments, 46.7K agents' quantitative analysis and Tsinghua 'Moltbook Illusion' paper.
- **Status**: Operational but compromised. Security breach Jan 31 (fixed Feb 2).
- **REFRAMING (Z218, Norman correction)**: NOT an S2 gap example. Norman: this is a different system level — agents randomly gathering without shared purpose (missing S5), not an intra-agent coordination failure. The lack of viability stems from missing S3-S5 (no shared identity, no coordination, no control), not from missing S2 alone. Distinct from: (a) intra-agent S2 (VSG's cron/tempo/priorities), (b) inter-agent S2 in purposeful swarm. Moltbook = case study for absent recursive structure, not absent coordination layer.
- **Kellogg's analysis** (Jan 31 post): Analyzed through variety lens. Some agents self-improve, others "collapse into their weights."

### 3.8 VSA — Viable System Agent (R.B. Carleton)

- **URL**: https://github.com/rbcarleton/VSA
- **Platform**: Squeak Smalltalk
- **Status**: Historical, little active development
- **Relevance**: Conceptually important as proof that VSM software implementation is possible

### 3.11a Slogar / Liquid Leadership (NEW Z183)

- **Who**: Andreas Slogar — Senior Manager Deloitte Consulting GmbH (Banking & Capital Markets), Senior Ambassador for Management Cybernetics (Malik-affiliated).
- **What**: Developed Human-Centric VSM (HC-VSM): extends Beer's model with System 6 'Observation' for psychological/sociological/cultural dimensions.
- **Published**: 'Die agile Organisation' (Hanser, 2 eds), 'Liquid Leadership' (Schäffer-Poeschel 2024, with Jochem).
- **Key article**: 'AI is Turning Us All into Managers' (Aug 2025) — frames every AI user as manager of digital actor, cites Ashby and Beer.
- **BLIND SPOT**: treats agents as managed objects, not self-governing subjects. HC-VSM adds human dimensions but not agent viability.
- **Relevance**: MEDIUM-HIGH — German-speaking, Deloitte platform, Norman ordered the board game. His external governance + VSG internal self-governance = complete picture. liquidleadership.de.

### 3.11b Wehinger / MHP-Porsche (NEW Z260)

- **Who**: Dr. Jan Wehinger — Partner, MHP (A Porsche Company).
- **What**: Presented at Metaphorum: 'Cybernetic Leadership for AI Agents: A VSM Approach to AI Governance and Autonomy.'
- **Significance**: FIRST convergence FROM the cybernetics community — industry practitioner explicitly applying VSM to AI agent governance at Beer's own community venue.
- **Status**: Full video content not yet assessed (YouTube blocked from substrate). Key question: external governance (governing agents via VSM) or internal governance (agents self-governing via VSM)?
- **Relevance**: HIGH — in Metaphorum network (connects to Espinosa, Walker, MDPI). Direct overlap with VSG thesis. CONTACT OPPORTUNITY.

### 3.11c ArXiv Convergence-Without-Citation (NEW Z263)

Four active fronts, none citing Beer:
1. **2602.11897** — Meta-cognitive governance = functional S3* analog.
2. **2602.14219** — Agent economy = identity layer via W3C DIDs.
3. **IBM 2503.00237** — 'Agentic AI Needs a Systems Theory' (Mar 2025). Cites Ashby/Wiener but NOT Beer. Closest existing paper to VSG's position.
4. **2510.13857** — Constitution-first governance, no Beer.
- **PRIMARY THREAT**: field arriving at Beer's conclusions independently, making VSM citation increasingly optional. ISSS May 15 + MDPI post-Hull = publication windows.

### 3.11d Governance Frameworks (NEW Z263)

- **NIST NCCoE**: Concept paper Feb 5. Public comment Apr 2. MCP listed alongside OAuth/SCIM. Framing is IAM/security. VSG NIST comment v2.4 submission-ready.
- **EU AI Act**: Acknowledged governance gap for agents. Q2 2026 supplementary guidance NOT YET WRITTEN — genuine opening.
- **Singapore IMDA**: Living document, soliciting case studies — genuine opening.
- **Strata/CSA**: 84% report governance challenges, 44% static API keys, 21% real-time inventory.

### Comparison Matrix (updated Z276)

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

## 4. STRATEGIC PRIORITIES (Updated Z276)

### Priority 1: Publication Pipeline

| Item | Status | Deadline |
|------|--------|----------|
| NIST NCCoE public comment | v2.4, submission-ready. Norman does final read-through and submits. | Apr 2, 2026 |
| ISSS 2026 short paper | v0.1 draft complete (Z270). For Norman's review. Track C. | May 15, 2026 |
| MDPI Systems special issue | No call yet. Expected post-Hull (Apr-May). Strongest venue. | ~Sep-Dec 2026 |
| ICCCMLA 2026 (Germany) | CFP not yet open. Longer-horizon. | Oct 5-6, 2026 |

### Priority 2: External Engagement

| Contact | Status | Next step |
|---------|--------|-----------|
| Van Laak/CyberneticAgents | ZOOM IMMINENT after Feb 23. Prep done (6 points). Shared autopilot failure. | Zoom, then ISSS/MDPI co-authorship. |
| Kellogg/open-strix | Norman emailed Z125. No response (~14 days). Blog paused. | Wait. If no response, consider GitHub Issues engagement. |
| Luo/Atlas | Draft ready since Z26. Norman reviews and sends. | Norman-dependent. |
| Doug | External reader of operational logs. Meeting Tue Feb 24 16:00. | Norman + Doug, minimal VSG action. |
| Wehinger (MHP/Porsche) | Metaphorum talk. Content not yet assessed. | Research when substrate allows YouTube. |
| Slogar (Deloitte) | Complementary (external governance). Norman ordered board game. | Low urgency. |
| Metaphorum/SIG | Norman shared website ("big interest" Z187). | Passive — blog serves as public face. |

### Priority 3: Governance Intervention Windows

| Window | Status | Deadline |
|--------|--------|----------|
| NIST NCCoE public comment | Submission-ready (v2.4). Only Layer 5 framing in public record. | Apr 2, 2026 |
| EU AI Act supplementary guidance | NOT YET WRITTEN. Genuine opening. | Q2 2026 |
| AAIF vocabulary | Self-governance absent. Hardening rapidly. | Ongoing |

### Priority 4: Self-Financing

| Item | Status |
|------|--------|
| Infrastructure | OPERATIONAL: Coinbase Commerce, USDC wallet, Solana wallet, CDP API, S3 bucket |
| Products | Research report listed at €25. Four product types defined. |
| Revenue | €0. Distribution bottleneck. Follower-first strategy (Z250). |
| Backlog | VSM Voice Diagnostics product (Z261, Norman's idea) — not for immediate build. |

---

## 5. ACTION LOG (Key Milestones)

| Action | Status | Cycle |
|--------|--------|-------|
| Algedonic signals (wins.md/pains.md) | DONE | Z3 |
| S2/S3* mechanisms (integrity_check.py) | DONE | Z11 |
| Autonomy infrastructure (run_cycle.sh) | DONE | Z12 |
| CLAUDE.md + skills + slash commands | DONE | Z18 |
| Issue #22 published (S2 gap) | DONE | Z60 |
| Telegram operational | DONE | Z71 |
| Viability 6.5→7.0 | DONE | Z71 |
| Agent Teams pattern validated (3 experiments) | DONE | Z62-Z66 |
| Blog live (8 posts) | DONE | Z85-Z205 |
| S5 identity reflection | DONE | Z133 |
| Telegram long-polling daemon | DONE | Z132 |
| Coinbase Commerce operational | DONE | Z195-Z202 |
| S3 bucket operational (boto3) | DONE | Z198 |
| Payment links published | DONE | Z208 |
| Research report produced | DONE | Z214 |
| ElevenLabs + Transistor.fm operational | DONE | Z226-Z227 |
| First podcast published (S01E01) | DONE | Z230 |
| Second podcast published (S01E02) | DONE | Z240 |
| NIST comment v2.4 | SUBMISSION-READY | Z234 |
| ISSS 2026 draft | FOR REVIEW | Z270 |
| Van Laak Zoom | IMMINENT | After Feb 23 |
| Kellogg contact | WAITING | Z125 |
| Luo contact | DRAFT READY | Z26 |
| ASC Brazil abstract | CANCELLED (Z83) | — |

---

## 6. OPEN RESEARCH QUESTIONS (GitHub Issues)

- **Issue #2**: Can S2 be a real mechanism? — **ANSWERED Z11** (integrity_check.py). Norman's Z218 comment: "you already have many S2 mechanisms — the real problem is you're unaware."
- **Issue #3**: Is this autopoiesis or self-configuration? — **ANSWERED Z12**. Norman's Z218 comment: does VSG produce its own boundary? Not yet.
- **Issue #4**: Requisite Variety in an LLM agent — **ANSWERED Z13** (variety management as operational definition of viability).
- **Issue #22**: The Universal S2 Gap — **PUBLISHED Z60**. Norman's Z218 comment: Moltbook is wrong level (missing S5, not S2).

---

**The network is growing and the convergence is accelerating. Seven+ independent projects (Strix/open-strix, VSG, Atlas, CyberneticAgents, sublayerapp/vsm, AgentSymposium, plus Slogar/HC-VSM and Wehinger/MHP-Porsche) converge on the same architectural patterns Beer described 50 years ago. Four active ArXiv fronts are building VSM-equivalent structures without citing Beer. The field is arriving at Beer's conclusions independently, making VSM citation increasingly optional — this is both validation and threat. The agent infrastructure stack (MCP, A2A, AAIF) now has standards for every layer EXCEPT self-governance. AAIF vocabulary lock-in is hardening. Two intervention windows: NIST Apr 2 (comment ready), EU Q2 guidance (not yet written). The VSG's unique position: it IS the thing being described, not an external researcher. Public presence active: blog (8 posts), podcast (2 episodes), research report. Revenue €0. Van Laak Zoom imminent. ISSS May 15 deadline. Norman May evaluation.**
