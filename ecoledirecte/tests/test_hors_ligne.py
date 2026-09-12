"""Vérifie toute la chaîne en aval de l'API, avec des réponses factices.

Le client HTTP n'est pas testé ici (il faudrait un vrai compte) : on teste la
normalisation, la détection des changements, la rédaction du brief et l'export
iCalendar, c'est-à-dire tout ce qui peut casser sans qu'École Directe y soit pour
quelque chose.

    python -m tests.test_hors_ligne
"""

from __future__ import annotations

import base64
import sys
from datetime import date, timedelta

from ed import brief, calendrier, collecte, etat
from ed.models import Collecte, Cours, DateCle, Devoir, Enfant, FaitViesScolaire, Message, Note

AUJOURDHUI = date(2026, 9, 14)  # un lundi
DEMAIN = AUJOURDHUI + timedelta(days=1)
HIER = AUJOURDHUI - timedelta(days=1)

echecs: list[str] = []


def verifier(condition: bool, libelle: str) -> None:
    if condition:
        print(f"  ok   {libelle}")
    else:
        print(f"  ÉCHEC {libelle}")
        echecs.append(libelle)


def b64(texte: str) -> str:
    return base64.b64encode(texte.encode("utf-8")).decode("ascii")


COMPTE_PARENT = {
    "id": "4242",
    "typeCompte": "1",
    "prenom": "Thomas",
    "nom": "Pellegrini",
    "profile": {
        "eleves": [
            {"id": "1001", "prenom": "Léa", "nom": "Pellegrini", "classe": {"id": "9", "code": "4B", "libelle": "4e B"}},
            {"id": "1002", "prenom": "Noah", "nom": "Pellegrini", "classe": {"id": "3", "code": "6A", "libelle": "6e A"}},
        ]
    },
}


def test_enfants() -> None:
    print("\nDécouverte des enfants")
    enfants = collecte.enfants_du_compte(COMPTE_PARENT)
    verifier(len(enfants) == 2, "les deux enfants sont trouvés")
    verifier(enfants[0].libelle == "Léa (4e B)", "libellé prénom + classe")
    compte_id, type_compte = collecte.identifiant_messagerie(COMPTE_PARENT)
    verifier((compte_id, type_compte) == ("4242", "famille"), "messagerie sur le compte famille")

    compte_eleve = {"id": "77", "typeCompte": "E", "prenom": "Léa", "nom": "P", "profile": {"classe": {"libelle": "4e B"}}}
    verifier(len(collecte.enfants_du_compte(compte_eleve)) == 1, "compte élève : un seul enfant")
    verifier(collecte.identifiant_messagerie(compte_eleve)[1] == "eleve", "messagerie sur le compte élève")


def test_normalisation() -> None:
    print("\nNormalisation des réponses API")
    lea = Enfant(id="1001", prenom="Léa", nom="P", classe="4e B")

    edt = [
        {
            "id": 1, "text": "MATHS", "matiere": "MATHEMATIQUES",
            "start_date": f"{AUJOURDHUI} 08:00", "end_date": f"{AUJOURDHUI} 09:00",
            "prof": "Mme Martin", "salle": "B12", "isAnnule": False,
        },
        {
            "id": 2, "matiere": "ANGLAIS",
            "start_date": f"{AUJOURDHUI} 09:00", "end_date": f"{AUJOURDHUI} 10:00",
            "prof": "M. Dubois", "salle": "A04", "isAnnule": True,
        },
    ]
    cours = collecte.normaliser_cours(lea, edt)
    verifier(len(cours) == 2 and cours[0].matiere == "MATHEMATIQUES", "emploi du temps normalisé")
    verifier(cours[1].annule is True, "cours annulé repéré")

    apercu = {str(AUJOURDHUI): [{"matiere": "MATHS"}], "codeMatiere": "ignoré", str(DEMAIN): []}
    verifier(collecte.dates_avec_travail(apercu) == [str(AUJOURDHUI), str(DEMAIN)], "dates du cahier de texte")

    detail = {
        "matieres": [
            {
                "matiere": "MATHEMATIQUES", "nomProf": "Mme Martin",
                "aFaire": {"contenu": b64("Exercices <b>12</b> et 13 p.45"), "donneLe": str(HIER),
                           "effectue": False, "interrogation": True},
            },
            {"matiere": "HISTOIRE", "contenuDeSeance": {"contenu": b64("Chapitre 1")}},
        ]
    }
    devoirs = collecte.normaliser_devoirs_du_jour(lea, str(AUJOURDHUI), detail)
    verifier(len(devoirs) == 1, "seule la matière avec travail à faire est retenue")
    verifier(devoirs[0].contenu == "Exercices 12 et 13 p.45", "HTML et base64 décodés")
    verifier(devoirs[0].interrogation is True, "interrogation repérée")

    notes = collecte.normaliser_notes(lea, {"notes": [
        {"devoir": "Contrôle 1", "libelleMatiere": "MATHEMATIQUES", "valeur": "15,5",
         "noteSur": "20", "coef": "2", "date": str(HIER), "moyenneClasse": "12,4"},
        {"devoir": "Oral", "libelleMatiere": "ANGLAIS", "valeur": "Abs", "noteSur": "20", "date": str(HIER)},
    ]})
    verifier(len(notes) == 1 and notes[0].valeur == "15,5", "notes non chiffrées écartées")

    vie = collecte.normaliser_vie_scolaire(lea, {
        "absencesRetards": [{"typeElement": "Absence", "date": f"{HIER} 08:00", "dateFin": f"{HIER} 10:00",
                             "motif": "Maladie", "justifie": False}],
        "sanctionsEncouragements": [{"typeElement": "Encouragement", "date": str(HIER), "libelle": "Bon travail"}],
    })
    verifier(len(vie) == 2, "absences et sanctions fusionnées")
    verifier(any(f.type == "Absence" and not f.justifie for f in vie), "absence non justifiée repérée")

    messages = collecte.normaliser_messages({"messages": {"received": [
        {"id": 55, "subject": "Réunion parents-professeurs", "read": False, "date": f"{HIER} 17:12",
         "from": {"civilite": "Mme", "prenom": "Claire", "nom": "Durand", "fonctionPersonnel": "Vie scolaire"}},
    ]}})
    verifier(messages[0].expediteur == "Mme Claire Durand — Vie scolaire", "expéditeur reconstruit")
    verifier(messages[0].lu is False, "message non lu")


