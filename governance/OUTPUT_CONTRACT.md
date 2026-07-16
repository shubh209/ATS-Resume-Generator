# Output Contract — JD Tailoring

> Locked June 2026 via grill session. This document overrides conflicting text in older prompts or handoffs.
> GPT behavior: `gpt/system-prompt.md` · Human checklist: `governance/DEFINITION_OF_DONE.md` · Truth rules: `governance/FACT_RULES.md`

---

## What happens when a JD is pasted

Run all steps automatically. **Do not wait for user confirmation** before generating tables and LaTeX.

### Output order (mandatory)

1. **Project Selection table**
2. **Fact Check table**
3. **Changed LaTeX sections only** (`PROJECTS`, `EXPERIENCE`, `SKILLS`, and `HEADER` if title changed)

**Do not output** Validation Summary unless the user says `show validation`.

**Do not output** keyword report unless the user says `show keywords`.

---

## 1. Project Selection table

| Column | Rule |
|--------|------|
| **Proposed lane** | Full Stack / Backend / AI Engineer — user confirms or overrides |
| **Header title** | Propose JD title if close match, else lane default from `CONTEXT.md` §6 |
| **Project 1–4** | JD-ranked by scoring algorithm; order may differ from `gpt/per-project-keywords.md` every time |
| **Bullets each** | First two projects in **this** order: 3 each; last two: 2 each |
| **Demo links** | Always include every URL from project MDs when available |
| **Keyword placement goal** | >75% of JD keywords in **first half of page 1** (via bullets, not Skills) |
| **Notes** | One line on any swap vs base variant and why |

### Project scoring (unchanged weights)

```
Project Score =
  (Keyword Match × 40%)
+ (Technology Match × 30%)
+ (Responsibility Match × 20%)
+ (Preferred Qualification Match × 10%)
```

Select **top 4** projects. Only drop to 3 after trim ladder (see One page).

### Lane defaults (header if JD title is generic)

| Lane | Default header |
|------|----------------|
| Full Stack | Full Stack Software Engineer |
| Backend | Software Engineer |
| AI Engineer | AI Software Engineer |

---

## 2. Fact Check table

Every metric and material claim in the LaTeX output must appear here before output.

| Column | Rule |
|--------|------|
| **Claim** | Metric or factual statement as it will appear on resume |
| **Source** | `gpt/projects/<file>.md` or `gpt/work-experience.md` (section) |
| **Label** | `MEASURED` or `ESTIMATE` |
| **Prototype** | `YES` if project is demo/prototype — flag for interview framing |
| **Status** | `OK` or `REJECT` |

**REJECT** and omit from LaTeX when:
- Technology not in master context appears in **project bullets** (see `FACT_RULES.md`)
- Violates a **Never Claim** list in project MD
- Claim cannot be traced to master context

---

## 3. LaTeX output

- **Section-wise only** — never full `templates/main.tex`
- **Section order** — Education → Projects → Experience → Skills (do not reorder sections)
- **Demo links** — `\resumeProjectHeading` second arg: live URL from project MD when available
- **Metrics** — `\metric{}` for numbers; both `MEASURED` and `ESTIMATE` allowed if sourced in master MD

---

## JD keyword sources

Extract from:
1. Required qualifications
2. Preferred qualifications
3. Responsibilities — **only** keywords not already covered in 1–2

**Ignore:** benefits, culture, boilerplate ("fast-paced", "passion for excellence").

Internally extract top **15** keywords (STEP 1). Do not print unless `show keywords`.

---

## Bullet rewrite rules

| Rule | Behavior |
|------|----------|
| Verbatim reuse | **No** — reword every bullet for JD mirror |
| Facts | **Locked** — stack, scale, outcomes from master MD / locked bullets |
| Framework | What + How + Where + Why on every bullet |
| Keywords per bullet | 3–6 from JD sources above |
| Internship / part-time | Soft-skill lead (STEP 2B); 3–6 non-technical keywords per bullet; no reuse within role |

---

## Work experience

| Rule | Behavior |
|------|----------|
| Default | **2 bullets per role** (ASU + eInfochips) |
| ASU 3rd bullet | Only when JD asks for non-technical / explain-to-stakeholders — use AI variant in `gpt/work-experience.md` |
| Entries | Never remove a role; only reduce bullet count |

---

## Skills section (hybrid)

- Keep **all categories**
- **Reorder** categories and items by JD relevance
- **Trim items** inside categories with zero JD match
- Do not add skills not in master skills list
- Unsupported tech: see `FACT_RULES.md` (Skills-only if adjacent)

---

## One-page trim ladder

When content exceeds one page, apply **in this order**:

1. **Experience** — drop ASU from 3 → 2 bullets (remove optional 3rd)
2. **Skills** — trim more items in low-match categories
3. **Projects** — last resort: drop 4th project, then reduce bullets on lowest-ranked project

Never cut Education. Never remove a work experience entry.

---

## User acceptance gate (not GPT)

GPT tables are **draft**. User accepts output only after `DEFINITION_OF_DONE.md` passes.

---

## Paste shortcut (user → GPT)

```
Tailor per governance/OUTPUT_CONTRACT.md
```
