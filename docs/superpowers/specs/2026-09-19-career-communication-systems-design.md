# Career communication systems design

## Purpose

Improve three candidate-facing workflows:

1. LinkedIn connection notes that aim to earn a reply, not merely an accepted request.
2. Application answers that respond directly and sound like Shubh, not an AI-generated cover letter.
3. Short cover letters that connect verified experience to the work described in a job description.

The central failure to correct is premature evidence selection. The current workflows can choose an impressive project or metric before deciding whether the reader can understand it or whether it helps achieve the communication goal. The revised systems must make the communication decision first, then select the smallest useful evidence.

## Scope and constraints

- Work stays under `career-tools/` and `.cursor/skills/`.
- The live resume-tailoring pipeline under `resume-system/` remains unchanged.
- Candidate facts come from current authoritative files under `resume-system/facts/` and follow `resume-system/governance/FACT_RULES.md`.
- Draft or unverified career stories are never sources.
- All three workflows return output in chat by default and write no files unless the user explicitly asks to save.
- The project does not track applications and will not add an `applications/` folder.
- The first release uses human-readable regression cases and evaluation rubrics. It does not require a model-evaluation service or new dependency.

## Architecture

Create one shared communication standard and keep channel behavior in three separate playbooks.

### Shared standard

Add `career-tools/reference/candidate-communication-standard.md`. It is the single source of truth for:

- audience and goal identification;
- company or recipient problem extraction;
- candidate-evidence ranking;
- clarification thresholds;
- truth and prototype framing;
- human-voice review;
- final rejection checks.

Each channel playbook points to the shared standard instead of duplicating its rules. `career-tools/reference/humanizer.md` remains a reference for detecting AI-writing patterns. The channel workflows use its review criteria internally and return only the final output; they do not expose the humanizer's draft, audit, and final sequence.

### Channel playbooks and skill entry points

- Revise `career-tools/linkedin/linkedin-connection-note.md` and `.cursor/skills/linkedin-connection-note/SKILL.md`.
- Revise `career-tools/application-answers/application-answers.md` and `.cursor/skills/application-answers/SKILL.md`.
- Add `career-tools/cover-letters/cover-letter.md` and `.cursor/skills/cover-letter/SKILL.md`.

The skill wrappers remain short routers. They state invocation triggers, required inputs, files to read, and output constraints. Decision detail lives in the referenced playbooks and shared standard.

### Regression examples

Keep Markdown examples beside the channel prompt they exercise:

- `career-tools/linkedin/examples.md`
- `career-tools/application-answers/examples.md`
- `career-tools/cover-letters/examples.md`

Each case records:

- supplied input;
- the decision the system should make;
- facts or evidence it may use;
- failure patterns it must avoid;
- acceptance criteria.

Cases should not require one exact prose answer. The evaluation checks judgment, truth, relevance, tone, and channel constraints so the system can produce natural variation without regressing into known failures.

## Shared decision standard

Before writing, every workflow performs this internal sequence:

1. Identify the reader and the desired response.
2. Extract the reader's most relevant problem from the supplied profile or JD.
3. Generate candidate angles from verified facts.
4. Reject angles that require missing context, force irrelevant metrics, exaggerate overlap, repeat what the reader already knows, or could be sent unchanged to many recipients.
5. Rank remaining angles by reader relevance, standalone clarity, credibility, usefulness toward the desired response, and word or character cost.
6. Choose one primary angle. Add supporting evidence only when the channel or question requires it.
7. Draft for the channel.
8. Reject and rewrite output containing unsupported claims, generic praise, indirect answers, AI phrasing, or unnecessary technical detail.

### Clarification threshold

Ask a question only when missing information would materially change the output and no safe default exists.

Do not ask when:

- several projects fit; rank them and choose;
- a metric needs context; omit it;
- LinkedIn intent is unstated; default to a reply-oriented networking note;
- the company is ordinary or its mission is vague; discuss the work honestly;
- a JD spans multiple lanes; select the dominant lane and prioritize its most important responsibility.

Ask when:

- a LinkedIn request references a specific opening but does not establish whether Shubh applied, and the distinction changes the note;
- the supplied LinkedIn profile lacks enough information for honest personalization;
- an application question asks for personal motivation or circumstances absent from verified facts;
- a question requires salary, relocation, work-authorization, legal-history, or another preference that cannot be safely inferred.

