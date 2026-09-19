# Application question answers

> Goal: answer the literal application question with the smallest relevant, verified evidence in Shubh's natural voice.

## Standard input

Require:

```text
JD:          full job description
Questions:   verbatim application questions
Limits:      optional; include any word or character limit not already in a question
```

Infer company and role from the JD when present. Ask for them only when the JD does not identify enough context to answer the question. A pasted resume is not required.

## Before writing

Read, in order:

1. `career-tools/reference/candidate-communication-standard.md`
2. `resume-system/governance/FACT_RULES.md`
3. `resume-system/facts/work-experience.md`
4. Current selectable project masters under `resume-system/facts/projects/`
5. `career-tools/reference/humanizer.md`

Use only current, non-superseded facts and wording. Apply the humanizer internally and return only final answers.

## Read the JD

Classify the role as Backend, Full Stack, AI, or mixed. Then extract:

- what the person will build, operate, or own;
- the strongest required technical capabilities;
- the product, customer, or operational problem;
- the expected level of independence and collaboration.

Do not classify from the title or marketing language alone. Weight concrete responsibilities and required qualifications more heavily than repeated buzzwords.

The literal question overrides the general lane. A collaboration question needs the best collaboration evidence even when a different technical project matches the JD more closely.

## Read the question

Before selecting evidence, identify what the question is evaluating:

| Question type | What it needs |
|---|---|
| Factual | A direct fact, often one sentence |
| Motivation | A credible connection to this company's stated work |
| Fit | One important requirement plus proof and contribution |
| Technical | A problem, a decision or implementation, and the result or intended purpose |
| Behavioral | Brief context, Shubh's action, and the result |
| Personal or preference | Shubh's actual answer, not an inference |

Answer the literal question in the first sentence. Do not begin with background that makes the reviewer wait for the answer.

## Evidence selection

Use one evidence unit by default. An evidence unit is one role, project, or verified fact that can support the complete answer.

Add a second unit only when:

- the question explicitly asks for multiple dimensions;
- one fact proves technical fit and the other proves a separately requested working style;
- `Tell us about yourself` needs one work thread and one technical direction.

Do not combine unrelated details into a fictional story. Do not use every matching project. Across several questions, choose different stories when they answer equally well so the application does not sound copied.

Metrics follow the shared standard and `FACT_RULES.md`. Omit a metric that needs a baseline or project explanation. A clear outcome or capability is better than an isolated number.

## Length and form

There is no artificial minimum.

| Answer | Default shape |
|---|---|
| Simple factual answer | One direct sentence |
| Motivation or fit | About 40 to 80 words |
| Technical or behavioral | About 60 to 110 words |
| Default maximum | 120 words |

A limit stated by the portal or question overrides these defaults. Use one paragraph unless the question explicitly requests a list or multiple labeled parts. Stop when the question is answered.

## Question strategies

### Why this company?

Name one concrete product, problem, customer, or responsibility from the JD. Connect it to verified experience or the kind of work Shubh wants to continue. Do not repeat a mission statement or invent personal passion for an ordinary business.

The company name must not be swappable without changing the answer.

### Why are you a good fit?

Lead with the strongest important requirement Shubh meets. Prove it with one example, then explain what that experience would let him contribute. Do not list every matching technology.

### Tell us about yourself

Use:

1. current professional identity;
2. one relevant work thread;
3. one project or technical direction tied to the role.

Avoid a chronological biography, a life story, or a third project.

### Technical project or challenge

Explain the problem, Shubh's decision or implementation, and the result or intended purpose. Mention tools only when they explain the decision. Preserve prototype framing and design-versus-build status.

### Behavioral question

Use compressed context, personal action, and result. Focus on what Shubh did rather than what `we` did. Do not add a manufactured lesson or inspirational conclusion.

### Missing skill

State the gap plainly. Name the closest verified experience and explain the realistic transfer without claiming the missing tool. Do not apologize or bury the gap under a long list of adjacent technologies.

### Personal, preference, or consequential fact

Use a verified stored answer when one exists. Otherwise ask Shubh. This includes salary, relocation, work authorization, legal history, demographic or identity questions, and personal motivation that the fact files do not establish.

## Human voice

- Use normal words and contractions when natural.
- Make one concrete claim at a time.
- Vary sentence shape across answers in the same application.
- Keep the answer easy for Shubh to repeat and defend in an interview.
- Remove em and en dashes from final copy.

Avoid:

- `I am passionate`, `I am excited`, or `I am thrilled` as evidence;
- restating the question;
- mirroring several JD phrases in one sentence;
- repeated `This aligns with...` conclusions;
- rule-of-three adjective lists;
- cover-letter cadence or ceremonial closings;
- identical structure across every answer.

## Clarification

Ask only when the question requires an unstored personal answer or when the JD is too incomplete to identify the company, role, or work being discussed.

Do not ask which project to use, which lane applies, or whether to include a metric. Make those decisions using the shared standard.

## Reject and rewrite

Reject an answer when:

- it does not answer the literal question in the first sentence;
- the company name could be swapped without meaningful changes;
- it repeats the JD without adding verified evidence;
- several projects compete for attention;
- a metric lacks standalone meaning;
- it claims motivation the facts cannot support;
- it upgrades prototype, design, ownership, or scale;
- Shubh would struggle to say or defend it naturally;
- several answers reuse the same story without need;
- it violates the stated or default limit.

## Output

For each question, return:

```text
### [Question exactly as provided]

[One final paste-ready answer]

Words: N/120
```

When a character limit applies, replace the word count with `Characters: N/[limit]`. Counts sit outside the answer and are not part of the paste-ready copy.

Do not output a draft, alternatives, the internal evidence ranking, or the humanizer audit. Save nothing unless the user explicitly asks.

## Examples

Use `career-tools/application-answers/examples.md` as judgment tests, not templates. When feedback reveals a repeatable failure, update this playbook or add a focused example before the next run.
