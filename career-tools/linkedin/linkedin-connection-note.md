# LinkedIn connection note

> Goal: earn a reply from the recipient. An accepted request without a reply is useful but incomplete.

## Standard input

Use what the user provides from the recipient's profile:

```text
Name:
Job title:
Company:
About section:       optional when unavailable
Experience section:
Context:             optional job, application, referral, or shared connection
```

Name, job title, company, and enough About or Experience detail to personalize are normally sufficient. Do not require a separate intent or reason field.

When the user gives no context, default to reply-oriented networking. When the user supplies a job, application, referral, or existing-relationship context, use it only when it improves the first conversation. A cold first note does not ask for a referral, application review, or meeting.

## Before writing

Read, in order:

1. `career-tools/reference/candidate-communication-standard.md`
2. `career-tools/linkedin/candidate-profile.md`
3. `resume-system/governance/FACT_RULES.md`
4. The relevant authoritative file under `resume-system/facts/` when selecting candidate evidence
5. `career-tools/reference/humanizer.md`

Use the candidate profile to find possible evidence, then confirm selected facts in their authoritative source. Apply the humanizer as an internal review and return only the final note.

## Recipient decision

Classify the recipient before choosing an angle:

| Recipient | Useful profile signal | Good question territory |
|---|---|---|
| Recruiter or talent partner | Roles, teams, or levels they recruit | A concrete distinction in how the company evaluates this type of candidate |
| Hiring manager | Team ownership, current hiring problem, product area | What the role will own or what prompted the hire |
| Engineer or potential teammate | Technical area, career transition, responsibility growth | A tradeoff, transition, or team problem visible in their experience |
| Founder or early employee | Product problem, engineering stage, role breadth | The engineering problem behind the product or the kind of ownership needed |

Choose one usable detail from the About or Experience section:

- current work or team scope;
- a meaningful career transition;
- a technical or product area;
- history at the target company.

Repeating a profile fact is not personalization by itself. Add a real observation or a question that could only come from reading this profile.

## Note construction

Build the note from three ingredients, not a fixed sentence template:

1. One specific observation about the recipient's work or path.
2. One concise reason Shubh has a genuine connection to that topic.
3. Exactly one low-friction question the recipient can answer in one sentence.

The question must:

- be informed by the supplied profile;
- be answerable without research or a long explanation;
- invite experience or judgment rather than free application review;
- not be readily answered on the company website.

Combine ingredients when that sounds more natural. The note may use two or three non-empty lines. Do not force each ingredient onto its own line.

## Length

- Hard maximum: 300 characters including spaces, punctuation, and line breaks.
- Use two or three non-empty lines.
- Count the exact copy block before returning it.
- If over the limit, remove secondary context first. Do not cut the profile-specific detail or turn the question generic.

## Evidence and metrics

Prefer a recognizable capability to an unexplained project name. Prefer the problem solved to a list of tools.

Omit metrics by default. A metric may appear only when:

- it is verified in the authoritative fact file;
- a reader with no project context understands why it matters;
- it strengthens the reason to reply;
- the note still has room to explain it honestly.

If a project name or benchmark needs another sentence of setup, use the capability instead. Never spend the character budget proving maximum technical depth.

Describe overlap precisely. `Adjacent` or `similar building blocks` is stronger than an exaggerated claim that falls apart under one follow-up question.

## Clarification

Generate without asking when the title, company, and profile sections provide one honest hook.

Ask one focused question when:

- the profile contains only a title and company with no meaningful work, path, or scope detail;
- a referenced opening makes applied versus not applied material to the note;
- the user requests a direct referral but has not established a relationship or said whether they applied.

Do not fill a sparse profile with generic praise or a random candidate metric.

## Reject and rewrite

Reject a note containing any of these:

- `Would love to connect` as the only ask;
- a referral, application-review, or calendar request on cold first contact;
- generic praise such as `impressed by your journey`;
- a copied profile fact with no observation;
- more than one question;
- an unexplained project name, benchmark, or technology list;
- a long self-introduction;
- a question that requires an essay;
- a claim of direct overlap when the work is only adjacent;
- wording that could be sent unchanged to most people with the same title.

## Output

Return one note only in this format:

```text
Recipient type: [recruiter | hiring manager | engineer | founder]
Angle: [short description]
Evidence: [verified capability used, or none]
Omitted: [metric/project omitted and why, or none]

--- COPY BELOW ---

[Two or three lines, exactly one question]

--- END ---
Characters: N/300
```

Metadata explains the decision but is not part of the copy. Do not output alternative notes unless the user explicitly asks for options.

## Examples

Use `career-tools/linkedin/examples.md` as judgment tests, not as templates. New user feedback should become a rule here or a focused example there, depending on whether the failure is general or case-specific.
