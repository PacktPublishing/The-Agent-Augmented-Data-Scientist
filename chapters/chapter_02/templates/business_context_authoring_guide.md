# Create your business context

Use this guide with your preferred AI agent to develop a concise `business_context.md` for your organization. Have relevant materials ready if available: a company overview, product documentation, existing definitions, or a trusted analysis. You can also begin with what you know.

The [Cascade Goods example](../../../cascade_goods/context/business_context.md) illustrates the scope and level of detail. Adapt the sections to your business.

## Starting prompt

> Help me create a business context document using this guide. Establish which part of the business it covers. Read my materials and research relevant public sources when available, then ask one question at a time to fill meaningful gaps. Surface assumptions and conflicting information for me to resolve. Draft a concise document and ask me to review and approve its contents before treating it as ready to use.

## Instructions for the agent

### Establish the scope

Establish which business unit, product family, or market the document covers. Briefly locate it within the broader company, then focus on that scope. Describe its customers, offerings, commercial relationships, and activities that affect analysis.

Keep the team's charter, stakeholders, responsibilities, and chosen lifecycle focus for `team_context.md`. For example, renewal is a business event; the team's responsibility for improving renewal belongs in team context. If the reader starts with their role, use that to identify business scope and retain the remaining details for the team document.

### Research alongside the conversation

Read supplied materials before asking questions they answer. When browsing is available, consult authoritative public sources for the relevant business and products. Use findings to propose descriptions and ask informed questions. Confirm their applicability with the reader. Keep internal details out of public search queries.

Keep research sources and evidence in the drafting conversation so the reader can check proposed claims. For conflicts, check authority, effective period, and affected population; newer material may cover a different scope. Public sources cannot establish internal account mappings, team responsibilities, or approved metric definitions without evidence. The reader reviews and approves all content, regardless of its source.

If sources are unavailable, proceed with the reader's knowledge and mark material gaps. Do not infer policy from sample data or copy another company's assumptions.

### Develop the context together

Choose one question at a time based on what remains materially unknown. Explain why it matters when the connection to analytical work is unclear. Offer examples when helpful, without turning them into assumed facts. Skip questions already answered and follow up where an answer exposes ambiguity.

Use these topics as prompts for discussion:

| Topic | Questions to explore |
|---|---|
| Offerings and business model | What does this part of the business provide, to whom, and how does it generate revenue or fulfill its mission? Which markets and channels matter? |
| Customers and users | Who buys, uses, or benefits? How do organizations, accounts, people, or households relate? What differences in customer size or value affect interpretation? |
| Commercial relationships | Where relevant, how do purchases, contracts, subscriptions, seats, or usage charges work? Do arrangements vary across products or customers? |
| Product relationships | Can customers use multiple products? What does that change about interpreting customer value, activity, or retention? |
| Activities and lifecycle | Which usage, purchase, renewal, expansion, cancellation, or other events matter here? What distinctions could an analyst misunderstand? Ask for a concrete example. |
| Supporting knowledge | Where are approved metrics, data documentation, team context, and analytical standards maintained? Who should review changes to this document? |

Adapt these topics to the business. Labels such as B2B or subscription do not establish a uniform commercial model. Explain consequential ambiguities and confirm interpretations. When the reader cannot resolve a gap, record its effect and continue drafting instead of repeatedly asking for unavailable information.

### Draft the document

Share short sections for correction as understanding develops. Label early drafts as partial and identify the next material gap. Aim for roughly 300–500 words; use fewer when sufficient. Add detail only when it changes interpretation across likely tasks.

Use headings that fit the organization and write a coherent account of the business. Omit labels such as “public facts,” “internal context,” and “analytical implication.” Keep research citations in the drafting conversation. Where useful, link to existing metric definitions, data documentation, team context, or analytical standards instead of duplicating them. These operational links are optional; do not create a references section solely to list unavailable documents.

Use the following metadata, replacing placeholders with confirmed values:

```yaml
---
name: "[organization]-business-context"
description: "[What this context covers and when an agent should read it.]"
owner: "[Name, role]"
status: draft
last_reviewed: "[YYYY-MM-DD]"
---
```

Keep the owner as a single value. Record when the reader reviewed the content; leave the date pending until then. Leave unknown metadata marked for completion. If operational links are included, format them as bullets under Supporting references and upkeep. Add a short upkeep statement naming the reviewer or marking that responsibility unresolved.

### Review before use

Check the draft with the reader:

- Has the reader checked the proposed claims and confirmed that they apply to the agreed business scope?
- Does the document explain the distinctions most likely to change an analysis?
- Have team-charter details, duplicated definitions, and assumptions borrowed from CG been removed?
- Are unresolved questions clear, including which work they affect?

Try the draft against one or two representative analytical questions. Explain what it clarifies and what additional context the agent would still need. Revise consequential gaps with the reader. This checks usefulness; it does not validate metric calculations or analytical results.

Keep consequential unknowns and their implications inside the file so they survive outside the conversation. Omit unsettled claims that are unnecessary to the current scope. Return remaining follow-up items separately. Ask the reader to approve the complete document before treating its contents as established shared context; approval does not resolve explicitly retained unknowns.
