---
name: cover-letter
description: >-
  Write a short, human cover letter for Shubh Kapadia from a supplied job
  description. Use when the user asks for a cover letter, application letter,
  or a concise two-paragraph letter tailored to a role or company.
---

# Cover letter

Write one body-only cover letter that makes a single evidence-backed argument for Shubh's fit.

## Route

1. Read `career-tools/cover-letters/cover-letter.md` for selection, structure, voice, and output rules.
2. Read `career-tools/reference/candidate-communication-standard.md` for evidence selection, clarification, truth, and final review.
3. Read `resume-system/governance/FACT_RULES.md`.
4. Read `resume-system/facts/work-experience.md`.
5. Read the current selectable project masters under `resume-system/facts/projects/`.
6. Read `career-tools/reference/humanizer.md` and apply it internally.

## Execute

- Treat the JD as the standard input and default source for company claims.
- Infer the company, title, dominant lane, role problem, and one central candidate argument.
- Select one work experience and one project by default only when they reinforce that argument.
- Draft exactly two paragraphs, target 130 to 180 words, and never exceed 200 words.
- Return body-only copy with the playbook's external angle, evidence, and word-count metadata.
- Run the playbook's truth, voice, and rejection checks before returning one final version.

Do not browse for company information or save output unless the user explicitly asks. Do not expose alternatives, drafting notes, or the humanizer audit.
