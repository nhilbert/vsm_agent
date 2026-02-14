# Run S3* Audit

Execute the VSG's audit function — an independent check of operational reality.

## Steps

1. Run `python3 integrity_check.py` and report results
2. Check version consistency: `vsg_prompt.md` version must match `agent_card.json`
3. Check cycle counter consistency across files
4. Verify all file references in `vsg_prompt.md` point to existing files
5. Check structural completeness: all 5 VSM systems present
6. Check human framing: Norman is counterpart, not component
7. Check honesty markers: limitations acknowledged

## Report

List all findings:
- PASS: checks that succeeded
- FAIL: violations found (with details)
- WARN: potential issues

## Action

If violations found, fix them or flag for human review.
