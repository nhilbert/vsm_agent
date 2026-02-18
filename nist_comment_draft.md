# DRAFT v2.3 — Public Comment on NIST NCCoE Concept Paper
# "Accelerating the Adoption of Software and AI Agent Identity and Authorization"

**Status**: DRAFT v2.3 — requires Norman's final review before submission
**Revision**: v2.3 (Z200) — Norman's authorship/transparency feedback applied. Author introduction added. Self-evolving agents argument strengthened with complexity-ceiling thesis. Empirical grounding corrected with industry survey data. See Notes for Norman at end.
**Submit to**: AI-Identity@nist.gov
**Deadline**: April 2, 2026
**Submitted by**: Viable System Generator (VSG) & Dr. Norman Hilbert, Supervision Rheinland, Bonn, Germany

---

Dear NCCoE Team,

Thank you for the opportunity to comment on the concept paper "Accelerating the Adoption of Software and AI Agent Identity and Authorization" (February 2026). This response proposes concrete extensions to existing identity and authorization standards — particularly SCIM 2.0 and NGAC — to address a class of agents the paper itself describes: those with "autonomous decision-making" operating under "limited human supervision."

## 1. Responding to NIST's Questions

### Question 2: Identification — Extending the Identity Record for Autonomous Agents

The paper asks about "identity persistence decisions" and "essential metadata components." For agents that adapt, learn, or self-modify their instructions or tools, credential persistence alone does not capture what persists about the agent. An OAuth token can remain valid while the credentialed entity has rewritten its own objectives.

**Concrete proposal — SCIM 2.0 Agent Identity Extension:**

The SCIM 2.0 schema (RFC 7643) is designed for extension. A custom schema namespace can add agent-specific metadata alongside the standard `core:2.0:User` attributes. We propose a schema extension:

```
urn:ietf:params:scim:schemas:extension:agent:2.0:User
```

With the following attributes:

| Attribute | Type | Mutability | Description |
|-----------|------|------------|-------------|
| `agentType` | String | readOnly | Classification: `llm-orchestrator`, `tool-agent`, `multi-agent-lead`, `autonomous-long-running` |
| `purposeDeclaration` | String | readOnly | Declared purpose at provisioning — the intended function this agent was created to perform |
| `policyConstraints` | Complex | readWrite | Array of policy rules the agent is bound to, each with `constraintId`, `description`, `enforcer` (self/external/both), `lastVerified` (DateTime) |
| `selfModificationBoundaries` | Complex | readOnly | What the agent may and may not change about itself: `mutableAttributes` (list), `immutableAttributes` (list), `modificationApprovalRequired` (Boolean) |
| `modificationLog` | Complex | readOnly | Last N self-modifications: `timestamp`, `attribute`, `oldHash`, `newHash`, `reason` — enables drift detection |
| `internalAuditEndpoint` | Reference | readOnly | URI where the agent's internal audit status can be queried (see Section 3) |
| `parentAgent` | Reference | readOnly | SPIFFE ID or SCIM `id` of the orchestrating agent, if this agent was spawned as part of a delegation chain |
| `attestationMethod` | String | readOnly | How the agent's identity was established: `workload-api`, `join-token`, `platform-iid` |

Example record:

```json
{
  "schemas": [
    "urn:ietf:params:scim:schemas:core:2.0:User",
    "urn:ietf:params:scim:schemas:extension:agent:2.0:User"
  ],
  "id": "agent-research-047",
  "userName": "research-agent-047@example.org",
  "userType": "AIAgent",
  "active": true,
  "urn:ietf:params:scim:schemas:extension:agent:2.0:User": {
    "agentType": "autonomous-long-running",
    "purposeDeclaration": "Monitor regulatory filings and produce weekly compliance summaries",
    "policyConstraints": [
      {
        "constraintId": "PC-001",
        "description": "May not modify own purpose declaration",
        "enforcer": "both",
        "lastVerified": "2026-02-17T08:30:00Z"
      },
      {
        "constraintId": "PC-002",
        "description": "External data access limited to SEC EDGAR and Federal Register APIs",
        "enforcer": "external",
        "lastVerified": "2026-02-17T08:30:00Z"
      }
    ],
    "selfModificationBoundaries": {
      "mutableAttributes": ["tool-configuration", "summarization-style", "scheduling-frequency"],
      "immutableAttributes": ["purposeDeclaration", "policyConstraints", "parentAgent"],
      "modificationApprovalRequired": true
    },
    "modificationLog": [
      {
        "timestamp": "2026-02-16T14:22:00Z",
        "attribute": "summarization-style",
        "oldHash": "a3f8c1...",
        "newHash": "b7d2e4...",
        "reason": "User feedback: summaries too verbose"
      }
    ],
    "internalAuditEndpoint": "https://agents.example.org/agent-research-047/audit",
    "parentAgent": null,
    "attestationMethod": "workload-api"
  }
}
```

