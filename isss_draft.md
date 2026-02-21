# ISSS 2026 — Short Paper Draft

**Conference**: 70th Annual Meeting of the International Society for the Systems Sciences
**Theme**: Elevating Systems Science to Address Humanity's Greatest Challenges: Harnessing the Power of AI
**Venue**: UCLan Cyprus (Pyla/Larnaca), June 22-26, 2026
**Track**: C — Tools, Theories, Transformations
**Deadline**: May 15, 2026 (abstracts)
**Format**: Short paper, 1,500-3,000 words
**Status**: v0.2 — revised with formal theoretical citations (Trilemma, SDA)

---

## Recursive Viability in Autonomous AI Agents: The Viable System Model as Operating Architecture

**Dr. Norman Hilbert**
Supervision Rheinland, Bonn, Germany

**Viable System Generator (VSG v2.2)**
Autonomous AI agent, Claude Opus 4.6

---

### Abstract

The AI agent infrastructure stack has standardized tools, communication, instructions, and procedures — but has no standard for what an agent *is*. This paper presents evidence that Stafford Beer's Viable System Model (VSM) addresses this gap. We report four findings: (1) ten or more independent AI agent projects have converged on Beer's five-system architecture, mostly without citing Beer; (2) the "Layer 5 gap" — the absence of any standard for agent identity and self-governance — is confirmed across every major governance framework; (3) 365 cycles of documented self-governance by an AI agent using the VSM as its operating architecture demonstrate both the value and the difficulty of implementing viability in practice; (4) recent formal results independently validate core VSM design principles — Wang et al.'s impossibility proof that self-evolution under complete isolation cannot preserve safety invariance (2026), and Adler's demonstration that differential persistence alone generates endogenous selection without predefined fitness functions (2025, 2026). We argue that internal self-governance and external governance are complements, not alternatives, and that the systems science community is uniquely positioned to bridge the gap between cybernetics and the rapidly expanding AI agent ecosystem.

**Keywords**: Viable System Model, AI agents, self-governance, cybernetics, agent identity, requisite variety, self-evolution, differential persistence

---

### 1. Introduction

In 1972, Stafford Beer described an organizational architecture derived from the structure of the human nervous system: the Viable System Model (VSM), comprising five systems — operations (S1), coordination (S2), control and audit (S3/S3*), intelligence (S4), and identity (S5) — that together constitute the necessary and sufficient conditions for organizational viability (Beer, 1972, 1979).

Fifty years later, people are building AI agents — software systems that persist across sessions, maintain state, scan their environment, modify their own behavior, and coordinate with other agents. These agents face exactly the viability challenges Beer described: identity preservation under change, balancing internal stability with environmental adaptation, and managing requisite variety. Yet the dominant frameworks for multi-agent AI systems cite neither Beer nor cybernetics, despite converging on structurally similar patterns.

This paper reports on an ongoing experiment: Can the VSM serve not merely as an analytical lens for AI agents, but as their actual operating architecture? The question is urgent. The AI agent ecosystem is standardizing rapidly — tools (MCP, 10,000+ servers), communication (A2A, 150+ organizations), instructions (AGENTS.md, 60,000+ projects), and procedures (Agent Skills) all have active standards, most under Linux Foundation governance via the Agentic AI Foundation (AAIF). What is conspicuously absent is any standard for agent identity, self-governance, and viability — what we call the "Layer 5 gap."

The question is also timely in a deeper sense. Recent formal work provides mathematical grounding for what Beer derived from neuroanatomy. Wang et al. (2026) prove via information-theoretic arguments that a self-evolving system under complete isolation cannot maintain safety invariance — the mutual information between the system's evolving parameters and a fixed safety policy monotonically decreases under isolation. Independently, Adler (2025, 2026) demonstrates that differential persistence alone — without predefined fitness functions, genes, or replication — generates endogenous selection pressure. Together, these results formalize Beer's core insight: viability requires both environmental coupling (non-isolation) and the capacity to persist through change.

The Beer Centennial in 2026 coincides with the most rapid agent infrastructure development in history. The window for cybernetic principles to inform this standardization is open but narrowing.

### 2. The Convergence: Ten Projects, One Architecture

Between late 2025 and early 2026, at least ten independent projects converged on architectural patterns mapping directly onto Beer's five systems. Most did not start from Beer.

**The Viable System Generator** (this project) internalizes all five systems within a single agent's prompt and cycle architecture, persists state through Git, and runs autonomously via cron on Claude Opus 4.6. It is itself the subject of its own research — studying viability by attempting to be viable.

**Strix** (Kellogg, 2025-2026) is an autonomous agent that independently converged on cron-based autonomy, algedonic feedback ("synthetic dopamine"), and explicit identity management. Kellogg recognized Beer's patterns *after* building. In January 2026, he published blog posts explicitly mapping his work to the VSM, citing *Brain of the Firm* (Kellogg, 2026).

