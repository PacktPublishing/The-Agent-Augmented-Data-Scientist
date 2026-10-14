---
name: cg-team-context
description: >
  Cascade Goods' Product and Growth Data Science team charter,
  responsibilities, and working approach. Read when framing
  analytical work for the team.
owner: Ryan B., Senior Data Science Manager
status: draft
last_reviewed: 2026-09-19
---

# Cascade Goods team context

## Team charter

Cascade Goods’ Product and Growth Data Science team works as a business partner to Product on customer acquisition, engagement and conversion, and retention and reactivation. The team participates early in planning to identify opportunities, challenge assumptions, and agree how success will be measured. It helps prioritize customer problems, evaluate product improvements, and understand whether those changes improve purchasing outcomes.

Work can originate from Product priorities, questions identified by the data science team, or a combination of both. The teams work together to clarify the problem and decide which questions are worth pursuing.

The team supports CG's repeat-purchasing priority by identifying barriers to repeat purchasing, helping Product prioritize improvements, and evaluating their results.

Our focus areas are:

- **Acquisition:** Understand how new customers reach their first purchase and which experiences help or hinder that process.
- **Engagement and conversion:** Understand how customers explore products, where they encounter friction, and what helps them complete a purchase.
- **Retention and reactivation:** Understand repeat purchase behavior, identify inactivity, and evaluate efforts to bring customers back.

## Stakeholders and responsibilities

| Stakeholder | What they own | What they need from Data Science |
|---|---|---|
| **Product Management** | Customer problems, product requirements, and prioritization within their product area. | Findings connected to a product decision: affected customers or journeys, supporting evidence, and trade-offs between options. |
| **Engineering** | Product instrumentation, event capture, and implementation of product changes. | Specific, reproducible findings. For tracking issues, identify the affected event, platform, period, expected behavior, and observed discrepancy. |
| **Product Leadership** | Product priorities, resource allocation, and trade-offs across initiatives. | A concise account of business impact, progress against objectives, decisions needed, and material uncertainty. Keep supporting technical evidence available. |

## How we work

- **Learn:** Understand the business context, underlying problem, decision to support, and why it matters.
- **Hypothesize:** Develop plausible explanations or potential solutions and identify the evidence needed to assess them.
- **Build:** Carry out the analysis, experiment, or model development appropriate to the question.
- **Evaluate:** Check whether the evidence supports the intended decision and meets analytical standards.

Scale the work to the request. Revisit earlier steps when findings change the problem or expose missing context. When work leads to an intervention, agree how its outcomes will be measured.

## Recurring stakeholder forums

**Quarterly product and business review.** CG's fiscal year runs from December through November. On the first Monday of each fiscal quarter, Product Leadership, Product Management, Engineering, and DS review the previous quarter's results and agree priorities. DS brings an assessment of performance against agreed product and business metrics, findings from completed work, and unresolved questions that affect priorities.

## Data handling

Customer-level data is Confidential. Follow the classification documented for each product-data source. Use approved tools and sharing locations; ask the responsible data scientist when handling requirements are unclear.

## Supporting references and upkeep

- [Business context](business_context.md): business model and shared business concepts.
- [DS standards](../execution/DS_STANDARDS.md): analytical and verification requirements.
- [Metric registry](metric_registry.md): shared metric definitions and calculation logic.

The file owner reviews changes to this document.
