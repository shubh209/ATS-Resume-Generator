# Application answers

Short supplemental answers for job portals (not cover letters).

## Workflow

| File | Purpose |
|------|---------|
| [`prompts/application-answers.md`](../prompts/application-answers.md) | Full rules, question playbooks, length caps |
| [`.cursor/skills/application-answers/SKILL.md`](../.cursor/skills/application-answers/SKILL.md) | Cursor skill |

## Input template

Paste in Cursor:

```
Company: Acme
Role: Backend Engineer
JD:
[paste job description]

Resume (.tex):
[paste your tailored resume source]

Questions:
1. Tell us about yourself
2. What makes you a good fit for this role?
```

Optional: `Character limit: 500` (or per-question limits in the question text).

## Defaults

| Setting | Value |
|---------|--------|
| Length | 50–90 words target, **120 words max** |
| Shape | One paragraph, 2–5 sentences |
| Truth | Only what's on the pasted `.tex` |
| Voice | `reference/humanizer.md` |

Say `long form` only if a portal truly needs more than 120 words.

## Related

- Resume tailoring: `gpt/system-prompt.md`
- LinkedIn connection notes: `networking/README.md`
