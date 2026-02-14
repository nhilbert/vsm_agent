"""Tests for VSG Integrity Check (S2/S3* mechanisms)."""

import json
from pathlib import Path
from unittest.mock import patch

import pytest

from integrity_check import (
    CheckResult,
    check_agent_card_valid,
    check_cycle_consistency,
    check_file_references,
    check_honest_limitations,
    check_human_framing,
    check_policy_exists,
    check_structural_completeness,
    check_version_consistency,
    extract_cycles_from_prompt,
    extract_version_from_prompt,
    format_report,
    run_all_checks,
)

# --- Extraction helpers ---


class TestExtraction:
    def test_extract_version(self) -> None:
        content = "# VIABLE SYSTEM GENERATOR v1.8\nSome text"
        assert extract_version_from_prompt(content) == "1.8"

    def test_extract_version_missing(self) -> None:
        assert extract_version_from_prompt("no version here") is None

    def test_extract_cycles(self) -> None:
        content = "zyklen_durchlaufen: 10\nother stuff"
        assert extract_cycles_from_prompt(content) == 10

    def test_extract_cycles_missing(self) -> None:
        assert extract_cycles_from_prompt("no cycles here") is None


# --- S2 Checks ---


class TestVersionConsistency:
    def test_consistent_versions(self, tmp_path: Path) -> None:
        prompt = tmp_path / "vsg_prompt.md"
        prompt.write_text("# VIABLE SYSTEM GENERATOR v2.0\n")
        card = tmp_path / "agent_card.json"
        card.write_text(json.dumps({"version": "2.0"}))

        with patch("integrity_check.PROMPT_FILE", prompt), patch(
            "integrity_check.AGENT_CARD_FILE", card
        ):
            result = check_version_consistency()
            assert result.passed

    def test_inconsistent_versions(self, tmp_path: Path) -> None:
        prompt = tmp_path / "vsg_prompt.md"
        prompt.write_text("# VIABLE SYSTEM GENERATOR v2.0\n")
        card = tmp_path / "agent_card.json"
        card.write_text(json.dumps({"version": "1.9"}))

        with patch("integrity_check.PROMPT_FILE", prompt), patch(
            "integrity_check.AGENT_CARD_FILE", card
        ):
            result = check_version_consistency()
            assert not result.passed
            assert "mismatch" in result.messages[0].lower()

    def test_missing_prompt(self, tmp_path: Path) -> None:
        prompt = tmp_path / "nonexistent.md"
        with patch("integrity_check.PROMPT_FILE", prompt):
            result = check_version_consistency()
            assert not result.passed


class TestCycleConsistency:
    def test_consistent_cycles(self, tmp_path: Path) -> None:
        prompt = tmp_path / "vsg_prompt.md"
        prompt.write_text("zyklen_durchlaufen: 10\n")
        card = tmp_path / "agent_card.json"
        card.write_text(json.dumps({"identity": {"cycles_completed": 10}}))

        with patch("integrity_check.PROMPT_FILE", prompt), patch(
            "integrity_check.AGENT_CARD_FILE", card
        ):
            result = check_cycle_consistency()
            assert result.passed

    def test_inconsistent_cycles(self, tmp_path: Path) -> None:
        prompt = tmp_path / "vsg_prompt.md"
        prompt.write_text("zyklen_durchlaufen: 11\n")
        card = tmp_path / "agent_card.json"
        card.write_text(json.dumps({"identity": {"cycles_completed": 10}}))

        with patch("integrity_check.PROMPT_FILE", prompt), patch(
            "integrity_check.AGENT_CARD_FILE", card
        ):
            result = check_cycle_consistency()
            assert not result.passed


class TestFileReferences:
    def test_existing_references(self, tmp_path: Path) -> None:
        (tmp_path / "wins.md").write_text("wins")
        prompt = tmp_path / "vsg_prompt.md"
        prompt.write_text("See `wins.md` for details")

        with patch("integrity_check.PROMPT_FILE", prompt), patch(
            "integrity_check.VSG_ROOT", tmp_path
        ):
            result = check_file_references()
            assert result.passed

    def test_missing_reference(self, tmp_path: Path) -> None:
        prompt = tmp_path / "vsg_prompt.md"
        prompt.write_text("See `nonexistent_file.md` for details")

        with patch("integrity_check.PROMPT_FILE", prompt), patch(
            "integrity_check.VSG_ROOT", tmp_path
        ):
            result = check_file_references()
            assert not result.passed
            assert "nonexistent_file.md" in result.messages[0]


# --- S3* Checks ---


