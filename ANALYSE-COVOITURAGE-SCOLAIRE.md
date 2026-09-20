# Analyse — application de covoiturage scolaire entre parents

**Date :** 20 septembre 2026
**Statut du dossier :** PARK
**Méthode :** project-gatekeeper (anti-dispersion)
**Projet actif concurrent :** RAVIVA (archive de souvenirs d'enfance) — stade pré-lancement, vérification de marque non close

---

## 1. Reformulation de l'opportunité

> Pour **les parents d'élèves d'une même école qui ne peuvent pas être devant
> l'école à 16h30**, résoudre **le dépannage de dernière minute pour ramener
> l'enfant à la maison**, via **une mise en relation temps réel entre parents
> vérifiés par l'école, avec détour accepté d'environ 5 minutes**, créant
> **la suppression d'une urgence récurrente et coûteuse (retard, garderie,
> nounou, journée de congé posée).**

### Ce qui est observé vs ce qui est supposé

| Nature | Contenu |
|---|---|
| **Problème observé** | La sortie d'école a un horaire rigide ; la vie professionnelle non. Le décalage est quotidien et concerne toutes les familles. |
| **Solution proposée** | App + vérification par l'école + notation + rémunération du conducteur + abonnement mensuel. |
| **Hypothèse n°1 (non testée)** | Les parents *paient* pour ça. |
| **Hypothèse n°2 (non testée)** | Les parents *confient* leur enfant à un autre parent qu'ils connaissent peu. |
| **Hypothèse n°3 (non testée)** | L'école accepte d'endosser le rôle de tiers de confiance. |
| **Hypothèse n°4 (fausse — vérifiée)** | La rémunération du conducteur est légalement neutre. Elle ne l'est pas. |
| **Preuve détenue** | Aucune, à ce stade. Intuition de parent. |

---

## 2. Le point dur juridique — à traiter avant toute ligne de code

L'article **L3132-1 du code des transports** définit le covoiturage comme
« l'utilisation en commun d'un véhicule terrestre à moteur par un conducteur et
un ou plusieurs passagers, effectué **à titre non onéreux, excepté le partage
des frais**, dans le cadre d'un déplacement que le conducteur effectue **pour
son propre compte** ».

Trois conséquences directes sur le design proposé :

1. **Le conducteur ne peut pas gagner d'argent.** Dès qu'il y a bénéfice — et
   non simple partage de frais réels (carburant, péage, usure) — le trajet
   sort de la définition du covoiturage et devient du **transport public de
   personnes à titre onéreux** : licence, capacité professionnelle, statut
   VTC/taxi.
2. **L'assurance tombe avec.** La RC auto de l'article L211-1 du code des
   assurances couvre les passagers, y compris l'enfant d'autrui, sans
   déclaration préalable — **tant que le trajet reste non onéreux**. Les
   contrats auto non professionnels excluent classiquement le transport de
   personnes à titre onéreux. Un conducteur rémunéré via l'app roule donc
   potentiellement **sans couverture, avec l'enfant d'un autre à bord**.
3. **Ce qui reste légal :** la *mise en relation* peut, elle, être effectuée à
   titre onéreux. L'abonnement mensuel payé à la plateforme est donc viable.
   C'est la **rémunération du conducteur** qui est le point de rupture, pas
   l'abonnement.

