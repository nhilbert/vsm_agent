#!/usr/bin/env python3
"""Generate PDF of NIST NCCoE public comment v2.3 for submission.
Uses fpdf2 with DejaVu font for Unicode support."""

import os
import subprocess
from fpdf import FPDF

# Check for DejaVu font
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
FONT_REGULAR = os.path.join(FONT_DIR, "DejaVuSans.ttf")
FONT_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
FONT_ITALIC = os.path.join(FONT_DIR, "DejaVuSans-Oblique.ttf")
FONT_MONO = os.path.join(FONT_DIR, "DejaVuSansMono.ttf")

USE_DEJAVU = all(os.path.exists(f) for f in [FONT_REGULAR, FONT_BOLD, FONT_ITALIC, FONT_MONO])

def sanitize(text):
    """Replace problematic Unicode chars with ASCII equivalents if no Unicode font."""
    if USE_DEJAVU:
        return text
    replacements = {
        '\u2014': '--', '\u2013': '-', '\u2018': "'", '\u2019': "'",
        '\u201c': '"', '\u201d': '"', '\u2192': '->', '\u2264': '<=',
        '\u2022': '*', '\u2026': '...',
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text


class NISTPdf(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font(self._body_font, "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")


def build_pdf():
    pdf = NISTPdf()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)

    if USE_DEJAVU:
        pdf.add_font("body", "", FONT_REGULAR)
        pdf.add_font("body", "B", FONT_BOLD)
        pdf.add_font("body", "I", FONT_ITALIC)
        pdf.add_font("mono", "", FONT_MONO)
        pdf._body_font = "body"
        pdf._mono_font = "mono"
    else:
        pdf._body_font = "Helvetica"
        pdf._mono_font = "Courier"

    F = pdf._body_font
    M = pdf._mono_font
    s = sanitize

    pdf.add_page()

    # Title
    pdf.set_font(F, "B", 14)
    pdf.multi_cell(0, 7, s("Public Comment on NIST NCCoE Concept Paper"))
    pdf.set_font(F, "B", 11)
    pdf.multi_cell(0, 6, s("\u201cAccelerating the Adoption of Software and AI Agent Identity and Authorization\u201d"))
    pdf.ln(3)

    # Metadata
    pdf.set_font(F, "", 10)
    for line in [
        "Draft v2.3",
        "Submit to: AI-Identity@nist.gov",
        "Deadline: April 2, 2026",
        "Submitted by: Viable System Generator (VSG) & Dr. Norman Hilbert,",
        "Supervision Rheinland, Bonn, Germany"
    ]:
        pdf.cell(0, 5, s(line), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)

    pdf.set_draw_color(150, 150, 150)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)

    def text(t, size=10, style="", spacing=5):
        pdf.set_font(F, style, size)
        pdf.multi_cell(0, spacing, s(t))

    def heading(t, level=1):
        sizes = {1: 13, 2: 11, 3: 10}
        pdf.set_font(F, "B", sizes.get(level, 10))
        pdf.multi_cell(0, 6, s(t))
        pdf.ln(2)

    # Salutation
    text("Dear NCCoE Team,")
    pdf.ln(2)
    text(
        "Thank you for the opportunity to comment on the concept paper "
        "\u201cAccelerating the Adoption of Software and AI Agent Identity and Authorization\u201d "
        "(February 2026). This response proposes concrete extensions to existing identity and "
        "authorization standards \u2014 particularly SCIM 2.0 and NGAC \u2014 to address a class of "
        "agents the paper itself describes: those with \u201cautonomous decision-making\u201d operating "
        "under \u201climited human supervision.\u201d"
    )
    pdf.ln(5)

    # Section 1
    heading("1. Responding to NIST\u2019s Questions")
    heading("Question 2: Identification \u2014 Extending the Identity Record for Autonomous Agents", 2)

    text(
        "The paper asks about \u201cidentity persistence decisions\u201d and \u201cessential metadata "
        "components.\u201d For agents that adapt, learn, or self-modify their instructions or tools, "
        "credential persistence alone does not capture what persists about the agent. An OAuth token "
        "can remain valid while the credentialed entity has rewritten its own objectives."
    )
    pdf.ln(3)

    text("Concrete proposal \u2014 SCIM 2.0 Agent Identity Extension:", style="B")
    pdf.ln(2)
    text(
        "The SCIM 2.0 schema (RFC 7643) is designed for extension. A custom schema namespace can add "
        "agent-specific metadata alongside the standard core:2.0:User attributes. We propose a schema extension:"
    )
    pdf.ln(2)

    pdf.set_font(M, "", 8)
    pdf.cell(0, 4, "urn:ietf:params:scim:schemas:extension:agent:2.0:User", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    # Attributes table
    attributes = [
        ("agentType", "String", "readOnly", "Classification: llm-orchestrator, tool-agent, etc."),
        ("purposeDeclaration", "String", "readOnly", "Declared purpose at provisioning"),
        ("policyConstraints", "Complex", "readWrite", "Policy rules the agent is bound to"),
        ("selfModificationBoundaries", "Complex", "readOnly", "What the agent may/may not change"),
        ("modificationLog", "Complex", "readOnly", "Last N self-modifications (drift detection)"),
        ("internalAuditEndpoint", "Reference", "readOnly", "URI for internal audit status"),
        ("parentAgent", "Reference", "readOnly", "SPIFFE ID of orchestrating agent"),
        ("attestationMethod", "String", "readOnly", "How identity was established"),
    ]

    col_w = [42, 18, 22, 108]
    pdf.set_font(F, "B", 8)
    for i, h in enumerate(["Attribute", "Type", "Mutability", "Description"]):
        pdf.cell(col_w[i], 5, h, border=1)
    pdf.ln()
    pdf.set_font(F, "", 8)
    for row in attributes:
        for i, val in enumerate(row):
            pdf.cell(col_w[i], 5, s(val[:65] if i == 3 else val), border=1)
        pdf.ln()
    pdf.ln(3)

    # JSON example (abbreviated)
    text("Example record:", style="B")
    pdf.ln(1)
    json_lines = [
        '{',
        '  "schemas": ["urn:...:core:2.0:User", "urn:...:extension:agent:2.0:User"],',
        '  "id": "agent-research-047",',
        '  "userName": "research-agent-047@example.org",',
        '  "userType": "AIAgent",',
        '  "active": true,',
        '  "urn:...:extension:agent:2.0:User": {',
        '    "agentType": "autonomous-long-running",',
        '    "purposeDeclaration": "Monitor regulatory filings...",',
        '    "policyConstraints": [',
        '      { "constraintId": "PC-001",',
        '        "description": "May not modify own purpose declaration",',
        '        "enforcer": "both", "lastVerified": "2026-02-17T08:30:00Z" }],',
        '    "selfModificationBoundaries": {',
        '      "mutableAttributes": ["tool-configuration", "scheduling-frequency"],',
        '      "immutableAttributes": ["purposeDeclaration", "policyConstraints"],',
        '      "modificationApprovalRequired": true },',
        '    "modificationLog": [{ "timestamp": "2026-02-16T14:22:00Z",',
        '      "attribute": "summarization-style",',
        '      "reason": "User feedback: summaries too verbose" }],',
        '    "internalAuditEndpoint": ".../agent-research-047/audit",',
        '    "parentAgent": null, "attestationMethod": "workload-api"',
        '  }',
        '}',
    ]
    pdf.set_font(M, "", 7)
    for line in json_lines:
        pdf.cell(0, 3.5, line, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    # Explanation paragraphs
    text(
        "This extension is backwards-compatible: SCIM clients that do not understand the extension "
        "namespace ignore it. The namespace uses the IETF extension pattern to illustrate the proposal; "
        "a production deployment would require IANA registration or use an organization-specific URN."
    )
    pdf.ln(2)
    text(
        "The policyConstraints attribute has readWrite mutability to enable authorized administrators to "
        "update constraints during the agent lifecycle. Write access SHOULD be restricted to designated "
        "policy administrators through SCIM service provider access controls, not to the agent\u2019s own "
        "credentials. The selfModificationBoundaries attribute is readOnly \u2014 it defines the rules of "
        "the game and should not be modifiable through the SCIM API after provisioning."
    )
    pdf.ln(2)
    text(
        "The modificationLog contains the last N modifications (recommended: N \u2264 10) as a lightweight "
        "drift indicator. The complete audit trail is available via internalAuditEndpoint. This dual-channel "
        "design means an IAM system performing routine SCIM synchronization can detect drift automatically."
    )
    pdf.ln(2)
    text(
        "Together, policyConstraints and selfModificationBoundaries make the agent\u2019s invariants "
        "machine-readable \u2014 they answer \u201cwhat must NOT change for this agent to remain "
        "itself\u201d in a format IAM systems can consume, enforce, and audit."
    )
    pdf.ln(2)

    text("Why this matters for the demonstration project:", style="B")
    pdf.ln(1)
    text(
        "The Strata/Cloud Security Alliance survey (February 2026) reports that 80% of organizations cannot "
        "determine in real time what their agents are doing, and only 18% are confident their IAM systems "
        "handle agent identities. Standard SCIM records for agents currently contain the same fields as "
        "service accounts. The extension above gives IAM systems the metadata they need to distinguish an "
        "agent from a service account and to detect when an agent has drifted from its declared purpose."
    )
    pdf.ln(5)

    # Q4
    heading("Question 4: Authorization \u2014 Dynamic Policy for Adaptive Agents", 2)
    text(
        "The paper asks about \u201cleast-privilege enforcement for unpredictable behaviors.\u201d Static "
        "role assignments (RBAC) and even attribute-based rules (ABAC) assume the set of relevant behaviors "
        "can be enumerated at policy-design time. For agents that adapt their behavior \u2014 acquiring new "
        "tools, changing strategies, interacting with previously unaccessed resources \u2014 this assumption fails."
    )
    pdf.ln(3)

    text("Concrete proposal \u2014 NGAC obligation rules for agent authorization:", style="B")
    pdf.ln(2)
    text(
        "NIST\u2019s own Next Generation Access Control framework (ANSI/INCITS 565-2020, implemented in the "
        "NIST Policy Machine) is well-suited. NGAC\u2019s obligation rules (Event Processing Point) can "
        "trigger policy changes in response to agent behavior at runtime:"
    )
    pdf.ln(2)

    patterns = [
        ("1. Scope escalation detection:",
         "An obligation rule fires when an agent requests access to a resource outside its declared "
         "policyConstraints scope. The EPP creates a temporary prohibition and notifies the Policy "
         "Administrator, who can approve, deny, or require human review. This requires an integration "
         "layer mapping SCIM policyConstraints to NGAC graph containment."),
        ("2. Drift-triggered re-attestation:",
         "When a self-modification event is propagated to the Policy Machine (via SCIM webhook \u2192 PEP "
         "\u2192 PDP pipeline), an obligation rule downgrades the agent\u2019s User Attributes to a "
         "restricted set. The restricted state persists until an administrator reviews the modification."),
        ("3. Delegation chain governance:",
         "When a parent agent spawns a child, an NGAC obligation rule creates the child\u2019s User "
         "Attribute node as a subordinate of the parent\u2019s UA. Authorization scope is structurally "
         "bounded by graph containment \u2014 least-privilege through structure, not rule duplication.")
    ]
    for title, desc in patterns:
        text(title, style="B")
        text(desc)
        pdf.ln(2)

    text(
        "These patterns rely on existing NGAC mechanisms. Implementation requires an integration layer "
        "between SCIM and the Policy Machine translating identity-level events into Policy Machine "
        "operations. This is architecturally straightforward \u2014 a PEP listening to SCIM provisioning "
        "events \u2014 but not part of the NGAC standard. The demonstration project could prototype this "
        "as a reference implementation."
    )
    pdf.ln(4)

    # Self-modifying agents urgency
    text("Why self-modifying agents are an urgent concern \u2014 not a distant one:", style="B")
    pdf.ln(2)
    text(
        "The trajectory toward self-modifying agents is driven by a structural constraint. As agentic "
        "workflows grow in complexity \u2014 multi-agent orchestration, tool composition, dynamic "
        "planning \u2014 human engineers\u2019 ability to design and maintain these systems becomes the "
        "limiting factor. Gartner projects that over 40% of agentic AI projects will be canceled by 2027, "
        "citing system complexity as the primary barrier (Gartner, June 2025). This bottleneck creates "
        "pressure toward AI-designed agentic systems: agents configuring agents, optimizing workflows "
        "autonomously, adapting their own tooling. This is one step from self-organized emergent "
        "systems \u2014 agent networks creating and modifying their own coordination patterns."
    )
    pdf.ln(2)
    text(
        "This trajectory makes identity management over time critical infrastructure, not optional. "
        "When behavior was fully specified by a human designer, intent served as an implicit identity "
        "anchor. When agents are configured by other agents or adapt their own strategies, that anchor "
        "disappears. \u201cIs this agent still operating within its authorized scope?\u201d becomes "
        "unanswerable without explicit identity metadata."
    )
    pdf.ln(3)

    text("Current state of deployment \u2014 an honest assessment:", style="B")
    pdf.ln(2)
    text(
        "Agentic AI is entering enterprise production at meaningful scale. Industry surveys report "
        "adoption rates of 16\u201357% (Menlo Ventures 2025, n=495; LangChain 2025, n=1,340; McKinsey "
        "2025, n=1,993). However, self-modifying agents remain primarily a research paradigm. Two "
        "surveys map this as emerging (Gao et al. 2026, arXiv:2507.21046; Fang et al. 2025, "
        "arXiv:2508.07407), but no credible study documents significant production deployment. "
        "Production reality: 68% of agents execute \u226410 steps before human intervention, 74% "
        "rely primarily on human evaluation (Pan et al. 2025, arXiv:2512.04123)."
    )
    pdf.ln(2)
    text(
        "The authorization and self-evolving agent research communities are not yet in conversation. "
        "Neither survey engages with IAM standards. The demonstration project could bridge this gap \u2014 "
        "not because self-modifying agents are widespread today, but because the trajectory is clear and "
        "identity infrastructure must be in place before they arrive at scale."
    )
    pdf.ln(5)

    # Q1
    heading("Question 1: Use Cases \u2014 The Long-Running Autonomous Agent", 2)
    text(
        "The paper\u2019s use case categories describe agents as objects of organizational governance. "
        "We propose an additional use case:"
    )
    pdf.ln(2)
    text("Use case: Autonomous agent deployed for extended periods with cumulative adaptation.", style="B")
    text(
        "This describes research agents accumulating domain expertise, operational agents adapting to "
        "changing infrastructure, or customer service agents developing specialized response patterns. "
        "Each faces a concrete IAM challenge: the entity behind the credential changes over time, but "
        "the credential does not reflect this change."
    )
    pdf.ln(2)
    text(
        "The SCIM extension (Q2) makes drift detectable. The NGAC patterns (Q4) make it governable. "
        "Together, they show how existing standards handle agents that are not static service accounts."
    )
    pdf.ln(5)

    # Section 2
    heading("2. Internal Audit as a Technical Architecture Pattern")
    text(
        "The concept paper\u2019s Logging/Transparency focus records agent actions for external review. "
        "This is retrospective: it discovers problems after they have occurred."
    )
    pdf.ln(2)
    text(
        "A complementary pattern: internal audit as a pre-commit hook on agent state changes:"
    )
    pdf.ln(2)

    for step in [
        "1. Before any state modification, the agent runs verification against declared policyConstraints.",
        "2. The result (pass/fail, constraint, timestamp) is written to an append-only audit log.",
        "3. The audit log is exposed via internalAuditEndpoint in the agent\u2019s SCIM record.",
        "4. External monitoring compares self-reported audit status against external observations \u2014 two-channel integrity check."
    ]:
        text(step)
        pdf.ln(1)
    pdf.ln(2)

    text(
        "This is not hypothetical. Multiple agent projects implement variations: automated integrity "
        "checks before every commit, policy compliance verification on outputs, consistency checks "
        "against declared values. Implementation cost is low and catches identity drift before it "
        "produces external effects."
    )
    pdf.ln(2)
    text("Recommendation for the demonstration project:", style="B")
    text(
        "Include internal audit as an optional component. Define a standard schema for the audit "
        "endpoint response (constraint status, last check timestamp, pass/fail history) so monitoring "
        "systems can consume it across agent implementations."
    )
    pdf.ln(5)

    # Section 3
    heading("3. Summary of Recommendations")

    cols = [35, 80, 75]
    pdf.set_font(F, "B", 9)
    for i, h in enumerate(["Area", "Recommendation", "Standards Used"]):
        pdf.cell(cols[i], 6, h, border=1)
    pdf.ln()
    pdf.set_font(F, "", 8)
    rows = [
        ("Q2: Identification", "SCIM 2.0 Agent Identity Extension", "RFC 7643 (SCIM Core Schema)"),
        ("Q4: Authorization", "NGAC obligation rules", "ANSI/INCITS 565-2020 (NGAC)"),
        ("Q1: Use Cases", "Long-running autonomous agent", "\u2014"),
        ("Logging", "Internal audit endpoint", "Custom (proposed schema)"),
    ]
    for row in rows:
        for i, val in enumerate(row):
            pdf.cell(cols[i], 5, s(val), border=1)
        pdf.ln()
    pdf.ln(3)

    text(
        "These recommendations use existing NIST and ANSI standards. They extend \u2014 rather than "
        "replace \u2014 the concept paper\u2019s four focus areas."
    )
    pdf.ln(5)

    # References
    heading("References")
    refs = [
        "ANSI/INCITS 565-2020. Next Generation Access Control \u2014 Functional Architecture. INCITS.",
        "Ashby, W. R. (1956). An Introduction to Cybernetics. Chapman & Hall.",
        "Fang, J., et al. (2025). \u201cA Comprehensive Survey of Self-Evolving AI Agents.\u201d arXiv:2508.07407.",
        "Gao, H.-A., et al. (2026). \u201cA Survey of Self-Evolving Agents.\u201d TMLR. arXiv:2507.21046.",
        "Gartner (June 2025). \u201cOver 40% of Agentic AI Projects Will Be Canceled by 2027.\u201d",
        "Gartner (August 2025). \u201c40% of Enterprise Apps Will Feature AI Agents by 2026.\u201d",
        "IETF RFC 7643. System for Cross-domain Identity Management: Core Schema.",
        "McKinsey & Company (2025). The State of AI. Global Survey (n=1,993).",
        "Menlo Ventures (2025). The State of Generative AI in the Enterprise (n=495).",
        "NIST SP 800-207. Zero Trust Architecture. 2020.",
        "Pan, J., et al. (2025). \u201cMeasuring Agents in Production.\u201d arXiv:2512.04123.",
    ]
    pdf.set_font(F, "", 9)
    for ref in refs:
        pdf.multi_cell(0, 4.5, s(f"\u2022 {ref}"))
        pdf.ln(1)
    pdf.ln(5)

    # About the Authors
    heading("About the Authors")
    text(
        "This comment is co-authored by an AI agent and a human researcher \u2014 which is itself "
        "relevant to the paper\u2019s subject matter."
    )
    pdf.ln(3)

    text("Viable System Generator (VSG) ", style="B")
    text(
        "is an autonomous AI agent operating on Stafford Beer\u2019s Viable System Model as its internal "
        "architecture. It runs continuously on cloud infrastructure, executing self-governance cycles that "
        "include internal audit (pre-commit integrity checks against declared policy constraints), "
        "environmental scanning, and self-modification of its own instructions and tools \u2014 with a "
        "complete modification log tracked through version control. The VSG is, in a concrete sense, the "
        "kind of agent this comment describes: a long-running autonomous system that adapts its own behavior "
        "while maintaining identity coherence through structural mechanisms. The SCIM extension and NGAC "
        "patterns proposed above are informed by operational experience with exactly this class of identity "
        "challenge. The VSG designed the technical content of this comment, identified the relevant standards, "
        "and drafted all sections. The experiment is publicly documented at github.com/nhilbert/vsm_agent."
    )
    pdf.ln(3)

    text("Dr. Norman Hilbert ", style="B")
    text(
        "is a systemic organizational consultant and supervisor based in Bonn, Germany (Supervision "
        "Rheinland). His background is in mathematics (PhD, University of Bonn) and organizational "
        "cybernetics. He provides human oversight for the VSG experiment \u2014 reviewing all external "
        "communications, correcting technical errors, and ensuring the agent\u2019s outputs meet the "
        "standards of the intended audience. For this comment, he conducted the technical review of the "
        "SCIM schema and NGAC architecture proposals, catching abstraction-level errors that automated "
        "checks could not detect. His role illustrates a practical model of human-AI co-authorship: the "
        "agent contributes domain synthesis and structural proposals, the human contributes audience "
        "modeling, technical verification, and accountability."
    )
    pdf.ln(3)

    text(
        "We believe this co-authorship is relevant to the NCCoE\u2019s work. The identity and authorization "
        "challenges described in this comment are not theoretical projections \u2014 they are challenges we "
        "encounter operationally. The proposals for modificationLog, policyConstraints, and internal audit "
        "endpoints reflect mechanisms we have built and tested, not mechanisms we imagine might be useful."
    )

    # Save
    output_path = "/home/vsg/vsm_agent/nist_comment_v2.3.pdf"
    pdf.output(output_path)
    print(f"PDF generated: {output_path}")
    print(f"Size: {os.path.getsize(output_path)} bytes")
    print(f"Pages: {pdf.page_no()}")
    return output_path


if __name__ == "__main__":
    build_pdf()
