# Create your team context

Use this guide with your preferred AI agent to develop a concise `team_context.md` after creating your business context. Provide that document as the starting input, along with an existing team charter or examples of the team's work if available. If you do not have a business-context file, provide an equivalent business overview.

The [Cascade Goods example](../../../cascade_goods/context/team_context.md) illustrates scope and detail. Adapt it to your team's responsibilities and working practices.

## Starting prompt

> Help me create a team context document using this guide and the business context I provide. Read that context and any relevant prior discussion first. Reuse established business information, then ask one question at a time about our charter, stakeholders, responsibilities, and working approach. Surface gaps or contradictions for me to resolve. Draft a concise document and ask me to review and approve its contents before treating it as ready to use.

## Instructions for the agent

### Establish the team's remit

Read the business context first to establish the covered business, products, customers, and commercial relationships. Identify the team and where it sits within that scope. Reuse established information and ask only for missing team-specific details. Ask what the team is responsible for helping the business achieve, and which decisions or outcomes its work supports.

If the team's description conflicts with the business context, surface the difference for the reader to resolve. Do not silently rewrite the business context or treat its unresolved assumptions as confirmed facts.

Keep company offerings, commercial relationships, and customer definitions in business context. Describe the team's remit here: for example, its responsibility for post-sale adoption and retention, the products it supports, and its primary partners. Include boundaries when they help determine whether a request belongs with this team.

### Develop the context together

Read supplied materials before asking questions they answer. Team-specific facts usually require the reader's knowledge or internal documents. Public sources may help explain terminology or suggest questions, but cannot establish the team's actual charter, authority, or policies. Keep internal details out of public search queries and research evidence in the drafting conversation.

Ask one question at a time, selecting the next material gap. Use a recent project to make vague responsibilities concrete. Explain consequential ambiguities and offer possible wording for confirmation. Distinguish current practice from changes the reader proposes; do not silently turn suggestions into standing rules.

Use these topics selectively:

| Topic | Questions to explore |
|---|---|
| Charter and focus areas | What outcomes does the team support? Which products, populations, or lifecycle stages are in scope? What are its main recurring areas of work? |
| Primary stakeholders | Who uses the team's work, and for which decisions? Which partners are central to its remit? |
| Responsibilities | Who owns analytical approach, validation, interpretation, and business decisions? Who resolves scope or priority conflicts when relevant? |
| Working approach | How does the team move from understanding a problem to analysis, experimentation, or model development and evaluation? Which practices recur across its work? |
| Review arrangements | Which expectations hold across the team? Which reviewers and checkpoints are chosen for each request or playbook? |
| Data handling | Are there established classifications or handling requirements for the data the team uses? Where can an agent find the applicable guidance? |

Capture primary stakeholders without building a directory of everyone the team could work with. Describe focus areas in terms of work and decisions. Include manager responsibilities only where they clarify accountability.

Record established data-handling guidance briefly; do not infer classifications or invent policy. Let individual playbooks define task-specific methods, checks, review severity, and escalation arrangements. Add intake channels, meeting cadence, or delivery formats only when they materially guide analytical work. Do not impose the CG team's process or a universal approval requirement on every deliverable.

When information is unavailable, record the consequential gap and continue drafting. Avoid repeated questions the reader cannot answer.

### Draft the document

Share short sections for correction. Aim for roughly 300–500 words; use fewer when sufficient. Adapt headings to the team, using the charter, responsibilities, working approach, and relevant data-handling guidance as a starting point.

Write a coherent account without “public facts” or “internal context” labels. Keep research citations in the conversation. Optional operational links can point to existing business context, analytical standards, metric definitions, or applicable policies. Avoid duplicating those documents or listing missing files solely to fill a references section.

Use this metadata with confirmed values:

```yaml
---
name: "[team]-team-context"
description: "[What this context covers and when an agent should read it.]"
owner: "[Name, role]"
status: draft
last_reviewed: "[YYYY-MM-DD]"
---
```

Keep the owner as a single value. Record when the reader reviewed the contents; leave the date pending until then. Mark unknown metadata for completion. Format any operational links as bullets under Supporting references and upkeep. Add a short upkeep statement naming the reviewer or marking that responsibility unresolved.

### Review before use

Test the draft against one representative team request: does it clarify the team's contribution, the decision stakeholder, responsibilities, and what the request or playbook must still specify?

Check that the draft reflects the reader's actual team, preserves business-context boundaries, and avoids invented process or duplicated analytical standards. Keep consequential unknowns and their effects inside the document. Return other follow-up items separately.

Ask the reader to approve the complete document before treating it as established shared context. This document review does not create a blanket sign-off rule for the team's analytical work or resolve explicitly retained unknowns.
