#!/usr/bin/env python3
"""Passage automatique : collecte École Directe, compare à l'état précédent, écrit le brief.

    python run.py                 # brief complet (le matin)
    python run.py --changements   # uniquement ce qui a bougé (passages de la journée)
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from datetime import date, datetime

from ed import brief, calendrier, collecte as module_collecte, config, etat
from ed.client import ClientED, DoubleAuthRequise, ErreurEcoleDirecte, IdentifiantsInvalides

log = logging.getLogger("ecoledirecte")


def analyser_arguments() -> argparse.Namespace:
    parseur = argparse.ArgumentParser(description="Compte rendu École Directe")
    parseur.add_argument(
        "--changements",
        action="store_true",
        help="n'écrire le brief que si quelque chose a changé depuis le dernier passage",
    )
    parseur.add_argument("--moment", default="", help="libellé affiché dans le titre (ex. « 7h00 »)")
    parseur.add_argument("--jours-avant", type=int, default=14)
    parseur.add_argument("--jours-apres", type=int, default=30)
    parseur.add_argument("--verbeux", action="store_true")
    return parseur.parse_args()


def main() -> int:
    arguments = analyser_arguments()
    logging.basicConfig(
        level=logging.DEBUG if arguments.verbeux else logging.INFO,
        format="%(levelname)s %(message)s",
    )

    try:
        reglages = config.charger()
    except config.ConfigurationManquante as exc:
        log.error("%s", exc)
        return 2

    config.preparer_dossiers()
    client = ClientED(reglages.identifiant, reglages.mot_de_passe, reglages.fa)

    try:
        compte = client.connexion()
    except DoubleAuthRequise as exc:
        log.error("%s", exc)
        return 3  # code distinct : c'est le seul cas qui réclame une action humaine
    except IdentifiantsInvalides as exc:
        log.error("Identifiants refusés : %s", exc)
        return 4
    except ErreurEcoleDirecte as exc:
        log.error("Connexion impossible : %s", exc)
        return 1

    aujourdhui = date.today()
    resultat = module_collecte.tout_collecter(
        client,
        compte,
        aujourdhui=aujourdhui,
        jours_avant=arguments.jours_avant,
        jours_apres=arguments.jours_apres,
    )
    log.info(
        "Collecte : %d enfant(s), %d cours, %d devoirs, %d notes, %d messages",
        len(resultat.enfants), len(resultat.cours), len(resultat.devoirs),
        len(resultat.notes), len(resultat.messages),
    )

    precedent = etat.charger_instantane(config.DOSSIER_ETAT)
    changements = etat.comparer(precedent, resultat)

    if arguments.changements and changements.vide:
        log.info("Rien de neuf depuis le dernier passage : aucun brief écrit.")
        etat.enregistrer_instantane(config.DOSSIER_ETAT, resultat)
        return 0

    texte = brief.construire(resultat, changements, aujourdhui, arguments.moment)
    horodatage = datetime.now().strftime("%Y%m%d-%H%M")

    (config.DOSSIER_SORTIE / "brief.md").write_text(texte, encoding="utf-8")
    (config.DOSSIER_SORTIE / "donnees.json").write_text(
        json.dumps(resultat.en_dict(), ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (config.DOSSIER_SORTIE / "ecoledirecte.ics").write_text(
        calendrier.construire(resultat, reglages.fuseau), encoding="utf-8"
    )

    etat.archiver(config.DOSSIER_ETAT, resultat, horodatage)
    etat.purger_archives(config.DOSSIER_ETAT)
    etat.enregistrer_instantane(config.DOSSIER_ETAT, resultat)

    print(texte)
    if resultat.erreurs:
        log.warning("%d ressource(s) en échec — voir la section « Incidents techniques »", len(resultat.erreurs))
    return 0


if __name__ == "__main__":
    sys.exit(main())
