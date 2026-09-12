"""Toutes les URLs de l'API interne École Directe, regroupées ici.

L'API n'est pas publique : elle change sans préavis. Quand quelque chose casse,
c'est presque toujours ce fichier (ou VERSION) qu'il faut corriger, et rien d'autre.
Pour retrouver la bonne valeur : ouvrir www.ecoledirecte.com dans un navigateur,
onglet Réseau, et lire le paramètre `v=` des requêtes vers api.ecoledirecte.com.
"""

BASE = "https://api.ecoledirecte.com/v3"

# Numéro de version envoyé dans le paramètre ?v= — à remonter quand l'API évolue.
VERSION = "4.80.0"

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)

LOGIN = "/login.awp"
DOUBLE_AUTH = "/connexion/doubleauth.awp"


def cahier_de_texte(eleve_id: str) -> str:
    """Vue d'ensemble : quelles dates portent du travail à faire."""
    return f"/Eleves/{eleve_id}/cahierdetexte.awp"


def cahier_de_texte_du_jour(eleve_id: str, date: str) -> str:
    """Détail du travail pour une date donnée (YYYY-MM-DD)."""
    return f"/Eleves/{eleve_id}/cahierdetexte/{date}.awp"


def notes(eleve_id: str) -> str:
    return f"/Eleves/{eleve_id}/notes.awp"


def vie_scolaire(eleve_id: str) -> str:
    """Absences, retards, sanctions, encouragements."""
    return f"/eleves/{eleve_id}/viescolaire.awp"


def emploi_du_temps(eleve_id: str) -> str:
    return f"/E/{eleve_id}/emploidutemps.awp"


def timeline(eleve_id: str) -> str:
    return f"/eleves/{eleve_id}/timeline.awp"


def messages(compte_id: str, type_compte: str = "famille") -> str:
    segment = "familles" if type_compte == "famille" else "eleves"
    return f"/{segment}/{compte_id}/messages.awp"


def message(compte_id: str, message_id: str, type_compte: str = "famille") -> str:
    segment = "familles" if type_compte == "famille" else "eleves"
    return f"/{segment}/{compte_id}/messages/{message_id}.awp"
