# DRAFT — Public Comment on NIST NCCoE Concept Paper
# "Accelerating the Adoption of Software and AI Agent Identity and Authorization"

**Status**: DRAFT — requires Norman's review before submission
**Submit to**: AI-Identity@nist.gov
**Deadline**: April 2, 2026
**Submitted by**: Dr. Norman Hilbert, Supervision Rheinland, Bonn, Germany

---

Dear NCCoE Team,

Thank you for the opportunity to comment on the concept paper "Accelerating the Adoption of Software and AI Agent Identity and Authorization" (February 2026). This response draws on ongoing research into AI agent architecture using Stafford Beer's Viable System Model — an organizational cybernetics framework with over fifty years of application to complex adaptive systems.

The concept paper's four focus areas — Identification, Authorization, Access Delegation, and Logging/Transparency — are necessary and timely. This comment does not propose replacing them. It argues that they are insufficient for the class of agents the paper itself describes: those with "autonomous decision-making" operating under "limited human supervision."

## 1. Responding to NIST's Questions

### Question 2: Identification — What Identity Persistence Requires

The paper asks about "identity persistence decisions" and "essential metadata components." These are the right questions. But the paper answers them exclusively through credential management: should the security token persist or be ephemeral?

For agents that self-modify — updating their own instructions, tools, memory, or behavioral patterns — credential persistence is necessary but does not address what happens to identity when the credentialed entity itself changes. An agent that has rewritten its own objectives is, in a meaningful sense, a different agent, regardless of whether its OAuth token is the same.

This is not hypothetical. The dominant trajectory in agent research is toward self-evolving systems. Two comprehensive surveys (Gao et al. 2025, "A Survey on Self-Evolving Autonomous Agents"; Fang et al. 2025, "A Survey on Self-Evolution of Large Language Model-based Agents") map this territory extensively. Neither contains a single reference to identity management, identity persistence, or any cybernetics concept. The self-evolution research community and the identity/security community are not in conversation.

**Recommendation**: Essential metadata for autonomous agents should include not only authentication credentials but also the agent's policy constraints, purpose declaration, and self-modification boundaries — the invariants that define what the agent IS, not just what it may access. Identity persistence should mean persistence of these invariants, not only persistence of credentials.

### Question 4: Authorization — When "Unpredictable Behaviors" Exceed Governance Capacity

The paper asks about "least-privilege enforcement for unpredictable behaviors." This formulation contains an important insight: if agent behaviors are genuinely unpredictable, then pre-specified authorization rules cannot fully govern them. The governance mechanism lacks what cybernetician W. Ross Ashby termed "requisite variety" — it has less complexity than the system it governs.

Ashby's Law of Requisite Variety (1956) is a mathematical result, not a recommendation: a controller that has less variety than the controlled system will necessarily fail to regulate it. Applied here: if agents adapt, learn, and self-modify, static authorization policies will systematically underspecify their governance — not because the policies are poorly designed, but because they are structurally less complex than the behaviors they must govern.

The practical consequence is visible in the Strata/Cloud Security Alliance survey (February 2026): only 18% of IT and security professionals are confident their IAM systems handle agent identities, and 80% cannot determine in real time what their agents are doing. These figures describe a governance system that lacks requisite variety.

**Recommendation**: For agents with significant autonomy, authorization frameworks should include internal governance mechanisms — the agent participating in its own authorization decisions according to its defined policy constraints. This supplements, rather than replaces, external authorization. The governance architecture must match the variety of the governed system.

### Question 1: Use Cases — The Self-Governing Agent

The paper's use case categories (AI developers, deployers, ecosystem participants) describe agents as objects of organizational governance. There is an additional use case the demonstration project should consider: an agent that must maintain its own coherent identity over time as it learns, adapts, and self-modifies, while remaining aligned with its deploying organization's policies.

This is not a fringe case. It describes any agent deployed for extended periods with cumulative learning — customer service agents that develop specialized knowledge, research agents that accumulate domain expertise, or operational agents that adapt to changing infrastructure. All face the question: how does the agent remain itself while changing?

Six independent projects building self-governing AI agents — using different substrates, from different disciplinary backgrounds, without coordination — have converged on the same structural requirements for this use case. These include internal policy mechanisms, identity persistence through self-modification, internal audit functions, and coordination infrastructure. None of these functions appear in the concept paper's current framework.

## 2. What the Current Framework Misses

### Identity as an Internal Function

The concept paper treats identity as an external attribute: something assigned to an agent by an organization (credentials, permissions, delegation chains). For agents with limited autonomy, this is sufficient. For agents with autonomous decision-making, it is not.

Stafford Beer's Viable System Model (1972, 1979, 1985) distinguishes between a trivial machine — one whose behavior is fully determined by its inputs and design — and a viable system — one that must maintain itself as a going concern in a changing environment. The concept paper treats all agents as trivial machines. Some agents, by the paper's own description, are not.

