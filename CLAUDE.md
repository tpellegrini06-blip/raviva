# CLAUDE.md — mode d'emploi de ce dépôt

Ce fichier est lu automatiquement au démarrage de **chaque** session Claude Code
(terminal, web, mobile). C'est le socle de la « situation pérenne » : tout ce
qui est écrit ici est su d'avance, sans avoir à le réexpliquer.

**Règle unique :** ce qui n'est pas écrit dans ce dépôt n'existe pas d'une
session à l'autre. Une conversation se perd. Un fichier commité reste.

---

## 1. Qui je suis, ce que je fais

> ⚠️ **À compléter par Thibault.** Tant que cette section est vide, chaque
> session repart de zéro sur le contexte métier. Cinq minutes ici économisent
> une heure par session. Voir `CONTEXTE/entreprise.md`.

- **Activité principale :** _(retail multi-magasins — à préciser : enseigne, nombre de points de vente, villes, CA, effectif, saisonnalité)_
- **Rôle :** dirigeant
- **Contact :** tpellegrini06@gmail.com

## 2. Projets actifs

| Projet | Statut | Fiche |
|---|---|---|
| **RAVIVA** — archive de souvenirs d'enfance (film annuel + livre + objet) | GO AVEC RÉSERVE — vérifications de registre en attente | `RECHERCHES/2026-08-10-verification-marque-raviva.md` |
| **La marque française du souvenir** — enseigne / chaîne | Exploration, recommandation posée | `RECHERCHES/2026-09-02-marque-francaise-du-souvenir.md` |

Détail et priorités : `CONTEXTE/projets.md`.
Décisions déjà tranchées (à ne pas rouvrir) : `CONTEXTE/journal-decisions.md`.

## 3. Comment je veux qu'on travaille

- **Français**, direct, pas de flatterie, pas de récapitulatif de ce que je viens de dire.
- **Des chiffres ou rien.** Une affirmation sans source ni ordre de grandeur ne vaut pas la peine d'être écrite.
- **Dire ce qui n'a pas pu être vérifié.** Un trou dans la preuve se signale, il ne se comble pas par une formulation. Méthode : `CONTEXTE/methode-preuve.md`.
- **Trancher.** Une recommandation, pas un panorama d'options équivalentes.
- **Anti-dispersion.** Une idée neuve passe par `project-gatekeeper` avant tout travail lourd. La compétence rare ici n'est pas de trouver des idées, c'est d'en tuer.

## 4. Les 7 compétences installées (`.claude/skills/`)

| Compétence | Quand elle se déclenche |
|---|---|
| `ceo-control-tower` | « qu'est-ce qui est urgent », brief quotidien, arbitrage |
| `dossier-resolver` | un dossier admin/fournisseur/banque/assurance à reconstituer |
| `friction-miner` | une galère, un bricolage, un « il devrait y avoir plus simple » |
| `opportunity-validator` | est-ce un vrai marché ? qui paie ? GO / TEST / KILL |
| `project-gatekeeper` | nouvelle idée → KILL, PARK, TEST ou BUILD |
| `mvp-executor` | une opportunité validée → produit testable |
| `retail-analyst` | ventes, stocks, marges, transferts, réassort multi-magasins |

Elles sont appelées automatiquement selon la question. Pas besoin de les nommer.

## 5. Ce que cet environnement ne peut PAS faire

Vérifié le 2 septembre 2026, inchangé depuis le 10 août : la politique
d'egress réseau de cet environnement **bloque tout hôte** hors GitHub et
registres de paquets (403 sur CONNECT).

Bloqués et re-testés : `rdap.nic.fr`, `rdap.org`, `data.inpi.fr`,
`www.tmdn.org`, `euipo.europa.eu`, `instagram.com`, `tiktok.com`.

**Conséquence :** aucune interrogation de registre de marques ou de domaines
n'est possible depuis ici. Seule la recherche web indexée fonctionne.
Une trace indexée prouve qu'une chose existe ; son absence ne prouve jamais
qu'une chose est libre.

**Comment lever ce plafond** (une seule fois, et c'est réglé pour tous les
projets à venir) : créer un environnement Claude Code avec une politique
réseau plus ouverte — documentation
<https://code.claude.com/docs/en/claude-code-on-the-web>. À défaut, rejouer
l'annexe de commandes du rapport RAVIVA depuis un poste non filtré et coller
les résultats dans le dépôt.

## 6. Où ranger quoi

```
CLAUDE.md                  ← ce fichier : le socle, lu à chaque session
CONTEXTE/entreprise.md     ← qui je suis, mes magasins, mes chiffres
CONTEXTE/projets.md        ← ce sur quoi je travaille, par priorité
CONTEXTE/journal-decisions.md ← ce qui est tranché (date, décision, raison)
CONTEXTE/methode-preuve.md ← comment on qualifie une information
RECHERCHES/AAAA-MM-JJ-sujet.md ← toute recherche, datée, avec ses sources
.claude/skills/            ← les 7 compétences métier
```

## 7. Le rituel (5 minutes par semaine)

1. Une décision prise ? Une ligne dans `CONTEXTE/journal-decisions.md`.
2. Un chiffre d'entreprise qui bouge ? `CONTEXTE/entreprise.md`.
3. Une recherche produite ? Elle est datée dans `RECHERCHES/`, jamais dans le fil de conversation.
4. Commiter. Un dépôt non poussé est un dépôt perdu.