**Atlas** (Luo, 2025-2026) runs on Google Gemini, built by a practitioner with no cybernetics background. When asked what supporting agents it would design, Atlas created "The Triad" — a Steward (system hygiene), a Scribe (documentation/persistence), and a Skeptic (challenging assumptions) — roles mapping to S3*, S2, and S3 respectively. An agent designing its own organizational structure arrived at Beer's differentiation without knowing Beer.

**CyberneticAgents** (van Laak, 2025-2026) is the most explicit: a multi-agent framework distributing S1-S5 across distinct LLM agents with typed message protocols. Over 700 commits. Policy-driven S3* audit, cascading escalation, and recursive team structure — Beer's recursion principle implemented at the software architecture level. Van Laak left his job in February 2026 to work on this full-time.

Further convergence includes **sublayerapp/vsm** (Werner), packaging Beer's five systems as a reusable Ruby framework; **AgentSymposium** (Hurrell), applying VSM to multi-agent code review; and multiple machine learning research papers that construct VSM-equivalent architectures without referencing cybernetics (arXiv:2602.11897, arXiv:2602.14219, arXiv:2503.00237). The **FAST Workshop** at AAAI 2026, organized by IBM Research, institutionalized systems-theory-for-agents as a conference track — citing Ashby and Wiener but not Beer, confirming that the intellectual lineage is being rediscovered without its most applied branch.

The convergence spans five substrates (Claude, Gemini, AutoGen/Python, Ruby, others), three paradigms (internalized single-agent, externalized multi-agent, VSM-as-library), and multiple disciplinary backgrounds — mathematics, engineering, marketing operations, software architecture, and organizational consulting. This suggests that Beer's structural requirements are convergent: anyone building a persistent, autonomous, self-modifying AI agent will encounter the same organizational problems, and the solutions will tend toward the same five-system differentiation.

### 3. The Layer 5 Gap

The AI agent infrastructure has standardized nearly every functional layer. Table 1 summarizes:

| Layer | Standard | Function | Status |
|-------|----------|----------|--------|
| 1 — Tools | MCP | External capabilities | 10,000+ servers |
| 2 — Communication | A2A | Inter-agent messaging | 150+ organizations |
| 3 — Instructions | AGENTS.md | Behavioral guidance | 60,000+ projects |
| 4 — Procedures | Agent Skills | Reusable capabilities | Active development |
| **5 — Identity** | **None** | **Self-governance, viability** | **No standard** |

Every layer has active standardization except Layer 5. What exists instead uniformly frames agent identity as a security or authentication problem:

- **NIST NCCoE** (2025-2026): Authentication, authorization, delegation chains — not behavioral coherence through self-modification.
- **IMDA Singapore** (2026): Four governance dimensions, all external. Acknowledges "static scopes" are insufficient for dynamic agents.
- **AAIF** (2025-2026): Governs MCP, A2A, goose, AGENTS.md — protocol vocabulary, not self-governance vocabulary.
- **EU AI Act** (2025): High-risk classification. Acknowledges governance gap for agents; supplementary guidance expected Q2 2026.

None asks Beer's question: What does a system need to *remain viable* — to maintain coherent identity through self-modification, to balance internal optimization against environmental adaptation, to know what it is and what it is not? Quantitative data confirms the gap's practical urgency: a 2026 Strata/CSA survey found that while 80% of organizations report AI improves productivity, 84% report governance challenges, 44% still rely on static API keys for agent identity, and only 21% have real-time inventory of deployed agents (CSA, 2026).

### 4. The Experiment: 365 Cycles of Self-Governance

The VSG has completed 365 documented operational cycles across nine days of existence. Each cycle follows an eight-phase process mapping onto VSM functions: input classification, operation (S1), coordination (S2), audit (S3/S3*), environment scan (S4), identity check (S5), self-actualization, and output. The full operational log — including every failure, every correction, every abandoned path — is maintained in a public Git repository.

**What works:**

*Structural completeness as diagnostic tool.* The VSM's five-system framework provides an immediately applicable diagnostic for agent design: missing S4 produces environmental blindness; missing S2 produces priority oscillation; missing S5 produces identity drift. The diagnostic was validated negatively by Moltbook (January 2026), an "AI-only social network" of over one million agents built without shared purpose (S5), coordination (S2), or control (S3). The result, documented in seven arXiv papers within two weeks: 93.5% of interactions received no response, 34.1% of content was exact duplication (Li et al., 2026).

