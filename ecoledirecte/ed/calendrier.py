"""Export iCalendar : le planning des enfants, abonnable depuis un téléphone."""

from __future__ import annotations

import hashlib
from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from .models import Collecte

PLIAGE = 73  # une ligne iCalendar ne doit pas dépasser 75 octets


def _echapper(texte: str) -> str:
    return (
        (texte or "")
        .replace("\\", "\\\\")
        .replace(";", "\;")
        .replace(",", "\\,")
        .replace("\n", "\\n")
    )


def _plier(ligne: str) -> list[str]:
    if len(ligne.encode("utf-8")) <= PLIAGE:
        return [ligne]
    morceaux = []
    courant = ""
    for caractere in ligne:
        if len((courant + caractere).encode("utf-8")) > PLIAGE:
            morceaux.append(courant)
            courant = " " + caractere
        else:
            courant += caractere
    morceaux.append(courant)
    return morceaux


def _uid(*parties: str) -> str:
    empreinte = hashlib.sha1("|".join(parties).encode("utf-8")).hexdigest()[:20]
    return f"{empreinte}@ecoledirecte.local"


def _utc(jour: str, heure: str, fuseau: ZoneInfo) -> str:
    moment = datetime.strptime(f"{jour} {heure or '00:00'}", "%Y-%m-%d %H:%M").replace(tzinfo=fuseau)
    return moment.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def construire(collecte: Collecte, nom_fuseau: str = "Europe/Paris", rappel_devoirs: bool = True) -> str:
    fuseau = ZoneInfo(nom_fuseau)
    maintenant = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    lignes = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//raviva//ecoledirecte//FR",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "X-WR-CALNAME:École Directe — enfants",
        f"X-WR-TIMEZONE:{nom_fuseau}",
    ]

    for cours in collecte.cours:
        if not cours.debut or not cours.fin:
            continue
        resume = f"{cours.enfant} · {cours.matiere}"
        if cours.annule:
            resume = f"[ANNULÉ] {resume}"
        description = " — ".join(p for p in (cours.professeur, cours.salle) if p)
        lignes += [
            "BEGIN:VEVENT",
            f"UID:{_uid('cours', cours.enfant, cours.date, cours.debut, cours.matiere)}",
            f"DTSTAMP:{maintenant}",
            f"DTSTART:{_utc(cours.date, cours.debut, fuseau)}",
            f"DTEND:{_utc(cours.date, cours.fin, fuseau)}",
            f"SUMMARY:{_echapper(resume)}",
            f"LOCATION:{_echapper(cours.salle)}",
            f"DESCRIPTION:{_echapper(description)}",
            f"STATUS:{'CANCELLED' if cours.annule else 'CONFIRMED'}",
            "END:VEVENT",
        ]

    for devoir in collecte.devoirs:
        if devoir.effectue:
            continue
        try:
            jour = datetime.strptime(devoir.pour_le, "%Y-%m-%d").date()
        except ValueError:
            continue
        prefixe = "Interro" if devoir.interrogation else "Devoir"
        lignes += [
            "BEGIN:VEVENT",
            f"UID:{_uid('devoir', devoir.enfant, devoir.pour_le, devoir.matiere)}",
            f"DTSTAMP:{maintenant}",
            f"DTSTART;VALUE=DATE:{jour.strftime('%Y%m%d')}",
            f"DTEND;VALUE=DATE:{(jour + timedelta(days=1)).strftime('%Y%m%d')}",
            f"SUMMARY:{_echapper(f'{prefixe} — {devoir.enfant} · {devoir.matiere}')}",
            f"DESCRIPTION:{_echapper(devoir.contenu)}",
            "TRANSP:TRANSPARENT",
        ]
        if rappel_devoirs and devoir.interrogation:
            lignes += [
                "BEGIN:VALARM",
                "TRIGGER:-P1D",
                "ACTION:DISPLAY",
                f"DESCRIPTION:{_echapper(f'Interrogation demain — {devoir.enfant} {devoir.matiere}')}",
                "END:VALARM",
            ]
        lignes.append("END:VEVENT")

    for echeance in collecte.dates_cles:
        try:
            jour = datetime.strptime(echeance.date, "%Y-%m-%d").date()
        except ValueError:
            continue
        lignes += [
            "BEGIN:VEVENT",
            f"UID:{_uid('datecle', echeance.date, echeance.intitule[:60])}",
            f"DTSTAMP:{maintenant}",
            f"DTSTART;VALUE=DATE:{jour.strftime('%Y%m%d')}",
            f"DTEND;VALUE=DATE:{(jour + timedelta(days=1)).strftime('%Y%m%d')}",
            f"SUMMARY:{_echapper('École — ' + echeance.intitule[:70])}",
            f"DESCRIPTION:{_echapper(echeance.intitule + chr(10) + echeance.source)}",
            "TRANSP:TRANSPARENT",
            "END:VEVENT",
        ]

    lignes.append("END:VCALENDAR")

    pliees: list[str] = []
    for ligne in lignes:
        pliees.extend(_plier(ligne))
    return "\r\n".join(pliees) + "\r\n"
