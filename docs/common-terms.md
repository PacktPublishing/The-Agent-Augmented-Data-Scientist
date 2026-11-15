# Common terms

This guide explains how the book uses common terms. Product terminology and setup mechanisms vary; use these definitions alongside the chapter instructions and your coding agent's documentation.

## Model

The underlying AI capability that interprets the request, reasons about the task, and generates responses or proposed actions. In an analytical workflow, it might propose an investigation plan or interpret a query result. Access to files and execution of code depend on the surrounding software and its available tools.

## Agent harness

The software that manages the model's interaction with context, tools, and execution. It passes tool results back to the model so work can continue, and manages permissions and other controls supported by the environment.

For example, the harness can make a file-reading tool available and run a requested Python script. The playbook specifies which context to consult and which calculations to use.

## Agent

In this book, an agent combines a model with a harness to carry out a task. It can plan, take actions through available tools, inspect results, and adjust its next steps. Its capabilities depend on the model, harness, tools, and permissions available.

## Analytical playbook

A versioned set of instructions and rules that guides a general-purpose agent through a recurring class of analytical work. It brings together context, workflow steps, constraints, checks, expected outputs, and points where the data scientist provides feedback or approval.

The playbooks developed in the book use two main files:

- **`instructions.md`** describes how to approach the work, including context to read, skills or specialist subagents to use, outputs to produce, and review checkpoints.
- **`rules.md`** specifies the conditions and constraints that apply, referencing shared definitions and standards where appropriate.

The existing harness executes the agent's actions. Written instructions alone do not guarantee that a gate will be enforced; a step that must be blocked requires an appropriate harness or code-level control.

## Skill

A reusable package of instructions and optional supporting resources for a particular task. In the Agent Skills format, a skill is a folder containing a `SKILL.md` file with metadata and instructions. It can also contain scripts, references, and templates. See the [Agent Skills overview](https://agentskills.io/home).

The [Chapter 1 brainstorming skill](../skills/brainstorm-agent-augmented-workflow/SKILL.md), for example, helps a reader examine a workflow and produce an opportunity brief. A playbook can call on skills for parts of its workflow.

Native skill discovery and invocation depend on the coding agent. Readers can also supply the instructions directly, as described in the [Chapter 1 setup](../chapters/chapter_01/README.md#load-the-companion-skill). Supplying instructions directly does not install a native skill.

## AGENTS.md

A Markdown file for project instructions used by coding agents that support it. It can describe the repository, working conventions, and commands or checks the agent should use. See the [AGENTS.md guide](https://agents.md/).

For a book exercise, such a file could point the agent to shared context, analytical standards, and the relevant playbook. It does not register specialist subagents or install skills. File discovery and instruction precedence depend on the coding agent.

## Specialist or custom subagent

An agent delegated a focused task by the primary agent. A custom subagent has role instructions configured for that purpose, such as reviewing an analytical plan against the question and available evidence.

The [analytical reviewer](../cascade_goods/execution/agents/analytical_reviewer.md) is an example role definition. The calling agent supplies the assignment, relevant context, and review criteria, then incorporates the returned findings.

A role file does not create or register a subagent automatically. Follow the harness's delegation or configuration mechanism. If the primary agent applies the role instructions itself, that is a review within the same session. See the [agent directory](../cascade_goods/execution/agents/README.md) for usage guidance. The data scientist retains the decisions and approvals specified by the playbook.

## Evaluation (eval)

A test of whether an agent using a playbook produces an expected result or meets specified criteria for a given request and input.

For example, give a weekly reporting playbook a fixed sample dataset with a known weekly active user count. Check whether each run reports the expected count. Additional cases can cover different inputs, and repeated runs can help assess consistency. The numerical result should match when the definition, data, and deterministic calculation code are fixed; the narrative may vary.

An eval can also assess behavior, such as whether the agent requests a required approval. Passing a test provides evidence about the tested cases; it does not enforce that behavior in future runs.

## Model Context Protocol (MCP)

A standard for connecting AI applications to external tools and data sources. For example, an MCP connection could let an agent search customer-support tickets for evidence relevant to an investigation. See the [MCP introduction](https://modelcontextprotocol.io/docs/getting-started/intro).

The connection provides access to a capability. The playbook specifies when to use it and how its results contribute to the work.

Return to the [repository guide](../README.md).
