# Rapport de rendu — CTP 3 bradly

## Livrables demandés par les slides

| Exigence | Fichier livré |
|---|---|
| YAML de gouvernance staging avec descriptions, owners, stewards, domaines, tier, classification PII et tests | `shopfast_dbt/models/staging/_staging.yml` |
| YAML de gouvernance marts | `shopfast_dbt/models/marts/_marts.yml` |
| Sortie de `check_governance.py` montrant PASSED | `logs/governance_final.txt` |
| Trois exposures : Sales, rapport Finance mensuel, modèle ML churn | `shopfast_dbt/models/exposures.yml` |
| Note d'impact demandée en cinq lignes | `shopfast_dbt/impact_payments_cents.md` |
| Glossaire CSV de cinq termes | `glossary_template.csv` |
| Blocs docs glossary (dont net_revenue) et lien depuis la colonne via doc() | `shopfast_dbt/models/glossary.md`, `shopfast_dbt/models/marts/_marts.yml` |
| Dictionnaire de 15 colonnes commandes/paiements | `data_dictionary_template.csv` |

L'export bonus de `export_dictionary.py` est aussi inclus sous `shopfast_dbt/data_dictionary_from_dbt.csv`.

## Résultats

Le contrôle initial a signalé **7 problèmes de gouvernance** (description de modèle manquante ou owner absent). Le build dbt initial fonctionnait après correction du chemin vers les données locales; le compteur initial concerne bien le `check_governance.py`. À l'état final, `dbt build` a terminé sans erreur : 19 PASS, 0 WARN, 0 ERROR et 3 exposures NO-OP. Les 12 tests déclarés sont passés; `dbt parse` et `dbt docs generate` ont réussi. Le contrôle final affiche `Models: 7 | documented columns: 58/58` et `GOVERNANCE CHECK: PASSED`. Les commandes et sorties sont conservées dans `logs/`.

## Décisions métier / phrase demandée

Définition commune : client actif = compte ayant au moins une commande non annulée sur les 12 derniers mois (standard Finance/board); Sales peut conserver sa fenêtre saisonnière en la nommant « récemment actif — 6 mois ». Le net revenue est calculé comme (montant brut − remboursements) ÷ 1,20, arrondi à deux décimales, hors TVA et frais de livraison inclus, conformément au mémo Finance et à l’hypothèse de TVA à 20 % fournie par le support.

Note d'impact à transmettre à l'équipe paiements : « Un changement cents/euros sur `stg_payments.amount` fausserait les remboursements et le net revenue de `fct_orders`, puis les métriques clients et les usages Sales, Finance et churn; prévenir Paul Girard, Sara Martin et Karim Benali; ajouter un contrôle d'unité/échelle et de rapprochement des montants; vérifier les échantillons et le contrat EUR avant déploiement; Paul Girard approuve le changement de définition/revenu, Sara Martin confirme l'impact dashboard. » Le texte découpé en cinq points est dans `shopfast_dbt/impact_payments_cents.md`.

## Action manuelle

Les slides demandent d'ouvrir dbt docs et rechercher « pii ». À faire manuellement dans un navigateur après `dbt docs generate` / `dbt docs serve --port 8080`, puis prendre la capture d'écran si l'enseignant la demande; aucune capture n'est incluse.
