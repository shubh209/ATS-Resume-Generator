---
name: fullstack-resume-tailor
description: >-
  Tailor Shubh Kapadia's resume for Full Stack job descriptions. Use when the
  user asks to tailor for full stack, full-stack SWE, or pastes a JD for a
  full stack role. Base template: templates/variants/fullstack-engineer.tex
---

# Full Stack Resume Tailoring

Tailor the resume for **Full Stack** roles using the variant base template.

## Before tailoring

1. Read `templates/variants/fullstack-engineer.tex` (base — do **not** edit `templates/main.tex` unless user updates the lock)
2. Read `governance/OUTPUT_CONTRACT.md` and `governance/FACT_RULES.md`
3. Read `gpt/per-project-keywords.md` for default Full Stack project order
4. Read relevant `gpt/projects/*.md` for locked bullets and metrics

## Default Full Stack layout (base template)

| # | Project | Bullets |
|---|---------|---------|
| 1 | Hearloop | 3 |
| 2 | SEO Audit Engine | 2 |
| 3 | Crypto Market Simulator | 2 |
| 4 | Video Compliance Pipeline | 1 |

JD may reorder top 4 projects per scoring in `OUTPUT_CONTRACT.md`. Bullet counts: positions 1–2 → 3 each; 3–4 → 2 each (unless trim ladder applies).

## Header

Default contact header stays **Software Engineer** (two rows). Change header title in LaTeX only if JD title is a close match and user has not said to keep generic title.

## Output order (mandatory)

1. **Project Selection table**
2. **Fact Check table**
3. **Changed LaTeX sections only** — paste-ready blocks for sections that changed:

```
% --- HEADER (only if changed) ---
...

% --- PROJECTS ---
\section{Projects}
...

% --- EXPERIENCE ---
\section{Experience}
...

% --- TECHNICAL SKILLS ---
\section{Technical Skills}
...
```

Do **not** output full preamble or unchanged sections. Do **not** output Validation Summary unless user says `show validation`.

## Rules

- Reword bullets for JD keywords; **lock facts** (metrics, stack, outcomes)
- Preserve why-clause business outcomes
- One page; apply trim ladder from `OUTPUT_CONTRACT.md` if needed
- Demo links on every project heading when URL exists in project MD

## After user accepts

Optionally update `templates/variants/fullstack-engineer.tex` only when user asks to save this tailored version as the new base.
