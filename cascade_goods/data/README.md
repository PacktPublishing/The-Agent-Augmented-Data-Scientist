---
name: cg-data-dictionary
description: >
  Shared CG data documentation covering the table relationships and dataset
  conventions in this README and the field definitions in data_dictionary.csv.
owner: Maya S, Senior Data Scientist
status: draft
last_reviewed: 2026-09-27
---

# Cascade Goods data

Update `last_reviewed` after reviewing both this README and the accompanying
[data dictionary](data_dictionary.csv) against the dataset and its source documentation.

## Data conventions

- **Currency:** All monetary amounts are in US dollars (USD).
- **Time:** Order timestamps are interpreted as UTC. The CSV stores them without a timezone offset; `order_date` is the UTC date portion.
- **Coverage:** Recorded orders span January 1, 2024 through December 31, 2025. Earlier purchase history is not provided.
- **Snapshot:** Customer account statuses and current catalog attributes are as of December 31, 2025. Current catalog prices and availability do not describe historical changes.

## Tables and relationships

| Table | Intended grain | Key and relationships | Use |
|---|---|---|---|
| [customers.csv](customers.csv) | One record per customer | `customer_id`; referenced by orders | Account, lifecycle, and customer attributes |
| [orders.csv](orders.csv) | One record per order | `order_id`; `customer_id` links to customers | Order-level outcomes and order status |
| [order_items.csv](order_items.csv) | One record per order line | `order_item_id`; `order_id` links to orders and `sku` links to products; includes a denormalized `customer_id` | Product-level sales, units, category, and basket analysis |
| [products.csv](products.csv) | One record per product | `sku`; referenced by order items | Catalog and category attributes |

See the [data dictionary](data_dictionary.csv) for field definitions and documented values.

Before using a table, confirm its grain, date coverage, refresh behavior, join keys, and whether the requested metric belongs at that grain. Intended relationships describe the data model; validate them in the data before joining or aggregating.
