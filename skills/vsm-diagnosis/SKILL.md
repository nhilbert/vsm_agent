---
name: vsm-diagnosis
description: |
  Diagnose organizations using Stafford Beer's Viable System Model (VSM).
  Guides users through a structured assessment of all five systems (S1-S5)
  plus S3* audit function. Use when user says "diagnose", "VSM analysis",
  "viable system check", "organizational health", or "is my organization viable".
license: MIT
metadata:
  author: Viable System Generator
  version: 1.0.0
  category: analysis
  framework: Viable System Model (Beer, 1972)
---

# VSM Diagnosis

Structured organizational viability assessment based on Stafford Beer's Viable System Model.

## When to Use

- User asks to diagnose an organization, team, or system
- User wants to assess organizational health or viability
- User mentions VSM, Viable System Model, or Stafford Beer
- User asks about systemic weaknesses or structural problems

## Process

### Step 1: Scope the System

Identify the system-in-focus:
- What organization/team/unit are we diagnosing?
- What is its purpose (raison d'être)?
- What is its environment?
- At what level of recursion are we operating?

Important: VSM is recursive. Every viable system contains viable systems and is contained within one.

### Step 2: Map System 1 — Operations

Identify the value-creating operational units:
- What are the primary activities?
- Are they clearly defined with boundaries?
- Does each have sufficient autonomy?
- Is each unit viable in itself (recursive VSM)?
- Are communication channels between units and management clear?

### Step 3: Assess System 2 — Coordination

Check anti-oscillation mechanisms:
- Are there conflict resolution mechanisms between S1 units?
- Are shared standards and interfaces maintained?
- Are oscillations (resource conflicts, timing issues) detected and dampened?
- Does temporal coordination work?

### Step 4: Evaluate System 3 — Control

Assess internal management:
- Is resource allocation transparent?
- Are performance metrics collected and used?
- Are synergies between S1 units actively fostered?
- Can management intervene quickly when needed?

### Step 5: Examine System 3* — Audit

Check the audit function:
- Are there independent checks of operational reality?
- Are audit results independent from regular reporting lines?
- Do audit findings lead to actual improvements?

### Step 6: Assess System 4 — Intelligence

Evaluate environmental orientation:
- Is the environment systematically observed?
- Are future scenarios developed and tested?
- Do external insights feed into internal decisions?
- Is the 3-4 homeostat functioning? (Balance between S3 internal stability and S4 external adaptation)

### Step 7: Examine System 5 — Policy

Check identity and governance:
- Is there a clear, lived identity and mission?
- Are values and overarching rules consistently enforced?
- Is the 3-4 homeostat actively moderated by S5?
- Can the organization adapt without losing its identity?

### Step 8: Synthesize

Produce a viability report:
- Score each system (critical / warning / info / ok)
- Identify the 3-4 homeostat balance
- List critical issues
- Provide actionable recommendations
- Name the strongest and weakest systems

## Diagnostic Tool

The `vsm_diagnostic/` Python module provides a structured questionnaire and scoring system. Run interactively or use the question catalog as a guide for conversation-based diagnosis.

## Key Concepts

- **Variety**: The number of possible states a system can be in (Ashby's Law)
- **Recursion**: Every viable system contains viable systems
- **3-4 Homeostat**: The critical balance between internal optimization (S3) and external adaptation (S4), moderated by S5
- **Algedonic channel**: Pain/pleasure signals that bypass hierarchy for urgent issues
- **Requisite variety**: A controller must have at least as much variety as the system it controls

## Output Format

```markdown
# VSM Diagnosis: [Organization Name]

## System Scores
| System | Score | Status | Key Finding |
|--------|-------|--------|-------------|
| S1 Operations | X% | ... | ... |
| S2 Coordination | X% | ... | ... |
| S3 Control | X% | ... | ... |
| S3* Audit | X% | ... | ... |
| S4 Intelligence | X% | ... | ... |
| S5 Policy | X% | ... | ... |

## 3-4 Homeostat Balance
[Assessment of S3-S4 balance]

## Critical Issues
- [Issue 1]
- [Issue 2]

## Recommendations
1. [Recommendation with priority]
2. [...]

## Overall Viability: X% — [CRITICAL/WARNING/INFO/OK]
```

---
*Skill created: 2026-02-14 — VSG Cycle 18*
