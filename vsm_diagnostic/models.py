"""Datenmodelle fuer die VSM-Diagnostik."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class SystemId(str, Enum):
    """Die fuenf Systeme des Viable System Model plus Audit-Funktion."""

    S1 = "S1"
    S2 = "S2"
    S3 = "S3"
    S3_STAR = "S3*"
    S4 = "S4"
    S5 = "S5"


class Severity(str, Enum):
    """Schweregrad einer Diagnose-Erkenntnis."""

    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"
    OK = "ok"


SYSTEM_NAMES: dict[SystemId, str] = {
    SystemId.S1: "Operations (S1) — Wertschoepfende Einheiten",
    SystemId.S2: "Coordination (S2) — Anti-Oszillation",
    SystemId.S3: "Control (S3) — Interne Steuerung",
    SystemId.S3_STAR: "Audit (S3*) — Sporadische Ueberpruefung",
    SystemId.S4: "Intelligence (S4) — Umweltbeobachtung",
    SystemId.S5: "Policy (S5) — Identitaet & Rahmensetzung",
}

SYSTEM_DESCRIPTIONS: dict[SystemId, str] = {
    SystemId.S1: (
        "Die operativen Einheiten, die den eigentlichen Zweck der Organisation erfuellen. "
        "Jede Einheit hat ihr eigenes lokales Management und ihre eigene Autonomie."
    ),
    SystemId.S2: (
        "Mechanismen zur Koordination zwischen den operativen Einheiten. "
        "Verhindert Konflikte, setzt Standards, daempft Oszillationen."
    ),
    SystemId.S3: (
        "Das interne Management-System. Verteilt Ressourcen, ueberwacht Leistung, "
        "stellt Synergie zwischen S1-Einheiten her."
    ),
    SystemId.S3_STAR: (
        "Die Audit-Funktion. Sporadische, unangekuendigte Ueberpruefungen der "
        "operativen Realitaet — unabhaengig von den regulaeren Berichtslinien."
    ),
    SystemId.S4: (
        "Das Intelligenz-System. Beobachtet die Umwelt, erkennt Trends, "
        "identifiziert Chancen und Bedrohungen, plant die Zukunft."
    ),
    SystemId.S5: (
        "Das Policy-System. Definiert Identitaet, Werte und uebergeordnete Regeln. "
        "Balanciert S3 (Innen) und S4 (Aussen) — der 3-4-Homeostat."
    ),
}


@dataclass
class Question:
    """Eine Diagnosefrage zu einem VSM-System."""

    system: SystemId
    text: str
    description: str
    weight: float = 1.0


@dataclass
class Answer:
    """Antwort auf eine Diagnosefrage (Skala 1-5)."""

    question: Question
    score: int  # 1 (sehr schlecht) bis 5 (sehr gut)

    def weighted_score(self) -> float:
        """Gewichteter Score (0.0 bis 1.0)."""
        return ((self.score - 1) / 4) * self.question.weight


@dataclass
class SystemDiagnosis:
    """Diagnose-Ergebnis fuer ein einzelnes VSM-System."""

    system: SystemId
    answers: list[Answer]
    score: float  # 0.0 bis 1.0
    severity: Severity
    findings: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)


@dataclass
class ViabilityReport:
    """Gesamtbericht der VSM-Diagnostik."""

    organization_name: str
    system_diagnoses: dict[SystemId, SystemDiagnosis]
    overall_score: float  # 0.0 bis 1.0
    overall_severity: Severity
    critical_issues: list[str] = field(default_factory=list)
    summary: str = ""
