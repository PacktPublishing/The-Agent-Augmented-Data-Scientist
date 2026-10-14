---
name: cg-business-context
description: >
  Cascade Goods' business model, customers, channels, and purchasing
  concepts. Read when interpreting a CG business question.
owner: Ryan B., Senior Data Science Manager
status: draft
last_reviewed: 2026-09-19
---

# Cascade Goods business context

This file covers CG's business model and shared business concepts. Metric definitions, data structure, and team procedures are maintained separately; their references and availability are listed below.

## Company and business model

Cascade Goods (CG) is a US retailer selling consumer electronics and general merchandise, including laptops, televisions, phones, cameras, smart-home products, and related accessories. CG sells directly to customers through its website, mobile app, and physical stores across ten US regions.

CG fulfills customer orders and generates revenue primarily through merchandise sales. Product costs, discounts, refunds, and returns affect profitability. CG has no subscription or recurring-billing component.

CG's current growth priority is to expand purchasing through its website and mobile app while continuing to serve customers through physical stores. This includes encouraging existing store customers to adopt its digital channels and giving customers reasons to return for purchases across its product range. The company wants these channels to support a longer purchasing relationship, beyond the individual product or promotion that first brought a customer to CG.

## Customers and purchasing behavior

CG's customer lifecycle spans discovering the retailer, making a first purchase, and developing an ongoing purchasing relationship. A simplified journey is:

Awareness → Consideration → Purchase → Post-purchase experience → Loyalty

Customers can revisit these stages, pause, or return after an absence. For CG, repeat purchasing can also span categories: a laptop buyer may later return for accessories, a television, or smart-home products. Retention concerns the customer's relationship with CG, rather than repeated purchases of the same product.

CG has no subscription cancellation or contract expiry that signals when a customer has left. A television buyer may have no reason to replace that product for several years. A holiday shopper may return each December, while another customer makes smaller purchases throughout the year. A period without purchases needs to be understood against those patterns. Likewise, a purchase after a prolonged absence indicates reactivation, but does not yet establish that the customer will continue purchasing.

The customer relationship spans CG's website, mobile app, and physical stores. An existing store customer making their first app purchase is adopting another channel, rather than becoming a new customer to CG.

Purchasing follows US retail seasonality, with higher order volumes around Black Friday and the December holidays. These events create opportunities for customers to return for gifts or planned purchases, so a seasonal return should not automatically be interpreted as year-round purchasing behavior.

## Orders and customer value

Orders can be completed, cancelled, or pending. Returns and refunds are recorded separately from order status. A completed order with a refund still records a purchase event; its treatment in a metric depends on the approved definition.

CG sells both low-priced accessories and higher-priced products such as televisions and laptops. Customers with similar purchase counts can therefore represent very different amounts of spending.

Discounts reduce what customers pay, while later refunds can reduce the revenue retained from a purchase. Revenue and profitability are not interchangeable: product costs and other relevant costs also affect profitability.

## Supporting references and upkeep

- [Metric registry](metric_registry.md): shared metric definitions, calculation rules, and links to SQL and checks.
- [Data documentation](../data/README.md): sources, fields, grain, and relationships.
- [Team context](team_context.md): responsibilities and working norms.
- [DS standards](../execution/DS_STANDARDS.md): analytical and verification requirements.

The file owner reviews changes to this document.
