"""CTP 2 Exercise 4: demonstrate that naive checks miss cents and value/distribution checks catch it.
GX Core 1.x (validated with 1.7.1). Historical and incident results use data/payments.csv plus payments_batch_2.csv.
"""
from pathlib import Path
import os
import pandas as pd
import great_expectations as gx

ROOT = Path(__file__).resolve().parent
DATA = Path(os.getenv("SHOPFAST_DATA_DIR", ROOT / "data"))
BATCH2 = Path(os.getenv("PAYMENTS_BATCH_2", ROOT / "payments_batch_2.csv"))
context = gx.get_context(mode="file")
source = context.data_sources.add_or_update_pandas("shopfast_payments")
asset = source.add_dataframe_asset(name="payments")
batch_def = asset.add_batch_definition_whole_dataframe("whole")
E = gx.expectations
def expectations(smart=False):
    checks = [
        E.ExpectColumnValuesToNotBeNull(column="payment_id"),
        E.ExpectColumnValuesToBeUnique(column="payment_id"),
        E.ExpectColumnValuesToNotBeNull(column="amount"),
        E.ExpectColumnValuesToBeInSet(column="currency", value_set=["EUR"]),
        E.ExpectColumnValuesToBeInSet(column="method", value_set=["card", "paypal", "apple_pay", "bank_transfer"]),
    ]
    if smart:
        checks += [
            E.ExpectColumnValuesToBeBetween(column="amount", min_value=0, max_value=1500, strict_min=True),
            E.ExpectColumnMeanToBeBetween(column="amount", min_value=1, max_value=500),
            E.ExpectColumnMedianToBeBetween(column="amount", min_value=1, max_value=500),
        ]
    return checks

def run(label, data_path):
    df = pd.read_csv(data_path, dtype=str)
    df["amount_txt"] = df["amount"]
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    for suite_name, checks in [("naive_payments", expectations()), ("smart_payments", expectations(smart=True))]:
        suite = context.suites.add_or_update(gx.ExpectationSuite(name=suite_name))
        for exp in checks:
            suite.add_expectation(exp)
        suite.save()
        result = batch_def.get_batch(batch_parameters={"dataframe": df}).validate(suite)
        failed = [r.expectation_config.type for r in result.results if not r.success]
        print(f"{label:<24} {suite_name:<15} success={result.success} failed={failed}")

print(f"GX {gx.__version__}; naive expectations={len(expectations())}; smart expectations={len(expectations(smart=True))}")
if (DATA / "payments.csv").exists():
    run("payments (history)", DATA / "payments.csv")
else:
    print(f"payments (history)      NOT RUN: missing {DATA / 'payments.csv'}")
if BATCH2.exists():
    run("payments_batch_2 (new)", BATCH2)
else:
    raise SystemExit(f"Missing incident batch: {BATCH2}")
