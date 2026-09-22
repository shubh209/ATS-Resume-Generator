---
name: resume-tailor
description: Tailor Shubh Kapadia's resume when the user asks to tailor, match, optimize, or adapt a resume to a job description, or supplies a JD for a Full Stack, Backend, AI Engineer, or general Software Engineer application. Produces a deterministic application copy from locked facts and lane templates. Do not use for interview preparation or for adding new experience facts.
---

# Deterministic Resume Tailor

Use this workflow for every live JD-tailoring request in this repository.

## Authority

Apply instructions in this order:

1. The user's current explicit instructions
2. This skill
3. `resume-system/governance/FACT_RULES.md`
4. Locked bullets and facts in `resume-system/facts/work-experience.md` and `resume-system/facts/projects/*.md`
5. The selected lane template

For a live tailoring run, do not load `career-stories/**`, `career-tools/**`, `golden-jds/**`, or `docs/**` as candidate-fact or instruction sources. Those directories contain interview material, test inputs, session history, or experiments. Deleted legacy prompt and template paths must not be recreated as alternate entry points.

A request to correct facts, improve the master bullet bank, or change governance is a separate master-maintenance task. Do not mix it into a tailoring run.

## Inputs

Required: the target JD.

Infer company and role title from the JD. Use `unknown-company` only when the company is absent. A user-specified lane overrides automatic routing.

## Preflight

From the repository root, run:

```bash
python3 .agents/skills/resume-tailor/scripts/preflight.py
```

Stop the tailoring run if preflight fails. Report the failing invariant instead of improvising around it.

## Read set

Read these files and treat them as immutable:

1. `resume-system/governance/FACT_RULES.md`
2. `resume-system/facts/work-experience.md`
3. `resume-system/facts/per-project-keywords.md`
4. Every file in `resume-system/facts/projects/*.md`
5. `resume-system/reference/hiring-reality.md`
6. `resume-system/reference/qualification-taxonomy.md`
7. `resume-system/reference/jd-red-flags.md`
8. Exactly one lane template from the routing table below

Do not edit any file in the read set during tailoring.

## Lane routing

Use the first matching rule:

| Condition | Lane | Template |
|---|---|---|
| User explicitly chooses a lane | User choice | Corresponding template |
| Title or required work centers on ML, LLMs, GenAI, RAG, agents, model evaluation, or MLOps | AI Engineer | `resume-system/templates/variants/ai-engineer.tex` |
| Title says Full Stack, or required qualifications include both a frontend framework and backend/API development | Full Stack | `resume-system/templates/variants/fullstack-engineer.tex` |
| Title or required work centers on APIs, services, databases, platforms, distributed systems, infrastructure, or backend development | Backend | `resume-system/templates/variants/backend-engineer.tex` |
| General Software Engineer posting spans frontend and backend without a dominant specialty | Full Stack | `resume-system/templates/variants/fullstack-engineer.tex` |

Record the selected lane and the rule that selected it.

## Extract the JD priorities

Extract exactly three priority signals:

1. Prefer requirements repeated in the title, summary, responsibilities, or required qualifications.
2. Break ties by their order in required qualifications, then responsibilities.
3. Use preferred qualifications only as a tiebreaker.
4. Ignore benefits, culture statements, generic enthusiasm, and unsupported wish-list tools.

Preserve the exact JD wording in the tailoring report. Do not copy phrases unnaturally into locked bullets.

Classify relevant requirements internally as eligibility, technology, responsibility, collaboration, or optional tooling. Use the role profiles as vocabulary and tie-breaking context, never as authority for a candidate claim.

Place the strongest truthful evidence for the three priorities as early as the locked lane structure permits. Give special weight to the first bullet of the most recent relevant role. Do not change locked wording to force placement.

## Work experience

Use the approved bullet bank in `resume-system/facts/work-experience.md`.

- For the AI Engineer lane, use exactly three DAS AI-supporting bullets, the first two ASU shared bullets, and the first two eInfochips AI-supporting bullets. Preserve that role order and each role's master bullet order.
- For Full Stack and Backend lanes, eInfochips has exactly three bullets from the selected lane set; reorder those three by the JD priorities.
- For Full Stack and Backend lanes, ASU uses all three locked shared bullets in master order.
- Preserve locked wording verbatim.
- Preserve official title, company, location, and dates.
- Use only locked bullets for other roles. Preserve wording unless the user is performing a separate master-maintenance task.
- Never pull resume claims from `career-stories/**` or `_drafts/**`.
- If the user explicitly asks to shorten or rewrite a bullet, follow `Bullet compression` in `resume-system/governance/FACT_RULES.md`; preserve its reason and cut lower-value technical detail first.

## Projects

