# Cover letter

> Goal: make one concise argument connecting Shubh's verified experience to the work in the JD.

## Standard input

The standard input is the full JD only.

Infer from it:

- company name;
- job title;
- dominant lane: Backend, Full Stack, AI, or mixed;
- the concrete problem or responsibility the hire will own;
- the strongest verified candidate evidence for that work.

Ask for more information only when the JD is missing or too incomplete to identify the role's work. Do not require a pasted resume or a separate list of candidate highlights.

## Before writing

Read, in order:

1. `career-tools/reference/candidate-communication-standard.md`
2. `resume-system/governance/FACT_RULES.md`
3. `resume-system/facts/work-experience.md`
4. Current selectable project masters under `resume-system/facts/projects/`
5. `career-tools/reference/humanizer.md`

Use only current, non-superseded facts. Apply the humanizer internally and return only the final letter.

## Read the JD

Classify the role from concrete responsibilities and required qualifications, not the title or repeated marketing words alone.

Extract:

1. The most important work the hire will perform.
2. The problem, user, or operational outcome behind that work.
3. The level of ownership and collaboration expected.
4. The one candidate theme that best connects Shubh to those needs.

The JD is the default source for company claims. Do not browse automatically. Do not turn a mission statement into a factual claim about the team.

When the JD provides little company or product context, focus on the role's stated work. Honest role specificity is better than invented company enthusiasm.

## Choose one argument

The letter is not a resume summary. Before drafting, complete this sentence internally:

```text
Shubh can contribute to [specific work] because he has [one coherent pattern of verified experience].
```

Every sentence must support that argument.

Normally use one work experience plus one project when they reinforce the same theme. A third fact is allowed only when it proves a separate, important requirement. Never mention three projects.

Prefer:

- a relevant problem and decision;
- what Shubh personally built or owned;
- the practical reason the work mattered;
- what that experience would let him contribute here.

Avoid copying resume bullets or listing every matching tool.

## Two-paragraph structure

### Paragraph one: connection

Open on the company's stated work or the role's concrete problem. Connect it immediately to Shubh's relevant experience and establish the central reason he fits.

Skip generic openings such as `I am writing to apply` or `I am excited to submit my application`.

### Paragraph two: proof and next step

Support the central argument with one or two connected examples. Explain what those examples would let Shubh contribute. Close with a direct invitation to discuss the role or one specific responsibility.

The closing asks for a conversation, not an interview guarantee or hiring decision.

## Output contract

- Exactly two paragraphs.
- Target 130 to 180 words total.
- Hard maximum: 200 words.
- Body only by default.
- No address block, date, subject line, or generic salutation.
- One final version in chat.
- Save nothing unless the user explicitly asks.

Count the exact body before returning it. Paragraphs are separated by one blank line.

## Evidence and metrics

Follow `career-tools/reference/candidate-communication-standard.md` and `FACT_RULES.md`.

- Preserve design, build, deployment, and prototype boundaries.
- Explain a project capability before naming the project when the name is not self-explanatory.
- Use a metric only when a reader understands its value without hidden project context.
- Prefer a clear capability or outcome over a benchmark that needs another sentence of explanation.
- Do not introduce a JD technology that the authoritative facts do not support.

## Voice

Use natural, confident first-person language. Confidence comes from specific evidence, not stronger adjectives.

Avoid:

- generic praise such as `innovative`, `industry-leading`, or `prestigious`;
- lifelong passion or personal motivation not established by the facts;
- formal filler such as `Please accept this letter` or `Thank you for your time and consideration`;
- technology inventories;
- copied resume bullets joined into prose;
- rule-of-three adjective lists;
- em and en dashes;
- a closing that merely says Shubh is a good fit.

## Clarification

Generate from the JD without asking when it identifies the role and concrete work.

Ask one focused question only when:

- the JD is incomplete enough that the role's work cannot be identified;
- the user requests personal motivation that the fact files do not establish;
- a consequential personal fact must be included but is not authoritative.

Do not ask which experience to use. Choose it using the shared decision standard.

## Reject and rewrite

Reject the letter when:

- the opening works unchanged for another company or role;
- paragraph one merely paraphrases the JD;
- paragraph two reads like resume bullets in sentence form;
- more than one central argument competes for attention;
- praise is stronger than the available company evidence;
- a project name or metric requires hidden context;
- a missing skill is presented as experience;
- ownership, scale, impact, or maturity is overstated;
- the closing is stiff, passive, or entitled;
- the body is not exactly two paragraphs or exceeds 200 words;
- Shubh would struggle to say or defend a sentence naturally.

## Output

Return:

```text
Angle: [one sentence describing the central argument]
Evidence: [the one or two connected sources used]

--- COPY BELOW ---

[Paragraph one]

[Paragraph two]

--- END ---
Words: N/200
```

Metadata and the word count stay outside the copy. Do not output alternatives, drafting notes, or the humanizer audit.

## Examples

Use `career-tools/cover-letters/examples.md` as judgment tests, not templates. Turn repeatable user feedback into a rule here or a focused case there.
