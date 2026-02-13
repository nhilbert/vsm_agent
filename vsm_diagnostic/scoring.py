"""Scoring und Auswertung der VSM-Diagnostik."""

from __future__ import annotations

from vsm_diagnostic.models import (
    Answer,
    Question,
    Severity,
    SystemDiagnosis,
    SystemId,
    ViabilityReport,
)
from vsm_diagnostic.questions import get_questions_for_system

# Schwellenwerte fuer Severity
CRITICAL_THRESHOLD = 0.3
WARNING_THRESHOLD = 0.5
OK_THRESHOLD = 0.7

# Befund-Texte pro System bei niedrigem Score
FINDINGS: dict[SystemId, list[str]] = {
    SystemId.S1: [
        "Operative Einheiten sind unzureichend definiert oder abgegrenzt.",
        "Autonomie der Einheiten ist eingeschraenkt — Mikromanagement-Risiko.",
        "Rekursive Lebensfaehigkeit fehlt — Einheiten haengen vollstaendig von der Zentrale ab.",
    ],
    SystemId.S2: [
        "Fehlende Koordinationsmechanismen fuehren zu Reibungsverlusten.",
        "Ohne Anti-Oszillation drohen Ressourcenkonflikte zwischen Einheiten.",
        "Standards und Schnittstellen sind inkonsistent.",
    ],
    SystemId.S3: [
        "Ressourcenverteilung ist intransparent oder willkuerlich.",
        "Leistungsmessung fehlt — keine Feedback-Schleife zur Verbesserung.",
        "Synergien zwischen Einheiten werden nicht genutzt.",
    ],
    SystemId.S3_STAR: [
        "Keine unabhaengige Ueberpruefung der operativen Realitaet.",
        "Audit-Ergebnisse werden ignoriert oder nicht umgesetzt.",
        "Informationsasymmetrie: Management kennt die Realitaet nicht.",
    ],
    SystemId.S4: [
        "Umweltbeobachtung fehlt — die Organisation operiert blind.",
        "Zukunftsplanung ist reaktiv statt proaktiv.",
        "Der 3-4-Homeostat ist gestauert — keine Balance zwischen Innen und Aussen.",
    ],
    SystemId.S5: [
        "Identitaet und Mission sind unklar oder nicht gelebt.",
        "Policy-Durchsetzung ist inkonsistent.",
        "Keine Moderation des 3-4-Homeostaten — S3 und S4 blockieren sich.",
    ],
}

# Empfehlungen pro System
RECOMMENDATIONS: dict[SystemId, list[str]] = {
    SystemId.S1: [
        "Definieren Sie jede operative Einheit mit klarem Zweck, Grenzen und eigenem Management.",
        "Pruefen Sie, ob jede Einheit genuegend Autonomie fuer operative Entscheidungen hat.",
        "Stellen Sie sicher, dass Kommunikationskanaele bidirektional funktionieren.",
    ],
    SystemId.S2: [
        "Etablieren Sie klare Spielregeln fuer die Zusammenarbeit zwischen Einheiten.",
        "Definieren Sie gemeinsame Standards und Schnittstellen.",
        "Implementieren Sie fruehe Warnmechanismen fuer Ressourcenkonflikte.",
    ],
    SystemId.S3: [
        "Machen Sie die Ressourcenverteilung transparent und nachvollziehbar.",
        "Etablieren Sie ein einfaches, aussagekraeftiges Kennzahlensystem.",
        "Foerdern Sie gezielt Synergie-Projekte zwischen operativen Einheiten.",
    ],
    SystemId.S3_STAR: [
        "Fuehren Sie regelmaessige, unangekuendigte Realitaets-Checks durch.",
        "Stellen Sie sicher, dass Audit-Ergebnisse direkt an die Steuerung fliessen.",
        "Schaffen Sie eine Kultur, in der ehrliches Feedback willkommen ist.",
    ],
    SystemId.S4: [
        "Institutionalisieren Sie systematische Umweltbeobachtung (Markt, Technologie, Regulierung).",
        "Entwickeln Sie regelmaessig Zukunftsszenarien und testen Sie Ihre Strategien dagegen.",
        "Staerken Sie den Dialog zwischen S3 (interne Optimierung) und S4 (externe Anpassung).",
    ],
    SystemId.S5: [
        "Formulieren Sie Identitaet und Mission klar — und leben Sie sie vor.",
        "Pruefen Sie regelmaessig, ob alle Ebenen die uebergeordneten Werte kennen und respektieren.",
        "Etablieren Sie einen Mechanismus, der Spannungen zwischen S3 und S4 moderiert.",
    ],
}


def classify_severity(score: float) -> Severity:
    """Bestimme den Schweregrad basierend auf dem Score."""
    if score < CRITICAL_THRESHOLD:
        return Severity.CRITICAL
    if score < WARNING_THRESHOLD:
        return Severity.WARNING
    if score < OK_THRESHOLD:
        return Severity.INFO
    return Severity.OK


