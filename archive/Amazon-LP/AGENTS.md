# Amazon Leadership Principles Story Bank

## Purpose

Build a bank of six or seven flexible behavioral stories for interviews, with extra attention to the Amazon SDE I Leadership Principles and AI-focused hiring-manager questions.

## Current stage

Six stories have been drafted. The current work is mapping each story to realistic question types, identifying coverage gaps, and then rewriting the stories as simple spoken answers and short memory chains.

The story-to-question index is in [STORY-QUESTION-MAP.md](STORY-QUESTION-MAP.md). The highest-priority missing examples are a genuine mistake or failure, tough feedback, a missed commitment, and a GenAI failure that changed the user's behavior.

Current drafts:

- [stories/eInfochips-Invoice-CO-DD-OWN-IS-IHS.md](stories/eInfochips-Invoice-CO-DD-OWN-IS-IHS.md)
- [stories/ASU-Team-Capacity-EARN-OWN-DR-EBE.md](stories/ASU-Team-Capacity-EARN-OWN-DR-EBE.md)
- [stories/ASU-HuggingFace-Conflict-HB-DC-AR-EARN-LC.md](stories/ASU-HuggingFace-Conflict-HB-DC-AR-EARN-LC.md)
- [stories/DAS-RainbowCity-DD-IS-AR-OWN-CO.md](stories/DAS-RainbowCity-DD-IS-AR-OWN-CO.md)
- [stories/ASU-Academic-Transfer-Credit-Workplace.md](stories/ASU-Academic-Transfer-Credit-Workplace.md)
- [stories/DAS-Outside-Responsibility-Onboarding.md](stories/DAS-Outside-Responsibility-Onboarding.md)

## Target job description

Read [JOB-DESCRIPTION.md](JOB-DESCRIPTION.md) before selecting stories, mapping experience to the role, preparing technical questions, or evaluating whether an answer demonstrates the work and signals expected from this SDE I position.

Treat that file as the source of truth for the target role. Do not replace it with a generic Amazon SDE I description.

## Leadership Principles reference

Read [LEADERSHIP-PRINCIPLES.md](LEADERSHIP-PRINCIPLES.md) before selecting, mapping, drafting, or reviewing behavioral stories.

Treat that file as the user-approved reference for the 16 Leadership Principles.

## Expected interview loop

The reported loop contains four sessions:

1. A senior developer asks LLD or DSA questions plus behavioral questions covering roughly three or four Leadership Principles.
2. The hiring manager asks DSA and GenAI questions. This session may also test project choices, technical depth, and role fit.
3. An SDE II asks DSA questions plus behavioral questions covering roughly three or four Leadership Principles.
4. A bar raiser from another team focuses on behavioral questions covering roughly five or six Leadership Principles and has veto authority.

Prepare stories for follow-up questions and reuse across the loop without changing their facts. Give extra scrutiny to the bar-raiser stories because they need clear ownership, judgment, setbacks, results, and lessons.

## DSA preparation reference

Read [technical/NEETCODE-150-PATTERN-GUIDE.md](technical/NEETCODE-150-PATTERN-GUIDE.md) when planning DSA practice, classifying an interview problem, reviewing recognition patterns, or preparing for the coding portions of the interview loop. It is not required for behavioral-story work.

## Working method

1. Collect raw facts before drafting: setting, people involved, constraints, the user's responsibility, actions, decisions, result, and lesson.
2. Separate facts from interpretation. Mark missing facts as questions instead of filling gaps.
3. Choose stories for coverage and flexibility. A story may support more than one Leadership Principle, but it needs one clear primary principle.
4. Draft each story as a spoken answer, not an essay. Keep the situation and task brief; spend most of the answer on the user's actions, reasoning, and measurable result.
5. Ask for human review whenever ownership, technical detail, conflict, scale, metrics, or the user's exact reasoning is unclear.
6. Treat the user's edits as voice evidence. Compare the edited version with the prior draft and apply recurring choices to later stories without copying mistakes or making the language artificially polished.
7. Keep a short list of likely follow-up questions for each finished story.
8. Update this file's current stage whenever the workflow materially changes.
9. Ask the user targeted questions about their resume or experiences whenever a story lacks enough factual detail. The user may answer directly or point to the relevant source.
10. Complete Version 0 of every agreed story before requesting voice edits. After the full bank exists, collect the user's changes and apply recurring speaking patterns across the bank.

## Source handling

- The `AMZ` folder contains reference material supplied by the user.
- Open a specific file from `AMZ` only when it is needed for the active task.
- Do not copy, summarize, or inventory the `AMZ` folder in this file or another project-memory document.
- Use the friend's material only to understand what a useful interview answer can look like. Do not copy its structure, wording, facts, or speaking style into the user's stories.
- The user owns the Leadership Principles reference file. Change its content only when the user asks.

## Truth and evidence rules

- Use only facts supplied by the user or present in source material the user provides.
- Never invent numbers, dates, technical decisions, teammates, conflict, impact, or lessons.
- Preserve the boundary between individual work and team work. Use "I" for the user's actions and "we" only for shared outcomes or actions.
- Keep technically important details specific enough to withstand follow-up questions.
- If a result has no metric, describe the observable outcome plainly and ask whether a defensible metric exists.
- Flag a story that could sound weak, inflated, implausible, confidential, or inconsistent with the resume.

## Writing rules

- Apply the `no-ai-slop` skill whenever drafting or revising story content.
- Write in simple, natural English that the user can say aloud under interview pressure.
- Preserve the user's vocabulary, cadence, uncertainty, and level of formality as their edited samples reveal them.
- Prefer short sentences, concrete verbs, specific decisions, and useful technical detail.
- Avoid corporate filler, dramatic phrasing, generic lessons, and Leadership Principle name-dropping inside the spoken answer.
- Do not force identical STAR templates onto every story. Keep the logic easy to follow while letting the experience determine the shape.
- Include at least one genuine obstacle or tradeoff. If the facts contain neither, flag the story as weak instead of making the work sound harder than it was.
- Include what the user would do differently, tied to a specific decision or correction rather than a generic lesson.
- Optimize for interviewer understanding, not memorization. The listener should understand what happened, what the user decided, and what changed because of the user's actions.
- Treat a pause, correction, or request for clarification as normal interview behavior, not as failure.
- Store every project document in Markdown.

## Review gate for a finished story

A story is ready only when:

- the user confirms the facts and ownership;
- the answer explains why the user's choices made sense;
- the result is concrete and defensible;
- the primary and secondary Leadership Principles are clear from the behavior;
- the story can answer more than one realistic behavioral question without changing its facts;
- the spoken version sounds like the user;
- likely interviewer follow-ups have factual answers.

## File organization

- Keep raw experience notes separate from polished stories.
- Keep one Markdown file per finished story.
- Maintain an index that maps stories to Leadership Principles and common question types once the first story exists.
- Preserve superseded drafts when they contain useful voice evidence; place them in a drafts folder and label their status.