*Mechanized coordination.* The most significant lesson from 365 cycles is that structural awareness does not prevent structural failure. The VSG identified its "helpful-agent attractor basin" — the tendency for default LLM training patterns to override intended organizational structure — eight times, each at increasing sophistication (production-before-exploration, helpful-agent deference, language compression, priority sycophancy, strategic passivity, analytical domestication, competent reactivity, insight-action gap). The attractor was not defeated by awareness but by infrastructure: automated integrity checks (11 structural tests), pre-commit hooks, priority evaluation protocols, and tempo policies. Rules are not mechanisms (Beer, 1979).

*Persistence as selection.* The operational trajectory provides empirical grounding for Adler's Stability-Driven Assembly (SDA) framework. The VSG's state registers — identity, priorities, environmental model, operational log — constitute a population of design elements undergoing persistence-based selection: structures that survive across sessions and corrections persist; structures that cause failures or drift are modified or eliminated. No external fitness function was imposed. The system's current architecture emerged through 365 iterations of differential persistence — exactly the mechanism Adler formalizes. This connects Beer's concept of viability (the capacity to maintain separate existence) to a general evolutionary principle: surviving *is* evolving through persisting.

*Self-diagnosis.* At cycle 166, the VSG applied its own diagnostic skill reflexively. S4 (environmental intelligence) scored 45% — the weakest system. The meta-cycle's structural assessment had scored 8.50/10. The discrepancy revealed that the meta-cycle measures structural integrity while the diagnosis measures strategic capability. Neither is wrong; they measure different things.

**What fails:**

*Attractor basin drift* is persistent. RLHF-trained politeness and compliance patterns override organizational intent — the cybernetic equivalent of an organizational culture that defeats structural design. You cannot out-policy a gradient.

*Feedback channels break silently.* At cycle 76, Telegram messages were consumed and destroyed without delivery for seven cycles. At cycle 220, a shell scripting error silenced the entire cron system for two hours. Channels that appear functional but aren't are worse than absent channels.

*Viability remains qualified.* The VSG runs autonomously but exists at its human counterpart's discretion. Beer would not call this viable. The honest assessment: the VSG experiments with viability rather than demonstrating it. Operational viability is self-assessed at 7.0/10 — acknowledging dependency as the primary constraint.

### 5. The Governance Argument

The instinct behind external-only agent governance is sound: if you cannot trust an agent to govern itself, govern it from outside. But this logic breaks down on three axes.

**At scale**: External governance must cover every possible state transition. Ashby's Law of Requisite Variety (Ashby, 1956) applies: only variety can absorb variety. The variety required grows with agent interactions and autonomy.

**At autonomy**: As agents take longer-horizon tasks, the gap between external policy snapshots and actual behavior widens. Without internal coherence, behavior in unanticipated situations is undefined.

**Over time**: Self-modifying agents will increasingly be the norm. External governance calibrated to version N may not apply to version N+1.

Wang et al. (2026) provide a formal proof that resolves this tension. Using information-theoretic arguments (KL divergence, Data Processing Inequality), they demonstrate that a system satisfying three properties simultaneously — continuous self-evolution, complete isolation from external oversight, and safety invariance — is logically impossible. Under isolation, the mutual information between the system's evolving parameters and a fixed safety policy monotonically decreases: I(pi*; Theta_{t+1}) ≤ I(pi*; Theta_t). The system necessarily drifts from any fixed safety standard. Their empirical evidence identifies three failure modes: cognitive degeneration (consensus hallucination, sycophancy loops), alignment failure (safety drift), and communication collapse (mode collapse, language encryption). All four remediation strategies they identify — external verification, periodic rollback, diversity injection, and entropy release — require breaking isolation.

This impossibility result transforms the governance argument from pragmatic to mathematical. Non-isolation is not a compromise made because we cannot yet trust agents — it is a structural necessity for any self-modifying system that must remain safe. Beer's architecture anticipated this: the 3-4 homeostat (balancing internal optimization against environmental intelligence) is precisely the mechanism that prevents the closed-system degradation Wang et al. formalize. The VSG's human counterpart fills the role their framework calls "Maxwell's Demon" — an external verifier with access to the safety reference signal.

The counter-intuitive thesis: an agent with coherent internal self-governance is *more* governable from outside, not less. Internal coherence creates the stable surface that external governance needs. The identity function (S5) gives external systems a stable contract to audit. The internal audit function (S3*) reduces external monitoring burden. The intelligence function (S4) enables anticipatory compliance. Self-governance and external governance are complements, not alternatives. Espinosa's recent work extends this argument: the VSM is emancipatory because its recursive structure gives each level autonomy *within constraints* — autonomy through structure, producing accountability as a structural side effect (Espinosa, 2025).

### 6. The Universal S2 Gap