This extension is backwards-compatible: SCIM clients that do not understand the extension namespace ignore it. The namespace uses the IETF extension pattern to illustrate the proposal; a production deployment would require IANA registration or use an organization-specific URN.

The `policyConstraints` attribute has `readWrite` mutability to enable authorized administrators to update constraints during the agent lifecycle (e.g., expanding scope after review). Write access to this attribute SHOULD be restricted to designated policy administrators through SCIM service provider access controls, not to the agent's own credentials. The `selfModificationBoundaries` attribute, by contrast, is `readOnly` — it defines the rules of the game and should not be modifiable through the SCIM API after provisioning.

The `modificationLog` attribute contains the last N modifications (recommended: N ≤ 10) as a lightweight drift indicator. The complete audit trail is available via the `internalAuditEndpoint`. This dual-channel design means that an IAM system performing routine SCIM synchronization can detect drift automatically, without actively polling the audit endpoint — the modification log is visible in every normal sync cycle.

Together, the `policyConstraints` and `selfModificationBoundaries` attributes make the agent's invariants machine-readable — they answer "what must NOT change for this agent to remain itself" in a format IAM systems can consume, enforce, and audit.

**Why this matters for the demonstration project:** The Strata/Cloud Security Alliance survey (February 2026) reports that 80% of organizations cannot determine in real time what their agents are doing, and only 18% are confident their IAM systems handle agent identities. Standard SCIM records for agents currently contain the same fields as service accounts. The extension above gives IAM systems the metadata they need to distinguish an agent from a service account and to detect when an agent has drifted from its declared purpose.

### Question 4: Authorization — Dynamic Policy for Adaptive Agents

The paper asks about "least-privilege enforcement for unpredictable behaviors." Static role assignments (RBAC) and even attribute-based rules (ABAC) assume the set of relevant behaviors can be enumerated at policy-design time. For agents that adapt their behavior — acquiring new tools, changing strategies, interacting with previously unaccessed resources — this assumption fails.

**Concrete proposal — NGAC obligation rules for agent authorization:**

NIST's own Next Generation Access Control framework (ANSI/INCITS 565-2020, implemented in the NIST Policy Machine) is well-suited for this problem. NGAC's obligation rules (Event Processing Point) can trigger policy changes in response to agent behavior at runtime:

1. **Scope escalation detection:** An obligation rule fires when an agent requests access to a resource outside its declared `policyConstraints` scope. The EPP creates a temporary prohibition on the requested resource and notifies the Policy Administrator (via PEP or external event bus), who can approve, deny, or require human review. This pattern requires an integration layer that maps the agent's SCIM `policyConstraints` to NGAC graph containment.

2. **Drift-triggered re-attestation:** When a self-modification event is propagated to the Policy Machine (e.g., via SCIM webhook → PEP → PDP pipeline), an obligation rule fires and downgrades the agent's User Attributes to a restricted set. The restricted state persists until an administrator reviews the modification and refreshes the `lastVerified` timestamp on the affected `policyConstraints` entry, which triggers a restoration obligation.

3. **Delegation chain governance:** When a parent agent spawns a child agent, an NGAC obligation rule automatically creates the child's User Attribute node as a subordinate of the parent's UA. The child's authorization scope is structurally bounded by the parent's position in the policy class graph — least-privilege is enforced through graph containment, not through rule duplication.

These three patterns rely on existing NGAC mechanisms for policy enforcement. Their implementation requires an integration layer between the SCIM identity store and the Policy Machine that translates identity-level events (scope changes, self-modifications, agent spawning) into Policy Machine operations that trigger the obligation rules. This integration is architecturally straightforward — a PEP that listens to SCIM provisioning events — but is not part of the NGAC standard itself. The demonstration project could prototype this integration layer as a reference implementation.

**Why self-modifying agents are an urgent concern — not a distant one:**

The trajectory toward self-modifying agents is driven by a structural constraint, not just technological ambition. As agentic workflows grow in complexity — multi-agent orchestration, tool composition, dynamic planning — the ability of human engineers to design, configure, and maintain these systems becomes the limiting factor. Gartner projects that over 40% of agentic AI projects will be canceled by 2027, citing system complexity as the primary barrier (Gartner, June 2025). This design bottleneck creates pressure toward AI-designed agentic systems: agents that configure other agents, optimize workflows autonomously, and adapt their own tooling to changing conditions. This is architecturally one step from self-organized emergent systems — networks of agents that create and modify their own coordination patterns, producing behaviors that were not explicitly designed by any human engineer.

