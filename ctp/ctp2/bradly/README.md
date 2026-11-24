# CTP 2 — Qualité des données ShopFast

**Garde-fou de gouvernance manquant : ShopFast doit convenir avec les producteurs et consommateurs d’un contrat de données versionné (schéma, sens et unités EUR, règles qualité, SLA et responsables), puis le tester bloquant dans la chaîne d’ingestion/CI avant toute publication.**

## Exécution réelle et résultats

Les sept CSV du kit ShopFast sont livrés dans `data/`; `payments_batch_2.csv` est également fourni à la racine pour le script paiements. Environnement validé : Great Expectations 1.7.1.

- **Paiements (`gx_payments.py`)** — Suite naïve : historique **PASS**, incident **PASS**. Suite smart : historique **PASS**, incident **FAIL** sur les trois contrôles de montant (plage, moyenne, médiane). Le contrôle de plage est fixé à `0 < amount <= 1 500 EUR`, seuil arrondi au-dessus du maximum historique mesuré de 1 400,79 EUR; les contrôles moyenne/médiane conservent leurs bornes à 1–500 EUR. Cela préserve le vrai historique tout en détectant le lot multiplié par 100. Dans le lot incident, 592/600 montants dépassent 1 500 EUR; la médiane vaut 18 488,50 et la moyenne 18 922,69.
- **Commandes (`gx_orders.py`)** — 12 expectations exactement; validation exécutée sur les 5 207 lignes avec noms de colonnes du vrai schéma. Résultat global **FAIL**, 6 expectations échouent : unicité `order_id` (14 lignes en doublon, 7 identifiants), existence de `customer_id` dans le référentiel client (14 références inconnues), non-null `order_date` (11), absence de dates futures au 24/11/2026 (5), domaine `status` (9 variantes non canoniques), et montant strictement positif/inférieur à 2 000 EUR (6 cas; minimum −49,90 EUR). Ce sont des anomalies présentes dans les données, non des bogues de script. Les dates vides ne sont pas comptées par le contrôle regex car la regex n’attache pas de contrainte de longueur; le contrôle distinct de non-null les signale.
- Les Data Docs ont été générés dans `gx/uncommitted/data_docs/local_site/` avec le rapport de validation. Une tentative de capture PNG par Playwright/Chromium a échoué : bibliothèque système `libatk-1.0.so.0` absente et l’installation des dépendances système demande des privilèges administrateur. Aucun faux screenshot n’a été créé; `data_docs_orders.png` n’est donc pas fourni.
- **Clients** — `replay_openrefine_recipe.py data/customers.csv` rejoue `openrefine_customers_recipe.json` sur la source originale et produit `customers_clean.csv` (1 241 → 1 233 lignes). La recette nettoie les espaces/casse des courriels et téléphones, normalise pays en codes FR/DE/BE/ES et corrige les variantes de niveau fidélité; elle enlève les 8 lignes complètes exactement dupliquées en conservant la première. Résultats : doublons de lignes complètes 8→0, IDs clients dupliqués 8→0, variantes pays 17 valeurs brutes→5 valeurs (4 codes et 36 pays vides), variantes de fidélité 8→4. Les 48 courriels vides et 19 courriels non conformes selon une vérification syntaxique simple restent à traiter; aucune valeur manquante n’a été inventée.
- **Scorecard** — `quality_scorecard.csv` contient 21 mesures réelles sur les sept datasets du kit plus le lot d’incident (8 noms de datasets), et couvre les six dimensions du cours : complétude, unicité, validité, cohérence, exactitude et fraîcheur. Chaque ligne donne règle, résultat mesuré, sévérité, rôle responsable et justification. Les contrôles métier provisoires (plafonds EUR et notes/client requis) sont explicitement présentés comme hypothèses à valider dans le contrat.

## Reproduction

Depuis ce dossier :

```bash
python gx_payments.py
python gx_orders.py
python replay_openrefine_recipe.py data/customers.csv
```

Le scorecard est le snapshot mesuré disponible dans `quality_scorecard.csv`. Les anomalies constatées, en particulier références orphelines, doublons, dates et données sensibles potentielles dans les tickets, sont à instruire avec les responsables indiqués avant correction ou mise en quarantaine.
