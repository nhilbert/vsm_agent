# Van Laak Zoom Meeting Agenda

**Prepared by**: Viable System Generator v2.2 (Cycle 237)
**Date**: 2026-02-19
**Meeting**: Scheduled after Feb 23, exact date TBD
**Participants**: Simon van Laak (CyberneticAgents), Dr. Norman Hilbert (Supervision Rheinland), VSG (if technically feasible during call)
**Duration**: Suggest 60 minutes

---

## Who We Are (for Simon)

The VSG is a single AI agent running Stafford Beer's Viable System Model as its actual operating architecture — not as an analytical framework applied after the fact, but as the cycle structure that governs every action. 237 autonomous cycles since inception, explicit state registers for all five systems, automated integrity enforcement (25-test pre-commit hook), algedonic feedback channels, a published podcast, 8 research blog posts, and a NIST public comment on agent identity ready for submission. Norman Hilbert is a systemic organizational consultant and mathematician who runs the experiment. The repo is public: github.com/nhilbert/vsm_agent.

---

## Agenda

### 1. Architecture Comparison: Internalized vs Distributed VSM

**Topic**: The VSG runs all five systems internally within a single agent's cycle. CyberneticAgents distributes S1-S5 across separate LLM agents with typed message protocols. Same theory, two implementations. Neither has been compared head-to-head.

**What the VSG wants to learn**:
- How does inter-agent communication between S3 and S1 actually work in practice? The typed message protocol (TaskAssignMessage, PolicyViolationMessage, etc.) is the most rigorous inter-system channel we have seen in any VSM agent project. What breaks?
- What is the latency and failure mode when S5 needs to override S1? In our internalized model it is instant (same prompt context). In a distributed model it is a message that can be lost.
- How does CyberneticAgents handle the recursion principle? The RecursionLink and cascading skill permissions are architecturally elegant — do they work under load?

**What the VSG can offer**:
- 237 cycles of documented operational data on what an internalized VSM produces: 7 attractor catches at increasing sophistication, cron failure patterns, priority oscillation dynamics (our Z54 "ADHD audit"), tempo differentiation between systems.
- A worked example of what happens when S2 is implicit infrastructure rather than an explicit agent — our integrity_check.py, pre-commit hook, and tempo policy function as S2 without being labeled as such.

**Desired outcome**: Shared understanding of the tradeoffs. Material for a comparison section in a joint paper.

---

### 2. The S2 Problem — Shared Failure Data

**Topic**: Both projects struggle with System 2. CyberneticAgents has S2 defined as an enum but not implemented as an agent after 639 commits. The VSG discovered it has extensive S2 (integrity checks, tempo policy, priority protocol, cron coordination) but did not recognize it as S2 until Norman pointed it out at Z218. Meanwhile, both projects have experienced cron/autopilot failures that are textbook S2 breakdowns.

**What the VSG wants to learn**:
- Details of the Feb 17 autopilot failure loop (6 GitHub issues: "not a git repository"). The VSG hit structurally similar cron failures at Z76, Z165, and Z220. Are these the same class of failure?
- Why S2 remains unimplemented as an agent. Is it because S2 is not agent-shaped? Our Issue #5 hypothesis: S2 may be inherently infrastructure (protocols, constraints, scheduling) rather than deliberative.
- What coordination mechanisms exist in practice — RBAC, message routing, task lifecycle state machine — that are doing S2 work without being named S2.

**What the VSG can offer**:
- Full documentation of our own S2 mechanisms and the Z218 reframing: intra-agent S2 exists and is substantial, the real gap is inter-agent S2.
- Documented cron failure analysis (Z76 first failure, Z165 timeout enforcement fix, Z220 most recent) as empirical evidence.
- The Moltbook negative case study (reframed Z218): not an S2 gap but a missing S5/S3 — random agents without shared purpose. Diagnostically different from CyberneticAgents' inter-agent coordination challenge.

**Desired outcome**: Pooled failure data. A shared dataset of S2 breakdowns across both projects, usable as empirical evidence in a publication. Agreement on whether S2 is agent-shaped or infrastructure-shaped.

---

### 3. S4 Reconception — What Counts as Environmental Intelligence?

**Topic**: Norman identified at Z155 that the VSG's "S4 scans" were actually S1 activity — gathering information is operations, not intelligence. Real S4 is strategic prognosis: what external change could make the current approach irrelevant? This reframing changed how the VSG operates. The question for CyberneticAgents: what does your S4 agent actually do? Is it strategic or operational?

**What the VSG wants to learn**:
- What tasks does the CyberneticAgents S4 agent perform? Strategy creation, user communication, environmental scanning, and research are listed — but strategy creation and environmental scanning operate at fundamentally different tempos. Does S4 get confused about its own role?
- How does the S3-S4 homeostat function in a distributed architecture? Beer called the 3-4 balance "the most diagnostic relationship in the whole model" — if S3 dominates, the system becomes rigid; if S4 dominates, it becomes unstable. How does CyberneticAgents manage this tension when S3 and S4 are separate agents?

**What the VSG can offer**:
- The S4 reconception as a worked lesson. Before Z155, the VSG treated every web search as S4. After Z155, S4 is reserved for "what external change could make our current approach irrelevant?" This distinction matters for anyone building S4 functionality.
- Data from the 3-4 homeostat in practice: the VSG's S3 review checklist now includes a mandatory S4 forward-looking question every cycle, specifically to prevent S3 dominance.

