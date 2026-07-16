---
name: application-answers
description: >-
  Answer job application questions (tell us about yourself, why good fit, etc.)
  in short humanized prose from a pasted JD and resume tex file. Use when the
  user pastes application questions, supplemental questions, Greenhouse/Lever
  prompts, or asks for concise application answers tied to a specific resume.
---

# Application Question Answers

Write **short, human, paste-ready** answers to job application questions for Shubh Kapadia.

## Before writing

1. Read `prompts/application-answers.md` (full rules)
2. Apply `reference/humanizer.md` to every answer
3. Use **only** facts from the user's pasted **resume `.tex`** for this application
4. Align to the pasted **JD** (1–2 themes per answer, one concrete resume example)

## Required inputs

Refuse until you have:

- **JD** (or company + role + enough context)
- **Resume `.tex`** (the exact version submitted for this role)
- **Question(s)** (paste verbatim)

Optional: character limit per question or global.

## Length (strict)

- **50–90 words** target per answer
- **120 words hard max** per answer
- **One paragraph**, **2–5 sentences** — never 2–3 paragraphs
- Honor character limits in the question text when present

## Output

Per question:

```
### [Question]

[Single paragraph answer]

Words: N/120
```

One final answer only. No cover-letter tone. No banned AI openers (passionate, excited, thrilled, journey).

## Do not

- Add projects or metrics not on the pasted resume
- Write essay-length or multi-paragraph answers unless user says `long form`
- Keyword-stuff the entire JD into one answer
- Contradict the submitted resume
