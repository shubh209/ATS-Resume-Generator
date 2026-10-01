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
5. `career-tools/reference/candidate-voice.md` for Shubh's real motivations and voice
6. `career-tools/reference/humanizer.md`

Use only current, non-superseded facts and wording. Facts come from the fact files; motivation and voice come from `candidate-voice.md`. Apply the humanizer internally and return only final answers.

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

Answer early. Do not begin with background that makes the reviewer wait for the answer. But "early" is not "an identical first sentence every time" — vary the opening across an application so the answers do not read as stamped from one mold. Sometimes the direct answer leads; sometimes one short line of real context leads and the answer lands in the second sentence. Keep it tight either way. Uniform structure across every answer is itself a reject condition (see Reject and rewrite); answering early and sounding varied are both required, not in competition.

## Evidence selection

Use one evidence unit by default. An evidence unit is one role, project, or verified fact that can support the complete answer.

Add a second unit when it genuinely adds a dimension the answer needs — not as something to avoid. This is a judgment call, and it is deliberately left to the writer's discretion rather than locked. Reach for a second unit when:

- the question explicitly asks for multiple dimensions;
- one fact proves technical fit and the other proves a separately requested working style;
- `Tell us about yourself` needs one work thread and one technical direction;
- a single unit answers correctly but a second genuinely makes the answer richer or shows range the role rewards.

Still stop at two, and still cut a second unit that only pads. One is the default; two is allowed on judgment.

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

A recurring recruiter framework for these answers is **role fit → proof → why now**: which stated duty Shubh matches, one concrete result as proof, and the honest timing reason. The "why now" slot is optional and only used when it is genuinely strong — for an early-career candidate it often is (graduating and wanting to go deep on this kind of work from the start). Never pad an answer to force all three; add "why now" only when it adds a real reason, not filler. (Framework per [hireflow](https://hireflow.net/blog/why-are-you-applying-for-this-job-2026); content rephrased for compliance.)

### Why this company?

Name one concrete product, problem, customer, or responsibility from the JD. Connect it to verified experience or the kind of work Shubh wants to continue. Optionally close on an honest "why now" when it strengthens the answer. Do not repeat a mission statement or invent personal passion for an ordinary business.

The company name must not be swappable without changing the answer. A swappable, internet-sounding answer is the single biggest red flag recruiters cite, and is increasingly read as an AI-written tell — specificity is what clears it. (Per [aiapply](https://blog.aiapply.co/blog/why-do-you-want-to-work-here) and [jobwizard](https://jobwizard.ai/blog/how-to-answer-greenhouse-custom-application-questions-without-sounding-generic); rephrased for compliance.)

### Why are you a good fit?

Lead with the strongest important requirement Shubh meets. Prove it with one example, then explain what that experience would let him contribute, and optionally why the timing fits. Do not list every matching technology. When a JD names the traits or attributes it values, reflect those with evidence rather than copied phrasing: Greenhouse answers are human-scored against predefined focus attributes, so matching a stated attribute with proof is rewarded, while phrase-mimicry is not. (Scorecard mechanics per [loopcv](https://blog.loopcv.pro/greenhouse-application-tips/) and [jobscan](https://www.jobscan.co/blog/greenhouse-ats-what-job-seekers-need-to-know/); rephrased for compliance.)

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

### Reframe a vague or "be specific" prompt

Some prompts are broad ("why us", "what excites you", "an innovative way you used AI") and some explicitly demand specifics. A generic true answer fails these, and Shubh's own supplied motivation is often generic ("I want to build products that help people"). Do not paste the generic seed. Anchor it to one concrete thing about this company or this project so the answer could not be reused elsewhere.

- Keep Shubh's real motivation as the backbone, then attach it to a specific product, problem, modality, or responsibility named in the JD.
- For "innovative use of AI", the honest strong answer is usually the rigor, not the novelty: evaluation, error analysis, guardrails, or a measured before/after, rather than claiming a flashy feature.
- Do not manufacture excitement for research or a specialty Shubh cannot defend (e.g. model architecture) when the role and evidence are on the product or platform side. Anchor to the part Shubh can speak to.

### Consequential eligibility gates

Before finalizing answers, check the JD for hard gates that can void the application regardless of answer quality: current-enrollment requirements (internships), in-person/location requirements, work-authorization or visa constraints, and seniority floors the candidate clearly does not meet. When one is present and the fact files do not confirm Shubh clears it, flag it in one or two lines alongside the answers so he can decide whether to spend the application. Do not silently answer around it, and do not pad the answer to hide it.

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

### Motivation questions — ask for the real reason, then record it

For a motivation question ("why this company", "why this role", "what excites you about this"), a synthesized reason anchored only to the JD is the weakest kind of answer. Before synthesizing one:

1. Read `career-tools/reference/candidate-voice.md` and check whether Shubh's real motivation for this kind of work is already recorded. If a recorded motivation fits, use it as the backbone and anchor it to the specific company or responsibility in the JD. Do not ask.
2. If nothing recorded fits, ask Shubh one short question for his real reason before writing the answer, rather than manufacturing enthusiasm. This is the one approved exception to "do not ask for motivation."
3. When Shubh answers, record his reason in `candidate-voice.md` (faithfully, not embellished) so the same question is not asked again. The asking is a bootstrap that retires itself as the file fills.

This exception is only for genuine motivation. Lane, project, and metric decisions are still never asked.

## Reject and rewrite

Reject an answer when:

- it buries the answer behind background instead of answering early (answering early does not require an identical first sentence; see Read the question);
- the company name could be swapped without meaningful changes;
- it repeats the JD without adding verified evidence;
- several projects compete for attention;
- a metric lacks standalone meaning;
- it claims motivation the facts cannot support;
- a "be specific" prompt is answered generically, or a broad prompt is answered with a seed that could be reused for any company;
- it manufactures excitement for a research area or specialty Shubh cannot defend, instead of anchoring to the product or platform angle he can;
- it upgrades prototype, design, ownership, or scale;
- it is not what Shubh would actually say in a recruiter screen — the written answer and the spoken answer must be the same person, because the real test is defending it in the follow-up conversation, not the words on the page (per [leonstaff](https://leonstaff.com/blogs/why-ai-generated-resumes-fail-interviews/) and [visualcv](https://www.visualcv.com/blog/ai-generated-resumes-software-engineers-reddit/); rephrased for compliance);
- several answers reuse the same story without need;
- it violates the stated or default limit.

## Output

For each question, return:

```text
### [Question exactly as provided]

[One final paste-ready answer]

Words: N/120
```

When the portal supplies a word limit, replace `120` with that limit. When a character limit applies, replace the word count with `Characters: N/[limit]`. Counts sit outside the answer and are not part of the paste-ready copy.

Do not output a draft, alternatives, the internal evidence ranking, or the humanizer audit. Save nothing unless the user explicitly asks.

## Examples

Use `career-tools/application-answers/examples.md` as judgment tests, not templates. When feedback reveals a repeatable failure, update this playbook or add a focused example before the next run.
