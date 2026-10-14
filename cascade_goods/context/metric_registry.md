---
name: cg-metric-registry
description: >
  Shared CG metric definitions and links to reusable calculations and checks.
  Read before calculating a registered metric.
owner: Maya S, Senior Data Scientist
status: draft
last_reviewed: 2026-09-19
---

# Cascade Goods metric registry

Draft definitions for review. Each entry uses the same seven attributes. Shared rules apply to all four metrics.

## Shared rules

- **Eligible customers:** Exclude accounts flagged as internal/test or using `cascadegoods.com` or `qa.cascadegoods.test`, after trimming and lowercasing domains. Exclude their purchases too. Resolve missing or invalid exclusion inputs before calculating.
- **Purchases:** Use completed orders, including partially and fully refunded purchases. Refunds reduce monetary value separately.
- **Reporting periods:** Use UTC order placement dates, with an inclusive start and exclusive end. Statuses and refunds reflect the dataset snapshot.

Each query applies these customer exclusions directly. [Data documentation](../data/README.md) supplies the snapshot date, currency, field definitions, and relationships.

## Completed orders

| Attribute | Definition |
|---|---|
| ID | `completed_orders` |
| Definition | Number of eligible completed purchase events, in orders. Use to measure purchase volume. |
| Source and grain | `orders.order_id` at order grain; join `customers` for eligibility. |
| Calculation | Count distinct qualifying `order_id`, applying shared rules. Return `0` when none qualify. |
| Time basis | Placement date within the reporting period; completion status at the snapshot. |
| Caveats | Completion timestamps are unavailable, so this cannot count purchases by completion date. |
| Implementation | [SQL](../execution/metrics/order_metrics.sql) → `completed_orders` output column. |

## Purchasing customers

| Attribute | Definition |
|---|---|
| ID | `purchasing_customers` |
| Definition | Number of eligible customers with a completed purchase in the period, in customers. Use to measure the size of the purchasing customer base. |
| Source and grain | `orders.customer_id`, joined to `customers` for eligibility; count each customer once per period. |
| Calculation | Count distinct customers on qualifying orders, applying shared rules. Return `0` when none qualify. |
| Time basis | Placement date within the reporting period; completion status at the snapshot. |
| Caveats | Includes new and returning customers. Do not sum period counts: the same customer can appear in several periods. |
| Implementation | [SQL](../execution/metrics/order_metrics.sql) → `purchasing_customers` output column. |

## Units per transaction

| Attribute | Definition |
|---|---|
| ID | `units_per_transaction` |
| Definition | Average originally purchased units per eligible completed order, in units per order. Use to compare basket quantity. |
| Source and grain | `order_items.quantity` at line grain, aggregated by `order_id` before joining `orders`; `customers` supplies eligibility. |
| Calculation | Sum qualifying purchased units ÷ `completed_orders`, retaining returned units. Return `NULL` when no orders qualify. |
| Time basis | Placement date within the reporting period; completion status at the snapshot. |
| Caveats | Missing item records on any qualifying order produce `NULL`; resolve missing data before interpreting it. To combine periods, weight averages by completed orders. |
| Implementation | [SQL](../execution/metrics/basket_metrics.sql) → `units_per_transaction` output column. |

## Net average order value

| Attribute | Definition |
|---|---|
| ID | `net_average_order_value` |
| Definition | Average merchandise value per eligible completed order after discounts and recorded refunds, in USD per order. Use to compare net basket value across periods or customer groups. |
| Source and grain | Use `orders.adjusted_revenue` at order grain; `customers` supplies eligibility. Do not substitute catalog prices or unadjusted line revenue. |
| Calculation | Sum qualifying `adjusted_revenue` ÷ `completed_orders`. Fully refunded orders remain in the denominator. Exclude shipping and tax. Return `NULL` when no orders qualify; round to two decimals for display. |
| Time basis | Placement date within the reporting period; completion status and recorded refunds at the snapshot. |
| Caveats | Recent periods may have incomplete refunds, making the average appear higher. Compare periods with similar time for returns to be recorded. |
| Implementation | [SQL](../execution/metrics/order_metrics.sql) → `net_average_order_value` output column. |

## Running and checking metrics

The order query returns completed orders, purchasing customers, and net average order value using customers and orders. The basket query adds order items to calculate units per transaction. Both apply the customer exclusions directly; definitions remain in the registry.

The [CSV runner](../execution/metrics/run_purchase_metrics.py) loads only the selected group's tables and fields into SQLite. It checks keys, references, dates, and exclusion inputs, plus monetary values for order metrics or quantities for basket metrics. Apply equivalent checks when running SQL directly. Missing item records leave units per transaction undefined; order metrics can run independently.

The [calculation tests](../evaluation/test_metrics.py) use known examples for exclusions, refunds, date boundaries, customer counts, join grain, missing lines, and empty periods. They test calculation behavior, not agent behavior or owner approval.

Run from the repository root:

```sh
python3 cascade_goods/execution/metrics/run_purchase_metrics.py --group orders --start-date 2025-01-01 --end-date 2026-01-01
python3 cascade_goods/execution/metrics/run_purchase_metrics.py --group basket --start-date 2025-01-01 --end-date 2026-01-01
python3 -m unittest discover -s cascade_goods/evaluation -p 'test_*.py'
```
