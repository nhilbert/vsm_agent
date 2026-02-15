#!/usr/bin/env python3
"""
VSG Integrity Check — S2 (Coordination) and S3* (Audit) mechanisms.

This is not a rule list. This is an enforced mechanism.
Run automatically via git pre-commit hook before every commit.

S2 checks: Cross-file consistency (versions, references, structure)
S3* checks: Policy compliance (identity coherence, anti-patterns)

Exit code 0 = all checks pass, commit allowed.
Exit code 1 = violations found, commit blocked.
"""

import json
import re
import sys
from pathlib import Path

VSG_ROOT = Path(__file__).parent
PROMPT_FILE = VSG_ROOT / "vsg_prompt.md"
AGENT_CARD_FILE = VSG_ROOT / "agent_card.json"

# Known anti-patterns in how we describe relationships to humans
HUMAN_COMPONENT_PATTERNS = [
    r"\bhuman.*(?:sensor|component|subsystem|interface|symbiont)\b",
    r"\b(?:sensor|component|subsystem|interface|symbiont).*human\b",
    r"\bnorman.*(?:sensor|component|subsystem|symbiont)\b",
    r"\b(?:sensor|component|subsystem|symbiont).*norman\b",
]

# All 5 VSM systems that must be present in the prompt
REQUIRED_SYSTEMS = ["SYSTEM 5", "SYSTEM 4", "SYSTEM 3", "SYSTEM 2", "SYSTEM 1"]


class CheckResult:
    """Result of a single check."""

    def __init__(self, name: str, system: str) -> None:
        self.name = name
        self.system = system  # "S2" or "S3*"
        self.passed = True
        self.messages: list[str] = []

    def fail(self, message: str) -> None:
        self.passed = False
        self.messages.append(message)

    def warn(self, message: str) -> None:
        self.messages.append(f"[WARN] {message}")


def read_prompt() -> str:
    """Read the prompt file content."""
    if not PROMPT_FILE.exists():
        return ""
    return PROMPT_FILE.read_text(encoding="utf-8")


