# Hiring Reality and Tailoring Contract Design

**Date:** 2026-09-22

## Purpose

Update the live resume-tailoring system so it consistently applies the user's stated hiring-market assumptions, role keyword profiles, and output preference. The system should optimize for how the user says recruiters and applicant-tracking systems operate, while continuing to protect factual integrity through the existing locked-fact rules.

The default tailoring experience must become quieter: deliver the tailored resume without a routine tailoring report. Reports remain available only when the user explicitly requests one.

## Authoritative decisions

For this repository, the user's statements in the September 2026 hiring-reality conversation are authoritative operating assumptions. The tailoring workflow must apply them without adding contrary caveats or re-litigating them during a live run.

These assumptions include:

- An ATS primarily stores applications, supports search and workflow stages, and applies employer-configured knockout questions.
- Recruiters may search by literal keyword, skim the upper portion of the resume, and stop after finding enough candidates.
- The most recent relevant role and its first bullet carry disproportionate value.
- The posting's exact terminology should be used when the candidate can truthfully support it.
- Qualifications require what was done, how it was done, why it mattered, and where it occurred.
- Skills sections and summaries do not substitute for contextual qualification evidence.
- Important requirements should not be left to implication.
- Technical detail should be paired with a reason understandable to a nontechnical reader.
- Referrals, careful knockout answers, early applications, plain formatting, and text-selectable PDFs are favored.
- Consumer ATS match scores are not a hiring probability or a standard that the resume must beat.
- One page is preferred below roughly five years of experience, with two pages acceptable afterward.
- Cover letters are low priority for engineering roles unless requested.
- Hidden or tiny keyword text is deceptive and prohibited.
- The current market is highly competitive; profiles should be tested across enough applications to generate useful outcome feedback, then improved.

These assumptions are internal tailoring bias. They are not a routine section in the generated resume or final response.

## Role keyword profiles

Add a qualification-taxonomy reference that preserves the user's supplied profiles as authoritative market guidance.

### Full Stack Software Engineer

- Degree
- TypeScript, JavaScript, HTML, CSS
- RESTful API or REST API
- SQL; AWS, GCP, or Azure
- Backend development using Python, C#/.NET, or Java
- React or React Native
- Git or GitHub
- CI/CD, Agile, DevOps
- Extra credit: AI tools, infrastructure user counts, cross-functional work
- Development tools such as Claude, Cursor, and GitHub Copilot

### Go / Node.js Engineer

- Degree and Agile
- Go/Golang, Fiber, Node.js, NestJS, SQL, MongoDB, Redis
- Cloud, CI/CD, Git, Kafka, RabbitMQ
- Docker and Kubernetes
- Additional languages such as C#, C++, or Java
- OOP

### AI Engineer

- Degree, Python or another backend language, ML, and LLMs
- Cloud, production systems, agentic systems, and multi-agent systems
- Agentic coding with Claude Code, OpenAI Codex, or Cursor
- LangGraph, LangChain, Google ADK, or OpenAI Agents SDK
- Communication of technical details to a nontechnical audience
- MLOps, AI architectures, and AI orchestration
- Less common differentiators: industry experience, SQL, RAG, Git, and NumPy

The target JD remains the primary source for the three priorities in a live run. The profiles provide vocabulary, expected coverage, and tie-breaking context; they do not authorize unsupported candidate facts.

## Module design

### Hiring-reality reference

Create `resume-system/reference/hiring-reality.md` as the persistent source for the operating assumptions above.

Its interface is intentionally small: the live skill reads it and applies it. It must not become a source of candidate facts, metrics, or technologies.

### Qualification-taxonomy reference

Create `resume-system/reference/qualification-taxonomy.md` containing the three supplied role profiles. Organize each profile under consistent labels where useful, but preserve the substance and priority of the user's lists.

