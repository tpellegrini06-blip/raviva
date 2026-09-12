#!/usr/bin/env python3
"""Envoie le brief par mail. Sans configuration SMTP, ne fait rien et ne bloque pas.

    python envoyer_mail.py sortie/brief.md
"""

from __future__ import annotations

import os
import smtplib
import sys
from email.message import EmailMessage
from pathlib import Path


def main() -> int:
    chemin = Path(sys.argv[1] if len(sys.argv) > 1 else "sortie/brief.md")
    if not chemin.exists():
        print(f"Rien à envoyer : {chemin} est absent.")
        return 0

    hote = os.environ.get("ED_SMTP_HOTE", "").strip()
    utilisateur = os.environ.get("ED_SMTP_UTILISATEUR", "").strip()
    mot_de_passe = os.environ.get("ED_SMTP_MOT_DE_PASSE", "")
    destinataire = os.environ.get("ED_MAIL_DESTINATAIRE", "").strip()
    if not all((hote, utilisateur, mot_de_passe, destinataire)):
        print("SMTP non configuré : envoi ignoré.")
        return 0

    texte = chemin.read_text(encoding="utf-8")
    premiere_ligne = texte.splitlines()[0].lstrip("# ").strip() if texte.strip() else "Brief École Directe"

    message = EmailMessage()
    message["Subject"] = premiere_ligne
    message["From"] = utilisateur
    message["To"] = destinataire
    message.set_content(texte)

    calendrier = chemin.parent / "ecoledirecte.ics"
    if calendrier.exists():
        message.add_attachment(
            calendrier.read_bytes(), maintype="text", subtype="calendar", filename="ecoledirecte.ics"
        )

    port = int(os.environ.get("ED_SMTP_PORT", "587"))
    with smtplib.SMTP(hote, port, timeout=30) as serveur:
        serveur.starttls()
        serveur.login(utilisateur, mot_de_passe)
        serveur.send_message(message)

    print(f"Brief envoyé à {destinataire}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