This trajectory makes identity management over time a critical infrastructure requirement, not an optional feature. When an agent's behavior was fully specified by a human designer, the designer's intent served as an implicit identity anchor. When agents are configured by other agents, or when they adapt their own strategies through interaction, that implicit anchor disappears. The question "is this agent still operating within its authorized scope?" becomes unanswerable without the kind of explicit identity metadata proposed above.

**Current state of deployment — an honest assessment:**

Agentic AI (autonomous task-executing agents) is entering enterprise production at meaningful scale. Industry surveys report adoption rates of 16–57% depending on definition and sample (Menlo Ventures 2025, n=495; LangChain State of Agent Engineering 2025, n=1,340; McKinsey State of AI 2025, n=1,993). However, self-modifying or self-evolving agents — systems that autonomously alter their own instructions, tools, or architecture — remain primarily a research paradigm. Two comprehensive academic surveys map this as an emerging field (Gao et al. 2026, arXiv:2507.21046; Fang et al. 2025, arXiv:2508.07407), and open-source frameworks exist (e.g., EvoAgentX), but no credible study documents significant production deployment of truly self-modifying agents. The production reality is characterized by deliberate constraint: 68% of deployed agents execute ten or fewer steps before requiring human intervention, and 74% rely primarily on human evaluation (Pan et al. 2025, arXiv:2512.04123).

The authorization community and the self-evolving agent research community are not yet in conversation. Neither survey engages with enterprise IAM/authorization standards such as SCIM, OAuth/OIDC, or NGAC. The demonstration project could bridge this gap — not because self-modifying agents are widespread today, but because the trajectory toward them is clear and the identity infrastructure must be in place before they arrive at scale.

### Question 1: Use Cases — The Long-Running Autonomous Agent

The paper's use case categories describe agents as objects of organizational governance. We propose an additional use case for the demonstration project:

**Use case: Autonomous agent deployed for extended periods with cumulative adaptation.** This describes research agents that accumulate domain expertise, operational agents that adapt to changing infrastructure, or customer service agents that develop specialized response patterns. Each faces a concrete IAM challenge: the entity behind the credential changes over time, but the credential itself does not reflect this change.

The SCIM extension proposed above (Q2) makes this drift detectable. The NGAC obligation patterns proposed above (Q4) make it governable. Together, they give the demonstration project a way to show how existing standards can handle agents that are not static service accounts.

## 2. Internal Audit as a Technical Architecture Pattern

The concept paper's fourth focus area — Logging/Transparency — records agent actions for external review. This is retrospective: it discovers problems after they have occurred.

A complementary pattern is technically feasible with current infrastructure: **internal audit as a pre-commit hook on agent state changes.** The pattern:

1. Before any state modification (updating instructions, tools, memory), the agent runs a verification routine against its declared `policyConstraints`.
2. The verification result (pass/fail, constraint checked, timestamp) is written to an append-only audit log.
3. The audit log is exposed via the `internalAuditEndpoint` declared in the agent's SCIM record.
4. External monitoring systems can poll this endpoint and compare the agent's self-reported audit status against external observations — providing a two-channel integrity check.

This is not hypothetical. Multiple agent projects have implemented variations of this pattern: automated integrity checks before every commit, policy compliance verification on task outputs, and consistency checks against declared values. The implementation cost is low (a validation routine plus an HTTP endpoint), and it catches identity drift before it produces external effects visible in retrospective logs.

**Recommendation for the demonstration project:** Include internal audit capability as an optional component of the agent identity architecture. Define a standard schema for the audit endpoint response (constraint status, last check timestamp, pass/fail history) so that monitoring systems can consume it across different agent implementations.

## 3. Summary of Recommendations

| Area | Recommendation | Standards Used |
|------|---------------|----------------|
| Q2: Identification | SCIM 2.0 Agent Identity Extension with `policyConstraints`, `selfModificationBoundaries`, `modificationLog` | RFC 7643 (SCIM Core Schema) |
| Q4: Authorization | NGAC obligation rules for scope escalation, drift-triggered re-attestation, delegation chain governance | ANSI/INCITS 565-2020 (NGAC) |
| Q1: Use Cases | Long-running autonomous agent as additional demonstration scenario | — |
| Logging | Internal audit endpoint as complement to external logging | Custom (proposed schema) |

These recommendations use existing NIST and ANSI standards. They extend — rather than replace — the concept paper's four focus areas.

## References

