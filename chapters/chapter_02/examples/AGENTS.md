# Working with Cascade Goods

This project uses the fictional Cascade Goods company and its companion data. Paths below are relative to the companion repository root, where this sample is intended to be installed as `AGENTS.md`.

## Shared resources

Read the resources relevant to the current request before using their definitions or guidance.

| Resource | When to read it |
|---|---|
| `cascade_goods/context/business_context.md` | When interpreting the business situation, objectives, or customer behavior. |
| `cascade_goods/context/team_context.md` | When establishing team responsibilities, stakeholders, and working practices. |
| `cascade_goods/execution/DS_STANDARDS.md` | Before analytical work and when reviewing its code, calculations, charts, or outputs. |
| `cascade_goods/context/metric_registry.md` | When defining, selecting, or calculating shared metrics. Follow its links to the relevant SQL and checks. |
| `cascade_goods/data/README.md` and `cascade_goods/data/data_dictionary.csv` | When identifying data sources, interpreting fields, or planning joins. |
| `cascade_goods/execution/agents/README.md` | When the user requests a specialist review. Read the selected role definition and provide its required inputs to the configured subagent. |

## Use the resources in the work

- Record the files and metric entries consulted, and explain which definitions and standards affect the proposed approach.
- Check each resource's status and limitations. Raise missing information or conflicting guidance with the data scientist before using it for the affected work.
- When a playbook is selected, read its instructions and rules before starting that workflow. Ask for its location if it is not available.
- Keep task-specific assumptions and decisions with the analysis. Obtain the data scientist's agreement before changing shared definitions or guidance, and preserve the source data.
- For a specialist review, supply the original question, supporting artifacts, relevant shared context, and review criteria. Role files describe responsibilities; they do not configure or launch subagents. If separate delegation is unavailable, report that limitation.
- Return findings and unresolved questions for human review. A reviewer subagent's assessment does not replace the data scientist's decisions or approval.
