---
name: "[organization]-metric-registry"
description: "Shared metric definitions and links to SQL. Read before calculating a registered metric."
owner: "[Name, role]"
status: draft
last_reviewed: "[YYYY-MM-DD]"
---

# [Organization] metric registry

Start with two foundational metrics relevant to the decisions your team supports. Use existing approved definitions where available. Add metrics as you develop playbooks. Replace the guidance below with your definitions; the [CG registry](../../../cascade_goods/context/metric_registry.md) provides worked examples.

## Shared rules

[Include only rules that apply across these metrics, such as population exclusions or reporting conventions. Omit this section if none apply. Keep metric-specific rules in their entries.]

## [Metric name]

Copy this entry for each metric. Keep the same seven attributes.

| Attribute | Definition |
|---|---|
| ID | [Stable metric identifier.] |
| Definition | [What it measures, its unit, and when to use it.] |
| Source and grain | [Source tables or views, relevant fields, unit of observation, and required joins.] |
| Calculation | [Formula, qualifying population, exclusions, and handling of empty populations or zero denominators where relevant.] |
| Time basis | [Relevant event date, reporting boundaries, time zone, and snapshot treatment where applicable.] |
| Caveats | [Limitations or interpretation traps that affect use.] |
| Implementation | [Link to the SQL, its dialect, required parameters, and corresponding output column.] |

## Checking the calculations

For each metric, record a check against a small example with an independently established expected result or a trusted result with matching scope. Include the inputs or period, expected and actual values, and any unresolved discrepancy. Check the definition's consequential cases, such as exclusions, date boundaries, or duplicate rows from joins.

A brief worked example or saved SQL check is sufficient for this starter. A Python runner or automated test suite is not required. Mark unrun SQL and unresolved checks explicitly; the existence of a query does not establish that the calculation is validated.
