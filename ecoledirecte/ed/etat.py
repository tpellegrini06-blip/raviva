"""Mémoire entre deux passages : c'est ce qui permet de dire « ça a changé depuis hier »."""

from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .models import Collecte

FICHIER_ETAT = "instantane.json"


class Changements:
    def __init__(self) -> None:
        self.nouveaux: list[Any] = []
        self.modifies: list[tuple[Any, str]] = []   # (élément, empreinte précédente)
        self.disparus: list[dict[str, Any]] = []

    @property
    def vide(self) -> bool:
        return not (self.nouveaux or self.modifies or self.disparus)

    def par_type(self, prefixe: str) -> list[Any]:
        return [item for item in self.nouveaux if item.cle.startswith(prefixe)]

    def modifies_par_type(self, prefixe: str) -> list[tuple[Any, str]]:
        return [couple for couple in self.modifies if couple[0].cle.startswith(prefixe)]


def _chemin(dossier: Path) -> Path:
    return Path(dossier) / FICHIER_ETAT


def charger_instantane(dossier: Path) -> dict[str, Any]:
    chemin = _chemin(dossier)
    if not chemin.exists():
        return {}
    try:
        return json.loads(chemin.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        # Un état corrompu ne doit pas bloquer le passage du matin : on repart de zéro.
        return {}


def enregistrer_instantane(dossier: Path, collecte: Collecte) -> None:
    Path(dossier).mkdir(parents=True, exist_ok=True)
    elements = {item.cle: item.empreinte for item in collecte.tous_les_elements()}
    charge = {
        "enregistre_le": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "elements": elements,
        "contenu": collecte.en_dict(),
    }
    _chemin(dossier).write_text(json.dumps(charge, ensure_ascii=False, indent=2), encoding="utf-8")


def comparer(precedent: dict[str, Any], collecte: Collecte) -> Changements:
    changements = Changements()
    connus: dict[str, str] = precedent.get("elements") or {}

    # Premier passage : tout est « nouveau », ce qui noierait le brief. On ne signale rien.
    if not connus:
        return changements

    actuels = {item.cle: item for item in collecte.tous_les_elements()}
    for cle, item in actuels.items():
        if cle not in connus:
            changements.nouveaux.append(item)
        elif connus[cle] != item.empreinte:
            changements.modifies.append((item, connus[cle]))

    for cle in connus:
        if cle not in actuels and cle.startswith(("cours|", "devoir|")):
            changements.disparus.append({"cle": cle, "empreinte": connus[cle]})

    return changements


def archiver(dossier: Path, collecte: Collecte, horodatage: str) -> Path:
    """Garde une trace datée de chaque passage, utile pour reconstituer l'historique."""
    archives = Path(dossier) / "archives"
    archives.mkdir(parents=True, exist_ok=True)
    chemin = archives / f"{horodatage}.json"
    chemin.write_text(json.dumps(collecte.en_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
    return chemin


def purger_archives(dossier: Path, a_conserver: int = 60) -> None:
    archives = sorted((Path(dossier) / "archives").glob("*.json"))
    for ancienne in archives[:-a_conserver]:
        ancienne.unlink(missing_ok=True)