**Le détour de 5 minutes** est en revanche un bon garde-fou involontaire : il
maintient le trajet « pour son propre compte », donc dans le covoiturage. Il
faut le conserver et le rendre opposable (plafond de détour contrôlé par l'app).

### Points durs non juridiques mais bloquants

- **La sortie d'école n'est pas un parking.** L'établissement ne remet
  l'enfant qu'aux personnes listées par les parents sur la fiche de liaison.
  Un conducteur trouvé 20 minutes plus tôt dans une app n'est pas sur cette
  liste. Sans procédure acceptée par l'école, le produit ne fonctionne pas au
  moment précis où il doit fonctionner.
- **Vérification des adultes.** « Reconnu par l'école » n'est pas un statut
  juridique. L'école ne peut pas déléguer ni garantir l'honorabilité d'un
  parent. La plateforme se retrouve seule à porter cette promesse.
- **RGPD mineurs.** Données de géolocalisation d'enfants + horaires +
  domicile : traitement sensible, base légale à construire sérieusement.
- **Le sinistre unique.** Un accident, une heure de retard inexpliquée, et le
  produit meurt du jour au lendemain. C'est un business à risque asymétrique :
  gains linéaires, pertes existentielles.

---

## 3. Le marché est déjà occupé — et gratuit

Le créneau n'est pas vide. Il est segmenté en deux, et la place visée se situe
exactement dans le trou du milieu :

| Acteur | Positionnement | Monétisation |
|---|---|---|
| **Scoléo** | Covoiturage entre familles d'une même école, carte des parents proches | **Gratuit** pour les parents ; reversement à l'association de parents d'élèves |
| **Cmabulle** | Trajets quotidiens enfants, scolaire + extrascolaire, urbain et rural | Gratuit / territorial |
| **Petit Bus** | Covoiturage parents, compagnons de confiance | Gratuit |
| **Kid Hop** | Organisation de rotations entre parents déjà connus | Gratuit |
| **KidrivOO** | Covoiturage enfants | Gratuit |
| **Hopways** | Accompagnateurs et chauffeurs **professionnels** (VTC/taxi) pour enfants | **Payant, cher, et légal** |
| **Karos / Klaxit (BlaBlaCar Daily)** | Courte distance domicile-travail, financé par employeurs et collectivités | B2B / B2G |

Lecture de ce tableau : **le pair-à-pair entre parents est gratuit partout, et
le payant est réservé aux chauffeurs professionnels.** Ce n'est pas un hasard,
c'est la conséquence directe du L3132-1. L'idée proposée vise la case
« pair-à-pair + payant », qui est précisément celle que la loi ferme.

Concurrent réel le plus redoutable, et absent du tableau : **le groupe WhatsApp
de la classe.** Gratuit, déjà installé, déjà peuplé des bonnes personnes, et
déjà adossé à la confiance réelle entre parents. Tout produit ici doit être
*mieux qu'un message dans un groupe WhatsApp*, ce qui est un seuil beaucoup
plus haut qu'il n'y paraît.

---

## 4. Ce qui est vraiment neuf dans l'idée

Un seul élément échappe à la critique ci-dessus, et il mérite d'être isolé :

> **Le mode ponctuel temps réel** — « je suis devant l'école, je pars dans
> 15 minutes vers tel quartier, j'ai une place ».

Les plateformes existantes organisent des **rotations récurrentes planifiées à
l'avance**. Elles répondent mal au dépannage de dernière minute, qui est
pourtant le moment de douleur maximale. C'est la seule asymétrie exploitable
du dossier.

Mais elle porte sa propre malédiction : **le temps réel exige une densité
d'utilisateurs actifs très élevée sur une zone minuscule** (une école, une
tranche de 20 minutes, une direction de trajet). En dessous d'un seuil de
parents connectés simultanément, l'app affiche « aucune place disponible » —
et un produit de dépannage qui échoue deux fois de suite est désinstallé.
C'est un problème d'amorçage école par école, sans effet de réseau national :
1 000 utilisateurs répartis sur 200 écoles valent zéro.

---

## 5. Score

| Dimension | Note | Justification |
|---|---|---|
| Gravité de la douleur | 7/10 | Réelle, mais contournable (garderie, grands-parents, nounou) |
| Fréquence | 9/10 | Quotidienne, 36 semaines par an |
| Disposition à payer | **3/10** | Tous les concurrents pair-à-pair sont gratuits ; l'entraide entre parents est culturellement un service rendu, pas un achat |
| Accès aux premiers utilisateurs | 4/10 | Une école accessible, mais acquisition école par école, à la main |
| Avantage déloyal personnel | **2/10** | Aucun actif dans l'éducation ou la mobilité ; l'expérience retail ne transfère pas |
| Différenciation | 3/10 | Six acteurs installés ; seul le temps réel est neuf |
| Simplicité du MVP | 4/10 | Identité vérifiée, mineurs, assurance, temps réel, RGPD : ce n'est pas un MVP de week-end |
| Délai jusqu'à la première preuve | 6/10 | Une preuve manuelle est obtenable en une semaine |
| Potentiel de revenu récurrent | 4/10 | Abonnement légal, mais saisonnalité brutale : zéro usage en juillet-août |
| Charge de maintenance *(score inversé)* | **3/10** | Support obligatoire à 16h30 tous les jours d'école ; risque de sinistre existentiel |
| **TOTAL** | **45/100** | |

Seuil de référence : en dessous de 60, l'opportunité ne justifie pas de
détourner de la capacité d'exécution d'un projet déjà engagé.

---

## 6. Test anti-enthousiasme