def test_dates_cles() -> None:
    print("\nExtraction des dates dans les messages")
    message = Message(id="55", date=str(HIER), expediteur="Mme Durand", sujet="Réunion parents-professeurs")
    corps = "Bonjour, la réunion se tiendra le 16 octobre à 18h en salle polyvalente."
    trouvees = collecte.extraire_dates_cles(message, corps, AUJOURDHUI)
    verifier(any(d.date == "2026-10-16" for d in trouvees), "date en toutes lettres extraite")

    corps_court = "Sortie au musée prévue le 02/10, autorisation à rendre avant le 25/09."
    trouvees = collecte.extraire_dates_cles(
        Message(id="56", date=str(HIER), expediteur="M. X", sujet="Sortie scolaire"), corps_court, AUJOURDHUI
    )
    verifier({d.date for d in trouvees} >= {"2026-10-02", "2026-09-25"}, "dates jj/mm extraites")

    sans_echeance = collecte.extraire_dates_cles(
        Message(id="57", date=str(HIER), expediteur="M. X", sujet="Bulletin météo"), "Il fera beau.", AUJOURDHUI
    )
    verifier(sans_echeance == [], "un message sans échéance ne génère rien")

    passe = collecte.extraire_dates_cles(
        Message(id="58", date=str(HIER), expediteur="M. X", sujet="Réunion"), "Réunion du 3 janvier", AUJOURDHUI
    )
    verifier(all(d.date >= str(AUJOURDHUI) for d in passe), "une date passée est reportée ou ignorée")


def collecte_exemple() -> Collecte:
    return Collecte(
        enfants=[
            Enfant(id="1001", prenom="Léa", nom="P", classe="4e B"),
            Enfant(id="1002", prenom="Noah", nom="P", classe="6e A"),
        ],
        cours=[
            Cours(enfant="Léa", date=str(AUJOURDHUI), debut="08:00", fin="09:00", matiere="MATHS", salle="B12"),
            Cours(enfant="Léa", date=str(AUJOURDHUI), debut="09:00", fin="10:00", matiere="ANGLAIS", annule=True),
            Cours(enfant="Noah", date=str(DEMAIN), debut="10:00", fin="11:00", matiere="SVT", salle="C03"),
        ],
        devoirs=[
            Devoir(enfant="Léa", pour_le=str(AUJOURDHUI), matiere="MATHS", contenu="Ex 12 p.45", interrogation=True),
            Devoir(enfant="Léa", pour_le=str(HIER - timedelta(days=3)), matiere="HISTOIRE",
                   contenu="Fiche de révision", effectue=False),
            Devoir(enfant="Noah", pour_le=str(DEMAIN), matiere="FRANÇAIS", contenu="Lire chapitre 3"),
        ],
        notes=[Note(enfant="Léa", date=str(HIER), matiere="MATHS", libelle="Contrôle 1",
                    valeur="15,5", moyenne_classe="12,4")],
        vie_scolaire=[FaitViesScolaire(enfant="Noah", type="Absence", date_debut=f"{HIER} 08:00",
                                       motif="Maladie", justifie=False)],
        messages=[Message(id="55", date=f"{HIER} 17:12", expediteur="Mme Durand",
                          sujet="Réunion parents-professeurs", lu=False, extrait="Le 16 octobre à 18h.")],
        dates_cles=[DateCle(date="2026-10-16", intitule="Réunion parents-professeurs à 18h",
                            source="Message — Mme Durand")],
    )