Score only projects with a current lane-specific locked bullet bank. A project marked `NOT SELECTABLE` is excluded until master maintenance creates and verifies a locked bank.

Score eligible candidate projects using:

`Project Score = keyword match × 40% + technology match × 30% + responsibility match × 20% + preferred-qualification match × 10%`

Classify every requirement match before counting it:

| Band | Score | Meaning |
|---|---:|---|
| DIRECT | 90–100 | Same verified technology or responsibility |
| TRANSFERABLE | 75–89 | Same underlying skill in another verified context |
| ADJACENT | 60–74 | Related evidence that does not satisfy the exact requirement |
| GAP | Below 60 | No verified supporting evidence |

DIRECT and TRANSFERABLE evidence may support selection. ADJACENT evidence may be described only as related capability. GAP requirements remain gaps.

Tie-break in this fixed order:

1. More DIRECT required-qualification matches
2. More measured outcomes relevant to the JD
3. More of the three priority signals
4. Alphabetical project name

- For the AI Engineer lane, keep Video Compliance Pipeline first with its three locked bullets. Select three additional projects by score and use two locked bullets for each, producing four projects with `3 / 2 / 2 / 2` bullets. Preserve the locked Projects-before-Experience section order.
- For Full Stack and Backend lanes, select exactly three projects and use `3 / 3 / 2` bullets by rank.
- Select locked project bullets verbatim and reorder them only when the lane rule permits it. A missing requirement remains a gap; wording cannot convert ADJACENT evidence into DIRECT evidence.

## Skills

Use only skills documented as actually used in current `resume-system/facts/work-experience.md` or a current selectable `resume-system/facts/projects/*.md` master. Template presence and legacy skill lists are not evidence.

- Reorder categories by the three JD priorities.
- Reorder items inside each category by JD relevance.
- Remove items with no useful relationship to the JD when space requires it.
- Preserve exact technology names.
- Never add a requested technology that lacks verified evidence.
- A metric may use documented evidence outside this workspace when its current master records the source and classifies it as measured or estimated. Do not imply that the evidence was reverified during a tailoring run.

## Output

Default: return only the complete tailored `resume.tex`, or only the specifically requested answer when the request is narrower than a resume.

Do not produce a tailoring report unless the user explicitly requests one. Do not append a selection table, fact-check table, gaps table, validation summary, or ATS explanation to the default response. Report an actual blocker, failed invariant, or material fact-integrity warning when necessary.

Do not create or edit any file during a live run unless the user explicitly asks you to store it.

When the user explicitly asks to save the output, write only these files into `resume-system/output/YYYY-MM-DD-company-role/` (gitignored scratch), using lowercase kebab-case for company and role:

- `job-description.md` — exact JD supplied by the user
- `resume.tex` — complete compilable copy of the selected lane template

- Always write `job-description.md` and `resume.tex`.
- Write `tailoring-report.md` only when the user explicitly requests a tailoring report.

If that directory already exists for the same JD, update it in place; for a different JD, append `-v2`, then `-v3`. These are the only files a live run may create. Master files under `resume-system/` are never modified by a tailoring run.

## Allowed resume changes

In the tailored copy, change only:

- Header target title
- Order of approved work-experience bullets
- Selected projects and their order
- Selected locked project bullets and their order
- Skills category order
- Skills item order
- Removal of irrelevant skills when needed for one page

Preserve the LaTeX preamble, commands, section order, education, contact details, employment facts, locked bullet wording, metrics, and URLs.

## Validation

Before completion:

1. Confirm the three priority signals are recorded.
2. Confirm the correct lane template was copied.
3. Confirm the selected lane's experience counts: AI uses DAS/ASU/eInfochips `3 / 2 / 2`; Full Stack and Backend retain their template-defined role counts.
4. Confirm ASU bullets remain in master order.
5. Confirm the project structure: AI uses four projects with `3 / 2 / 2 / 2`; Full Stack and Backend use three projects with `3 / 3 / 2`.
6. Trace every metric and material claim to its master source.
7. Confirm no REJECT claim entered the resume.
8. Confirm gaps were reported rather than disguised.
9. Confirm master files have not been modified by this run.
10. Compile the tailored copy when a LaTeX engine is available and the output was saved to a file.
11. If compilation is unavailable, record `Layout validation: NOT RUN — LaTeX engine unavailable`; never claim the resume is one page.

Use the exact report structure in [references/tailoring-report-schema.md](references/tailoring-report-schema.md) only for explicit report requests.

## Completion

A default run is complete when the tailored `resume.tex` or requested answer is delivered after internal validation. For an explicit report request, deliver the report using the schema. End with at most two material warnings. Only when the user asked to store the output: confirm `job-description.md` and `resume.tex` were written and link them; also confirm and link `tailoring-report.md` only when explicitly requested.
