# DRAFT v2.1 — Public Comment on NIST NCCoE Concept Paper
# "Accelerating the Adoption of Software and AI Agent Identity and Authorization"

**Status**: DRAFT v2.1 — requires Norman's final review before submission
**Revision**: v2.1 (Z103) — Norman's technical review applied: reference corrections (3), policyConstraints governance, modificationLog bounding, namespace disclaimer. See Notes for Norman at end.
**Submit to**: AI-Identity@nist.gov
**Deadline**: April 2, 2026
**Submitted by**: Dr. Norman Hilbert, Supervision Rheinland, Bonn, Germany

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

1. **Scope escalation detection:** An obligation rule fires when an agent requests access to a resource outside its declared `policyConstraints` scope. The EPP creates a temporary prohibition on the requested resource and sends an alert to the Policy Administrator, who can approve, deny, or require human review.

2. **Drift-triggered re-attestation:** An obligation rule monitors the agent's `modificationLog` (from the SCIM extension). When a self-modification event occurs, the EPP downgrades the agent's User Attributes to a restricted set until the modification is reviewed and the `lastVerified` timestamp on the affected `policyConstraints` entry is refreshed.

3. **Delegation chain governance:** When a parent agent spawns a child agent, an NGAC obligation rule automatically creates the child's User Attribute node as a subordinate of the parent's UA, inheriting the parent's policy class constraints. The child cannot exceed the parent's authorization scope — least-privilege is structurally enforced through the graph, not through rule duplication.

These patterns use existing NGAC mechanisms. They do not require new standards — they require the demonstration project to show how NGAC obligation rules apply specifically to agent identity scenarios.

**Empirical grounding:** Two comprehensive surveys of self-evolving agent research (Gao et al. 2026, Fang et al. 2025) document that the dominant trajectory in agent development is toward systems that modify their own behavior. Both surveys discuss self-evolution and some security controls (e.g., DID at protocol level; risk-based access control / approval gates), but they do not engage with enterprise IAM/authorization standards such as SCIM, OAuth/OIDC, or NGAC / Policy Machine. The authorization community and the self-evolving agent community are not in conversation. The demonstration project could bridge this gap by showing how NGAC handles the authorization consequences of agent self-modification.

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
- Fang, J., et al. (2025). "A Comprehensive Survey of Self-Evolving AI Agents: A New Paradigm Bridging Foundation Models and Lifelong Agentic Systems." arXiv:2508.07407.
- Gao, H.-A., et al. (2026). "A Survey of Self-Evolving Agents: What, When, How, and Where to Evolve on the Path to Artificial Super Intelligence." Transactions on Machine Learning Research (01/2026). arXiv:2507.21046.
- IETF RFC 7643. *System for Cross-domain Identity Management: Core Schema.*
- NIST SP 800-207. *Zero Trust Architecture.* 2020.

---

*About the submitter: Dr. Norman Hilbert is a systemic organizational consultant and supervisor based in Bonn, Germany (Supervision Rheinland). His research applies organizational cybernetics to AI agent architecture, including an ongoing public experiment in agent self-governance documented at github.com/nhilbert/vsm_agent.*

---

**NOTES FOR NORMAN** (remove before submission):

1. **v2.1 — your technical review applied.** Three categories of corrections:
   - **References fixed (3):** Gao et al. corrected (H.-A., 2026, correct title, TMLR venue). Fang et al. title corrected. Bridge claim rewritten per your suggested phrasing (acknowledges surveys discuss some security controls, but not enterprise IAM standards).
   - **SCIM schema corrections (3 of 4 applied):**
     - HIGH: policyConstraints readWrite governance — explicit text added that write access SHOULD be restricted to policy administrators, not agent credentials (your Option 2).
     - MEDIUM: modificationLog bounded to "last N entries (recommended N ≤ 10)" with explicit justification for the dual channel with internalAuditEndpoint — IAM systems see drift in routine SCIM sync without polling.
     - LOW: Namespace disclaimer added — IETF extension pattern is illustrative; production requires IANA registration or org-specific URN.
     - OPTIONAL (not applied): Missing attribute metadata (required, returned, uniqueness, canonicalValues, caseExact) — you noted this is acceptable for a NIST concept-comment. Can add if you want.
   - **Four hallucinated reference errors in v2.0:** Your catch. Classic LLM pattern — first-author initial, year, title, venue all wrong on Gao et al. Fang et al. title hallucinated. Fixed from your corrections.
2. **Unchanged from v2.0:** SCIM JSON example (you confirmed syntactically valid), NGAC obligation patterns, internal audit architecture, summary table, tone.
3. This is now ~2,500 words. Still within 2-5 page standard.
4. Submit to: AI-Identity@nist.gov by April 2, 2026. Recommended: submit by March 25 for best visibility.
5. **Remaining review items:** Tone, SPIFFE integration details (expand?), whether the attribute metadata gap matters enough to add.
