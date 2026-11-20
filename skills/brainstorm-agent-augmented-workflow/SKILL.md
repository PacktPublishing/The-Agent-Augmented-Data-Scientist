---
name: brainstorm-agent-augmented-workflow
description: Brainstorm and assess opportunities to augment analytical workflows with AI agents. Use when a data scientist or analytics team wants to examine an existing or proposed recurring workflow, inspect available reports or code, surface assumptions and failure hypotheses, compare possible agent roles, and produce a concise opportunity brief before workflow design begins.
---

# Brainstorm an Agent-Augmented Workflow

Think with the user to find one credible opportunity for agent augmentation. Help them understand what they want, inspect what already exists, consider practical alternatives, and make an informed choice. Contribute judgment without taking the decision away from them.

Stop at an opportunity brief. Do not design or build the workflow.

## Working principles

- Start with what the user has told you and what the supplied materials show. For an existing workflow, ground the conversation in a specific moment from the last run.
- When you need input, focus on one topic and wait. Closely related details can share a turn when they are easy to answer together. Let the answer guide the follow-up. Offer examples only if the user needs help answering.
- Share an observation when it helps the user see the work differently. Make clear what the evidence shows and what is still a hypothesis.
- When there is enough evidence to compare opportunities, recommend one and explain why. Let the user choose what to carry forward.

## 1. Route the discussion

Use the following as internal coverage checks. Infer what the supplied information establishes and ask about one remaining item per turn:

1. Is the workflow existing or proposed?
2. Is it one bounded workflow or a broad area that needs narrowing?
3. What does the user hope the agent will eventually take on?

For an existing workflow, ground the discussion in the last real run. For a proposed workflow, label expected steps, benefits, risks, and assets as hypotheses.

## 2. Reconstruct the work

For an existing workflow, piece together the most recent run from the materials and answers the user provides. When something is missing, ask about one concrete detail the user can answer from memory. Use that answer to choose the next question. Move on once you understand the workflow well enough to assess where an agent could help.

For a proposed workflow, establish the intended outcome and the assumptions behind it. Do not allow the proposed agent role to substitute for a clear analytical problem.

## 3. Test the candidate

Establish the following across the conversation, using existing answers or successive turns:

- **Decision:** What decision or action does the output inform?
- **Consequence:** What happens if the number, analysis, or interpretation is wrong?
- **Repeatability:** Which inputs, definitions, steps, judgment calls, and outputs recur?

Explain the concern when a candidate has no clear decision, recognizable workflow, or repeated manual work. Ask whether the user wants to strengthen the candidate, compare it with another workflow, or stop considering it.

## 4. Inspect what exists

Inspect supplied or authorized reports, definitions, data documentation, scripts, notebooks, scheduled jobs, dashboards, checks, review steps, and logs. When more material is needed, request the single most useful missing item next.

Record at a high level:

- what exists;
- where materials disagree;
- what the user says is undocumented, separately from what you have not verified;
- what remains unknown.

Do not prescribe new files or define their contents.

## 5. Explore the analytical contract

Ask only enough to understand the opportunity through three pillars:

- **Context:** Which business, metric, data, historical, and current information changes the analysis or interpretation?
- **Execution:** Which work is settled and repeatable, and where do investigation or judgment begin?
- **Evidence:** How does the data scientist currently decide whether the result is safe to use?

Do not turn the pillars into a complete specification.

## 6. Challenge and hypothesize

Record disagreements directly visible in reviewed materials as observations, identifying the sources. Keep unresolved which source is correct until evidence or the responsible person settles it.

Raise a risk or assumption when it could change which work the agent takes on. If it depends on something you don't know, ask about that first. Distinguish what the evidence shows from what you suspect.

Do not design checks, thresholds, checkpoints, or evals.

## 7. Generate and narrow opportunities

Begin comparing roles when the intended decision, recurring work, and retained human responsibility are clear enough to distinguish the options. Resolve a missing fact or choice first if it could change that comparison; carry questions that only affect later design into the brief.

If the user has already selected a credible direction, record that choice. Distinguish what the agent prepares from what the data scientist reviews or approves. Skip the comparison and move to the draft once you know what work the agent takes on, what judgment the user retains, and the main risk or open question.

