# Skills du projet

Skills disponibles automatiquement dans toute session Claude Code ouverte sur ce dépôt.
Chaque skill vit dans `<nom>/SKILL.md` (frontmatter `name` + `description`).

| Skill | Quand elle se déclenche |
|---|---|
| `ceo-control-tower` | « qu'est-ce qui est urgent ? », brief quotidien/hebdo, file d'actions priorisée |
| `dossier-resolver` | un dossier concret (facture, assurance, banque, fournisseur, impôt) à reconstituer |
| `friction-miner` | une gêne récurrente / bricolage manuel à transformer en friction documentée |
| `opportunity-validator` | une friction mérite enquête : marché, concurrents, acheteur, GO/TEST/KILL |
| `project-gatekeeper` | une nouvelle idée de projet à arbitrer : KILL / PARK / TEST / BUILD |
| `mvp-executor` | décision BUILD/GO actée : construire l'artefact testable le plus court |
| `retail-analyst` | données multi-magasins : réassort, transferts, marges, invendus, anomalies |

## Enchaînement prévu

```
friction-miner → opportunity-validator → project-gatekeeper → mvp-executor
```

`ceo-control-tower`, `dossier-resolver` et `retail-analyst` s'utilisent seuls,
selon le sujet.