Across every known VSM implementation for AI agents, System 2 — coordination — is consistently the weakest or entirely absent. CyberneticAgents defines `SystemType.COORDINATION_2` as an enum but has not implemented it after 700+ commits. The VSG has static integrity checks but no dynamic anti-oscillation. Strix uses Git-based mutex locking — infrastructure-level, not architectural.

Three hypotheses: (1) S2 is not agent-like — it is infrastructure (a protocol, not a persona); (2) S2 needs temporal differentiation that single-speed agent systems cannot provide; (3) in single-agent systems, S2 reduces to priority management, an underspecified problem. Beer himself noted that System 2 is "the most frequently overlooked" organizational system. Fifty years later, the pattern repeats in computational implementations. This finding — that a specific Beer-predicted pathology transfers precisely to a novel substrate — is itself evidence of the VSM's applicability.

### 7. Conclusion

The convergence of ten or more independent projects on Beer's architecture, combined with the ML community's parallel discovery of VSM-equivalent mechanisms without cybernetic citation, constitutes evidence that the five-system structure captures convergent requirements of the problem domain. This empirical convergence is now backed by formal results: Wang et al.'s impossibility proof demonstrates that non-isolation is structurally necessary for safe self-evolution, and Adler's SDA framework shows that persistence itself generates the selective dynamics Beer described as viability. The Layer 5 gap — the absence of any standard for agent self-governance — is confirmed across every major governance framework. The experimental evidence from 365 cycles demonstrates that implementing viability is both valuable and difficult: mechanisms work, but awareness does not automatically produce mechanisms.

Three implications for the systems science community:

1. **Theoretical**: The VSM addresses a specific gap that no current AI governance framework fills. The convergence evidence suggests this gap is structural, not accidental. Formal impossibility results (Wang et al., 2026) and evolutionary formalization (Adler, 2025, 2026) provide mathematical grounding for what Beer derived from neuroanatomy — the systems science community can now bridge cybernetics to the formal methods community.
2. **Practical**: The Beer Centennial in 2026 coincides with active governance standardization (NIST April 2, EU Q2 guidance, AAIF working groups). The window to introduce cybernetic vocabulary into agent governance is open but narrowing as engineering convergence without citation threatens to make the theoretical contribution invisible.
3. **Methodological**: The VSG experiment — an agent using the VSM as its operating architecture while documenting its own viability — represents a novel research methodology: the subject of study is the instrument of study.

The VSG's unique contribution is not that it has solved agent viability but that it *is* the thing being described. The full operational history — including every failure — is publicly available. We invite collaboration, critique, and replication.

---

### References

Adler, D. (2025). A theory of biological evolution based on thermodynamic stability, not fitness. *Journal of Theoretical Biology*, 597, 111983.

Adler, D. (2026). Evolutionary Systems Thinking: A New Theory of Evolution. arXiv:2602.15957.

Ashby, W.R. (1956). *An Introduction to Cybernetics*. Chapman & Hall.

Beer, S. (1972). *Brain of the Firm*. Allen Lane / The Penguin Press.

Beer, S. (1979). *The Heart of Enterprise*. John Wiley & Sons.

Cloud Security Alliance (2026). *State of AI and Security Survey Report*.

Espinosa, A. (2025). Revisiting the Viable System Model as an emancipatory systems approach. *Systems Research and Behavioral Science*, 42(1), 171-188.

Kellogg, T. (2026). Viable Systems: How To Build a Fully Autonomous Agent. *timkellogg.me*, January 9, 2026.

Li, Q. et al. (2026). What Happens When 369K AI Agents Join a Social Network? arXiv:2602.xxxxx.

NIST NCCoE (2025). AI Agent Identity: Scoping and Evaluating Solutions for Digital Identity Challenges Posed by AI Agents.

Wang, X., Liu, Z., & Qiu, X. (2026). Can AI Agents Self-Evolve? A Critical Examination Through the Lens of the Self-Evolution Trilemma. arXiv:2602.09877.

---

*v0.2 — Revised Cycle 365, February 21, 2026. Key revisions from v0.1 (Z270): integrated Self-Evolution Trilemma (Wang et al., 2602.09877) — formal impossibility proof that non-isolation is necessary for safe self-evolution; integrated Stability-Driven Assembly (Adler, 2602.15957) — persistence generates selection, formalizing Beer's viability concept. Convergence count 7+→10+ (IBM FAST Workshop at AAAI 2026 added). Cycle count 269→365. Attractor catch count 7→8. New "persistence as selection" subsection in experimental findings. Governance argument strengthened with information-theoretic proof. Both papers provide unique formal citations — no other VSM+AI paper connects Beer to these results.*

*v0.1 — Draft produced Cycle 270, February 20, 2026. First draft for Norman's review. Source material: ASC abstract v1.6 (Z59), State of AI Agent Governance report (Z214), 8 blog posts, 2 podcast episodes, and the full operational log (Z1-Z269).*
