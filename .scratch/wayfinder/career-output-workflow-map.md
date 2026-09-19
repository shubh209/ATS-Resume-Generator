---
title: Build a validated career-output workflow
labels:
  - wayfinder:map
status: open
---

## Destination

Build a reusable local workflow that takes a job description plus either `resume` or `application` mode and produces evidence-grounded output, evaluates it against locked rules, returns only the requested format, and changes repository files only after an explicit `save` or `lock` command.

## Notes

Domain: resume tailoring and job application writing.

Consult the profile evidence, project records, work-experience records, templates, and the humanizer skill. Use the same factual source for both modes, but keep their output rules and evaluators separate.

Standing preferences: concise output, plain language, no invented claims, no generic application language, WHAT + HOW + WHERE + WHY for resume bullets, 3–6 keywords per bullet, three bullets per selected project by default, and no full `.tex` file unless explicitly requested.

Future accepted application answers require an explicit user decision before entering the golden dataset.

## Decisions so far

- No closed decision tickets yet. The destination, evidence statuses, two workflow modes, output controls, selection rules, bullet checks, application checks, verification sources, golden dataset location, and confirmation-based evidence updates were settled during charting and will be captured by the child tickets below.

## Not yet specified

- Exact schema and migration plan for `gpt/profile-evidence.md`.
- Exact skill name, trigger phrases, mode syntax, and reference-file layout.
- Exact evaluator format, scoring thresholds, and whether deterministic checks need a script.
- Exact resume golden examples and regression corpus.
- Exact template-selection and LaTeX validation behavior.
- Exact review-loop behavior when an output fails evaluation.

## Out of scope

- Automatically submitting applications or sending recruiter messages.
- Automatically editing project repositories or external Kiro/Cursor sessions.
- Claiming production usage, customers, scale, or domain experience without verified evidence.