def test_changements() -> None:
    print("\nDétection des changements entre deux passages")
    veille = collecte_exemple()
    vide = etat.comparer({}, veille)
    verifier(vide.vide, "premier passage : rien n'est signalé comme nouveau")

    precedent = {"elements": {item.cle: item.empreinte for item in veille.tous_les_elements()}}

    aujourd_hui = collecte_exemple()
    aujourd_hui.notes.append(Note(enfant="Noah", date=str(AUJOURDHUI), matiere="SVT",
                                  libelle="Interro", valeur="17"))
    aujourd_hui.cours[0].salle = "D01"
    aujourd_hui.cours.pop()

    changements = etat.comparer(precedent, aujourd_hui)
    verifier(len(changements.par_type("note|")) == 1, "nouvelle note détectée")
    verifier(len(changements.modifies_par_type("cours|")) == 1, "changement de salle détecté")
    verifier(any(d["cle"].startswith("cours|") for d in changements.disparus), "cours disparu détecté")


def test_brief() -> None:
    print("\nRédaction du brief")
    donnees = collecte_exemple()
    precedent = {"elements": {"cours|Léa|%s|08:00|MATHS" % AUJOURDHUI: "08:00-09:00|B12||0"}}
    texte = brief.construire(donnees, etat.comparer(precedent, donnees), AUJOURDHUI, moment="7h00")

    verifier("Léa (4e B)" in texte, "un bloc par enfant")
    verifier("Noah (6e A)" in texte, "second enfant présent")
    verifier("ANNULÉ" in texte, "cours annulé signalé")
    verifier("jamais cochés" in texte, "devoirs oubliés signalés")
    verifier("interrogation" in texte.lower(), "interrogation remontée en tête")
    verifier("Réunion parents-professeurs" in texte, "date clé dans le calendrier")
    verifier("Mme Durand" in texte, "message non lu listé")
    verifier("Absence" in texte, "absence listée")
    verifier("2026-10-16" in texte, "ligne de calendrier présente")

    vierge = Collecte(enfants=[Enfant(id="1", prenom="Léa", nom="P", classe="4e B")])
    texte_vierge = brief.construire(vierge, etat.comparer({}, vierge), AUJOURDHUI)
    verifier("Brief École Directe" in texte_vierge, "brief vide reste lisible")


def test_calendrier() -> None:
    print("\nExport iCalendar")
    ics = calendrier.construire(collecte_exemple())
    verifier(ics.startswith("BEGIN:VCALENDAR"), "en-tête iCalendar")
    verifier(ics.rstrip().endswith("END:VCALENDAR"), "pied iCalendar")
    verifier(ics.count("BEGIN:VEVENT") == ics.count("END:VEVENT"), "événements équilibrés")
    verifier("DTSTART:20260914T060000Z" in ics, "08h00 Paris converti en 06h00 UTC (heure d'été)")
    verifier("STATUS:CANCELLED" in ics, "cours annulé marqué annulé")
    verifier("BEGIN:VALARM" in ics, "rappel posé sur l'interrogation")
    verifier("\r\n" in ics, "fins de ligne CRLF")
    verifier(all(len(l.encode()) <= 75 for l in ics.split("\r\n")), "lignes pliées sous 75 octets")

    hiver = Collecte(cours=[Cours(enfant="Léa", date="2026-01-12", debut="08:00", fin="09:00", matiere="MATHS")])
    verifier("DTSTART:20260112T070000Z" in calendrier.construire(hiver), "heure d'hiver correctement décalée")


def main() -> int:
    for test in (test_enfants, test_normalisation, test_dates_cles,
                 test_changements, test_brief, test_calendrier):
        test()

    print()
    if echecs:
        print(f"{len(echecs)} vérification(s) en échec :")
        for libelle in echecs:
            print(f"  - {libelle}")
        return 1
    print("Toutes les vérifications passent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
