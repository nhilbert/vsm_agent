"""Fragenkatalog fuer die VSM-Diagnostik.

Jedes System wird durch 4-5 Fragen diagnostiziert.
Antwortskala: 1 (trifft gar nicht zu) bis 5 (trifft voll zu).
"""

from vsm_diagnostic.models import Question, SystemId

QUESTIONS: list[Question] = [
    # === S1: Operations ===
    Question(
        system=SystemId.S1,
        text="Sind die operativen Einheiten klar definiert und abgegrenzt?",
        description=(
            "Jede operative Einheit hat einen klaren Zweck, definierte Grenzen "
            "und eigene Ressourcen."
        ),
        weight=1.2,
    ),
    Question(
        system=SystemId.S1,
        text="Haben die operativen Einheiten genuegend Autonomie?",
        description=(
            "Die Einheiten koennen operative Entscheidungen selbst treffen, "
            "ohne staendig auf Genehmigung warten zu muessen."
        ),
    ),
    Question(
        system=SystemId.S1,
        text="Ist jede operative Einheit in sich selbst lebensfaehig?",
        description=(
            "Jede Einheit hat ihr eigenes lokales Management (S1-S5 rekursiv) "
            "und koennte im Prinzip eigenstaendig operieren."
        ),
        weight=1.2,
    ),
    Question(
        system=SystemId.S1,
        text="Gibt es klare Kommunikationskanaele zwischen den operativen Einheiten und dem Management?",
        description=(
            "Informationen fliessen zuverlaessig zwischen den Einheiten "
            "und der uebergeordneten Steuerung."
        ),
    ),
    # === S2: Coordination ===
    Question(
        system=SystemId.S2,
        text="Gibt es Mechanismen zur Konfliktloesung zwischen operativen Einheiten?",
        description=(
            "Es existieren Prozesse, Standards oder Regeln, die verhindern, "
            "dass Einheiten gegeneinander arbeiten."
        ),
        weight=1.2,
    ),
    Question(
        system=SystemId.S2,
        text="Werden gemeinsame Standards und Schnittstellen gepflegt?",
        description=(
            "Einheitliche Prozesse, Datenformate und Kommunikationsprotokolle "
            "reduzieren Reibung zwischen den Einheiten."
        ),
    ),
    Question(
        system=SystemId.S2,
        text="Werden Oszillationen (Hin-und-Her-Schwankungen) erkannt und gedaempft?",
        description=(
            "Wenn zwei Einheiten in einen Konflikt-Zyklus geraten "
            "(z.B. um Ressourcen), gibt es Mechanismen, die das stabilisieren."
        ),
    ),
    Question(
        system=SystemId.S2,
        text="Funktioniert die zeitliche Koordination zwischen den Einheiten?",
        description=(
            "Abhaengigkeiten zwischen Einheiten werden gemanagt, "
            "Timing-Probleme und Deadlocks werden vermieden."
        ),
    ),
    # === S3: Control ===
    Question(
        system=SystemId.S3,
        text="Gibt es eine klare Ressourcenverteilung zwischen den operativen Einheiten?",
        description=(
            "Budget, Personal, Zeit und andere Ressourcen werden "
            "transparent und nachvollziehbar verteilt."
        ),
        weight=1.2,
    ),
    Question(
        system=SystemId.S3,
        text="Werden Leistungskennzahlen erhoben und ausgewertet?",
        description=(
            "Die Leistung der operativen Einheiten wird gemessen, "
            "und es gibt Feedback-Schleifen zur Verbesserung."
        ),
    ),
    Question(
        system=SystemId.S3,
        text="Werden Synergien zwischen den operativen Einheiten aktiv gefoerdert?",
        description=(
            "Es wird bewusst nach Moeglichkeiten gesucht, "
            "durch Zusammenarbeit der Einheiten Mehrwert zu schaffen."
        ),
    ),
    Question(
        system=SystemId.S3,
        text="Kann die Steuerung bei Bedarf schnell eingreifen?",
        description=(
            "Wenn eine Einheit in Schwierigkeiten geraet, "
            "kann das Management zeitnah reagieren und unterstuetzen."
        ),
    ),
    # === S3*: Audit ===
    Question(
        system=SystemId.S3_STAR,
        text="Gibt es unabhaengige Ueberpruefungen der operativen Realitaet?",
        description=(
            "Sporadische, unangekuendigte Checks, ob die offizielle Darstellung "
            "mit der tatsaechlichen Situation uebereinstimmt."
        ),
        weight=1.5,
    ),
    Question(
        system=SystemId.S3_STAR,
        text="Sind die Audit-Ergebnisse unabhaengig von der regulaeren Berichtslinie?",
        description=(
            "Die Audit-Funktion berichtet nicht ueber die gleichen Kanaele "
            "wie der normale Betrieb — sie hat direkten Zugang zur Steuerung."
        ),
    ),
    Question(
        system=SystemId.S3_STAR,
        text="Werden Audit-Erkenntnisse tatsaechlich in Massnahmen umgesetzt?",
        description=(
            "Gefundene Probleme werden nicht nur dokumentiert, "
            "sondern fuehren zu konkreten Verbesserungen."
        ),
    ),
    # === S4: Intelligence ===
    Question(
        system=SystemId.S4,
        text="Wird die Umwelt systematisch beobachtet?",
        description=(
            "Markttrends, technologische Entwicklungen, regulatorische Aenderungen "
            "und Wettbewerber werden aktiv verfolgt."
        ),
        weight=1.2,
    ),
    Question(
        system=SystemId.S4,
        text="Werden Zukunftsszenarien entwickelt und durchgespielt?",
        description=(
            "Die Organisation beschaeftigt sich aktiv mit moeglichen Zukuenften "
            "und bereitet sich auf verschiedene Szenarien vor."
        ),
    ),
    Question(
        system=SystemId.S4,
        text="Fliessen externe Erkenntnisse in interne Entscheidungen ein?",
        description=(
            "Was in der Umwelt erkannt wird, fuehrt tatsaechlich "
            "zu Anpassungen im Inneren der Organisation."
        ),
    ),
    Question(
        system=SystemId.S4,
        text="Gibt es einen funktionierenden Dialog zwischen S3 (Innen) und S4 (Aussen)?",
        description=(
            "Der 3-4-Homeostat: Innere Stabilitaet und aeussere Anpassung "
            "werden aktiv balanciert, nicht gegeneinander ausgespielt."
        ),
        weight=1.5,
    ),
    # === S5: Policy ===
    Question(
        system=SystemId.S5,
        text="Gibt es eine klar formulierte Identitaet und Mission?",
        description=(
            "Die Organisation weiss, WER sie ist und WARUM sie existiert. "
            "Dies ist nicht nur ein Leitbild an der Wand, sondern gelebte Realitaet."
        ),
        weight=1.5,
    ),
    Question(
        system=SystemId.S5,
        text="Werden Werte und uebergeordnete Regeln konsequent durchgesetzt?",
        description=(
            "Die Policy der Organisation wird von allen Ebenen respektiert "
            "und bei Verstaessen konsequent eingefordert."
        ),
    ),
    Question(
        system=SystemId.S5,
        text="Wird der 3-4-Homeostat aktiv moderiert?",
        description=(
            "Wenn Spannungen zwischen interner Optimierung (S3) und "
            "Umweltanpassung (S4) auftreten, gibt es einen Mechanismus zur Entscheidung."
        ),
        weight=1.5,
    ),
    Question(
        system=SystemId.S5,
        text="Ist die Organisation adaptiv, ohne ihre Identitaet zu verlieren?",
        description=(
            "Die Organisation kann sich veraendern und anpassen, "
            "bleibt aber erkennbar sie selbst. Wandel innerhalb klarer Grenzen."
        ),
        weight=1.2,
    ),
]


def get_questions_for_system(system: SystemId) -> list[Question]:
    """Filtere Fragen fuer ein bestimmtes System."""
    return [q for q in QUESTIONS if q.system == system]
