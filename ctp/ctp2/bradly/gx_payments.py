#!/usr/bin/env python3
"""Suite naïve et contrôles de plage/distribution pour reproduire l'incident EUR/cents."""
from pathlib import Path
import pandas as pd
import great_expectations as gx
HERE=Path(__file__).resolve().parent
KIT=Path('/home/user/ctp2/shopfast-kit/data')
if not KIT.exists(): KIT=HERE/'shopfast-kit/data'
BATCH=Path('/home/user/ctp2/payments_batch_2.csv')
if not BATCH.exists(): BATCH=HERE/'payments_batch_2.csv'
files={'historique':KIT/'payments.csv','lot_2':BATCH}
ctx=gx.get_context(mode='file', project_root_dir=str(HERE/'gx_payments_context'))
src=ctx.data_sources.add_or_update_pandas('shopfast_payments')
asset=src.add_dataframe_asset(name='payments')
bdef=asset.add_batch_definition_whole_dataframe('whole')
E=gx.expectations
naive=[E.ExpectColumnValuesToNotBeNull(column='payment_id'),E.ExpectColumnValuesToBeUnique(column='payment_id'),E.ExpectColumnValuesToNotBeNull(column='amount'),E.ExpectColumnValuesToBeInSet(column='currency',value_set=['EUR']),E.ExpectColumnValuesToBeInSet(column='method',value_set=['card','paypal','apple_pay','bank_transfer'])]
smart=naive+[E.ExpectColumnValuesToBeBetween(column='amount',min_value=0,strict_min=True,max_value=2000),E.ExpectColumnMedianToBeBetween(column='amount',min_value=100,max_value=500),E.ExpectColumnMeanToBeBetween(column='amount',min_value=100,max_value=500)]
def validate(name,exps,df):
 suite=ctx.suites.add_or_update(gx.ExpectationSuite(name=name))
 for exp in exps: suite.add_expectation(exp.copy())
 suite.save()
 return bdef.get_batch(batch_parameters={'dataframe':df}).validate(suite)
all_ok=True
for label,path in files.items():
 df=pd.read_csv(path,dtype=str);df['amount_txt']=df.amount;df['amount']=pd.to_numeric(df.amount,errors='coerce')
 naive_result=validate('payments_naive_'+label,naive,df)
 smart_result=validate('payments_smart_'+label,smart,df)
 failed=[r.expectation_config.type for r in smart_result.results if not r.success]
 print(f'{label}: lignes={len(df)} naïf={naive_result.success} intelligent={smart_result.success}; échecs intelligents={failed}; médiane={df.amount.median():.2f}; moyenne={df.amount.mean():.2f}')
 all_ok &= naive_result.success and smart_result.success==(label=='historique')
if not all_ok: raise SystemExit('Validation payments inattendue')
