#!/usr/bin/env python3
"""Étape unique et interactive : répondre à la question de sécurité École Directe.

Elle produit un couple cn/cv à stocker comme secret (ED_FA_CN / ED_FA_CV).
Tant qu'il est valide, les passages automatiques se connectent sans question.
Quand École Directe repose la question, il suffit de relancer ce script.

    python bootstrap_2fa.py
"""

from __future__ import annotations

import getpass
import os
import sys

from ed.client import ClientED, DoubleAuthRequise, ErreurEcoleDirecte


def main() -> int:
    identifiant = os.environ.get("ED_IDENTIFIANT") or input("Identifiant École Directe : ").strip()
    mot_de_passe = os.environ.get("ED_MOT_DE_PASSE") or getpass.getpass("Mot de passe : ")

    client = ClientED(identifiant, mot_de_passe)

    try:
        client.connexion()
    except DoubleAuthRequise:
        pass  # attendu : c'est précisément ce qu'on vient régler
    except ErreurEcoleDirecte as exc:
        print(f"Connexion refusée : {exc}", file=sys.stderr)
        return 1
    else:
        print("Le compte ne demande pas de double authentification : aucun couple cn/cv nécessaire.")
        return 0

    try:
        question, propositions = client.question_double_auth()
    except ErreurEcoleDirecte as exc:
        print(f"Impossible de récupérer la question de sécurité : {exc}", file=sys.stderr)
        return 1

    print(f"\nQuestion : {question}\n")
    for index, proposition in enumerate(propositions, start=1):
        print(f"  {index}. {proposition}")

    while True:
        saisie = input("\nNuméro de la bonne réponse : ").strip()
        if saisie.isdigit() and 1 <= int(saisie) <= len(propositions):
            choix = propositions[int(saisie) - 1]
            break
        print("Numéro invalide.")

    try:
        couple = client.repondre_double_auth(choix)
    except ErreurEcoleDirecte as exc:
        print(f"Réponse refusée : {exc}", file=sys.stderr)
        return 1

    try:
        client.fa = [couple]
        compte = client.connexion()
    except ErreurEcoleDirecte as exc:
        print(f"Le couple a été délivré mais la reconnexion échoue : {exc}", file=sys.stderr)
        return 1

    eleves = (compte.get("profile") or {}).get("eleves") or []
    print("\nConnexion validée.")
    if eleves:
        for eleve in eleves:
            classe = (eleve.get("classe") or {}).get("libelle", "")
            print(f"  • {eleve.get('prenom')} {eleve.get('nom')} — {classe}")

    print("\nEnregistre ces deux valeurs comme secrets (jamais dans le dépôt) :\n")
    print(f"  ED_FA_CN={couple['cn']}")
    print(f"  ED_FA_CV={couple['cv']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