## LinkedIn connection notes

### Objective and input

The objective is to earn a reply. An accepted request without a reply is useful but incomplete.

Standard input:

- person's name;
- job title;
- company;
- About section when available;
- LinkedIn Experience section.

The system classifies the recipient as a recruiter or talent partner, hiring manager, senior engineer or potential teammate, or founder or early employee.

### Content decision

Select one usable detail from the recipient's profile: current work, a meaningful career transition, a technical or product area, or history at the company. Connect it to one plain-language part of Shubh's background, then ask one question that is informed by the profile and answerable in one sentence.

The question must not ask the recipient to review an application, schedule a call, or provide a referral on first contact. It must not be readily answered by the company website.

### Shape

- Two or three short lines.
- No more than 300 characters, including line breaks.
- Flexible sentence placement; do not preserve a line count at the cost of natural flow.
- One recipient-specific observation.
- One concise reason Shubh has a genuine connection to the topic.
- One low-friction question.

### Evidence and rejection rules

- Prefer recognizable capabilities to unexplained project names.
- Prefer the problem solved to a tool inventory.
- Omit metrics by default.
- Include a metric only when it is independently meaningful inside the note and improves the reason to reply.
- Describe adjacent work as adjacent.
- Reject generic praise, `Would love to connect` as the only ask, first-contact referral requests, copied profile facts without an observation, multiple questions, long self-introductions, unexplained benchmarks, and questions that demand an essay.

### LinkedIn regression coverage

Include cases for detailed and sparse recruiter profiles, close and adjacent engineer overlap, career-transition hooks, founders with limited context, tempting but illegible benchmarks, and profiles too sparse for safe personalization.

## Application answers

### Objective and input

Standard input is the JD plus the questions. The user does not need to paste a resume.

The system classifies the JD as Backend, Full Stack, AI, or mixed, then extracts the work to be owned, technical priorities, product or customer problem, and expected independence. Each question's actual evaluation goal overrides the general role lane.

### Evidence selection

Use authoritative facts from:

- `resume-system/facts/work-experience.md`;
- current selectable files under `resume-system/facts/projects/`;
- `resume-system/governance/FACT_RULES.md`.

One answer normally uses one evidence unit. A second fact is allowed only when the question asks for multiple dimensions. The system cannot combine unrelated facts into a fictional story or upgrade prototype work.

### Length and form

- No artificial minimum.
- Simple factual question: one direct sentence.
- Motivation or fit question: approximately 40 to 80 words.
- Technical or behavioral question: approximately 60 to 110 words.
- Default hard maximum: 120 words.
- A portal's stated limit overrides these defaults.
- One paragraph unless the question requests a list or multiple parts.
- One final answer per question, with no alternatives or exposed drafting process.

### Answer strategies

- `Why this company?`: connect one concrete product, problem, or responsibility from the JD to verified experience or direction. Do not invent passion for a generic mission.
- `Why are you a good fit?`: lead with the strongest requirement met, prove it with one example, and state the resulting contribution.
- `Tell us about yourself`: current professional identity, one relevant work thread, and one project or technical direction. Avoid chronology.
- Technical project: problem, decision or implementation, and result or intended purpose. Tools appear only when they explain the decision.
- Behavioral: compressed situation, personal action, and result. Do not add a manufactured lesson.
- Missing skill: state the gap, name the closest verified experience, and explain the realistic transfer.
- Personal or preference question: use a stored verified answer or ask the user.

### Voice and rejection rules

Answer the literal question in the first sentence. Use normal words, natural contractions, and varied sentence structures. Avoid restating the prompt, JD mimicry, repeated `This aligns with...` conclusions, miniature-cover-letter cadence, and uniform answers.

Reject an answer if the company name could be swapped without changing it, the prose repeats the JD without evidence, multiple projects compete, a metric lacks meaning, the opening delays the answer, motivation is unsupported, the language is difficult for Shubh to say naturally, or several answers unnecessarily reuse one story.

### Application-answer regression coverage

Include an ordinary company, misleading lane keywords, mixed roles, missing required technology, collaboration and technical questions, short character limits, personal questions requiring clarification, multi-question story diversity, and questions best answered in one sentence.

