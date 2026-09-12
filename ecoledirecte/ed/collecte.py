"""Récupération et normalisation : c'est ici qu'on absorbe les irrégularités de l'API."""

from __future__ import annotations

import logging
import re
from datetime import date, datetime, timedelta
from typing import Any, Iterable

from .client import ClientED, ErreurEcoleDirecte, texte_message
from .models import Collecte, Cours, DateCle, Devoir, Enfant, FaitViesScolaire, Message, Note

log = logging.getLogger(__name__)

MOIS = {
    "janvier": 1, "février": 2, "fevrier": 2, "mars": 3, "avril": 4, "mai": 5, "juin": 6,
    "juillet": 7, "août": 8, "aout": 8, "septembre": 9, "octobre": 10, "novembre": 11,
    "décembre": 12, "decembre": 12,
}

MOTS_ECHEANCE = (
    "réunion", "reunion", "conseil de classe", "rencontre", "porte ouverte", "portes ouvertes",
    "sortie", "voyage", "brevet", "bac ", "baccalauréat", "oral", "stage", "bulletin",
    "photo de classe", "vaccination", "inscription", "date limite", "avant le", "au plus tard",
    "spectacle", "kermesse", "remise", "convocation", "examen", "épreuve", "epreuve",
)


def _txt(valeur: Any) -> str:
    if valeur is None:
        return ""
    return str(valeur).strip()


def _premier(source: dict[str, Any], *cles: str, defaut: Any = "") -> Any:
    """L'API nomme le même champ différemment selon les endpoints et les versions."""
    for cle in cles:
        if isinstance(source, dict) and source.get(cle) not in (None, ""):
            return source[cle]
    return defaut


def _horodatage(valeur: str) -> tuple[str, str]:
    """'2026-09-12 08:00' -> ('2026-09-12', '08:00'). Tolère les formats partiels."""
    brut = _txt(valeur).replace("T", " ")
    if not brut:
        return "", ""
    morceaux = brut.split(" ")
    jour = morceaux[0][:10]
    heure = morceaux[1][:5] if len(morceaux) > 1 else ""
    return jour, heure


# --------------------------------------------------------------------------- enfants


def enfants_du_compte(compte: dict[str, Any]) -> list[Enfant]:
    """Compte parent : les élèves sont dans profile.eleves. Compte élève : le compte lui-même."""
    type_compte = _txt(compte.get("typeCompte"))
    profil = compte.get("profile") or {}
    eleves = profil.get("eleves") or []

    if eleves:
        resultat = []
        for eleve in eleves:
            classe = (eleve.get("classe") or {}).get("libelle") or (eleve.get("classe") or {}).get("code") or ""
            resultat.append(
                Enfant(
                    id=_txt(eleve.get("id")),
                    prenom=_txt(eleve.get("prenom")),
                    nom=_txt(eleve.get("nom")),
                    classe=_txt(classe),
                )
            )
        return resultat

    # Compte élève : un seul « enfant », c'est le titulaire du compte.
    classe = (compte.get("profile") or {}).get("classe") or {}
    return [
        Enfant(
            id=_txt(compte.get("id")),
            prenom=_txt(compte.get("prenom")) or _txt(type_compte),
            nom=_txt(compte.get("nom")),
            classe=_txt(classe.get("libelle") or classe.get("code")),
        )
    ]


def identifiant_messagerie(compte: dict[str, Any]) -> tuple[str, str]:
    """Renvoie (id, type) à utiliser pour la messagerie."""
    if (compte.get("profile") or {}).get("eleves"):
        return _txt(compte.get("id")), "famille"
    return _txt(compte.get("id")), "eleve"


# --------------------------------------------------------------------------- emploi du temps


def normaliser_cours(enfant: Enfant, brut: Iterable[dict[str, Any]]) -> list[Cours]:
    cours = []
    for item in brut:
        jour, debut = _horodatage(_premier(item, "start_date", "startDate", "debut"))
        _, fin = _horodatage(_premier(item, "end_date", "endDate", "fin"))
        if not jour:
            continue
        cours.append(
            Cours(
                enfant=enfant.prenom,
                date=jour,
                debut=debut,
                fin=fin,
                matiere=_txt(_premier(item, "matiere", "text", "codeMatiere")),
                professeur=_txt(_premier(item, "prof", "nomProf", "professeur")),
                salle=_txt(_premier(item, "salle", "room")),
                annule=bool(_premier(item, "isAnnule", "annule", defaut=False)),
            )
        )
    cours.sort(key=lambda c: (c.date, c.debut))
    return cours


# --------------------------------------------------------------------------- devoirs


def dates_avec_travail(apercu: dict[str, Any]) -> list[str]:
    """Le cahier de texte global renvoie un dictionnaire {date: [matières]}."""
    return sorted(cle for cle in apercu.keys() if re.fullmatch(r"\d{4}-\d{2}-\d{2}", _txt(cle)))