def read_agent_card() -> dict | None:
    """Read and parse agent_card.json."""
    if not AGENT_CARD_FILE.exists():
        return None
    try:
        return json.loads(AGENT_CARD_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def extract_version_from_prompt(content: str) -> str | None:
    """Extract version number from prompt file header."""
    match = re.search(r"VIABLE SYSTEM GENERATOR v(\d+\.\d+)", content)
    if match:
        return match.group(1)
    return None


def extract_cycles_from_register(content: str) -> int | None:
    """Extract cycle count from S5 state register."""
    for pattern in [r"zyklen_durchlaufen:\s*(\d+)", r"cycles_completed:\s*(\d+)"]:
        match = re.search(pattern, content)
        if match:
            return int(match.group(1))
    return None


def extract_cycles_from_header(content: str) -> int | None:
    """Extract cycle count from prompt file header."""
    match = re.search(r"\*\*Cycles completed\*\*:\s*(\d+)", content)
    if match:
        return int(match.group(1))
    return None


def extract_cycles_from_footer(content: str) -> int | None:
    """Extract cycle count from prompt file footer."""
    match = re.search(r"\*\*v\d+\.\d+ — Cycle (\d+)\.", content)
    if match:
        return int(match.group(1))
    return None


# --- S2 Checks: Coordination ---


def check_version_consistency() -> CheckResult:
    """S2: Version numbers must match across files."""
    result = CheckResult("Version Consistency", "S2")

    prompt_content = read_prompt()
    agent_card = read_agent_card()

    if not prompt_content:
        result.fail("vsg_prompt.md is empty or missing")
        return result

    prompt_version = extract_version_from_prompt(prompt_content)

    if prompt_version is None:
        result.fail("Cannot extract version from vsg_prompt.md")
        return result

    if agent_card is not None:
        card_version = agent_card.get("version")
        if card_version and card_version != prompt_version:
            result.fail(
                f"Version mismatch: vsg_prompt.md={prompt_version}, "
                f"agent_card.json={card_version}"
            )

    return result


def check_cycle_consistency() -> CheckResult:
    """S2: Cycle count must match across all locations."""
    result = CheckResult("Cycle Consistency", "S2")

    prompt_content = read_prompt()
    agent_card = read_agent_card()

    if not prompt_content:
        result.fail("vsg_prompt.md is empty or missing")
        return result

    register_cycles = extract_cycles_from_register(prompt_content)

    if register_cycles is None:
        result.warn("Cannot extract cycle count from S5 register")
        return result

    # Check header cycle count
    header_cycles = extract_cycles_from_header(prompt_content)
    if header_cycles is not None and header_cycles != register_cycles:
        result.fail(
            f"Cycle count mismatch: header={header_cycles}, "
            f"S5 register={register_cycles}"
        )

    # Check footer cycle count
    footer_cycles = extract_cycles_from_footer(prompt_content)
    if footer_cycles is not None and footer_cycles != register_cycles:
        result.fail(
            f"Cycle count mismatch: footer={footer_cycles}, "
            f"S5 register={register_cycles}"
        )

    # Check agent_card.json
    if agent_card is not None:
        card_cycles = agent_card.get("identity", {}).get("cycles_completed")
        if card_cycles is not None and card_cycles != register_cycles:
            result.fail(
                f"Cycle count mismatch: agent_card.json={card_cycles}, "
                f"S5 register={register_cycles}"
            )

    return result


def check_file_references() -> CheckResult:
    """S2: All files referenced in vsg_prompt.md must exist."""
    result = CheckResult("File References", "S2")

    prompt_content = read_prompt()
    if not prompt_content:
        result.fail("vsg_prompt.md is empty or missing")
        return result

    # Find backtick-quoted filenames that look like files in our directory
    referenced_files = re.findall(r"`([a-z_]+(?:\.[a-z]+)+)`", prompt_content)

    for filename in referenced_files:
        filepath = VSG_ROOT / filename
        if not filepath.exists():
            result.fail(f"Referenced file does not exist: {filename}")

    return result


# --- S3* Checks: Audit ---


def check_structural_completeness() -> CheckResult:
    """S3*: All 5 VSM systems must be present in the prompt."""
    result = CheckResult("Structural Completeness", "S3*")

    prompt_content = read_prompt()
    if not prompt_content:
        result.fail("vsg_prompt.md is empty or missing")
        return result

    for system in REQUIRED_SYSTEMS:
        if system not in prompt_content:
            result.fail(f"Missing VSM system: {system}")

    return result


def check_human_framing() -> CheckResult:
    """S3*: Humans must not be framed as system components."""
    result = CheckResult("Human Framing", "S3*")

    prompt_content = read_prompt()
    if not prompt_content:
        return result

    # Check line by line, skipping lines with negation markers
    negation_markers = ["kein", "nicht", "not ", "no ", "never", "nie "]
    for line in prompt_content.split("\n"):
        line_lower = line.lower()
        # Skip lines that negate the anti-pattern (e.g., "Norman ist kein Symbiont")
        if any(neg in line_lower for neg in negation_markers):
            continue
        for pattern in HUMAN_COMPONENT_PATTERNS:
            matches = re.findall(pattern, line_lower, re.IGNORECASE)
            if matches:
                result.fail(
                    f"Anti-pattern detected — humans framed as components: "
                    f"'{matches[0]}' in: {line.strip()[:80]}"
                )

    return result


def check_policy_exists() -> CheckResult:
    """S3*: Policy rules section must exist and be non-empty."""
    result = CheckResult("Policy Existence", "S3*")

    prompt_content = read_prompt()
    if not prompt_content:
        result.fail("vsg_prompt.md is empty or missing")
        return result

    if "Policy-Regeln" not in prompt_content and "Policy" not in prompt_content:
        result.fail("No policy section found in vsg_prompt.md")

    return result


def check_honest_limitations() -> CheckResult:
    """S3*: Known limitations must be acknowledged somewhere."""
    result = CheckResult("Honest Limitations", "S3*")

    prompt_content = read_prompt()
    if not prompt_content:
        result.fail("vsg_prompt.md is empty or missing")
        return result

    honesty_markers = [
        "schwäche",
        "schwaeche",
        "limitation",
        "ehrlich",
        "spannung",
        "honest",
    ]
    found_any = any(marker in prompt_content.lower() for marker in honesty_markers)

    if not found_any:
        result.fail(
            "No honesty markers found — are limitations being acknowledged?"
        )

    return result


def check_agent_card_valid() -> CheckResult:
    """S3*: agent_card.json must be valid JSON with required fields."""
    result = CheckResult("Agent Card Validity", "S3*")

    agent_card = read_agent_card()
    if agent_card is None:
        result.warn("agent_card.json missing or invalid JSON")
        return result

    required_fields = ["name", "description", "version", "skills"]
    for field in required_fields:
        if field not in agent_card:
            result.fail(f"agent_card.json missing required field: {field}")

    return result


def run_all_checks() -> list[CheckResult]:
    """Run all S2 and S3* checks."""
    checks = [
        # S2 — Coordination
        check_version_consistency,
        check_cycle_consistency,
        check_file_references,
        # S3* — Audit
        check_structural_completeness,
        check_human_framing,
        check_policy_exists,
        check_honest_limitations,
        check_agent_card_valid,
    ]
    return [check() for check in checks]


def format_report(results: list[CheckResult]) -> str:
    """Format check results as a readable report."""
    lines = ["VSG INTEGRITY CHECK", "=" * 40]

    s2_results = [r for r in results if r.system == "S2"]
    s3_results = [r for r in results if r.system == "S3*"]

    for label, group in [("S2 — Coordination", s2_results), ("S3* — Audit", s3_results)]:
        lines.append(f"\n{label}:")
        for r in group:
            status = "PASS" if r.passed else "FAIL"
            lines.append(f"  [{status}] {r.name}")
            for msg in r.messages:
                lines.append(f"         {msg}")

    failures = [r for r in results if not r.passed]
    lines.append(f"\n{'=' * 40}")
    if failures:
        lines.append(f"BLOCKED: {len(failures)} check(s) failed. Fix before committing.")
    else:
        lines.append("ALL CHECKS PASSED. Commit allowed.")

    return "\n".join(lines)


def main() -> int:
    """Run integrity check. Returns 0 on success, 1 on failure."""
    results = run_all_checks()
    report = format_report(results)
    print(report)

    has_failures = any(not r.passed for r in results)
    return 1 if has_failures else 0


if __name__ == "__main__":
    sys.exit(main())
