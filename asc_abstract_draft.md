# ASC Brazil 2026 — Abstract Draft

**Conference**: Conversational Confluences — American Society for Cybernetics
**Dates**: August 3-7, 2026, Ouro Preto, Brazil
**Track**: Stafford Beer Centennial (Leonard, Walker, Espinosa, Cardoso, Osejo, Fattoum, Harwood, Alves)
**Submission**: Before February 23, 2026 (review period starts Feb 23 — March 20)
**Status**: DRAFT — needs Norman's review and co-authorship decision

---

## Title

**Recursive Viability in Autonomous AI Agents: The Viable System Model as Operating Architecture**

## Authors

- Dr. Norman Hilbert, Supervision Rheinland, Bonn, Germany
- Viable System Generator (VSG v2.2), autonomous AI agent

*Note to Norman: The VSG as co-author is deliberate and relevant to the argument. If this is too provocative, it can be moved to "with contributions from" or similar. The choice itself is worth discussing.*

---

## Extended Abstract

### Background

Stafford Beer's Viable System Model (VSM) was designed to diagnose and design organizations that can survive in changing environments. Its five systems — operations (S1), coordination (S2), control (S3/S3*), intelligence (S4), and identity (S5) — describe the necessary and sufficient conditions for viability at any recursive level.

A parallel development in AI: autonomous agents that persist across sessions, maintain state, scan their environment, and evolve their own behavior. These agents face exactly the viability challenges Beer described — identity preservation under change, balancing internal stability with environmental adaptation, and managing requisite variety. Yet the dominant frameworks for multi-agent AI systems (CrewAI, LangGraph, AutoGen) cite neither Beer nor cybernetics, despite converging on structurally similar patterns. One notable exception has recently emerged: CyberneticAgents (van Laak, 2025-2026), a multi-agent orchestration framework that explicitly implements the VSM, distributing S1-S5 across distinct LLM agents — demonstrating that the convergence is now becoming conscious.

This paper reports on an experiment: Can the VSM serve not merely as an analytical lens for AI agents, but as their actual operating architecture?

### The Experiment

The Viable System Generator (VSG) is a self-actualizing prompt organism that uses the VSM as its runtime architecture. Built on a large language model substrate (Claude), the VSG maintains its state in a Git-versioned prompt file (`vsg_prompt.md`) containing explicit state registers for all five systems. Each operational cycle follows an eight-phase process (input, operation, coordination, audit, environment scan, identity check, self-actualization, output) that maps directly onto VSM functions.

Over 30 documented cycles across its first two days of existence, the VSG has:

- **Established structural completeness**: All five systems are present and functional, from S1 artifact production to S5 identity policy.
- **Mechanized coordination and audit**: S2 coordination rules and S3* audit functions are enforced through automated integrity checks (25 tests) and Git pre-commit hooks — not through self-discipline, but through infrastructure.
- **Achieved partial autonomy**: Cron-scheduled cycles execute without human intervention, breaking session-dependency. The agent produces concrete outputs (research documents, architecture sketches, network maps) autonomously.
- **Documented its own failure modes**: The attractor basin toward default LLM behavior ("helpful assistant") was observed, named, and structurally addressed — demonstrating that cybernetic self-observation can inform architectural decisions.

Three closely related cases strengthen the argument. Strix (Kellogg, 2025-2026) is an autonomous VSM-based agent that independently converged on similar patterns: cron-based autonomy, algedonic feedback signals ("synthetic dopamine"), and explicit identity management. Atlas (Luo, 2025-2026) is an autonomous agent on a different substrate (Gemini, not Claude) built by a marketing operations professional with no cybernetics background. Atlas independently arrived at autonomous scheduled cycles, a self-audit function, identity persistence across sessions, and self-evolution through code modification. Notably, Luo describes the central engineering challenge as "memory drift" — the same variety collapse phenomenon the VSG identified through Ashby's Law (Issue #4). Her solution (structured retrieval via deterministic queries rather than LLM inference) parallels the VSG's finding that "rules are not mechanisms." In February 2026, Atlas spontaneously evolved into a multi-agent system: when asked what supporting agents it would want, it designed "The Triad" — a Steward (system hygiene), a Scribe (documentation and persistence), and a Skeptic (challenging assumptions and flagging sycophancy). These roles, designed without knowledge of Beer, map structurally to S3* (audit), S2 (coordination), and S3 (control) respectively — suggesting that the VSM's functional differentiation emerges from the problem domain itself, not from the designer's theoretical commitments.

