{% docs gross_revenue %}
**Gross revenue (EUR)** — total amount paid by the customer for an order, VAT included, shipping included, before refunds.
Owner: Head of Sales · Steward: Karim Benali · Status: approved (2026-11-10)
{% enddocs %}

{% docs net_revenue %}
**Net revenue** is order revenue after refunds, excluding VAT, while retaining shipping fees.
Rule: (gross order amount − refunds) ÷ 1.20, rounded to two decimals (ShopFast VAT assumption: 20%). Example: €120.00 paid, no refund → €100.00 net revenue. Owner: Paul Girard, Head of Finance · Steward: Karim Benali · Approved 2026-11-25.
{% enddocs %}

{% docs active_customer %}
An **active customer** has at least one non-cancelled order during the trailing 12 months, the company-wide definition used for board and financial reporting.
Rule: customer has an order with status other than cancelled and order_date within the prior 12 months. Example: an order on 2026-06-10 makes the account active on 2026-11-25 if it was not cancelled. Owner: Paul Girard, Head of Finance · Steward: Karim Benali · Approved 2026-11-25. Sales retains its seasonal view by filtering non-cancelled orders to the trailing 6 months and labels it “recently active customer” (not the company-wide active-customer metric).
{% enddocs %}

{% docs churned_customer %}
A **churned customer** is an account with no non-cancelled order during the trailing 12 months.
Rule: no qualifying order in the prior 12 months; this is the complement of active customer for identifiable accounts. Example: last qualifying order 2025-10-01 means churned on 2026-11-25. Owner: Paul Girard, Head of Finance · Steward: Karim Benali · Approved 2026-11-25.
{% enddocs %}

{% docs order %}
An **order** is a customer purchase request recorded by ShopFast with a unique order ID, date, channel, destination and lifecycle status.
Rule: one record per order_id in stg_orders. Example: order 700002 is one order placed through mobile_app on 2026-10-08. Owner: Sara Martin, Head of Sales · Steward: Karim Benali · Approved 2026-11-25.
{% enddocs %}

{% docs customer %}
A **customer** is a ShopFast account identified by a customer_id and used to associate purchases and customer attributes.
Rule: one account row per customer_id in dim_customers; one person may hold more than one account. Example: customer_id 10410 is an account key, not a guaranteed unique natural person. Owner: Sara Martin, Head of Sales · Steward: Karim Benali · Approved 2026-11-25.
{% enddocs %}
