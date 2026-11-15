# [Team] agent registry

List specialist agents available to your team, when to use them, and where their definitions live. Start with roles that serve your work and add others as playbooks reveal a need. Replace the placeholder row below.

| Agent | When to use | Definition |
|---|---|---|
| [Role name] | [Distinct assignment this role helps with.] | [Path to its definition.] |

For each role, define its purpose, required inputs, responsibilities and boundaries, and returned output. Reference shared context rather than repeating it. The calling playbook or request supplies the assignment and relevant review criteria.

You can start with the [analytical reviewer provided in this book](../../../cascade_goods/execution/agents/analytical_reviewer.md). Update its metadata and context links for your team and add it to the registry; creating a new agent is optional. You can also choose a different specialist that fits your work and add roles as needed while developing playbooks.

## Set up the role as a subagent

After adapting the role definition, configure it as a subagent in your chosen coding agent. Adding it to this registry does not register it with the tool.

You can ask your coding agent to help:

> Set up an Analytical Reviewer subagent for this project using the supplied analytical_reviewer.md file. Follow your tool’s current subagent setup documentation. Preserve the role’s responsibilities and boundaries, and check that its referenced files are accessible. Explain how to invoke it and confirm that it runs as a separate subagent.

Review the resulting configuration, including its instructions and tool access. Then try it on an analysis you understand. Give the main agent the original question, supporting artifacts, and relevant context, and ask it to delegate the review. Confirm that a separate subagent runs, then inspect whether its findings are supported by the supplied evidence.

For tool-specific guidance, see:
- [Claude Code: Create custom subagents](https://code.claude.com/docs/en/sub-agents)
- [Codex: Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
