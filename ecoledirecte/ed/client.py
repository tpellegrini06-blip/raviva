"""Client HTTP École Directe : connexion, double authentification, appels authentifiés."""

from __future__ import annotations

import base64
import html
import json
import logging
import time
from typing import Any

import requests

from . import endpoints

log = logging.getLogger(__name__)

# Codes de retour renvoyés par l'API dans le corps JSON (le HTTP est presque toujours 200).
CODE_OK = 200
CODE_DOUBLE_AUTH = 250
CODE_IDENTIFIANTS_INVALIDES = 505
CODE_TOKEN_INVALIDE = 525


class ErreurEcoleDirecte(RuntimeError):
    def __init__(self, message: str, code: int | None = None) -> None:
        super().__init__(message)
        self.code = code


class DoubleAuthRequise(ErreurEcoleDirecte):
    """Le couple cn/cv est absent ou périmé : il faut refaire le bootstrap."""


class IdentifiantsInvalides(ErreurEcoleDirecte):
    pass


def _decode(valeur: str | None) -> str:
    """Les libellés de la double authentification arrivent en base64, parfois avec des entités HTML."""
    if not valeur:
        return ""
    try:
        texte = base64.b64decode(valeur).decode("utf-8", errors="replace")
    except Exception:  # noqa: BLE001 — valeur déjà en clair selon les versions de l'API
        texte = valeur
    return html.unescape(texte).strip()


def _encode(valeur: str) -> str:
    return base64.b64encode(valeur.encode("utf-8")).decode("ascii")


