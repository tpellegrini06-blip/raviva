"""Rédaction du compte rendu : ce que la famille lit réellement le matin."""

from __future__ import annotations

from datetime import date, datetime, timedelta

from .etat import Changements
from .models import Collecte, Cours, DateCle, Devoir, FaitViesScolaire, Message, Note

JOURS = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
MOIS = [
    "janvier", "février", "mars", "avril", "mai", "juin",
    "juillet", "août", "septembre", "octobre", "novembre", "décembre",
]


def date_longue(jour: date) -> str:
    return f"{JOURS[jour.weekday()]} {jour.day} {MOIS[jour.month - 1]}"


def _jour(valeur: str) -> date | None:
    try:
        return datetime.strptime(valeur[:10], "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


def _heure(valeur: str) -> str:
    return valeur.replace(":", "h") if valeur else ""


def _extrait(texte: str, longueur: int = 180) -> str:
    propre = " ".join((texte or "").split())
    return propre if len(propre) <= longueur else propre[: longueur - 1] + "…"


# --------------------------------------------------------------------------- sélections


def devoirs_pour(collecte: Collecte, enfant: str, jour: date) -> list[Devoir]:
    return [d for d in collecte.devoirs if d.enfant == enfant and _jour(d.pour_le) == jour]


def devoirs_a_venir(collecte: Collecte, enfant: str, depuis: date, jusqua: date) -> list[Devoir]:
    resultat = [
        d
        for d in collecte.devoirs
        if d.enfant == enfant and (j := _jour(d.pour_le)) and depuis < j <= jusqua
    ]
    return sorted(resultat, key=lambda d: d.pour_le)


def devoirs_en_retard(collecte: Collecte, enfant: str, aujourdhui: date) -> list[Devoir]:
    """Travail dont la date est passée et qui n'a jamais été coché comme fait."""
    resultat = [
        d
        for d in collecte.devoirs
        if d.enfant == enfant
        and not d.effectue
        and (j := _jour(d.pour_le))
        and j < aujourdhui
    ]
    return sorted(resultat, key=lambda d: d.pour_le, reverse=True)


def cours_du_jour(collecte: Collecte, enfant: str, jour: date) -> list[Cours]:
    return sorted(
        (c for c in collecte.cours if c.enfant == enfant and _jour(c.date) == jour),
        key=lambda c: c.debut,
    )


# --------------------------------------------------------------------------- rendu


def construire(
    collecte: Collecte,
    changements: Changements,
    aujourdhui: date | None = None,
    moment: str = "",
) -> str:
    aujourdhui = aujourdhui or date.today()
    demain = aujourdhui + timedelta(days=1)
    lignes: list[str] = []

    entete = f"# Brief École Directe — {date_longue(aujourdhui)}"
    if moment:
        entete += f" ({moment})"
    lignes += [entete, ""]

    urgences = _urgences(collecte, changements, aujourdhui)
    if urgences:
        lignes += ["## À traiter aujourd'hui", ""]
        lignes += [f"- {u}" for u in urgences]
        lignes.append("")

    bloc_changements = _bloc_changements(changements)
    if bloc_changements:
        lignes += ["## Ce qui a changé depuis le dernier passage", ""] + bloc_changements + [""]

    for enfant in collecte.enfants:
        lignes += _bloc_enfant(collecte, enfant.prenom, enfant.libelle, aujourdhui, demain)

    lignes += _bloc_calendrier(collecte, aujourdhui)
    lignes += _bloc_messagerie(collecte)

    if collecte.erreurs:
        lignes += ["## Incidents techniques", ""]
        lignes += [f"- {e}" for e in collecte.erreurs]
        lignes.append("")

    return "\n".join(lignes).rstrip() + "\n"


def _urgences(collecte: Collecte, changements: Changements, aujourdhui: date) -> list[str]:
    urgences: list[str] = []

    for enfant in collecte.enfants:
        retards = devoirs_en_retard(collecte, enfant.prenom, aujourdhui)
        if retards:
            matieres = ", ".join(sorted({d.matiere for d in retards})[:4])
            urgences.append(
                f"**{enfant.prenom}** : {len(retards)} devoir(s) jamais cochés comme faits ({matieres})"
            )
        interros = [
            d
            for d in devoirs_a_venir(collecte, enfant.prenom, aujourdhui - timedelta(days=1), aujourdhui + timedelta(days=2))
            if d.interrogation
        ]
        for interro in interros:
            quand = _jour(interro.pour_le)
            urgences.append(
                f"**{enfant.prenom}** : interrogation de {interro.matiere} "
                f"{'aujourd’hui' if quand == aujourdhui else date_longue(quand) if quand else interro.pour_le}"
            )

    for fait in changements.par_type("vie|"):
        if isinstance(fait, FaitViesScolaire) and not fait.justifie:
            urgences.append(
                f"**{fait.enfant}** : {fait.type.lower()} du {fait.date_debut} à justifier"
            )

    for message in changements.par_type("message|"):
        if isinstance(message, Message) and not message.lu:
            urgences.append(f"Message non lu — {message.expediteur} : {message.sujet}")

    proches = [
        d
        for d in collecte.dates_cles
        if (j := _jour(d.date)) and aujourdhui <= j <= aujourdhui + timedelta(days=3)
    ]
    for echeance in proches:
        jour = _jour(echeance.date)
        urgences.append(f"{date_longue(jour) if jour else echeance.date} — {_extrait(echeance.intitule, 120)}")

    return urgences


def _bloc_changements(changements: Changements) -> list[str]:
    if changements.vide:
        return []
    lignes: list[str] = []

    annules = [c for c in changements.nouveaux + [m[0] for m in changements.modifies]
               if isinstance(c, Cours) and c.annule]
    for cours in annules:
        lignes.append(f"- Cours annulé — {cours.enfant}, {cours.date} {_heure(cours.debut)} {cours.matiere}")

    for cours, _ in changements.modifies_par_type("cours|"):
        if isinstance(cours, Cours) and not cours.annule:
            salle = f", salle {cours.salle}" if cours.salle else ""
            lignes.append(
                f"- Cours modifié — {cours.enfant}, {cours.date} {_heure(cours.debut)} {cours.matiere}{salle}"
            )

    for devoir in changements.par_type("devoir|"):
        if isinstance(devoir, Devoir):
            marque = " (interrogation)" if devoir.interrogation else ""
            lignes.append(
                f"- Nouveau devoir — {devoir.enfant}, {devoir.matiere} pour le {devoir.pour_le}{marque} : "
                f"{_extrait(devoir.contenu, 120)}"
            )

    for note in changements.par_type("note|"):
        if isinstance(note, Note):
            moyenne = f" (moyenne classe {note.moyenne_classe})" if note.moyenne_classe else ""
            lignes.append(
                f"- Nouvelle note — {note.enfant}, {note.matiere} : {note.valeur}/{note.bareme}"
                f" « {note.libelle} »{moyenne}"
            )

    for fait in changements.par_type("vie|"):
        if isinstance(fait, FaitViesScolaire):
            etat = "justifiée" if fait.justifie else "à justifier"
            lignes.append(f"- {fait.type} — {fait.enfant}, {fait.date_debut} ({etat}) {fait.motif}".rstrip())

    for message in changements.par_type("message|"):
        if isinstance(message, Message):
            lignes.append(f"- Nouveau message — {message.expediteur} : {message.sujet}")

    for echeance in changements.par_type("datecle|"):
        if isinstance(echeance, DateCle):
            lignes.append(f"- Date repérée — {echeance.date} : {_extrait(echeance.intitule, 120)}")

    return lignes


def _bloc_enfant(
    collecte: Collecte, prenom: str, libelle: str, aujourdhui: date, demain: date
) -> list[str]:
    lignes = [f"## {libelle}", ""]

    for jour, titre in ((aujourdhui, "Aujourd'hui"), (demain, "Demain")):
        cours = cours_du_jour(collecte, prenom, jour)
        if cours:
            lignes.append(f"**{titre} — {date_longue(jour)}**")
            lignes.append("")
            for c in cours:
                marque = " — ANNULÉ" if c.annule else ""
                salle = f" · {c.salle}" if c.salle else ""
                lignes.append(f"- {_heure(c.debut)}–{_heure(c.fin)} {c.matiere}{salle}{marque}")
            lignes.append("")

    for jour, titre in ((aujourdhui, "Devoirs pour aujourd'hui"), (demain, "Devoirs pour demain")):
        devoirs = devoirs_pour(collecte, prenom, jour)
        if devoirs:
            lignes += [f"**{titre}**", ""]
            for d in devoirs:
                etat = "fait" if d.effectue else "à faire"
                marque = " ⚠ interrogation" if d.interrogation else ""
                lignes.append(f"- {d.matiere} ({etat}){marque} — {_extrait(d.contenu)}")
            lignes.append("")

    suite = devoirs_a_venir(collecte, prenom, demain, aujourdhui + timedelta(days=10))
    if suite:
        lignes += ["**À venir (10 jours)**", ""]
        for d in suite:
            marque = " ⚠ interrogation" if d.interrogation else ""
            lignes.append(f"- {d.pour_le} · {d.matiere}{marque} — {_extrait(d.contenu, 110)}")
        lignes.append("")

    retards = devoirs_en_retard(collecte, prenom, aujourdhui)
    if retards:
        lignes += ["**Devoirs jamais cochés comme faits**", ""]
        for d in retards[:10]:
            lignes.append(f"- {d.pour_le} · {d.matiere} — {_extrait(d.contenu, 110)}")
        lignes.append("")

    recents = [
        f
        for f in collecte.vie_scolaire
        if f.enfant == prenom and (j := _jour(f.date_debut)) and j >= aujourdhui - timedelta(days=21)
    ]
    if recents:
        lignes += ["**Vie scolaire (3 dernières semaines)**", ""]
        for f in recents:
            etat = "justifiée" if f.justifie else "NON justifiée"
            lignes.append(f"- {f.date_debut} · {f.type} — {etat} {f.motif}".rstrip())
        lignes.append("")

    notes = [n for n in collecte.notes if n.enfant == prenom][:6]
    if notes:
        lignes += ["**Dernières notes**", ""]
        for n in notes:
            moyenne = f" · classe {n.moyenne_classe}" if n.moyenne_classe else ""
            lignes.append(f"- {n.date} · {n.matiere} : {n.valeur}/{n.bareme} « {n.libelle} »{moyenne}")
        lignes.append("")

    return lignes


def _bloc_calendrier(collecte: Collecte, aujourdhui: date) -> list[str]:
    horizon = aujourdhui + timedelta(days=45)
    entrees: list[tuple[str, str, str]] = []

    for echeance in collecte.dates_cles:
        jour = _jour(echeance.date)
        if jour and aujourdhui <= jour <= horizon:
            entrees.append((echeance.date, _extrait(echeance.intitule, 110), echeance.source))

    for devoir in collecte.devoirs:
        jour = _jour(devoir.pour_le)
        if devoir.interrogation and jour and aujourdhui <= jour <= horizon:
            entrees.append((devoir.pour_le, f"Interrogation {devoir.matiere}", devoir.enfant))

    if not entrees:
        return []

    entrees.sort(key=lambda e: e[0])
    lignes = ["## Calendrier des prochaines semaines", "", "| Date | Quoi | Source |", "| --- | --- | --- |"]
    for jour, quoi, source in entrees:
        lignes.append(f"| {jour} | {quoi.replace('|', '/')} | {source.replace('|', '/')} |")
    lignes.append("")
    return lignes


def _bloc_messagerie(collecte: Collecte) -> list[str]:
    non_lus = [m for m in collecte.messages if not m.lu]
    if not non_lus:
        return []
    lignes = ["## Messagerie — non lus", ""]
    for message in non_lus[:15]:
        lignes.append(f"- **{message.date}** — {message.expediteur} : {message.sujet}")
        if message.extrait:
            lignes.append(f"  > {_extrait(message.extrait, 200)}")
    lignes.append("")
    return lignes
