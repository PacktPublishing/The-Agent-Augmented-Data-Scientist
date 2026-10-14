# Chapter 2: Setting Up the Analytics Playbook Stack

## Purpose

Build the shared foundation for analytical playbooks in your own organization: business and team context, analytical standards, a starter metric registry, and a starter agent registry.

## Before you start

Start by reflecting on your work: the team you belong to, the part of the business it supports, and the decisions your analyses inform. Consider where that knowledge already lives—in a team wiki, Slack discussions, emails, Word documents, or previous analyses. Gather relevant material you can share with your agent and use it, along with your own knowledge, to develop the business and team context. You do not need a complete set of documents to begin.

When you reach the metric registry, bring existing metric definitions, data documentation, and trusted queries where available. Access to the relevant data will let you check the SQL; keep any missing inputs explicit.

## Materials

### Create your own

| Resource | Use it to |
|---|---|
| [Business-context authoring guide](templates/business_context_authoring_guide.md) | Describe the relevant business, customers, products, and commercial relationships. |
| [Team-context authoring guide](templates/team_context_authoring_guide.md) | Define your team's charter and responsibilities using your business context as input. |
| [Metric-registry starter](templates/metric_registry.md) | Define foundational metrics and link their SQL. |

### Adapt these starters

| Resource | Use it to |
|---|---|
| [DS standards](templates/DS_STANDARDS.md) | Establish shared analytical practices, adjusting them to your team. |
| [Agent registry](templates/agent_registry.md) | List specialist roles that fit your team and link to their definitions. |

Replace placeholder metadata and paths in your copies, and review the guidance for your setting.

### Explore the Cascade Goods example

| Resource | What it illustrates |
|---|---|
| [Business context](../../cascade_goods/context/business_context.md) and [team context](../../cascade_goods/context/team_context.md) | Populated examples of the two context documents. |
| [Analytical standards](../../cascade_goods/execution/DS_STANDARDS.md) and [agent directory](../../cascade_goods/execution/agents/README.md) | CG's working standards and analytical reviewer example. |
| [Metric registry](../../cascade_goods/context/metric_registry.md) | Definitions linked to SQL and calculation checks. |
| [Data and dictionary](../../cascade_goods/data/) | The example dataset, fields, and relationships. |
| [Metric SQL and runner](../../cascade_goods/execution/metrics/) and [calculation tests](../../cascade_goods/evaluation/test_metrics.py) | How CG calculates and checks its registered metrics. |

Use these examples to understand the approach. When working on your own setup, establish definitions and assumptions that fit your business. The CG documents are currently marked as drafts.

## Work through the chapter

### 1. Create your business and team context

1. Start with the [business-context guide](templates/business_context_authoring_guide.md). Attach it or paste its full contents into your agent conversation, then use its starting prompt. Establish the relevant business scope and review the resulting document.
2. Provide that business context with the [team-context guide](templates/team_context_authoring_guide.md). The agent should reuse established business information and ask about your team's charter, stakeholders, responsibilities, and working approach. An equivalent business overview can serve as input if you do not yet have a business-context file.
3. Review and approve each document before treating it as established shared context. Keep consequential unresolved points explicit.

These guides work as instructions supplied to an agent; skill installation is not required. Keep the full guide available during the conversation so the agent can follow its drafting and review guidance.

### 2. Adapt the analytical standards

Use the [DS standards starter](templates/DS_STANDARDS.md) as starting pointers for your team's shared analytical practices. Attach them alongside your business and team context, or ask your agent to read them. Review which standards fit, adjust them as needed, and replace placeholder names, metadata, and links in your own copy. Keep task-specific methods and review checkpoints in individual playbooks.

Suggested prompt:

> Help me adapt these analytical standards using our business and team context. Explain any changes you recommend and ask about unresolved requirements. Keep the document concise and present the proposed version for my review.

### 3. Start a metric registry

Use the [registry starter](templates/metric_registry.md) to define at least two foundational metrics that support your team's likely analytical questions. Start with approved definitions when available. An agent can help identify candidates and clarify definitions; you review the choices and their business meaning.

For each metric, define its source, calculation, time basis, and caveats, then link to accompanying SQL for your data environment. One SQL query can return multiple metrics when their populations, sources, and reporting logic align; identify the output column for each entry. Add further metrics as you build playbooks.

Check the SQL against a small worked example or a trusted result with matching scope, and retain the expected and actual results. Readers do not need to reproduce CG's SQLite runner or Python test suite for this exercise. Automated checks can be added as calculations grow or are reused; untested queries should remain clearly marked.

Suggested prompt:

> Using our business and team context, help me choose two foundational metrics and populate this registry starter. Reuse approved definitions where available and ask me to resolve ambiguous choices. Inspect the data documentation before writing SQL; do not invent tables or fields. Provide the accompanying SQL and a simple way to check its results. Keep missing inputs and unvalidated calculations explicit for my review.

### 4. Start an agent registry

Use the [agent-registry starter](templates/agent_registry.md) to list specialist roles that would help your team, with their purpose and links to their definitions. Choose roles based on the work you need help with.

Start with the [analytical reviewer](../../cascade_goods/execution/agents/analytical_reviewer.md) provided in this book, or choose another specialist that fits your work. Using the reviewer is a complete starting option; you do not need to create a new agent. Update its metadata and context links for your team, then add it to your registry. Reuse or adapt further agents from the book and add your own as needed while developing playbooks.

The [CG agent directory](../../cascade_goods/execution/agents/README.md) illustrates how to use role definitions. Follow your tool's delegation or configuration mechanism when running a role as a separate subagent.

## What you should have

- Business and team context reviewed for your organization, with consequential unknowns explicit.
- Analytical standards adapted to your team's work.
- At least two foundational metric entries with accompanying SQL and recorded checks, or clearly identified inputs needed to complete them.
- A starter agent registry with links to specialist definitions chosen for your work.

Keep these files available for the playbooks you develop in later chapters. In Chapter 3, use the [playbook template guide](../chapter_03/templates/playbook_template_guide.md) and the [`instructions.md`](../chapter_03/templates/instructions.md) and [`rules.md`](../chapter_03/templates/rules.md) templates to define a playbook's workflow, constraints, checks, and human review requirements.

Return to the [repository guide](../../README.md) for other chapters and reusable materials.
