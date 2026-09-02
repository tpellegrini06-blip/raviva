# Méthode — comment on qualifie une information

Reprise de la méthode du rapport RAVIVA du 10 août 2026, qui vaut pour tout
le dépôt. Elle existe parce qu'une session peut chercher longtemps et ne rien
prouver — et que le pire résultat n'est pas l'absence de preuve, c'est
l'absence de preuve présentée comme une preuve.

## Les quatre niveaux

| Niveau | Ce que c'est | Ce qu'on peut en faire |
|---|---|---|
| **Direct** | Interrogation de la source primaire (registre, API, base officielle), résultat lu | Décider |
| **Indexé** | Trace trouvée via recherche web, source secondaire identifiable | Orienter, jamais décider seul |
| **Indirect** | Inférence à partir d'un faisceau (ex. « cinq acteurs contournent le .com, donc il est sans doute pris ») | Formuler une hypothèse à tester |
| **Néant** | La source n'a pas pu être interrogée | Rien. Et le dire. |

## Les trois règles

1. **Une absence de trace n'est jamais une disponibilité.** Un compte, une
   marque, un domaine peuvent exister sans être indexés.
2. **Chaque affirmation porte son niveau.** Un tableau récapitulatif sans
   colonne « niveau de preuve » est un tableau qui ment par omission.
3. **Toute vérification impossible ici repart en annexe**, sous forme de
   commandes exactes rejouables depuis un poste non filtré. Le travail n'est
   pas perdu, il est déplacé.

## Le plafond actuel de cet environnement

Egress réseau limité à GitHub et aux registres de paquets. Testé le
2026-09-02 : `rdap.nic.fr`, `rdap.org`, `data.inpi.fr`, `www.tmdn.org` →
403 sur CONNECT. Seule la recherche web indexée passe.

Tant que ce plafond tient, **aucune vérification de marque ou de domaine ne
peut dépasser le niveau « indexé »** depuis cet environnement.