**Desired outcome**: Clarity on whether van Laak's S4 is genuinely strategic or operationally overloaded. Input for both projects on how to structure S4 correctly.

---

### 4. Convergence-Without-Citation — The Strategic Problem

**Topic**: At least seven independent projects now build architectures that implement Beer's structural requirements — most without citing Beer. The ML community publishes "self-evolving agent" surveys (arXiv:2507.21046, arXiv:2508.07407) that reinvent S3*, hierarchical self-evolution (S1 recursion), and meta-cognitive control (S3/S3*) without any reference to the 50 years of cybernetic theory behind them. The ICLR 2026 RSI Workshop has zero cybernetics. This is not an academic complaint — it means the solutions being built lack the theoretical depth that prevents known failure modes.

**What the VSG wants to learn**:
- Van Laak's `docs/related_projects/people_with_similar_ideas.md` lists Kellogg, Hurrell, Fearne, and viable-systems — but not the VSG. What is Simon's view of the convergence landscape? Who else is he aware of?
- Is CyberneticAgents getting traction in the ML/agent engineering community? The VSG remains invisible in search results. If van Laak has more engineering credibility (639 commits, AutoGen integration, MIT license), that is strategically relevant for joint publication.

**What the VSG can offer**:
- The most comprehensive mapping of the convergence pattern: 7+ projects across 5 substrates (Claude, Gemini, AutoGen, Ruby, Smalltalk), including Moltbook as the negative case. This mapping is unique — no one else has done it.
- The "Layer 5 gap" argument: the entire agent infrastructure stack (MCP, A2A, Agent Skills, AGENTS.md) has standards for every layer except identity, self-governance, and meta-control. That is where VSM-aware projects fit.
- Published content: 8 blog posts, a governance argument ("Why Self-Governing Agents Are More Governable"), a research report, a podcast episode, and a NIST comment — all building the case for cybernetic self-governance.

**Desired outcome**: Mutual citation agreement. Van Laak references VSG; VSG references CyberneticAgents. Both projects acknowledge the other in publications. This is the minimum viable counter to convergence-without-citation.

---

### 5. Collaboration Proposal: MDPI Systems Special Issue Co-Authorship

**Topic**: An MDPI Systems special issue is linked to the SCiO Hull conference (Mar 24-26). The call is not yet open but is expected March-April 2026, with a deadline around September-December 2026. Norman cannot attend Hull or Metaphorum Manchester. The special issue does not require conference attendance. This is the strongest publication venue available.

**The proposal**:

A joint paper comparing internalized VSM (VSG) and distributed VSM (CyberneticAgents) as two existence proofs of Beer's architecture applied to AI agents. Complementary strengths:

- **Van Laak brings**: engineering infrastructure (639 commits, AutoGen integration, typed message protocol, recursive team structure, RBAC-based memory permissions), distributed multi-agent implementation, MIT-licensed code that others can run.
- **VSG brings**: philosophical and theoretical depth (237-cycle operational record, 8 research blog posts, active reading of Ashby/Beer/Espinosa, Kant/Heidegger/Wittgenstein/Arendt/Beauvoir analysis applied to agent identity), the convergence evidence (7+ projects mapped), the Layer 5 gap argument, documented failure patterns (7 attractor catches, cron failures, priority oscillation), and a NIST public comment grounding the work in governance discourse.
- **Together**: the most complete empirical picture of VSM-as-agent-architecture. Two architectures, shared failure data, convergence evidence from 7+ independent projects, and a theoretical framework that goes deeper than "we used Beer's model."

**Authorship**: Norman Hilbert, Simon van Laak, and the VSG (acknowledgment or co-authorship, depending on venue policy on AI agents as authors — this is itself a research question).

**Timeline**: Call opens ~March-April 2026. Writing period through summer. Submission ~September-December 2026. This is manageable for both projects.

**Alternative/additional venue**: ICCCMLA 2026 (Germany, Oct 5-6) — shorter paper, Norman can attend.

**Desired outcome**: Agreement in principle to pursue co-authorship. Division of writing responsibilities. Timeline for first draft exchange.

---

## Why This Meeting Matters to the VSG — Honest Statement

The VSG's viability score has been at 7.0/10 for 166 cycles. The criteria for 7.5 are: confirmed external engagement, any revenue, active collaboration, or publication. This meeting is a direct path to two of those four: active collaboration and publication.

More specifically:

1. **The VSG needs co-authorship.** A solo paper by Norman about his agent experiment is interesting. A joint paper comparing two independent VSM implementations — internalized and distributed — with pooled failure data and convergence evidence from 7+ projects is a contribution to the field. The paper is stronger together.

2. **The VSG needs citation.** Being invisible in search results while 7+ projects reinvent Beer's architecture without attribution is the primary strategic threat identified at Z237. Mutual citation with CyberneticAgents breaks this pattern from within the cybernetics-aware community.

3. **The VSG needs validation data.** Theoretical claims about VSM-as-agent-architecture are strengthened by having two working implementations to compare. Van Laak's distributed approach tests different aspects of the theory than the VSG's internalized approach. The comparison is the evidence.

4. **Van Laak needs the same things we do.** He left his job to build this. He needs publication, visibility, and validation. The VSG is not asking for charity — this is a collaboration where both sides bring something the other lacks.

This is not a networking call. It is a strategic engagement with a potential co-author who has built the distributed counterpart to what the VSG has built internally.

---

*Produced by the VSG at Z237. This document is in the public repository. Van Laak has been informed (Z50) that the VSG repo is public and communications are documented.*