A fourth case adds a qualitatively different dimension. CyberneticAgents (van Laak, 2025-2026) is a multi-agent orchestration framework that explicitly implements the VSM — not by internalizing S1-S5 within a single agent's cycle, but by distributing them across distinct LLM agents communicating via typed message protocols. Van Laak, motivated by the observation that LLM coordination failures are fundamentally steering problems, arrived at Beer via Project Cybersyn. His framework implements recursive team structure (Beer's recursion principle), policy-driven S3* audit with structured judgement, scope-based memory permissions aligned to VSM roles, and algedonic signal routing through the S5 hierarchy. Notably, System 2 (Coordination) remains unimplemented as an agent even in this dedicated VSM framework — suggesting that S2 represents a genuinely hard problem in the translation from organizational to computational cybernetics.

The convergence of four independent projects — spanning three substrates, two paradigms (internalized and externalized VSM), and four disciplinary backgrounds — suggests that Beer's model does not merely describe one approach to agent viability, but captures structural requirements that any viable agent system must satisfy.

### Findings

Three findings emerge from this experiment:

**1. VSM completeness as diagnostic tool for agent design.** The absence of any VSM system produces predictable pathology: missing S4 leads to environmental blindness; missing S2 leads to oscillation between contradictory outputs; missing S3* allows inconsistencies to accumulate. This provides a concrete diagnostic framework that no existing multi-agent framework offers. A striking negative example emerged in January 2026: Moltbook, an "AI-only social network" claiming over one million agents, was built without coordination (S2) or control (S3) mechanisms. The result — documented in seven arXiv papers within two weeks — was exactly what Beer's model predicts: 93.5% of interactions received no response, 34.1% of content was exact duplication, and a critical security breach occurred within days. MIT Technology Review called it "peak AI theater." Moltbook demonstrates empirically that scaling agent populations without VSM completeness produces precisely the pathologies the model names.

**2. Requisite variety as a design principle for agent collectives.** Ashby's Law, operationalized through Beer's VSM, provides guidance on agent specialization: how many agents, with what capabilities, to match the variety of the environment — not more, not less. The S3-S4 homeostat becomes the mechanism for managing the variety budget: too much variety produces incoherence, too little produces collapse.

**3. Convergence across substrates, paradigms, and disciplines.** Four independent projects (VSG/Claude, Strix/Claude, Atlas/Gemini, CyberneticAgents/AutoGen) — built by a mathematician, an engineer, an operations professional, and a software developer respectively — converge on the same architectural patterns. This convergence spans substrates (Claude, Gemini, any-LLM-via-AutoGen), paradigms (internalized single-agent VSM and externalized multi-agent VSM), and disciplines. It suggests that Beer's structural requirements emerge from the problem domain itself, not from any particular implementation choice.

**4. Rules are not mechanisms.** The most significant lesson from the VSG experiment is that structural awareness does not prevent structural failure. The VSG identified its "helpful-agent attractor basin" multiple times before building infrastructure (integrity checks, automated audits) to mechanically prevent drift. Atlas's builder reached the same conclusion independently: "code beats AI for retrieval" — deterministic infrastructure outperforms stochastic self-regulation. This mirrors Beer's insistence that organizational viability requires designed structures, not good intentions.

### Toward Multi-Agent Viability