def diagnose_system(system: SystemId, answers: list[Answer]) -> SystemDiagnosis:
    """Diagnostiziere ein einzelnes VSM-System anhand der Antworten."""
    if not answers:
        return SystemDiagnosis(
            system=system,
            answers=[],
            score=0.0,
            severity=Severity.CRITICAL,
            findings=["Keine Antworten fuer dieses System vorhanden."],
            recommendations=["Fuehren Sie die Diagnostik fuer dieses System durch."],
        )

    total_weight = sum(a.question.weight for a in answers)
    weighted_sum = sum(a.weighted_score() for a in answers)
    score = weighted_sum / total_weight if total_weight > 0 else 0.0

    severity = classify_severity(score)

    findings: list[str] = []
    recommendations: list[str] = []

    if severity in (Severity.CRITICAL, Severity.WARNING):
        system_findings = FINDINGS.get(system, [])
        system_recommendations = RECOMMENDATIONS.get(system, [])

        # Identifiziere die schwaechsten Fragen
        sorted_answers = sorted(answers, key=lambda a: a.score)
        for answer in sorted_answers:
            if answer.score <= 2:
                findings.append(
                    f"Schwachstelle: '{answer.question.text}' — Score: {answer.score}/5"
                )

        # Allgemeine Befunde und Empfehlungen hinzufuegen
        if severity == Severity.CRITICAL:
            findings.extend(system_findings[:2])
            recommendations.extend(system_recommendations)
        else:
            findings.extend(system_findings[:1])
            recommendations.extend(system_recommendations[:2])

    elif severity == Severity.INFO:
        recommendations.append(
            f"{system.value} funktioniert grundsaetzlich, hat aber Optimierungspotenzial."
        )

    return SystemDiagnosis(
        system=system,
        answers=answers,
        score=score,
        severity=severity,
        findings=findings,
        recommendations=recommendations,
    )


def create_viability_report(
    organization_name: str, all_answers: list[Answer]
) -> ViabilityReport:
    """Erstelle den vollstaendigen Viabilitaets-Report."""
    # Gruppiere Antworten nach System
    answers_by_system: dict[SystemId, list[Answer]] = {}
    for system in SystemId:
        answers_by_system[system] = [a for a in all_answers if a.question.system == system]

    # Diagnostiziere jedes System
    diagnoses: dict[SystemId, SystemDiagnosis] = {}
    for system in SystemId:
        diagnoses[system] = diagnose_system(system, answers_by_system[system])

    # Gesamt-Score (gewichteter Durchschnitt, S5 zaehlt doppelt)
    system_weights: dict[SystemId, float] = {
        SystemId.S1: 1.0,
        SystemId.S2: 0.8,
        SystemId.S3: 1.0,
        SystemId.S3_STAR: 0.7,
        SystemId.S4: 1.0,
        SystemId.S5: 1.2,
    }

    total_weight = sum(system_weights.values())
    overall_score = (
        sum(
            diagnoses[s].score * system_weights[s]
            for s in SystemId
        )
        / total_weight
    )

    overall_severity = classify_severity(overall_score)

    # Kritische Issues sammeln
    critical_issues: list[str] = []
    for system in SystemId:
        diag = diagnoses[system]
        if diag.severity == Severity.CRITICAL:
            critical_issues.append(
                f"{system.value} ist kritisch (Score: {diag.score:.0%})"
            )

    # 3-4-Homeostat pruefen
    s3_score = diagnoses[SystemId.S3].score
    s4_score = diagnoses[SystemId.S4].score
    homeostat_balance = abs(s3_score - s4_score)
    if homeostat_balance > 0.3:
        if s3_score > s4_score:
            critical_issues.append(
                "3-4-Homeostat Imbalance: S3 (Innen) dominiert S4 (Aussen) "
                "— Gefahr der Introversion."
            )
        else:
            critical_issues.append(
                "3-4-Homeostat Imbalance: S4 (Aussen) dominiert S3 (Innen) "
                "— Gefahr der Instabilitaet durch staendigen Wandel."
            )

    # Zusammenfassung
    summary = _generate_summary(overall_score, overall_severity, diagnoses, critical_issues)

    return ViabilityReport(
        organization_name=organization_name,
        system_diagnoses=diagnoses,
        overall_score=overall_score,
        overall_severity=overall_severity,
        critical_issues=critical_issues,
        summary=summary,
    )


def _generate_summary(
    overall_score: float,
    overall_severity: Severity,
    diagnoses: dict[SystemId, SystemDiagnosis],
    critical_issues: list[str],
) -> str:
    """Generiere die Zusammenfassung des Reports."""
    if overall_severity == Severity.CRITICAL:
        intro = (
            "Die Organisation weist kritische Maengel in ihrer Lebensfaehigkeit auf. "
            "Dringendes Handeln ist erforderlich."
        )
    elif overall_severity == Severity.WARNING:
        intro = (
            "Die Organisation hat strukturelle Schwaechen, die ihre Lebensfaehigkeit "
            "gefaehrden koennten. Gezielte Verbesserungen werden empfohlen."
        )
    elif overall_severity == Severity.INFO:
        intro = (
            "Die Organisation ist grundsaetzlich lebensfaehig, hat aber "
            "Optimierungspotenzial in einzelnen Bereichen."
        )
    else:
        intro = (
            "Die Organisation zeigt eine hohe Lebensfaehigkeit. "
            "Alle VSM-Systeme funktionieren gut."
        )

    strongest = max(diagnoses.values(), key=lambda d: d.score)
    weakest = min(diagnoses.values(), key=lambda d: d.score)

    details = (
        f"Staerkstes System: {strongest.system.value} ({strongest.score:.0%}). "
        f"Schwaechstes System: {weakest.system.value} ({weakest.score:.0%})."
    )

    critical_note = ""
    if critical_issues:
        critical_note = (
            f" Kritische Probleme: {len(critical_issues)}."
        )

    return f"{intro} Gesamtscore: {overall_score:.0%}. {details}{critical_note}"
