"""Formes normalisées : l'API renvoie des structures hétérogènes, tout le reste du code lit celles-ci."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class Enfant:
    id: str
    prenom: str
    nom: str
    classe: str

    @property
    def libelle(self) -> str:
        return f"{self.prenom} ({self.classe})" if self.classe else self.prenom


@dataclass
class Cours:
    enfant: str
    date: str          # YYYY-MM-DD
    debut: str         # HH:MM
    fin: str           # HH:MM
    matiere: str
    professeur: str = ""
    salle: str = ""
    annule: bool = False

    @property
    def cle(self) -> str:
        return f"cours|{self.enfant}|{self.date}|{self.debut}|{self.matiere}"

    @property
    def empreinte(self) -> str:
        return f"{self.debut}-{self.fin}|{self.salle}|{self.professeur}|{int(self.annule)}"


@dataclass
class Devoir:
    enfant: str
    pour_le: str       # date à laquelle le travail doit être fait
    matiere: str
    contenu: str = ""
    donne_le: str = ""
    effectue: bool = False
    interrogation: bool = False

    @property
    def cle(self) -> str:
        return f"devoir|{self.enfant}|{self.pour_le}|{self.matiere}"

    @property
    def empreinte(self) -> str:
        return f"{int(self.effectue)}|{int(self.interrogation)}|{self.contenu[:200]}"


@dataclass
class Note:
    enfant: str
    date: str
    matiere: str
    libelle: str
    valeur: str
    bareme: str = "20"
    coefficient: str = "1"
    moyenne_classe: str = ""

    @property
    def cle(self) -> str:
        return f"note|{self.enfant}|{self.date}|{self.matiere}|{self.libelle}"

    @property
    def empreinte(self) -> str:
        return f"{self.valeur}/{self.bareme}"


@dataclass
class FaitViesScolaire:
    enfant: str
    type: str          # Absence, Retard, Sanction, Encouragement
    date_debut: str
    date_fin: str = ""
    motif: str = ""
    justifie: bool = False
    commentaire: str = ""

    @property
    def cle(self) -> str:
        return f"vie|{self.enfant}|{self.type}|{self.date_debut}|{self.date_fin}"

    @property
    def empreinte(self) -> str:
        return f"{int(self.justifie)}|{self.motif}"


@dataclass
class Message:
    id: str
    date: str
    expediteur: str
    sujet: str
    lu: bool = False
    extrait: str = ""
    destinataire: str = ""

    @property
    def cle(self) -> str:
        return f"message|{self.id}"

    @property
    def empreinte(self) -> str:
        return f"{int(self.lu)}"


@dataclass
class DateCle:
    """Une échéance repérée dans un message ou l'agenda : réunion, sortie, conseil de classe…"""

    date: str
    intitule: str
    source: str
    enfant: str = ""

    @property
    def cle(self) -> str:
        return f"datecle|{self.date}|{self.intitule[:60]}"

    @property
    def empreinte(self) -> str:
        return self.intitule[:200]


@dataclass
class Collecte:
    """Tout ce qui a été ramené en un passage."""

    enfants: list[Enfant] = field(default_factory=list)
    cours: list[Cours] = field(default_factory=list)
    devoirs: list[Devoir] = field(default_factory=list)
    notes: list[Note] = field(default_factory=list)
    vie_scolaire: list[FaitViesScolaire] = field(default_factory=list)
    messages: list[Message] = field(default_factory=list)
    dates_cles: list[DateCle] = field(default_factory=list)
    erreurs: list[str] = field(default_factory=list)

    def tous_les_elements(self) -> list[Any]:
        return [*self.cours, *self.devoirs, *self.notes, *self.vie_scolaire, *self.messages, *self.dates_cles]

    def en_dict(self) -> dict[str, Any]:
        return {
            "enfants": [asdict(e) for e in self.enfants],
            "cours": [asdict(c) for c in self.cours],
            "devoirs": [asdict(d) for d in self.devoirs],
            "notes": [asdict(n) for n in self.notes],
            "vie_scolaire": [asdict(v) for v in self.vie_scolaire],
            "messages": [asdict(m) for m in self.messages],
            "dates_cles": [asdict(d) for d in self.dates_cles],
            "erreurs": list(self.erreurs),
        }
