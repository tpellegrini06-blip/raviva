# École Directe — compte rendu familial automatique

Se connecte chaque matin à École Directe, ramène tout ce qui concerne les enfants,
le compare au passage précédent et en fait un compte rendu lisible :

- **emploi du temps** du jour et du lendemain, cours annulés ou déplacés signalés ;
- **devoirs** à faire, interrogations annoncées, et surtout les **devoirs jamais cochés
  comme faits** dont la date est passée ;
- **absences, retards, sanctions**, avec ce qui reste à justifier ;
- **notes** récentes ;
- **messagerie** de l'établissement, avec les dates repérées dans les messages
  (réunion parents-professeurs, sortie, date limite de retour d'autorisation…) ;
- un **calendrier .ics** regroupant cours, devoirs et échéances, abonnable depuis un téléphone.

## ⚠️ Avant tout : la question du dépôt

Ce dépôt (`tpellegrini06-blip/raviva`) est **public**. Les données ramenées
— notes, absences, messages nominatifs concernant des mineurs — **ne doivent pas y atterrir**.

Trois protections sont en place :

1. `sortie/` et `etat/` sont dans le `.gitignore` ;
2. le workflow GitHub Actions **refuse de démarrer** si le dépôt est public
   (sur un dépôt public, les artefacts de job sont téléchargeables par tout le monde) ;
3. aucun identifiant n'est lu ailleurs que dans les variables d'environnement.

Pour une exécution automatique, il faut donc déplacer ce dossier dans un **dépôt privé**,
ou faire tourner le script sur une machine à soi (NAS, Raspberry Pi, Mac allumé le matin).

## Installation

```bash
cd ecoledirecte
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## 1. Amorçage de la double authentification (une fois)

École Directe pose une question de sécurité à la première connexion. Il faut y répondre
une fois à la main ; on récupère un couple `cn`/`cv` qui évite la question ensuite.

```bash
export ED_IDENTIFIANT="…"
python bootstrap_2fa.py
```

Le script affiche la question, les propositions, puis le couple à conserver :

```
ED_FA_CN=…
ED_FA_CV=…
```

Ce couple **expire au bout de quelques semaines ou mois**, et immédiatement si le mot de
passe change. Quand cela arrive, le passage automatique s'arrête avec le code de retour `3`
et un message explicite : il suffit de relancer `bootstrap_2fa.py` et de remettre les deux
secrets à jour. C'est la seule intervention manuelle récurrente.

## 2. Passage quotidien

```bash
python run.py                    # brief complet
python run.py --changements      # n'écrit que si quelque chose a bougé
```

Produit dans `sortie/` :

| Fichier | Contenu |
| --- | --- |
| `brief.md` | le compte rendu à lire |
| `ecoledirecte.ics` | le calendrier à abonner (cours, devoirs, échéances) |
| `donnees.json` | tout le détail normalisé, pour un tableau de bord ultérieur |

Codes de retour : `0` succès · `1` erreur réseau ou API · `2` configuration absente ·
`3` double authentification à refaire · `4` identifiants refusés.

## 3. Automatisation

`.github/workflows/ecoledirecte.yml` fait trois passages par jour : brief complet à 7h,
puis contrôles à 13h et 18h30 qui ne produisent quelque chose que si l'emploi du temps
ou les devoirs ont changé. Les secrets attendus : `ED_IDENTIFIANT`, `ED_MOT_DE_PASSE`,
`ED_FA_CN`, `ED_FA_CV`, et pour l'envoi par mail `ED_SMTP_*` / `ED_MAIL_DESTINATAIRE`.

## Ce qui est vérifié, et ce qui ne l'est pas

`python -m tests.test_hors_ligne` couvre 40 vérifications : découverte des enfants,
normalisation de chaque type de réponse, extraction des dates dans les messages,
détection des changements, rédaction du brief, export iCalendar (y compris le passage
heure d'été / heure d'hiver).

En revanche **rien n'a encore été confronté à l'API réelle** : l'accès réseau vers
`api.ecoledirecte.com` était bloqué au moment de l'écriture, et aucun compte n'a été
utilisé. Les URL et les noms de champs viennent de l'API interne de l'application web.
Ils sont plausibles mais doivent être validés lors du premier vrai passage.

## Quand ça casse

L'API n'est pas publique et change sans préavis. Dans l'ordre de probabilité :

1. **`VERSION` dans `ed/endpoints.py`** est périmée → ouvrir www.ecoledirecte.com,
   onglet Réseau du navigateur, lire le paramètre `v=` d'une requête vers l'API, le recopier.
2. **Le couple cn/cv a expiré** → relancer `bootstrap_2fa.py` (code de retour `3`).
3. **Un champ a été renommé** → tout le décodage passe par `_premier(...)` dans
   `ed/collecte.py`, qui accepte plusieurs noms pour un même champ : ajouter le nouveau nom.

Une ressource en échec n'interrompt jamais le passage : l'erreur est listée dans la
section « Incidents techniques » du brief et le reste est produit normalement.

## Organisation du code

```
ed/endpoints.py   toutes les URL et le numéro de version, en un seul endroit
ed/client.py      HTTP, connexion, double authentification, jeton
ed/collecte.py    appels + normalisation des réponses hétérogènes
ed/models.py      formes normalisées (Cours, Devoir, Note, Absence, Message, DateCle)
ed/etat.py        instantané d'un passage et comparaison avec le précédent
ed/brief.py       rédaction du compte rendu
ed/calendrier.py  export iCalendar
```

## Cadre

Compte personnel, données de ses propres enfants, usage familial. L'API utilisée est
celle de l'application officielle : elle n'est pas documentée publiquement et les CGU
d'École Directe ne prévoient pas de client tiers. Le risque concret est la panne
technique lors d'une mise à jour de leur côté, pas autre chose.
