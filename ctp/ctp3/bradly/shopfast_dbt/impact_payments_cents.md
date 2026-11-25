1. A cents-to-euros change to `stg_payments.amount` would misstate `fct_orders.refunded_eur` and `net_revenue_eur`, and could affect `dim_customers` lifetime revenue and all three downstream exposures.
2. Warn Paul Girard (Finance, owner of net revenue and monthly report), Sara Martin (Sales dashboard and customer dimension), and Karim Benali (steward).
3. Add a unit/scale reconciliation test comparing captured payment totals to order totals within a documented tolerance, plus a currency and non-negative amount check.
4. Verify sample rows and the EUR two-decimal contract before deploying; do not reinterpret amount as cents without a coordinated migration.
5. Paul Girard (Head of Finance) approves the revenue definition and amount-unit change, with Sara Martin confirming dashboard impact.
