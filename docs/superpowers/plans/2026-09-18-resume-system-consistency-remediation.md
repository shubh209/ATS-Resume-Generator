# Resume System Consistency Remediation Implementation Plan

> **For agentic workers:** If this plan is delegated in a future session, use `superpowers:subagent-driven-development` or `superpowers:executing-plans`. This session will execute it inline because no delegation was requested.

**Goal:** Resolve the audit findings using the user's confirmed facts, prevent stale or unsupported material from reaching live resume output, and preserve unrelated working-tree changes.

**Architecture:** Keep current master facts in `gpt/`, live behavior in `.agents/skills/resume-tailor/`, and selectable output in the three official lane templates. Historical and superseded material remains available only when clearly isolated from live workflows. A strengthened preflight enforces high-risk invariants.

**Tech Stack:** Markdown, LaTeX, Python standard-library tests and validation scripts.

**Spec:** `docs/superpowers/specs/2026-09-18-resume-system-consistency-remediation-design.md`

## Global Constraints

- Preserve all unrelated and pre-existing working-tree changes.
- Do not stage, commit, reset, restore, clean, or otherwise mutate Git state.
- Use `apply_patch` for every source edit.
- Do not browse the internet or use another repository as evidence.
- Do not silently choose between unresolved facts; use only the decisions recorded in the approved design.
- Treat externally unverified metrics as unavailable to live output until supporting evidence exists in this workspace.

### Task 1: Add regression checks for live-source invariants

**Files:**

- Create: `tests/test_resume_preflight.py`
- Modify: `.agents/skills/resume-tailor/scripts/preflight.py`

1. Add subprocess tests proving that preflight rejects selectable projects without a locked bullet bank, multiple current versions in one locked lane, stale employment titles, and prohibited unsupported outcome language in active templates.
2. Run the new tests and record the expected failures against the current preflight.
3. Extend preflight with the smallest general checks needed to make the tests pass.
4. Run the focused test file and the preflight against the current workspace.

### Task 2: Canonicalize employment facts

**Files:**

- Modify: `gpt/work-experience.md`
- Modify: official and optional LaTeX templates containing DAS or ASU employment facts
- Modify: career stories, networking profile, prompts, and interview material that present those facts as current

1. Set Digital Aid Seattle title to `Software Engineer`.
2. Set DAS scale to `400 active members across 12 ensembles`.
3. Set ASU title to `Data Management Intern`, retaining January 2026–May 2026.
4. Update reachable current references and explicitly label saved/historical artifacts that must not govern current facts.

### Task 3: Canonicalize project claims and selection status

**Files:**

- Modify: `gpt/projects/*.md`
- Modify: `templates/variants/fullstack-engineer.tex`
- Modify: `templates/variants/backend-faang.tex`
- Modify: `templates/variants/ai-engineer-faang.tex`
- Modify: optional or historical templates only as needed to isolate them from live use

1. Relabel Hearloop Backend Version 1 superseded and retain Backend Version 2 as canonical; leave AI Version 1 current.
2. Remove or qualify unsupported realized outcomes for side projects using `designed to`, `projected`, or equivalent honest framing.
3. Mark projects without a valid locked bank as not selectable.
4. Remove externally unverified metrics from active lane templates while preserving what/how/context/why.
5. Keep the live lane bullet counts and section order compliant with the tailoring skill.

### Task 4: Canonicalize behavioral-story evidence

**Files:**

- Modify: `Amazon-LP/stories/ASU-HuggingFace-Full-Stack-Deployment.md`
- Modify: `Amazon-LP/stories/DAS-Rainbow-Duplicate-Records.md`
- Modify: `Amazon-LP/Amazon-Behavioral-Stories-Version-1.md`
- Modify: `Amazon-LP/STORY-QUESTION-MAP.md`

1. Limit the ASU Hugging Face ownership claim to Gradio frontend integration and the frontend–backend contract.
2. Make the Rainbow story state only that an ensemble manager discovered duplicates caused by different emails and reversed name order; name-token matching with human approval was added; deployment and recurrence metrics are unconfirmed.
3. Remove or isolate the previous Rainbow version from active story selection.

### Task 5: Align live instructions and isolate legacy workflows

**Files:**

- Modify: `.agents/skills/resume-tailor/SKILL.md`
- Modify: `governance/FACT_RULES.md`
- Modify: `governance/RESUME_AUDIT_REPORT_SCHEMA.md`
- Modify: active onboarding documents and legacy prompt/skill copies identified by the audit

1. Require Technical Skills support from current master facts, not from a selected template.
2. State that live tailoring selects locked bullets and does not rewrite them.
3. Remove active references to prohibited legacy sources.
4. Add conspicuous non-live labels and canonical pointers to historical prompt and skill copies.

### Task 6: Clean reachable networking and application material

**Files:**

- Modify: `networking/candidate-profile.md`
- Modify: `prompts/networking.md`
- Modify: `prompts/application-answers.md`
- Modify: affected saved application or interview artifacts only to correct current claims or isolate them as historical

1. Correct employment titles, dates, and supported technologies.
2. Remove unsupported project costs, adoption, test counts, or business outcomes from material reachable by current workflows.
3. Preserve legitimate tailoring differences and historical records when clearly bounded.

### Task 7: Verify and document remediation

**Files:**

- Create: `audits/2026-09-18-resume-system-consistency-remediation.md` or next available suffix

1. Run the focused tests and preflight.
2. Search all audited text for every superseded title, metric, outcome phrase, and ambiguous current-version marker.
3. Inspect active templates for required counts, headings, titles, dates, and source-supported skills.
4. Capture final Git status and diff summaries without changing Git state.
5. Record resolved clusters, intentionally isolated historical material, remaining external-evidence limitations, tests, and integrity observations in the remediation report.
