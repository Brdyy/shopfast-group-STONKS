# CTP 3 — Gouvernance dbt — bradly

Dossier de rendu du CTP 3. Le projet dbt est dans `shopfast_dbt/`; les CSV fournis nécessaires à l’exécution sont dans `shopfast_dbt/data/` et le chemin de source est relatif au répertoire du projet.

## Vérification locale

Depuis `shopfast_dbt/`, avec `dbt-duckdb` installé :

```bash
dbt build --profiles-dir .
dbt parse --profiles-dir .
python check_governance.py
dbt docs generate --profiles-dir .
```

Le build vérifié termine avec 19 tests/modèles réussis, aucun échec et trois exposures sans action de build (NO-OP). Le contrôle de gouvernance affiche `GOVERNANCE CHECK: PASSED` (58/58 colonnes décrites). Les logs initiaux et finaux sont conservés dans `logs/`.

## Contenu à remettre

- `shopfast_dbt/models/staging/_staging.yml` et `shopfast_dbt/models/marts/_marts.yml` : documentation, propriétaires/stewards/domaines/tier, PII classifiées et tests.
- `shopfast_dbt/models/exposures.yml` et `shopfast_dbt/impact_payments_cents.md` : trois usages downstream et note d’impact de cinq lignes.
- `glossary_template.csv` et `shopfast_dbt/models/glossary.md` : cinq termes approuvés, règles, exemples, propriétaires et dates; `net_revenue_eur` utilise le bloc docs via `doc()`.
- `data_dictionary_template.csv` : 15 colonnes des modèles stg_orders et stg_payments.
- `shopfast_dbt/data_dictionary_from_dbt.csv` : export bonus généré depuis le manifest dbt.

Le rapport de rendu détaillé est dans `rapport_rendu.md`.