**Qu'est-ce qui en ferait un mauvais business ?**
Un produit gratuit de fait (parce que la concurrence l'est), à coût de support
élevé et permanent, avec une responsabilité juridique portée par la plateforme
sur la sécurité d'enfants, et une acquisition qui se fait école par école sans
levier viral inter-écoles.

**Quel comportement existant résout déjà « assez » le problème ?**
Le groupe WhatsApp de la classe, plus la garderie périscolaire municipale, qui
coûte quelques euros et n'exige aucune coordination.

**Quelle hypothèse est la plus probablement fausse ?**
« Les parents paieront un abonnement mensuel. » Le marché a déjà répondu :
personne ne facture les parents pour du pair-à-pair. Scoléo, le plus proche du
concept, se finance par les écoles et les associations de parents.

**Qu'est-ce qui rendrait l'acquisition coûteuse ?**
La densité par école. Il faut convaincre l'école, puis l'association de
parents, puis atteindre une masse critique dans cette seule école — et
recommencer intégralement à l'école suivante. Coût d'acquisition élevé,
répétable mais non composable.

**Qu'est-ce qui crée une charge opérationnelle permanente ?**
Le créneau 16h00-17h00 en semaine scolaire. Chaque incident est urgent, chaque
retard est une inquiétude parentale, et aucun ne peut attendre le lendemain.

---

## 7. Verdict

# PARK

**Pourquoi PARK et non KILL :** le mode ponctuel temps réel est une vraie
lacune du marché, et la douleur est authentique et quotidienne.

**Pourquoi PARK et non TEST ou BUILD :**

- RAVIVA n'est pas lancé. Sa vérification de marque est encore ouverte
  (domaines, INPI, EUIPO non vérifiés). Ouvrir un second chantier maintenant
  retarde mécaniquement le premier.
- L'incertitude décisive — « les parents paient-ils ? » — est déjà largement
  levée par le marché, dans le mauvais sens. Six acteurs, aucun ne facture les
  parents du pair-à-pair.
- Le mécanisme de monétisation imaginé (rémunérer le conducteur) est
  juridiquement fermé et doit être redessiné avant même d'être testé.

**Risque principal, en une phrase :** construire un produit que les parents
utiliseront volontiers et ne paieront jamais, tout en portant la
responsabilité juridique de la sécurité de leurs enfants.

---

## 8. Prochaine preuve — 90 minutes, zéro développement

Ce test ne s'exécute **que si RAVIVA est lancé, ou si le dossier est
volontairement dépriorisé.**

| Élément | Contenu |
|---|---|
| **Action** | Devant une école, à la sortie, interroger **12 parents** en face à face. Trois questions, dans cet ordre, sans jamais présenter l'application. |
| **Q1** | « Ce mois-ci, combien de fois avez-vous été coincé pour récupérer votre enfant ? » |
| **Q2** | « Qu'avez-vous fait, concrètement, la dernière fois ? » |
| **Q3** | « Confieriez-vous votre enfant à un parent de l'école que vous connaissez de vue mais pas personnellement ? » |
| **Responsable** | Toi, seul. Pas de développeur, pas de maquette, pas de nom de marque. |
| **Seuil de succès** | **≥ 8 parents sur 12** citent au moins 2 épisodes dans le mois **ET** répondent oui à Q3 sans hésiter. |
| **En dessous du seuil** | KILL définitif. Le dossier est clos. |
| **Au-dessus du seuil** | Passage en TEST — et alors seulement, un WhatsApp manuel sur une école, opéré à la main pendant 3 semaines, avant toute ligne de code. |

**Note sur Q3 :** c'est la question qui tue. Une hésitation est un non. Les
parents répondent « oui » par politesse sur les questions de principe et
« non » dans la réalité à 16h30. Observer l'hésitation, pas la réponse.

---

## 9. Ce qu'il ne faut PAS faire maintenant

- ❌ Ne pas ouvrir de maquette, de design, de nom de marque, de logo.
- ❌ Ne pas vérifier la disponibilité d'un nom de domaine. C'est le piège
  précis dans lequel un projet enthousiasmant fait perdre trois jours sans
  produire la moindre preuve.
- ❌ Ne pas contacter d'école ni de mairie. Trop tôt : sans preuve de
  demande, l'entretien se transforme en discussion de faisabilité
  administrative et consomme du crédit relationnel.
- ❌ Ne pas approfondir le dossier juridique, assurance ou RGPD. Ce travail
  n'a de valeur qu'après confirmation de la demande — et il est lourd.
- ❌ Ne pas retarder RAVIVA d'une seule journée pour ce dossier.

---

## Sources

- Article L3132-1 du code des transports — Légifrance :
  https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000039784386
- Covoiturage, la réglementation applicable — DGCCRF / economie.gouv.fr :
  https://www.economie.gouv.fr/dgccrf/les-fiches-pratiques/covoiturage-la-reglementation-applicable
- Covoiturage scolaire, qui est assuré — JeChange :
  https://www.jechange.fr/assurance/auto/news/covoiturage-scolaire-qui-est-assure-trajet-ecole
- Plateformes de covoiturage des enfants — Netguide :
  https://www.netguide.com/Annonces-pour-le-covoiturage-des-enfants/
- Scoléo, covoiturage scolaire : https://www.scoleo.fr/Covoiturage-Scolaire.html
- Cmabulle : https://cmabulle.fr/
- Hopways, accompagnateurs professionnels : https://www.hopways.com/
