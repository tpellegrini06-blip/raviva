# Vérification de disponibilité — marque « RAVIVA »

**Projet :** service d'archive de souvenirs d'enfance (film annuel, livre imprimé, objet physique de collection)
**Marchés :** France, puis Belgique / Suisse / Québec
**Date de la vérification :** 10 août 2026

---

## ⚠️ Avertissement méthodologique — à lire avant le tableau

Les vérifications 1 à 4 **n'ont pas pu être exécutées en direct**. La session
d'exécution est protégée par une politique d'egress réseau qui bloque tout hôte
hors GitHub et registres de paquets. Les hôtes suivants ont été testés et
refusés (403 sur CONNECT, puis `EGRESS_BLOCKED`) :

| Hôte | Vérification concernée | Résultat |
|---|---|---|
| `rdap.nic.fr` | domaine .fr | bloqué |
| `rdap.org` | domaine .com | bloqué |
| `rdap.verisign.com` | domaine .com (repli) | bloqué |
| `data.inpi.fr` | marques françaises | bloqué |
| `www.tmdn.org` | TMview | bloqué |
| `euipo.europa.eu` | marques UE | bloqué |
| `www.instagram.com` | handles | bloqué |
| `www.tiktok.com` | handles | bloqué |

Seule la **recherche web indexée** est restée disponible. Les constats
ci-dessous reposent donc sur des **traces indexées**, pas sur des interrogations
de registre. Une trace indexée prouve qu'une chose **existe** ; son absence ne
prouve **jamais** qu'une chose est libre. Chaque ligne du tableau porte son
niveau de preuve.

Les commandes exactes à rejouer depuis un poste non filtré sont en annexe.

---

## Tableau récapitulatif

| # | Axe | Statut | Niveau de preuve |
|---|---|---|---|
| 1 | Domaines (.fr / .com / .app / getraviva) | **NON VÉRIFIÉ** — présomption `.com` pris | Aucun (RDAP bloqué) |
| 2 | INPI — marques françaises | **NON VÉRIFIÉ** | Aucun (API bloquée) |
| 3 | EUIPO / TMview | **NON VÉRIFIÉ** | Aucun (base bloquée) |
| 4 | Réseaux sociaux @raviva / @raviva.fr | **À SURVEILLER** — voisinage dense, handles exacts non vérifiés | Indirect |
| 5 | Google — territoire sémantique | **DISPONIBLE** sur le créneau souvenirs/famille | Direct, solide |

---

## 1. DOMAINES — non vérifié

RDAP inaccessible. Aucune interrogation de registre n'a pu aboutir sur
`raviva.fr`, `raviva.com`, `raviva.app` ni `getraviva.com`.

**Indice indirect, à manier avec prudence :** il existe au moins cinq entités
commerciales actives nommées « Raviva » dans le monde, et **aucune n'utilise le
`.com`**. Elles se sont rabattues sur des extensions alternatives :

- `raviva.in` — Raviva Infotech Private Limited (Maharashtra, Inde)
- `raviva.life` — Raviva Healing Center (Plantation, Floride)
- Raviva Company (Rockville, Maryland) — présence Instagram/Yelp seulement
- Raviva jewellery (`@raviva_in`) — Instagram seulement
- Raviva Winery — référencée via Vivino

Quand cinq acteurs portant le même nom contournent tous le `.com`, l'hypothèse
la plus économique est que le `.com` est **déjà détenu** — par un tiers, ou par
un revendeur de noms de domaine. C'est une inférence, pas un constat : elle doit
être confirmée avant toute décision.

Rien n'a été trouvé sur `raviva.fr`, dans un sens ni dans l'autre.

## 2. INPI — non vérifié

`data.inpi.fr` inaccessible. La recherche indexée sur « RAVIVA marque INPI » n'a
renvoyé que des pages génériques d'explication du dépôt de marque — aucun
enregistrement.

