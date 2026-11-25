#!/usr/bin/env python3
"""Tests GX Core 1.x pour les commandes ShopFast; référence temporelle fixe: 2026-11-25."""
from pathlib import Path
import os
os.environ["TQDM_DISABLE"] = "1"
import pandas as pd
import great_expectations as gx
BASE=Path('/home/user/ctp2/shopfast-kit/data')
if not BASE.exists(): BASE=Path(__file__).parent/'shopfast-kit/data'
orders=pd.read_csv(BASE/'orders.csv',dtype=str)
customers=pd.read_csv(BASE/'customers.csv',dtype=str)
orders['order_date_dt']=pd.to_datetime(orders.order_date,format='%Y-%m-%d',errors='coerce')
orders['total_amount_eur']=pd.to_numeric(orders.total_amount_eur,errors='coerce')
ctx=gx.get_context(mode='file', project_root_dir=str(Path(__file__).resolve().parent/'gx_orders_context'))
src=ctx.data_sources.add_or_update_pandas('shopfast_orders')
asset=src.add_dataframe_asset(name='orders')
batch=asset.add_batch_definition_whole_dataframe('all_orders')
suite=ctx.suites.add_or_update(gx.ExpectationSuite(name='orders_suite'))
E=gx.expectations
expectations=[
 E.ExpectColumnValuesToNotBeNull(column='order_id'),
 E.ExpectColumnValuesToBeUnique(column='order_id'),
 E.ExpectColumnValuesToNotBeNull(column='customer_id'),
 E.ExpectColumnValuesToBeInSet(column='customer_id',value_set=set(customers.customer_id.dropna())),
 E.ExpectColumnValuesToNotBeNull(column='order_date'),
 E.ExpectColumnValuesToMatchRegex(column='order_date',regex=r'^\d{4}-\d{2}-\d{2}$'),
 E.ExpectColumnValuesToBeBetween(column='order_date_dt',min_value=pd.Timestamp('1900-01-01'),max_value=pd.Timestamp('2026-11-25'),strict_max=False),
 E.ExpectColumnValuesToBeInSet(column='status',value_set=['pending','shipped','delivered','cancelled','returned']),
 E.ExpectColumnValuesToBeInSet(column='channel',value_set=['web','mobile_app','marketplace']),
 E.ExpectColumnValuesToBeInSet(column='shipping_country',value_set=['FR','DE','ES','BE']),
 E.ExpectColumnValuesToBeBetween(column='total_amount_eur',min_value=0,strict_min=True,max_value=5000),
 E.ExpectColumnValuesToNotBeNull(column='total_amount_eur'),
]
for e in expectations: suite.add_expectation(e)
suite.save()
vd=ctx.validation_definitions.add_or_update(gx.ValidationDefinition(name='orders_validation',data=batch,suite=suite))
cp=ctx.checkpoints.add_or_update(gx.Checkpoint(name='orders_checkpoint',validation_definitions=[vd],actions=[gx.checkpoint.UpdateDataDocsAction(name='docs')]))
result=cp.run(batch_parameters={'dataframe':orders})
print('GX version:',gx.__version__,'; expectations:',len(expectations),'; overall:',result.success)
for vr in result.run_results.values():
 for r in vr.results:
  print(('PASS' if r.success else 'FAIL'),r.expectation_config.type,r.expectation_config.kwargs.get('column'), 'unexpected=',r.result.get('unexpected_count','-'))
print('Data Docs: gx/uncommitted/data_docs/local_site/index.html')
