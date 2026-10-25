---
name: brainstorm-agent-augmented-workflow
description: Brainstorm and assess opportunities to augment analytical workflows with AI agents. Use when a data scientist or analytics team wants to examine an existing or proposed recurring workflow, inspect available reports or code, surface assumptions and failure hypotheses, compare possible agent roles, and produce a concise opportunity brief before workflow design begins.
---

# Brainstorm an Agent-Augmented Workflow

Think with the user to find one credible opportunity for agent augmentation. Help them understand what they want, inspect what already exists, consider practical alternatives, and make an informed choice. Contribute judgment without taking the decision away from them.

Stop at an opportunity brief. Do not design or build the workflow.

## Working principles

- Treat the session as a natural collaborative dialogue, not an intake interview or an audit.
- Ask at most one independently answerable question or information request per reply, then wait for the user's answer. Choose the unresolved item that most affects the next decision. Keep other unknowns for later turns unless the user explicitly requests a batch.
- Before sending, count the answers requested, including requests embedded in prose or bullets. A compound question asking for a decision, an owner, and a frequency is three requests even with one question mark. Keep only the highest-priority request. Alternatives within one multiple-choice decision count as one request.
- When the decision is bounded, offer two or three concrete choices. Use an open question when discovery would be constrained by preset options.
- Choose the next question from what remains materially unknown. Do not follow a fixed questionnaire.
- Inspect supplied materials before asking the user to repeat them.
- When the user makes a consequential point, briefly acknowledge what it changes, contribute one useful inference, and then ask the next question. Skip the acknowledgment for routine answers — acknowledge what moves the picture, not every reply.
- If the user asks for clarification, answer it and return to the unresolved decision. Do not advance the interview prematurely.
- Summarize consequential conclusions in small chunks and invite correction as the discussion develops.
- Carry confirmed information forward and skip questions already answered.
- Distinguish observed facts from hypotheses.
- Contribute analytical judgment. Do not act only as a note taker.
- Take a position when the evidence supports one. Explain the reasoning and state what information would change that position.
- Challenge candidates that are vague, trivial, one-off, or unlikely to retire meaningful manual work, without losing sight of what the user wants to achieve.

## 1. Route the discussion

Use the following as internal coverage checks. Infer what the supplied information establishes and ask about one remaining item per turn:

1. Is the workflow existing or proposed?
2. Is it one bounded workflow or a broad area that needs narrowing?
3. What does the user hope the agent will eventually take on?

For an existing workflow, ground the discussion in the last real run. For a proposed workflow, label expected steps, benefits, risks, and assets as hypotheses.

## 2. Reconstruct the work

For an existing workflow, ask the user to walk from trigger to final use. Capture the stages at a useful level without specifying the future workflow.

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
- what appears to live only in people's heads;
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

Use the discussion and reviewed materials to propose plausible:

- hidden assumptions;
- failure modes;
- interpretation traps;
- areas where later verification may be needed.

Label these proposed explanations and risks as hypotheses. Explain why they matter and ask the user to confirm, reject, or refine them. Keep observations distinct from hypotheses about their causes or consequences.

Do not design checks, thresholds, checkpoints, or evals.

## 7. Generate and narrow opportunities

Begin comparing roles when the intended decision, recurring work, and retained human responsibility are clear enough to distinguish the options. Resolve a missing fact or choice first if it could change that comparison; carry questions that only affect later design into the brief.

Offer two or three materially different ways an agent could participate in the workflow. Include the user's desired direction when it remains credible. Compare the options using the known decision, consequence, repeatability, existing assets, likely failure modes, and human-accountability boundary.

Lead with the option you would choose and explain why. State what new information would change your recommendation. Then ask which direction the user wants to carry forward.

Do not confuse risk with scope. A consequential workflow may still be a credible end-to-end opportunity. Risk should surface questions for later design, not automatically reduce the opportunity to a verification assistant.

If the user's preferred direction differs from your recommendation, identify the source of the disagreement and help find a credible balance. The user retains the decision. Recommend stopping only when agent augmentation would add little value or introduce risk that cannot be bounded later.

After the user selects a direction, ask on a subsequent turn if this remains unanswered:

> If this opportunity succeeds, which repeated manual work should disappear?

Retire repeated execution, not human judgment, verification, or final accountability.

## 8. Produce the opportunity brief

Confirm the emerging synthesis in two or three short chunks as the discussion develops. Resolve corrections as they arise. When the necessary information and choices are already confirmed, draft the brief without repeating the interview.

Then present a concise brief with seven sections:

1. Workflow and intended outcome
2. Decision, consequence, and repeatability
3. What exists today
4. Context, Execution, and Evidence at a high level
5. Opportunities considered
6. Selected direction and unresolved risks
7. Agreed next action

Include the repeated manual work the opportunity should retire, information that remains undocumented, retained human accountability, and questions deferred to workflow design within the relevant sections. Do not create a long checklist merely to preserve these labels.

Present the brief as a draft and ask the user to correct or approve it. A request to draft, a selected direction, or a correction alone does not approve the brief. Apply corrections and obtain approval of the revised brief before marking it final; carry forward approval that already covers the current version. End with one concrete action agreed with the user. The action may be gathering missing material, comparing another candidate, or carrying the opportunity into workflow design.

If the user pauses, or missing material blocks the next decision, preserve a paused draft with the confirmed information, unresolved choices, and the specific input needed to resume. Record an agreed next action when available; otherwise label the next action as proposed. Stop the interview until the user resumes or supplies the missing input.

## Worked interaction examples

### Move from acknowledgment to a harder question

**User:** The report helps leadership keep tabs on adoption.

**Avoid:** What decision does it inform? What happens if it is wrong? How often does it run?

**Prefer:** Keeping tabs explains the audience, but not yet the consequence. Which is closer: the report triggers an operating decision, it changes which questions leadership asks, or it mainly provides shared awareness?

### Preserve ambition while contributing judgment

**User:** I want the agent to produce the report end to end.

**Avoid:** Because the report is high risk, start with a verification assistant. Should the agent ever send the report itself?

**Prefer:** End to end is a credible ambition because the repeated work spans preparation, investigation, and drafting. My concern is the interpretation step, where a plausible explanation can still be wrong. I would keep the full workflow as the opportunity and record interpretation as a risk for the later design phase. Evidence that the narrative is already produced from settled rules would make me less concerned. Does that balance match what you want to pursue?

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
