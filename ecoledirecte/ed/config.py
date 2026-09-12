"""Configuration : uniquement des variables d'environnement, jamais de secret versionné."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
DOSSIER_ETAT = Path(os.environ.get("ED_STATE_DIR", RACINE / "etat"))
DOSSIER_SORTIE = Path(os.environ.get("ED_OUTPUT_DIR", RACINE / "sortie"))


class ConfigurationManquante(RuntimeError):
    pass


@dataclass(frozen=True)
class Config:
    identifiant: str
    mot_de_passe: str
    fa_cn: str | None
    fa_cv: str | None
    fuseau: str = "Europe/Paris"

    @property
    def fa(self) -> list[dict[str, str]]:
        """Le couple rejoué à chaque login pour ne pas repasser la double authentification."""
        if self.fa_cn and self.fa_cv:
            return [{"cn": self.fa_cn, "cv": self.fa_cv}]
        return []


def charger(exiger_2fa: bool = True) -> Config:
    identifiant = os.environ.get("ED_IDENTIFIANT", "").strip()
    mot_de_passe = os.environ.get("ED_MOT_DE_PASSE", "")
    if not identifiant or not mot_de_passe:
        raise ConfigurationManquante(
            "ED_IDENTIFIANT et ED_MOT_DE_PASSE doivent être définis dans l'environnement "
            "(secrets GitHub Actions ou variables d'environnement de la machine). "
            "Ne jamais les écrire dans un fichier du dépôt."
        )

    cn = os.environ.get("ED_FA_CN", "").strip() or None
    cv = os.environ.get("ED_FA_CV", "").strip() or None
    if exiger_2fa and not (cn and cv):
        raise ConfigurationManquante(
            "ED_FA_CN / ED_FA_CV absents : lance d'abord `python bootstrap_2fa.py` "
            "pour répondre une fois à la question de sécurité, puis enregistre le couple obtenu."
        )

    return Config(
        identifiant=identifiant,
        mot_de_passe=mot_de_passe,
        fa_cn=cn,
        fa_cv=cv,
        fuseau=os.environ.get("ED_FUSEAU", "Europe/Paris"),
    )


def preparer_dossiers() -> None:
    DOSSIER_ETAT.mkdir(parents=True, exist_ok=True)
    DOSSIER_SORTIE.mkdir(parents=True, exist_ok=True)