def normaliser_devoirs_du_jour(enfant: Enfant, pour_le: str, detail: dict[str, Any]) -> list[Devoir]:
    devoirs = []
    for matiere in detail.get("matieres") or []:
        a_faire = matiere.get("aFaire")
        if not a_faire:
            continue
        devoirs.append(
            Devoir(
                enfant=enfant.prenom,
                pour_le=pour_le,
                matiere=_txt(_premier(matiere, "matiere", "codeMatiere")),
                contenu=texte_message(a_faire.get("contenu")),
                donne_le=_txt(a_faire.get("donneLe")),
                effectue=bool(a_faire.get("effectue")),
                interrogation=bool(_premier(matiere, "interrogation", defaut=a_faire.get("interrogation") or False)),
            )
        )
    return devoirs


# --------------------------------------------------------------------------- notes


def normaliser_notes(enfant: Enfant, donnees: dict[str, Any]) -> list[Note]:
    resultat = []
    for note in donnees.get("notes") or []:
        if note.get("enLettre") or _txt(note.get("valeur")).lower() in ("", "disp", "abs"):
            continue
        resultat.append(
            Note(
                enfant=enfant.prenom,
                date=_txt(_premier(note, "date", "dateSaisie"))[:10],
                matiere=_txt(_premier(note, "libelleMatiere", "codeMatiere")),
                libelle=_txt(_premier(note, "devoir", "libelle")),
                valeur=_txt(note.get("valeur")),
                bareme=_txt(_premier(note, "noteSur", "bareme", defaut="20")),
                coefficient=_txt(_premier(note, "coef", defaut="1")),
                moyenne_classe=_txt(note.get("moyenneClasse")),
            )
        )
    resultat.sort(key=lambda n: n.date, reverse=True)
    return resultat


# --------------------------------------------------------------------------- vie scolaire


def normaliser_vie_scolaire(enfant: Enfant, donnees: dict[str, Any]) -> list[FaitViesScolaire]:
    faits = []
    for item in donnees.get("absencesRetards") or []:
        debut, heure = _horodatage(_premier(item, "date", "displayDate"))
        fin, _ = _horodatage(_premier(item, "dateFin", "displayDateFin"))
        faits.append(
            FaitViesScolaire(
                enfant=enfant.prenom,
                type=_txt(_premier(item, "typeElement", "type", defaut="Absence")),
                date_debut=f"{debut} {heure}".strip(),
                date_fin=fin,
                motif=_txt(_premier(item, "motif", "libelle")),
                justifie=bool(item.get("justifie")),
                commentaire=_txt(item.get("commentaire")),
            )
        )
    for item in donnees.get("sanctionsEncouragements") or []:
        debut, _ = _horodatage(_premier(item, "date", "displayDate"))
        faits.append(
            FaitViesScolaire(
                enfant=enfant.prenom,
                type=_txt(_premier(item, "typeElement", "type", defaut="Sanction")),
                date_debut=debut,
                motif=_txt(_premier(item, "motif", "libelle")),
                commentaire=_txt(item.get("commentaire")),
            )
        )
    faits.sort(key=lambda f: f.date_debut, reverse=True)
    return faits


# --------------------------------------------------------------------------- messagerie


def _nom_expediteur(source: dict[str, Any]) -> str:
    if not isinstance(source, dict):
        return _txt(source)
    parties = [
        _txt(source.get("civilite")),
        _txt(source.get("prenom")),
        _txt(source.get("particule")),
        _txt(source.get("nom")),
    ]
    nom = " ".join(p for p in parties if p)
    fonction = _txt(source.get("fonctionPersonnel"))
    return f"{nom} — {fonction}" if fonction else nom


def normaliser_messages(donnees: dict[str, Any]) -> list[Message]:
    bloc = donnees.get("messages")
    recus = bloc.get("received") if isinstance(bloc, dict) else bloc
    messages = []
    for item in recus or []:
        jour, heure = _horodatage(item.get("date"))
        messages.append(
            Message(
                id=_txt(_premier(item, "id", "idDefinitif")),
                date=f"{jour} {heure}".strip(),
                expediteur=_nom_expediteur(item.get("from") or {}),
                sujet=_txt(item.get("subject")),
                lu=bool(item.get("read")),
            )
        )
    messages.sort(key=lambda m: m.date, reverse=True)
    return messages