class ClientED:
    def __init__(self, identifiant: str, mot_de_passe: str, fa: list[dict[str, str]] | None = None) -> None:
        self.identifiant = identifiant
        self.mot_de_passe = mot_de_passe
        self.fa = fa or []
        self.token: str | None = None
        self.compte: dict[str, Any] = {}
        self._session = requests.Session()
        self._session.headers.update(
            {
                "User-Agent": endpoints.USER_AGENT,
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json, text/plain, */*",
                "Origin": "https://www.ecoledirecte.com",
                "Referer": "https://www.ecoledirecte.com/",
            }
        )

    # ------------------------------------------------------------------ bas niveau

    def _appel(
        self,
        chemin: str,
        donnees: dict[str, Any] | None = None,
        params: dict[str, str] | None = None,
        tolerer: tuple[int, ...] = (),
    ) -> dict[str, Any]:
        url = endpoints.BASE + chemin
        parametres = {"v": endpoints.VERSION}
        parametres.update(params or {})
        corps = "data=" + json.dumps(donnees or {}, separators=(",", ":"), ensure_ascii=False)

        entetes = {}
        if self.token:
            entetes["X-Token"] = self.token

        derniere_erreur: Exception | None = None
        for tentative in range(3):
            try:
                reponse = self._session.post(
                    url, params=parametres, data=corps.encode("utf-8"), headers=entetes, timeout=30
                )
                reponse.raise_for_status()
                charge = reponse.json()
                break
            except (requests.RequestException, ValueError) as exc:
                derniere_erreur = exc
                attente = 2 ** tentative
                log.warning("Appel %s en échec (%s), nouvelle tentative dans %ss", chemin, exc, attente)
                time.sleep(attente)
        else:
            raise ErreurEcoleDirecte(f"Appel {chemin} impossible : {derniere_erreur}")

        # L'API renvoie un token rafraîchi à chaque appel : il faut le reprendre.
        if charge.get("token"):
            self.token = charge["token"]

        code = int(charge.get("code", CODE_OK))
        if code == CODE_OK or code in tolerer:
            return charge
        if code == CODE_DOUBLE_AUTH:
            raise DoubleAuthRequise(charge.get("message") or "Double authentification requise", code)
        if code == CODE_IDENTIFIANTS_INVALIDES:
            raise IdentifiantsInvalides(charge.get("message") or "Identifiant ou mot de passe refusé", code)
        if code == CODE_TOKEN_INVALIDE:
            raise ErreurEcoleDirecte("Jeton de session invalide ou expiré", code)
        raise ErreurEcoleDirecte(f"{chemin} a répondu {code} : {charge.get('message')}", code)

    # ------------------------------------------------------------------ connexion

    def connexion(self) -> dict[str, Any]:
        """Ouvre la session. Lève DoubleAuthRequise si le couple cn/cv manque ou a expiré."""
        charge = {
            "identifiant": self.identifiant,
            "motdepasse": self.mot_de_passe,
            "isReLogin": False,
            "uuid": "",
        }
        if self.fa:
            charge["fa"] = self.fa

        reponse = self._appel(endpoints.LOGIN, charge, tolerer=(CODE_DOUBLE_AUTH,))
        if int(reponse.get("code", CODE_OK)) == CODE_DOUBLE_AUTH:
            raise DoubleAuthRequise(
                "École Directe redemande la question de sécurité : le couple cn/cv est périmé. "
                "Relance `python bootstrap_2fa.py`.",
                CODE_DOUBLE_AUTH,
            )

        comptes = (reponse.get("data") or {}).get("accounts") or []
        if not comptes:
            raise ErreurEcoleDirecte("Connexion acceptée mais aucun compte renvoyé par l'API")
        self.compte = comptes[0]
        return self.compte

    def question_double_auth(self) -> tuple[str, list[str]]:
        """Récupère la question de sécurité et ses propositions, en clair."""
        reponse = self._appel(endpoints.DOUBLE_AUTH, {}, params={"verbe": "get"})
        donnees = reponse.get("data") or {}
        question = _decode(donnees.get("question"))
        propositions = [_decode(p) for p in donnees.get("propositions") or []]
        return question, propositions

    def repondre_double_auth(self, reponse_choisie: str) -> dict[str, str]:
        """Envoie la réponse et renvoie le couple {cn, cv} à conserver comme secret."""
        reponse = self._appel(
            endpoints.DOUBLE_AUTH, {"choix": _encode(reponse_choisie)}, params={"verbe": "post"}
        )
        donnees = reponse.get("data") or {}
        if not donnees.get("cn") or not donnees.get("cv"):
            raise ErreurEcoleDirecte("Réponse acceptée mais aucun couple cn/cv renvoyé")
        self.fa = [{"cn": donnees["cn"], "cv": donnees["cv"]}]
        return {"cn": donnees["cn"], "cv": donnees["cv"]}

    # ------------------------------------------------------------------ ressources

    def cahier_de_texte(self, eleve_id: str) -> dict[str, Any]:
        return self._appel(endpoints.cahier_de_texte(eleve_id), {}, params={"verbe": "get"}).get("data") or {}

    def cahier_de_texte_du_jour(self, eleve_id: str, date: str) -> dict[str, Any]:
        chemin = endpoints.cahier_de_texte_du_jour(eleve_id, date)
        return self._appel(chemin, {}, params={"verbe": "get"}).get("data") or {}

    def notes(self, eleve_id: str, annee_scolaire: str = "") -> dict[str, Any]:
        params = {"verbe": "get"}
        if annee_scolaire:
            params["anneeScolaire"] = annee_scolaire
        return self._appel(endpoints.notes(eleve_id), {}, params=params).get("data") or {}

    def vie_scolaire(self, eleve_id: str) -> dict[str, Any]:
        return self._appel(endpoints.vie_scolaire(eleve_id), {}, params={"verbe": "get"}).get("data") or {}

    def emploi_du_temps(self, eleve_id: str, debut: str, fin: str) -> list[dict[str, Any]]:
        charge = {"dateDebut": debut, "dateFin": fin, "avecTrous": False}
        donnees = self._appel(
            endpoints.emploi_du_temps(eleve_id), charge, params={"verbe": "get"}
        ).get("data")
        return donnees if isinstance(donnees, list) else []

    def messages(self, compte_id: str, type_compte: str = "famille", annee: str = "") -> dict[str, Any]:
        params = {
            "verbe": "get",
            "orderBy": "date",
            "order": "desc",
            "page": "0",
            "itemsPerPage": "50",
            "onlyRead": "",
            "query": "",
            "typeRecuperation": "received",
        }
        if annee:
            params["anneeMessages"] = annee
        chemin = endpoints.messages(compte_id, type_compte)
        return self._appel(chemin, {}, params=params).get("data") or {}

    def message(self, compte_id: str, message_id: str, type_compte: str = "famille") -> dict[str, Any]:
        chemin = endpoints.message(compte_id, str(message_id), type_compte)
        params = {"verbe": "get", "mode": "destinataire"}
        return self._appel(chemin, {}, params=params).get("data") or {}


def texte_message(contenu: str | None) -> str:
    """Le corps des messages arrive en base64 et contient du HTML."""
    import re

    brut = _decode(contenu)
    sans_balises = re.sub(r"<br\s*/?>|</p>", "\n", brut, flags=re.I)
    sans_balises = re.sub(r"<[^>]+>", " ", sans_balises)
    sans_balises = html.unescape(sans_balises)
    # Le retrait des balises laisse des espaces doubles : on les resserre ligne par ligne.
    lignes = [re.sub(r"[ \t]+", " ", ligne).strip() for ligne in sans_balises.splitlines()]
    return "\n".join(ligne for ligne in lignes if ligne).strip()