**Aucune donnée n'a été obtenue** sur RAVIVA ni sur les variantes demandées
(RAVIVE, RAVVIVA, RAVIVA') dans les classes 9, 16, 38, 41 et 42. Ni titulaire,
ni classe, ni date de dépôt, ni statut. Cette section est vide, et son vide ne
vaut pas disponibilité.

### Point de droit à instruire en parallèle — distinctivité

Indépendamment des antériorités, un risque propre au signe mérite examen :
**« raviva » est un mot français réel** — troisième personne du singulier du
passé simple de *raviver* (source : Wiktionnaire). Pour un service dont la
promesse est précisément de *raviver des souvenirs*, l'INPI peut soulever une
objection de **défaut de distinctivité** (art. L.711-2 du Code de la propriété
intellectuelle) : un signe qui décrit la caractéristique du service ne peut être
approprié.

L'argument de défense existe et est sérieux — une forme verbale conjuguée au
passé simple est **évocatrice** plutôt que descriptive, et l'évocation est
admise. Mais l'objection est plausible, en particulier en classe 41. À faire
trancher par un conseil en propriété industrielle avant dépôt, et à considérer
comme un poste de risque distinct de celui des antériorités.

## 3. EUIPO / TMview — non vérifié

Base inaccessible. Une recherche de repli sur les agrégateurs de marques
(Justia, TrademarkElite, uspto.report) n'a fait remonter que des signes
**voisins**, jamais RAVIVA lui-même : REVA, REVIVA, RAVIYA, REÏVA, RIVA.

Ce voisinage n'est pas neutre. Il indique que la zone phonétique autour de
« raviva » est **occupée**, ce qui est le terrain habituel des oppositions pour
risque de confusion. Il ne dit rien de RAVIVA en propre, et ces résultats sont
majoritairement américains — hors périmètre UE demandé.

## 4. RÉSEAUX SOCIAUX — à surveiller

Les handles exacts **@raviva** et **@raviva.fr** n'ont pu être vérifiés
directement sur Instagram ni TikTok : les deux plateformes sont bloquées.
Aucun des deux n'est apparu dans les résultats indexés, ce qui est **un indice
faible et non concluant** — un compte peut exister sans être indexé.

Comptes « Raviva » dont l'existence est en revanche **confirmée** :

**Instagram**
- [`@raviva_in`](https://www.instagram.com/raviva_in/) — Raviva jewellery
- [`@ravivacompany`](https://www.instagram.com/ravivacompany/) — Raviva Company (zone DMV, USA)
- [`@ravivahealingcenter`](https://www.instagram.com/ravivahealingcenter/) — Raviva Healing Center
- [`@raviva.au`](https://www.instagram.com/raviva.au/) — Australie
- [`@_raviva`](https://www.instagram.com/_raviva/) — compte personnel
- [`@centre_raviva`](https://www.instagram.com/centre_raviva/) — **Raviva médecine esthétique, ~15 000 abonnés**

**TikTok**
- [`@raviva.life`](https://www.tiktok.com/@raviva.life) — Raviva Healing Center (~821 abonnés)

**Facebook**
- [`@ravivabeauty`](https://www.facebook.com/ravivabeauty/) — Raviva Beauty

Le point le plus important de cette section : **`@centre_raviva`, « Raviva
médecine esthétique », est libellé en français et compte environ 15 000
abonnés.** C'est le seul acteur francophone identifié portant le nom. Sa
localisation exacte (France, Belgique, Suisse, Québec ?) n'a pas pu être établie
— la recherche ciblée n'a rien donné de plus. Avec 15 000 abonnés, cet acteur
est assez installé pour détenir une marque, et la médecine esthétique relève de
la classe 44, hors des classes visées. Cela réduit le risque juridique frontal
mais **pas** le risque de confusion sur les réseaux, où les classes de Nice
n'existent pas.

**À instruire en priorité :** identifier ce compte et son pays.

## 5. GOOGLE — territoire sémantique disponible

C'est la seule section reposant sur des observations directes et complètes.

Le nom « Raviva » est utilisé dans le monde, mais **dans des secteurs sans aucun
rapport** avec le projet : bijouterie, médecine esthétique et bien-être,
plans de travail et cuisines, informatique de services, viticulture, cosmétique,
prêt-à-porter de seconde main.

**Aucun acteur nommé Raviva n'occupe le champ souvenirs / mémoire familiale /
film / livre photo.** Les acteurs réellement présents sur ce créneau portent
d'autres noms :

- [Memolife](https://memolife.ai/) — œuvres cinématographiques à partir du patrimoine familial
- [Souvenirs Vivants](https://app.souvenirsvivants.com/) — photos animées, films courts livrés sous 48 h
- [Raconte-moi ton histoire](https://racontemoitonhistoire-livres.com/) — livres souvenirs
- Flexilivre, Photobox, Blurb, Fnac Photo — livres photo

Le territoire sémantique visé est donc **libre de tout homonyme**. À noter au
passage : Memolife et Souvenirs Vivants sont des concurrents directs sur la
proposition de valeur, indépendamment de la question du nom.

---

## Recommandation

### GO AVEC RÉSERVE — réserve procédurale, pas sur le nom

Cette recommandation porte sur ce qui a pu être établi. Elle doit être relue
après les vérifications de registre, qui restent à faire.

**Ce qui plaide pour :** le créneau visé est vide d'homonymes. Un service
d'archive de souvenirs nommé RAVIVA n'entrerait en collision frontale avec
personne sur son marché. Le nom est court, prononçable dans les quatre
territoires visés, et son sens français travaille pour le produit.

**Ce qui impose la réserve — trois points, par ordre de gravité :**

1. **Les registres n'ont pas été interrogés.** INPI, EUIPO et RDAP sont tous
   restés inaccessibles. Le risque juridique n'est pas faible : il est
   **inconnu**. Aucun engagement — dépôt, achat de domaine, impression,
   communication — ne devrait précéder ces trois vérifications.

2. **La distinctivité du signe est discutable.** « Raviva » décrit de près
   l'effet promis par le service. L'objection INPI est plausible, surtout en
   classe 41. À faire trancher par un conseil en PI avant dépôt.

3. **Un acteur francophone homonyme existe** (`@centre_raviva`, ~15 000
   abonnés, médecine esthétique). Classe différente, donc conflit juridique
   improbable ; mais confusion possible sur les réseaux sociaux dans le même
   espace linguistique.

**Séquence recommandée :** rejouer l'annexe depuis un poste non filtré →
identifier `@centre_raviva` et son pays → soumettre le signe à un conseil en PI
sur la distinctivité → puis seulement décider.

Si les trois registres reviennent vides et que le conseil valide la
distinctivité, la réserve tombe et la recommandation passe à **GO**.

---

## Annexe — commandes à rejouer depuis un poste non filtré

```bash
# 1. Domaines — RDAP
curl -s https://rdap.nic.fr/domain/raviva.fr | jq .
curl -sL https://rdap.org/domain/raviva.com | jq .
curl -sL https://rdap.org/domain/raviva.app | jq .
curl -sL https://rdap.org/domain/getraviva.com | jq .
# Lecture : HTTP 404 = libre. HTTP 200 = enregistré ; lire "events" (dates)
# et "entities" (titulaire, si non masqué par le RGPD — sur .fr, les
# titulaires personnes physiques sont masqués par défaut).

# 2. INPI — marques françaises
# API : https://data.inpi.fr/  (compte gratuit requis pour l'accès API)
# Interface : https://data.inpi.fr/search?q=RAVIVA
# Rechercher : RAVIVA, RAVIVE, RAVVIVA, RAVIVA'
# Filtrer sur les classes de Nice 9, 16, 38, 41, 42
# Relever pour chaque résultat : titulaire, classes, date de dépôt, statut

# 3. EUIPO / TMview
# https://www.tmdn.org/tmview/  — recherche « RAVIVA », territoire UE
# https://euipo.europa.eu/eSearch/  — recherche EUTM
# Penser à la recherche phonétique / « similar marks », pas seulement exacte

# 4. Réseaux sociaux
# https://www.instagram.com/raviva/       → 404 = libre
# https://www.instagram.com/raviva.fr/    → 404 = libre
# https://www.tiktok.com/@raviva          → 404 = libre
# https://www.tiktok.com/@raviva.fr       → 404 = libre
```
