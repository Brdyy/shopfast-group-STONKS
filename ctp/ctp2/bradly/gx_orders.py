"""CTP 2 Exercise 3. Great Expectations Core 1.x (validated with 1.7.1).
Requires data/orders.csv and data/customers.csv next to this script (or SHOPFAST_DATA_DIR).
The channel and shipping-country allowed values are profiled from the supplied batch;
this detects novel values on that batch but should be replaced by contract domains in production.
"""
from pathlib import Path
import os
import pandas as pd
import great_expectations as gx

DATA = Path(os.getenv("SHOPFAST_DATA_DIR", Path(__file__).resolve().parent / "data"))
orders_path, customers_path = DATA / "orders.csv", DATA / "customers.csv"
if not orders_path.exists() or not customers_path.exists():
    raise SystemExit(f"Missing required ShopFast data: need {orders_path} and {customers_path}; the provided starter zip contains no orders.csv/customers.csv.")
orders = pd.read_csv(orders_path, dtype=str)
customers = pd.read_csv(customers_path, dtype=str)
orders["total_amount_eur"] = pd.to_numeric(orders["total_amount_eur"], errors="coerce")
orders["order_date_dt"] = pd.to_datetime(orders["order_date"], format="%Y-%m-%d", errors="coerce")
customer_ids = set(customers["customer_id"].dropna().astype(str))
channels = sorted(orders["channel"].dropna().astype(str).unique().tolist())
countries = sorted(orders["shipping_country"].dropna().astype(str).unique().tolist())

context = gx.get_context(mode="file")
source = context.data_sources.add_or_update_pandas("shopfast")
asset = source.add_dataframe_asset(name="orders")
batch_def = asset.add_batch_definition_whole_dataframe("all_orders")
suite = context.suites.add_or_update(gx.ExpectationSuite(name="orders_suite"))
E = gx.expectations
expectations = [
    E.ExpectTableRowCountToBeBetween(min_value=1000, max_value=100000),
    E.ExpectColumnValuesToNotBeNull(column="order_id"),
    E.ExpectColumnValuesToBeUnique(column="order_id"),
    E.ExpectColumnValuesToNotBeNull(column="customer_id"),
    E.ExpectColumnValuesToBeInSet(column="customer_id", value_set=sorted(customer_ids)),
    E.ExpectColumnValuesToNotBeNull(column="order_date"),
    E.ExpectColumnValuesToMatchRegex(column="order_date", regex=r"^\d{4}-\d{2}-\d{2}$"),
    E.ExpectColumnValuesToBeBetween(column="order_date_dt", max_value=pd.Timestamp("2026-11-24")),
    E.ExpectColumnValuesToBeInSet(column="status", value_set=["pending", "shipped", "delivered", "cancelled", "returned"]),
    E.ExpectColumnValuesToBeInSet(column="channel", value_set=channels),
    E.ExpectColumnValuesToBeInSet(column="shipping_country", value_set=countries),
    E.ExpectColumnValuesToBeBetween(column="total_amount_eur", min_value=0, max_value=2000, strict_min=True, strict_max=True),
]
assert len(expectations) == 12
for exp in expectations:
    suite.add_expectation(exp)
suite.save()
vd = context.validation_definitions.add_or_update(gx.ValidationDefinition(name="orders_validation", data=batch_def, suite=suite))
checkpoint = context.checkpoints.add_or_update(gx.Checkpoint(name="orders_checkpoint", validation_definitions=[vd], actions=[gx.checkpoint.UpdateDataDocsAction(name="docs")]))
result = checkpoint.run(batch_parameters={"dataframe": orders})
print(f"GX {gx.__version__}; expectations={len(expectations)}; suite_passed={result.success}")
for validation in result.run_results.values():
    for r in validation.results:
        config = r.expectation_config
        print(f"{'PASS' if r.success else 'FAIL'} {config.type} column={config.kwargs.get('column','')} unexpected={r.result.get('unexpected_count','-')}")
print("Data Docs: gx/uncommitted/data_docs/local_site/index.html")