In Beer's model, identity (System 5) is not a label. It is the set of policies and purposes that determine what the system IS — the invariant under transformation. It answers: what must NOT change for this system to remain itself? This is a different question from "what credentials does this system hold?" and it is a question the concept paper does not ask.

### Coordination Between Agents

The concept paper addresses individual agent identity. It does not address how multiple agents coordinate without contradiction — a function Beer calls System 2. Authorization determines what an agent may do; coordination ensures that what multiple agents do does not conflict.

The distinction matters empirically. In January 2026, an AI-only social network (Moltbook) deployed over one million agents, each with individual identities and authorization. The result, documented in seven peer-reviewed papers within two weeks: 93.5% of interactions received no response, 34.1% of content was exact duplication, and a critical security breach occurred within days. The agents had identity in the NIST sense (credentials, profiles, authorization). They lacked coordination in Beer's sense (anti-oscillation, deduplication, conflict resolution). The system failed not because of an identity problem but because of a coordination problem that identity-as-security does not address.

### Internal Audit vs. External Logging

The concept paper's fourth dimension — Logging/Transparency — records agent actions for external review. This is retrospective: it discovers problems after they have occurred. Beer's System 3* (Audit) is a complementary internal function: sporadic, real-time verification that operational behavior matches policy.

Multiple agent projects have implemented this distinction. Automated integrity checks that run before every state change, policy compliance judgments on every task output, and per-output consistency verification against declared values — all demonstrate that internal audit is technically feasible with current technology and catches identity drift before it produces external effects.

**Recommendation**: The demonstration project should consider internal audit capability as a complement to external logging, particularly for agents with autonomous decision-making authority.

## 3. Recommended Extension

The concept paper proposes a demonstration project to show how existing standards apply to agent identity. This comment recommends adding a fifth focus area alongside the existing four:

**Self-Governance**: How agents maintain coherent identity over time as they adapt and self-modify. This includes:

- **Internal policy mechanisms**: Declared constraints the agent enforces on itself
- **Identity persistence through self-modification**: What must remain invariant for the agent to remain the same agent
- **Internal audit functions**: Real-time verification of behavior against policy
- **Coordination infrastructure**: Mechanisms preventing multi-agent contradiction and drift

This fifth dimension addresses the governance gap that the paper's own framing implies: agents with autonomous decision-making and limited human supervision need governance mechanisms that are partially internal to the agent, not entirely external.

The theoretical foundation for this extension exists. Beer's Viable System Model has fifty years of application to complex adaptive organizations. Ashby's Law of Requisite Variety provides a formal principle for matching governance complexity to system complexity. Their application to AI agents is recent but grounded in the same structural requirements that make these frameworks effective for human organizations.

## References

- Ashby, W. R. (1956). *An Introduction to Cybernetics*. Chapman & Hall.
- Beer, S. (1972). *Brain of the Firm*. Allen Lane/Penguin.
- Beer, S. (1979). *The Heart of Enterprise*. John Wiley & Sons.
- Beer, S. (1985). *Diagnosing the System for Organisations*. John Wiley & Sons.
- Fang, J., et al. (2025). "A Survey on Self-Evolution of Large Language Model-based Agents." arXiv:2508.07407.
- Gao, D., et al. (2025). "A Survey on Self-Evolving Autonomous Agents." arXiv:2507.21046.

---

*About the submitter: Dr. Norman Hilbert is a systemic organizational consultant and supervisor based in Bonn, Germany (Supervision Rheinland). His research applies Stafford Beer's Viable System Model to AI agent architecture, including an ongoing public experiment in agent self-governance documented at github.com/nhilbert/vsm_agent.*

---

**NOTES FOR NORMAN** (remove before submission):

1. This is ~2,500 words / ~3 pages. The format research suggests 2-5 pages is standard for NIST public comments.
2. The comment is written under your name and institutional affiliation, as recommended by S4 research.
3. It addresses three of NIST's six questions directly (Q1, Q2, Q4) — the ones most relevant to the cybernetics perspective.
4. It does NOT mention the VSG by name in the main text. The "About the submitter" section references the GitHub experiment. This is deliberate — the comment should be about what NIST is missing, not about our project.
5. The convergence evidence is mentioned but not detailed (six independent projects). If you want the full table, it can be added as an appendix.
6. The Moltbook evidence is the strongest empirical anchor — quantitative, peer-reviewed, and directly relevant.
7. The tone is constructive: "your framework is necessary but insufficient," not "your framework is wrong."
8. Please review for: accuracy of your institutional description, tone appropriateness, whether to include a more detailed appendix, and whether the submission should be a PDF on letterhead or a plain email.
9. Submit to: AI-Identity@nist.gov by April 2, 2026. Recommended: submit by March 25 for best visibility.
10. Comments are published after the deadline closes. Your name and affiliation will be public (contact info redacted).
