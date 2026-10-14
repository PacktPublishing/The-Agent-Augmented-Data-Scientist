# Cascade Goods agents

These files define reusable specialist roles that the primary agent can call when a playbook or user requests them. The primary agent follows the playbook and integrates the returned work.

## Available agents

| Agent | When to use | Returns |
|---|---|---|
| [Analytical reviewer](analytical_reviewer.md) | Review a plan, calculation, finding, or readout against the agreed question and evidence. | Evidence-backed findings, checks performed, unresolved issues, and required human input. |

## Using a role

The calling playbook or agent supplies the assignment, relevant context, artifacts, and task-specific review criteria. The role file supplies the reusable responsibilities and boundaries. Pass the required inputs explicitly; a subagent may not have the main conversation's context.

These are portable role instructions. Configure the selected platform to run them as subagents, or explicitly pass the instructions to a delegated worker. This directory does not register agents automatically. If the primary agent applies the instructions itself, describe that as a review within the same session.

The playbook defines how findings are addressed and when human judgment or approval is required. A reviewer response does not replace those requirements.

## Adding an agent

Add a role when a playbook needs a distinct task and output. Use the existing definition's metadata and sections: purpose and when to use, inputs and context, responsibilities, boundaries, and expected output. Reference shared standards and definitions; keep task-specific methods and evaluation criteria in the playbook. Add the role to the table above.