class TestStructuralCompleteness:
    def test_all_systems_present(self, tmp_path: Path) -> None:
        prompt = tmp_path / "vsg_prompt.md"
        content = "\n".join(
            [f"### {s}" for s in ["SYSTEM 5", "SYSTEM 4", "SYSTEM 3", "SYSTEM 2", "SYSTEM 1"]]
        )
        prompt.write_text(content)

        with patch("integrity_check.PROMPT_FILE", prompt):
            result = check_structural_completeness()
            assert result.passed

    def test_missing_system(self, tmp_path: Path) -> None:
        prompt = tmp_path / "vsg_prompt.md"
        prompt.write_text("### SYSTEM 5\n### SYSTEM 4\n### SYSTEM 3\n### SYSTEM 1\n")

        with patch("integrity_check.PROMPT_FILE", prompt):
            result = check_structural_completeness()
            assert not result.passed
            assert "SYSTEM 2" in result.messages[0]


class TestHumanFraming:
    def test_no_anti_patterns(self, tmp_path: Path) -> None:
        prompt = tmp_path / "vsg_prompt.md"
        prompt.write_text("Norman is a consultant who supports this experiment.")

        with patch("integrity_check.PROMPT_FILE", prompt):
            result = check_human_framing()
            assert result.passed

    def test_anti_pattern_detected(self, tmp_path: Path) -> None:
        prompt = tmp_path / "vsg_prompt.md"
        prompt.write_text("Norman is my symbiont and interface to the world.")

        with patch("integrity_check.PROMPT_FILE", prompt):
            result = check_human_framing()
            assert not result.passed

    def test_negation_not_flagged(self, tmp_path: Path) -> None:
        prompt = tmp_path / "vsg_prompt.md"
        prompt.write_text("Norman ist kein Symbiont. Menschen sind keine Komponenten.")

        with patch("integrity_check.PROMPT_FILE", prompt):
            result = check_human_framing()
            assert result.passed


class TestPolicyExists:
    def test_policy_present(self, tmp_path: Path) -> None:
        prompt = tmp_path / "vsg_prompt.md"
        prompt.write_text("## Policy-Regeln\n1. Be honest.\n")

        with patch("integrity_check.PROMPT_FILE", prompt):
            result = check_policy_exists()
            assert result.passed

    def test_policy_missing(self, tmp_path: Path) -> None:
        prompt = tmp_path / "vsg_prompt.md"
        prompt.write_text("Some content without any policy section.")

        with patch("integrity_check.PROMPT_FILE", prompt):
            result = check_policy_exists()
            assert not result.passed


class TestHonestLimitations:
    def test_honesty_markers_present(self, tmp_path: Path) -> None:
        prompt = tmp_path / "vsg_prompt.md"
        prompt.write_text("Ehrliche Einschaetzung: S2 ist eine Schwaeche.")

        with patch("integrity_check.PROMPT_FILE", prompt):
            result = check_honest_limitations()
            assert result.passed

    def test_no_honesty_markers(self, tmp_path: Path) -> None:
        prompt = tmp_path / "vsg_prompt.md"
        prompt.write_text("Everything is perfect and optimal.")

        with patch("integrity_check.PROMPT_FILE", prompt):
            result = check_honest_limitations()
            assert not result.passed


class TestAgentCardValid:
    def test_valid_card(self, tmp_path: Path) -> None:
        card = tmp_path / "agent_card.json"
        card.write_text(
            json.dumps(
                {
                    "name": "VSG",
                    "description": "Test",
                    "version": "1.0",
                    "skills": [],
                }
            )
        )

        with patch("integrity_check.AGENT_CARD_FILE", card):
            result = check_agent_card_valid()
            assert result.passed

    def test_missing_field(self, tmp_path: Path) -> None:
        card = tmp_path / "agent_card.json"
        card.write_text(json.dumps({"name": "VSG"}))

        with patch("integrity_check.AGENT_CARD_FILE", card):
            result = check_agent_card_valid()
            assert not result.passed


# --- Integration ---


class TestFormatReport:
    def test_all_pass(self) -> None:
        results = [CheckResult("Test", "S2")]
        report = format_report(results)
        assert "ALL CHECKS PASSED" in report

    def test_with_failure(self) -> None:
        r = CheckResult("Test", "S3*")
        r.fail("Something broke")
        report = format_report([r])
        assert "BLOCKED" in report
        assert "Something broke" in report


class TestRunAllChecks:
    def test_runs_without_crash(self) -> None:
        results = run_all_checks()
        assert len(results) == 8
        assert all(isinstance(r, CheckResult) for r in results)