The taxonomy may identify literal wording variants such as `Go`/`Golang`, `REST API`/`RESTful API`, and `CI/CD`/`CICD`. It must not add market corrections that contradict the supplied profiles.

### Project keyword mapping

Revise `resume-system/facts/per-project-keywords.md` so project coverage is evaluated against the new profiles. Keep the file non-authoritative for facts. Project masters and work-experience masters remain the only evidence sources.

Existing project mappings should be reconciled with the new profile vocabulary, but locked bullets, metrics, and project facts must not be changed as part of this work.

### Live tailoring skill

Update `.agents/skills/resume-tailor/SKILL.md` to:

1. Read the hiring-reality and qualification-taxonomy references during every live tailoring run.
2. Classify relevant JD requirements internally as eligibility, technology, responsibility, collaboration, or optional tooling.
3. Continue extracting exactly three JD priorities.
4. Place the strongest truthful evidence for those priorities as early as the locked structure permits, especially in the first bullet of the most recent relevant role.
5. Use exact JD wording where supported, without inventing facts or changing locked wording during live tailoring.
6. Preserve the existing DIRECT, TRANSFERABLE, ADJACENT, and GAP protections.
7. Avoid producing routine analysis artifacts in the final response.

## Output contract

### Default chat output

Return only the complete tailored `resume.tex`, or only the specifically requested application answer when the request is narrower than a resume. Do not append:

- A tailoring report
- A selection table
- A fact-check table
- A gaps table
- A validation summary
- An explanation of ATS assumptions

An actual blocker, failed invariant, or material fact-integrity warning may still be reported because silently producing an invalid resume is not acceptable.

### Saved output

When the user asks to save a normal tailoring run, write only:

- `job-description.md`
- `resume.tex`

Write `tailoring-report.md` only when the user explicitly requests a tailoring report. The existing report schema remains available for that opt-in path.

### Internal validation

Preflight, source tracing, gap handling, locked-bullet checks, compilation, and page-count validation remain required internally where applicable. Passing validation does not cause a report to be emitted.

## Auditor changes

Replace the auditor's fixed `<75% JD keywords in the first half of page 1` placement rule with a priority-first rule:

> The three JD priorities must appear in the earliest available truthful evidence allowed by the lane's locked structure. A supported priority should not be buried beneath less relevant evidence.

The auditor remains an explicitly invoked second-pass tool. Its output contract does not affect the default live-tailoring response.

## Preflight and tests

Update preflight and regression tests to verify:

- Both new reference files exist.
- The live skill includes them in its immutable read set.
- Default saved output no longer requires `tailoring-report.md`.
- The report schema remains reachable for explicitly requested reports.
- The obsolete fixed 75% placement rule is absent from the auditor.
- Locked facts, templates, and bullet banks remain unchanged by this feature.

Tests should validate contracts and required references, not attempt to prove hiring-market claims.

## Documentation

Update the root README directory map and quick lookup so future maintainers can find:

- Hiring-reality assumptions
- Role qualification taxonomy
- Optional tailoring-report schema

## Explicit exclusions

This change will not:

- Add the previously proposed extra evidence rules for production, scale, cross-functional work, technical communication, AI tooling, or MLOps.
- Add PDF extraction or `pdftotext` validation.
- Rewrite locked bullets or project facts.
- Change verified metrics.
- Change the LaTeX design or section order.
- Create an application-tracking subsystem.
- Add external-source caveats to the user's hiring assumptions.

## Acceptance criteria

The work is complete when:

1. The two new references persist the user's hiring assumptions and role profiles.
2. The live skill reads and applies both references.
3. A normal tailoring request returns the tailored resume without a report.
4. An explicit report request still produces the established report schema.
5. Saved normal runs contain two files; report-requested runs contain three.
6. Priority placement uses the three JD priorities rather than a fixed keyword-percentage threshold.
7. Preflight and regression tests pass.
8. No locked facts, bullets, metrics, or templates are unintentionally changed.
