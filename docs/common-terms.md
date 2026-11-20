# Terms used in this book

This glossary explains how the book uses each term.

## Model

The underlying AI capability that interprets the request, reasons about the task, and generates responses or proposed actions. In an analytical workflow, it might propose an investigation plan or interpret a query result. Access to files and execution of code depend on the surrounding software and its available tools.

## Agent harness

The software that manages the model's interaction with context, tools, and execution. It passes tool results back to the model so work can continue, and manages permissions and other controls supported by the environment.

For example, the harness can make a file-reading tool available and run a requested Python script. The playbook specifies which context to consult and which calculations to use.

## Agent

In this book, an agent combines a model with a harness to carry out a task. It can plan, take actions through available tools, inspect results, and adjust its next steps. Its capabilities depend on the model, harness, tools, and permissions available.

## Analytical playbook

In this book, an analytical playbook is a versioned set of instructions and rules that guides an agent through a recurring analytical workflow. It specifies which context to use, what to check, what outputs to produce, and when the data scientist provides feedback or approval.

The playbooks developed in the book use two main files:

- **`instructions.md`** describes how to approach the work, including context to read, skills or specialist subagents to use, outputs to produce, and review checkpoints.
- **`rules.md`** specifies the conditions and constraints that apply, referencing shared definitions and standards where appropriate.

The existing harness executes the agent's actions. Written instructions alone do not guarantee that a gate will be enforced; a step that must be blocked requires an appropriate harness or code-level control.

## Skill

A reusable package of instructions and optional supporting resources for a particular task. In the Agent Skills format, a skill is a folder containing a `SKILL.md` file with metadata and instructions. It can also contain scripts, references, and templates. See the [Agent Skills overview](https://agentskills.io/home).

For example, a playbook might use an interview skill to clarify a stakeholder’s request before drafting an analysis plan.

## AGENTS.md

A Markdown file for project instructions used by coding agents that support it. It can describe the repository, working conventions, and commands or checks the agent should use. See the [AGENTS.md guide](https://agents.md/).

The file can point the agent to shared context, analytical standards, and the relevant playbook. It does not register specialist subagents or install skills. File discovery and instruction precedence depend on the coding agent.

## Specialist or custom subagent

A subagent is an agent to which the primary agent delegates a focused task. A custom subagent has instructions for a particular role. For example, the primary agent might send a draft analysis plan to a reviewer, along with the original question and review criteria. The reviewer returns its findings. If the primary agent reads the reviewer instructions and checks the plan itself, that review happens in the same session.

## Evaluation (eval)

A test of whether an agent using a playbook produces an expected result or meets specified criteria for a given request and input.

For example, an eval for a weekly reporting playbook compares the reported weekly active user count with the known count for a fixed sample dataset. Repeated runs can reveal whether the count stays consistent even when the narrative varies.

An eval can also assess behavior, such as whether the agent requests a required approval. Passing a test provides evidence about the tested cases; it does not enforce that behavior in future runs.

## Model Context Protocol (MCP)

A standard for connecting AI applications to external tools and data sources. For example, an MCP connection could let an agent search customer-support tickets for evidence relevant to an investigation. See the [MCP introduction](https://modelcontextprotocol.io/docs/getting-started/intro).

The connection provides access to a capability. The playbook specifies when to use it and how its results contribute to the work.

Return to the [repository guide](../README.md).
