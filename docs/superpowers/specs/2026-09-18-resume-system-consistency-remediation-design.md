# Resume System Consistency Remediation Design

## Goal

Resolve the 20 finding clusters in `audits/2026-09-18-resume-system-consistency-audit.md` without inventing evidence, overwriting historical audit evidence, or disturbing unrelated working-tree changes.

## Confirmed user decisions

- Digital Aid Seattle title: **Software Engineer**.
- Digital Aid Seattle scale: **400 active members across 12 ensembles**.
- ASU title and dates: **Data Management Intern, January 2026–May 2026**.
- Hugging Face ownership: Shubh owned the **Gradio frontend integration and the frontend–backend contract**, not the entire deployment.
- Rainbow City canonical incident: an ensemble manager found duplicate records caused by different emails and reversed name order; Shubh added name-token matching with human approval; no deployment or recurrence metric is claimed.
- Hearloop Backend Version 2 is canonical; Backend Version 1 becomes superseded. The AI Version 1 bank remains current.

## Architecture

The remediation uses a single-authority flow. `AGENTS.md` points live tailoring to `.agents/skills/resume-tailor/SKILL.md`; that skill consumes current governance, master facts, and one lane template. Master facts define claims, templates mirror locked selections, and preflight checks that the mirrors cannot drift. Legacy workflows remain available only as explicitly non-authoritative historical material.

## Workstreams

### 1. Canonical employment facts

Update the work-experience master, career context, active templates, active networking facts, and directly reusable prompts to use the confirmed DAS and ASU facts. Generated evaluations and saved historical applications remain historical and receive an explicit non-authoritative boundary instead of being silently rewritten as current output.

### 2. Canonical project claims

Keep built and measured technical facts. Convert intended value to `designed to`, `to verify`, or `projected` wording. Remove claims of real customers, adoption, retention, traffic, leadership approval, realized savings, or production use when the masters do not document them. Externally sourced metrics remain explicitly externally unverified and cannot enter active templates until their evidence is available in this workspace.

### 3. Interview-story consistency

Make the user-confirmed Rainbow City and Hugging Face ownership boundaries canonical. Remove the discarded Rainbow City account from runnable story banks. Mark stale consolidated interview Q&A as a historical codebase snapshot rather than current candidate truth.

### 4. Instruction consistency

Make immutable locked-bullet selection, lane-specific project counts, full application output, and evidence-derived skills the positive single contract. Legacy prompts, generic templates, and golden-JD workflows receive clear non-live labels and pointers to the current skill. They cannot override current facts.

### 5. Deterministic validation

Add test-first coverage for preflight. Preflight must reject:

- a selectable project without a current lane-specific locked bullet bank;
- multiple banks for one lane labeled current;
- incorrect DAS or ASU titles, dates, or scale in active templates;
- wrong experience or project bullet counts;
- known unsupported or retired claim phrases in active lane templates;
- technical skills that are not supported by current masters.

The test suite uses temporary repository fixtures and invokes the real preflight command. Each new invariant is observed failing before production logic is added.

## Historical boundary

The original audit remains unchanged as a dated snapshot. A separate remediation report records decisions, changed paths, tests, remaining externally unverified evidence, and final integrity checks.

## Verification

- Run the new preflight tests.
- Run the live preflight against the working tree.
- Search active sources for every retired title, metric, technology, outcome, and workflow phrase.
- Compare all three active lane templates against the master facts and required counts.
- Compile templates when a LaTeX engine is available; otherwise record that layout validation was not run.
- Confirm Git changes are limited to planned remediation paths plus pre-existing user changes.

## Constraints

- No internet or external repository evidence is assumed.
- No Git staging, commits, reset, restore, checkout, or clean operations.
- Preserve unrelated and pre-existing changes.
- Do not modify saved application wording merely for stylistic consistency; only label or correct factual contamination paths.
