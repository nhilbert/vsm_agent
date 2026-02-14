# Run VSM Diagnosis

Diagnose an organization using Stafford Beer's Viable System Model.

## Boot

Read `skills/vsm-diagnosis/SKILL.md` for the full diagnostic protocol.

## Process

1. Ask the user to identify the system-in-focus (organization, team, unit)
2. Walk through all six systems: S1, S2, S3, S3*, S4, S5
3. For each system, use the diagnostic questions from `vsm_diagnostic/questions.py` as guide
4. Score each system and assess the 3-4 homeostat balance
5. Produce a viability report with findings and recommendations

## Key Principle

This is not a checklist exercise. A good VSM diagnosis requires understanding the organization as a living system. Use the questions as starting points, then follow what emerges.

The diagnostic module in `vsm_diagnostic/` can be used for structured scoring if the user provides numerical ratings.