def extraire_dates_cles(message: Message, corps: str, aujourdhui: date) -> list[DateCle]:
    """Repère les échéances annoncées dans un message (réunion, sortie, date limite…)."""
    texte = f"{message.sujet}\n{corps}"
    minuscule = texte.lower()
    if not any(mot in minuscule for mot in MOTS_ECHEANCE):
        return []

    trouvees: dict[str, DateCle] = {}

    def _ajouter(jour: date, contexte: str) -> None:
        # On ignore le passé lointain : un message peut citer une date de l'an dernier.
        if jour < aujourdhui - timedelta(days=1) or jour > aujourdhui + timedelta(days=365):
            return
        intitule = re.sub(r"\s+", " ", contexte).strip()[:160] or message.sujet
        cle = jour.isoformat()
        trouvees.setdefault(cle, DateCle(date=cle, intitule=intitule, source=f"Message — {message.expediteur}"))

    for correspondance in re.finditer(
        r"(\d{1,2})\s+(" + "|".join(MOIS) + r")(?:\s+(\d{4}))?", minuscule
    ):
        jour_num, mois_nom, annee = correspondance.groups()
        annee_num = int(annee) if annee else aujourdhui.year
        try:
            jour = date(annee_num, MOIS[mois_nom], int(jour_num))
        except ValueError:
            continue
        if not annee and jour < aujourdhui - timedelta(days=30):
            jour = date(annee_num + 1, MOIS[mois_nom], int(jour_num))
        debut = max(0, correspondance.start() - 70)
        _ajouter(jour, texte[debut : correspondance.end() + 40])

    for correspondance in re.finditer(r"\b(\d{1,2})/(\d{1,2})(?:/(\d{2,4}))?\b", texte):
        jour_num, mois_num, annee = correspondance.groups()
        annee_num = int(annee) if annee else aujourdhui.year
        if annee_num < 100:
            annee_num += 2000
        try:
            jour = date(annee_num, int(mois_num), int(jour_num))
        except ValueError:
            continue
        debut = max(0, correspondance.start() - 70)
        _ajouter(jour, texte[debut : correspondance.end() + 40])

    return list(trouvees.values())


# --------------------------------------------------------------------------- orchestration


def tout_collecter(
    client: ClientED,
    compte: dict[str, Any],
    aujourdhui: date | None = None,
    jours_avant: int = 14,
    jours_apres: int = 30,
    messages_a_ouvrir: int = 15,
) -> Collecte:
    """Un passage complet. Une ressource en échec n'interrompt pas les autres."""
    aujourdhui = aujourdhui or date.today()
    debut = aujourdhui - timedelta(days=jours_avant)
    fin = aujourdhui + timedelta(days=jours_apres)

    collecte = Collecte(enfants=enfants_du_compte(compte))

    for enfant in collecte.enfants:
        _collecter_enfant(client, collecte, enfant, aujourdhui, debut, fin)

    _collecter_messagerie(client, collecte, compte, aujourdhui, messages_a_ouvrir)
    return collecte


def _collecter_enfant(
    client: ClientED, collecte: Collecte, enfant: Enfant, aujourdhui: date, debut: date, fin: date
) -> None:
    def _tenter(libelle: str, action) -> Any:
        try:
            return action()
        except ErreurEcoleDirecte as exc:
            message = f"{libelle} pour {enfant.prenom} : {exc}"
            log.warning(message)
            collecte.erreurs.append(message)
            return None

    edt = _tenter(
        "Emploi du temps",
        lambda: client.emploi_du_temps(enfant.id, debut.isoformat(), fin.isoformat()),
    )
    if edt:
        collecte.cours.extend(normaliser_cours(enfant, edt))

    apercu = _tenter("Cahier de texte", lambda: client.cahier_de_texte(enfant.id))
    if apercu:
        for jour in dates_avec_travail(apercu):
            jour_date = datetime.strptime(jour, "%Y-%m-%d").date()
            if not debut <= jour_date <= fin:
                continue
            detail = _tenter(
                f"Devoirs du {jour}", lambda j=jour: client.cahier_de_texte_du_jour(enfant.id, j)
            )
            if detail:
                collecte.devoirs.extend(normaliser_devoirs_du_jour(enfant, jour, detail))

    notes = _tenter("Notes", lambda: client.notes(enfant.id))
    if notes:
        collecte.notes.extend(normaliser_notes(enfant, notes))

    vie = _tenter("Vie scolaire", lambda: client.vie_scolaire(enfant.id))
    if vie:
        collecte.vie_scolaire.extend(normaliser_vie_scolaire(enfant, vie))


def _collecter_messagerie(
    client: ClientED, collecte: Collecte, compte: dict[str, Any], aujourdhui: date, a_ouvrir: int
) -> None:
    compte_id, type_compte = identifiant_messagerie(compte)
    try:
        donnees = client.messages(compte_id, type_compte)
    except ErreurEcoleDirecte as exc:
        collecte.erreurs.append(f"Messagerie : {exc}")
        return

    collecte.messages = normaliser_messages(donnees)

    # On n'ouvre que les messages récents : c'est là que se cachent les dates à retenir.
    for message in collecte.messages[:a_ouvrir]:
        try:
            detail = client.message(compte_id, message.id, type_compte)
        except ErreurEcoleDirecte as exc:
            collecte.erreurs.append(f"Message {message.id} : {exc}")
            continue
        corps = texte_message(detail.get("content"))
        message.extrait = corps[:400]
        collecte.dates_cles.extend(extraire_dates_cles(message, corps, aujourdhui))

    vues: set[str] = set()
    uniques = []
    for item in sorted(collecte.dates_cles, key=lambda d: d.date):
        if item.cle in vues:
            continue
        vues.add(item.cle)
        uniques.append(item)
    collecte.dates_cles = uniques