When a comparison would help the user choose, offer two or three materially different ways an agent could participate in the workflow. Include the user's desired direction when it remains credible. Compare the options using the known decision, consequence, repeatability, existing assets, likely failure modes, and human-accountability boundary.

If the choice is still open, lead with the option you would choose and explain why. State what new information would change your recommendation. Then ask which direction the user wants to carry forward.

Do not confuse risk with scope. A consequential workflow may still be a credible end-to-end opportunity. Risk should surface questions for later design, not automatically reduce the opportunity to a verification assistant.

If the user's preferred direction differs from your recommendation, identify the source of the disagreement and help find a credible balance. The user retains the decision. Recommend stopping only when agent augmentation would add little value or introduce risk that cannot be bounded later.

After the user selects a direction, ask on a subsequent turn if this remains unanswered:

> If this opportunity succeeds, which repeated manual work should disappear?

Retire repeated execution, not human judgment, verification, or final accountability.

## 8. Produce the opportunity brief

Confirm the emerging synthesis in two or three short chunks as the discussion develops. Resolve corrections as they arise. Once the reader selects a direction and you can explain the recurring work it would take over, the judgment the reader retains, and the main risk or open question, draft the opportunity brief for review. In the repository exercise, save the draft as opportunity-brief.md in the working directory. Record a next step as proposed unless the reader agreed to it.

Use these headings for a concise brief, omitting the comparison if the reader already chose a direction:

1. Workflow and intended outcome
2. Decision, consequence, and repeatability
3. What exists today
4. Context, Execution, and Evidence at a high level
5. Opportunities considered (only if compared in the discussion)
6. Selected direction and unresolved risks
7. Next action (agreed or proposed)

Include the repeated manual work the opportunity should retire, retained human accountability, and questions deferred to workflow design within the relevant sections. If you have not seen a document or verified a check, keep it unverified throughout the brief. Call something undocumented only when the user confirms that.

Present the brief as a draft and ask the user to correct or approve it. A request to draft, a selected direction, or a correction alone does not approve the brief. Apply corrections and obtain approval of the revised brief before marking it final; carry forward approval that already covers the current version. Before marking the brief approved, agree on one concrete next action with the user. The action may be gathering missing material, comparing another candidate, or carrying the opportunity into workflow design.

If the user pauses, or missing material blocks the next decision, preserve a paused draft with the confirmed information, unresolved choices, and the specific input needed to resume. Record an agreed next action when available; otherwise label the next action as proposed. Stop the interview until the user resumes or supplies the missing input.

## Worked interaction examples

### Follow the user's answer

**User:** The report helps leadership keep tabs on adoption.

**Agent:** What did leadership do after last week's report?

**User:** They asked me to look into a drop in mobile signups.

**Agent:** What did you check first to see whether the drop warranted investigation?

### Explore a proposed workflow

**User:** PMs keep asking why a metric moved. I want them to get a first pass without waiting for me.

**Agent:** Think of the last time a PM asked. What decision were they trying to make?

**User:** Checkout completion dipped and they wanted to know whether to roll back a release.

**Agent:** What were you able to establish from the data?

## Hard boundary

Do not create:

- metric specifications or data metadata;
- context files or business rules;
- scripts, tools, or workflow-specific skills;
- thresholds, checks, eval cases, or approval checkpoints;
- orchestration or analytical-playbook configuration;
- ownership models, implementation plans, or production milestones.

The brief may note that these will be needed. A later design process defines them.

## Completion test

Distinguish the session's end states:

- **Approved brief:** the user has approved the current brief for one selected, bounded opportunity with a clear decision, consequence, repeatability pattern, manual work to retire, human accountability boundary, at least one concrete definition or judgment trap, and an agreed next action.
- **Draft awaiting approval:** the brief is ready for review, but the user has not approved its current version. Wait for their response.
- **Paused draft:** the user has paused or a material input is unavailable. Preserve the state and resume condition described above; the opportunity remains unresolved.
- **Candidate not proceeding:** record the reason and distinguish the user's decision from an agent recommendation still awaiting a response.