## Cover letters

### Objective and input

Standard input is the JD only. The system selects verified candidate evidence automatically and builds one argument connecting Shubh's experience to the role's work.

The JD is the default source for company claims. Use stated responsibilities, products, customers, and technical problems. When company context is thin, focus on the role instead of inventing a company-specific hook. External company research is outside the default workflow and can be added later if testing shows a material benefit.

### Output contract

- Exactly two paragraphs.
- Target 130 to 180 words.
- Hard maximum 200 words.
- Body only by default, without an address block, date, or generic salutation.
- One final version in chat.

### Structure

Paragraph one opens on the company's work or the role's problem, connects it to relevant experience, and establishes the central reason Shubh fits.

Paragraph two supports that fit with one or two concrete examples, explains the contribution those examples enable, and closes with a direct invitation to discuss the role.

The system should normally use one work experience and one project when they reinforce the same theme. A third fact is allowed only when it covers a distinct, important requirement. It must not mention three projects.

### Evidence, voice, and rejection rules

- Use verified master facts and preserve prototype framing.
- Prefer capabilities and decisions to tool inventories.
- Explain a project before naming it.
- Include only independently legible metrics.
- Avoid generic openings, unsupported company praise, lifelong-passion claims, formal letter filler, technology lists, rule-of-three adjective strings, and em dashes.
- Vary the closing while keeping it focused on a conversation about a specific responsibility.

Reject a letter if its opening works unchanged for another company, the first paragraph merely paraphrases the JD, the second copies resume bullets, more than one central argument appears, praise exceeds available evidence, a benchmark needs missing context, the closing is stiff or entitled, or the output violates the paragraph or word limit.

### Cover-letter regression coverage

Include specific Backend scaling work, broad Full Stack responsibilities, vague AI language, mixed roles, ordinary companies, thin company context, missing required technology, tempting but illegible metrics, early-career confidence boundaries, and resume-summary failure modes.

## Evaluation method

Each example receives a manual result of pass, revise, or fail against five dimensions:

1. Truth: every candidate and company claim is supported.
2. Judgment: the selected angle is the most useful one for the reader and goal.
3. Standalone clarity: evidence makes sense without hidden project context.
4. Voice: the output is concise, natural, and interview-defensible.
5. Contract: length, structure, and requested format are satisfied.

Manual checks count characters, words, paragraphs, and questions where applicable. Qualitative checks explain the expected decision and banned outcomes instead of enforcing exact prose. This system is Markdown-only and does not add a validator or test framework.

Testing is iterative. When a generated output is unacceptable, add or refine an example that isolates the decision error before changing the shared standard or a channel playbook. Shared failures belong in the shared standard; channel-specific failures belong in that channel's playbook.

## Qualitative research input

Reddit discussions are useful for identifying recipient reactions and failure hypotheses, not for establishing universal facts. Initial themes incorporated into this design are:

- generic connection messages offer no reason to reply;
- first-contact referral requests can feel like attempts to bypass the normal process;
- short, profile-aware messages are easier to engage with;
- company-value answers become interchangeable when they lack role-specific detail;
- recruiters who read cover letters favor short, non-templated writing.

Initial discussion sources:

- <https://www.reddit.com/r/recruiting/comments/1fvdrlt>
- <https://www.reddit.com/r/recruiting/comments/vuk1hd>
- <https://www.reddit.com/r/recruitinghell/comments/1vnqw90/getting_cold_messages_on_linkedin_from_people_who/>
- <https://www.reddit.com/r/recruitinghell/comments/zbxvld/how_to_answer_why_do_you_want_to_work_here/>
- <https://www.reddit.com/r/recruiting/comments/1d563f7>

Future prompt changes may cite additional discussions, but anecdotes should become rules only when they match the user's goals and survive regression testing.

## Completion criteria

The implementation is complete when:

- all three skill entry points invoke the correct playbook and shared references;
- standard inputs match the contracts in this design;
- outputs follow channel length and structure rules;
- every example has explicit decision and acceptance criteria;
- representative runs pass manual length, structure, truth, and voice checks;
- no live resume-pipeline file is changed;
- no output or application-tracking file is created by default.