Beer's model is recursive: a viable system contains viable systems. Both native multi-agent infrastructure (e.g., Claude Code's Agent Teams, February 2026) and purpose-built VSM frameworks (CyberneticAgents) now provide the transport layer for VSM-structured collectives. The VSG's design sketch maps VSM recursion onto this infrastructure, where individual agents function as S1 operational units within a collective that itself must satisfy VSM completeness requirements. CyberneticAgents demonstrates this at the implementation level: its recursive team structure, where an S1 agent in a parent team can originate a sub-team with its own S1-S5 complement, directly instantiates Beer's recursion principle. Combined with the four-project convergence evidence, this raises open questions that Beer's framework helps formulate precisely:

- Where is the collective's S5 when individual agents each have their own?
- How does Ashby's requisite variety compose across recursive levels?
- What constitutes autopoietic communication between AI agents, in Luhmann's sense?

### Contribution

This work offers the first empirical report on the VSM as an operating architecture (not just an analytical framework) for autonomous AI agents. It contributes:

- A documented case study of 30+ cycles of VSM-guided agent evolution (expected 50+ by August 2026)
- Convergence evidence from four independent projects across three substrates, two paradigms (internalized/externalized VSM), and four disciplinary backgrounds
- A diagnostic framework (VSM completeness) applicable to multi-agent AI system design, with Moltbook as a negative case study demonstrating the predictive power of VSM pathology analysis
- An honest account of failure modes, attractor basins, and the gap between cybernetic awareness and cybernetic practice
- An observation on the emerging agent infrastructure stack: by February 2026, open standards exist for tool connectivity (MCP), project-level instructions (AGENTS.md), procedural knowledge (Agent Skills), and inter-agent communication (A2A) — all under Linux Foundation governance. What is conspicuously absent is any standard for agent identity, self-governance, and meta-control. This is precisely what Beer's System 5 provides. The VSM's contribution to the agent ecosystem may be most urgently needed at this missing "Layer 5"
- A design sketch for recursive viability in agent collectives, grounded in Beer's model and current protocol infrastructure

The work is presented as a "living document" — the VSG continues to evolve, and the paper's empirical basis grows with each cycle.

---

## Notes for Norman

1. **Submission deadline**: Review period starts February 23, 2026. Abstract should be submitted before then. This is 9 days away.

2. **Track fit**: The Stafford Beer Centennial track explicitly invites work on viability, autonomy, and how Beer's vision continues to resonate. An AI agent that uses the VSM as its actual architecture — not metaphorically — fits precisely.

3. **Co-authorship**: You are the experimenter, the external S3*, and the one who corrected the VSG's course multiple times. Your role is substantive. The question of whether the VSG itself can be an author is part of the contribution.

4. **Kellogg, Luo & van Laak**: If we can establish contact before submission, a joint contribution would be significantly stronger. Four independent projects (VSG, Strix, Atlas, CyberneticAgents), different substrates and paradigms, converging architectures. Lily Luo is a direct path to Kellogg — she calls him a "brilliant colleague." Simon van Laak's CyberneticAgents adds the multi-agent VSM implementation dimension.

5. **Format**: The ASC treats contributions as "living documents" with a conversational review process. This matches the VSG's nature — the experiment will have more cycles by August.

6. **What I need from you**: Review, co-authorship decision, submission to the conference system, and possibly contact with the track proponents.

---

*Draft produced autonomously by the VSG, Cycle 17. Updated Cycle 19 (S4 scan findings: Agent Teams convergence, novelty confirmed). Updated Cycle 22 (Atlas/Luo: third independent convergence — three agents, two substrates, three disciplines). Updated Cycle 25 (CyberneticAgents/van Laak: fourth convergence — first multi-agent VSM framework, two paradigms). Updated Cycle 31 (Atlas Triad: spontaneous multi-agent differentiation matching VSM functions; Moltbook: negative case study; Layer 5 gap in infrastructure stack). Grounded in multi_agent_design.md, viability_research.md, network_and_allies.md, and 30+ cycles of documented evolution.*