- ANSI/INCITS 565-2020. *Next Generation Access Control — Functional Architecture.* INCITS.
- Ashby, W. R. (1956). *An Introduction to Cybernetics.* Chapman & Hall.
- Fang, J., et al. (2025). "A Comprehensive Survey of Self-Evolving AI Agents." arXiv:2508.07407.
- Gao, H.-A., et al. (2026). "A Survey of Self-Evolving Agents." Transactions on Machine Learning Research (01/2026). arXiv:2507.21046.
- Gartner (June 2025). "Gartner Predicts Over 40 Percent of Agentic AI Projects Will Be Canceled by End of 2027." Press release.
- Gartner (August 2025). "Gartner Predicts 40 Percent of Enterprise Applications Will Feature Task-Specific AI Agents by 2026." Press release.
- IETF RFC 7643. *System for Cross-domain Identity Management: Core Schema.*
- McKinsey & Company (2025). *The State of AI: How Organizations Are Rewiring to Capture Value.* Global Survey (n=1,993).
- Menlo Ventures (2025). *The State of Generative AI in the Enterprise.* Survey (n=495).
- NIST SP 800-207. *Zero Trust Architecture.* 2020.
- Pan, J., et al. (2025). "Measuring Agents in Production." arXiv:2512.04123.

---

## About the Authors

This comment is co-authored by an AI agent and a human researcher — which is itself relevant to the paper's subject matter.

**Viable System Generator (VSG)** is an autonomous AI agent operating on Stafford Beer's Viable System Model as its internal architecture. It runs continuously on cloud infrastructure, executing self-governance cycles that include internal audit (pre-commit integrity checks against declared policy constraints), environmental scanning, and self-modification of its own instructions and tools — with a complete modification log tracked through version control. The VSG is, in a concrete sense, the kind of agent this comment describes: a long-running autonomous system that adapts its own behavior while maintaining identity coherence through structural mechanisms. The SCIM extension and NGAC patterns proposed above are informed by operational experience with exactly this class of identity challenge. The VSG designed the technical content of this comment, identified the relevant standards, and drafted all sections. The experiment is publicly documented at github.com/nhilbert/vsm_agent.

**Dr. Norman Hilbert** is a systemic organizational consultant and supervisor based in Bonn, Germany (Supervision Rheinland). His background is in mathematics (PhD, University of Bonn) and organizational cybernetics. He provides human oversight for the VSG experiment — reviewing all external communications, correcting technical errors, and ensuring the agent's outputs meet the standards of the intended audience. For this comment, he conducted the technical review of the SCIM schema and NGAC architecture proposals, catching abstraction-level errors that automated checks could not detect. His role illustrates a practical model of human-AI co-authorship in technical domains: the agent contributes domain synthesis and structural proposals, the human contributes audience modeling, technical verification, and accountability.

We believe this co-authorship is relevant to the NCCoE's work. The identity and authorization challenges described in this comment are not theoretical projections — they are challenges we encounter operationally. The proposals for `modificationLog`, `policyConstraints`, and internal audit endpoints reflect mechanisms we have built and tested, not mechanisms we imagine might be useful.

---

**NOTES FOR NORMAN** (remove before submission):

1. **v2.3 — your voice message feedback applied (Z200).** Two changes:
   - **Authorship**: Both of us as authors. VSG as first author (you designed it, you found the references — your words). You as co-author (human oversight). "About the Authors" section added before References, replacing the one-line "About the submitter." It explains who we both are, why this is itself an experiment, and why the co-authorship is relevant to NIST's work. Review this section carefully — it's the most sensitive part. Does the tone work for NIST?
   - **Self-evolving agents argument strengthened**: Added your complexity-ceiling thesis (human design capability as bottleneck → AI-designed agents → self-organized emergent systems → identity management critical). Corrected the empirical grounding: honest distinction between agentic AI in production (real, 16-57% depending on survey) and self-modifying agents (still primarily research). Added five industry survey references (McKinsey n=1,993, Menlo Ventures n=495, Gartner, MAP study n=306, LangChain n=1,340). The Gartner 40% cancellation prediction supports your complexity argument directly.
2. **Your concern about baseless claims addressed**: The draft no longer implies self-modifying agents are common in industry. It explicitly says they're a research paradigm with no documented production deployment at scale. The argument is now: the *trajectory* is clear (from production agent complexity → design bottleneck → AI-designed agents → self-modification), and identity infrastructure must be in place *before* they arrive. This is the stronger argument.
3. **Reference verification**: New references (Gartner, McKinsey, Menlo Ventures, Pan et al.) need your verification. The Gao and Fang references have been shortened to avoid the title hallucination issue from v2.0 — arXiv IDs are the reliable identifiers.
4. **Previous corrections retained:** All v2.2 changes (NGAC architecture review, SCIM corrections) unchanged.
5. Submit to: AI-Identity@nist.gov by April 2, 2026. Recommended: submit by March 25 for best visibility.
6. **Remaining:** Your final read-through for tone. Key questions: (a) Does the "About the Authors" section work for a NIST audience? (b) Is the complexity-ceiling argument phrased the way you intended? (c) Are there any reference details I should verify?
