# Job OS Approach 1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship Phases 1–4 of the Job OS: file knowledge base, update-knowledge curator contracts, answers/LinkedIn rewired to KB, and role-lane goldens + run-log stubs.

**Architecture:** Single Cursor router (`experimental/job-os-router.md` + `.cursor/skills/job-os-router/`) over markdown memory in `knowledge/` plus existing `gpt/` facts. No multi-agent platform. KB writes are propose → approve → write with per-project `_ingest_index.json`.

**Tech Stack:** Markdown contracts, Cursor skills, optional small Python validator for KB skeleton; existing governance for resume (P1, untouched except README pointers).

**Spec:** `docs/superpowers/specs/2026-07-16-job-os-approach1-design.md`  
**Router prompt (Phase 0 done):** `experimental/job-os-router.md` (moved from `prompts/job-os-router.md` during the 2026-08 repo restructure — this file is not yet in active use)

## Global Constraints

- P0 = answers + LinkedIn (+ update-knowledge); P1 = resume (do not rewrite OUTPUT_CONTRACT in this plan)
- Never invent metrics/stories; empty KB → thin / `[NEED:]`
- No per-company application folders
- Propose → approve → write for all KB mutations
- Session ingest index required for update-knowledge
- Voice B + `reference/humanizer.md`; no em dashes in paste-ready output
- Goldens by role lane, not company
- Commits only when the user explicitly asks to commit (do not auto-commit)

## File map

| Path | Responsibility |
|------|----------------|
| `knowledge/**` | Durable process memory (A/B/stories/artifacts/index) |
| `experimental/job-os-router.md` | Ultimate router prompt (exists) |
| `.cursor/skills/job-os-router/SKILL.md` | Cursor discovery for router |
| `prompts/application-answers.md` | Answers contract (rewrite) |
| `.cursor/skills/application-answers/SKILL.md` | Answers skill (rewrite) |
| `prompts/linkedin-connection-note.md` | Connection note (update) |
| `prompts/linkedin-message.md` | Post-connect messages (new) |
| `.cursor/skills/linkedin-connection-note/SKILL.md` | Update |
| `.cursor/skills/linkedin-message/SKILL.md` | New |
| `.cursor/skills/update-knowledge/SKILL.md` | Curator mode |
| `evals/golden/<lane>/` | Role-lane regression questions + expectations |
| `governance/run-log.md` | Trace stubs |
| `scripts/validate_knowledge_skeleton.py` | Structure check for Phase 1 |
| `README.md` / `CONTEXT.md` | Point to Job OS without rewriting resume system |

---

### Task 1: Knowledge skeleton + validator

**Files:**
- Create: `knowledge/README.md`
- Create: `knowledge/identity.md`
- Create: `knowledge/stories.md`
- Create: `knowledge/projects/<id>/{decisions,walkthrough,stories,artifacts}.md` and `_ingest_index.json` for each id in `gpt/projects/` (filename without `.md`)
- Create: `knowledge/experience/einfochips/stories.md`
- Create: `knowledge/experience/asu-academic-records/stories.md`
- Create: `scripts/validate_knowledge_skeleton.py`
- Modify: `.gitignore` — ignore `knowledge/_raw/` (and optionally `**/chat-exports/`)

**Interfaces:**
- Consumes: list of project files under `gpt/projects/*.md`
- Produces: empty templates with schema headings matching the spec; `_ingest_index.json` shape `{"sessions":[]}`; validator exit 0 when skeleton complete

- [ ] **Step 1: Add gitignore entries for raw dumps**

Append to `.gitignore` (create file if missing):

```gitignore
# Job OS — raw chat dumps (approved summaries live in knowledge/)
knowledge/_raw/
**/chat-exports/
```

- [ ] **Step 2: Write `knowledge/README.md`**

Include: purpose; layout; propose→approve→write; how to run `update-knowledge`; pointer to spec and router prompt; empty sections OK.

- [ ] **Step 3: Write template bodies**

For each `decisions.md`:

```markdown
# Decisions — <Project Name>

<!-- Approved entries only. Agent proposes; user approves. -->

## Entries

<!--
### <short title>
- Decision:
- Alternatives considered:
- Why stuck with it:
- Mistake / dead end:
- I'd do differently now:
- Source: manual | session-note | chat-export
- Date:
-->
```

For each `walkthrough.md`: headings One-minute pitch; How it works; Constraints designed for; Hard parts; Demo / repo pointers (empty sections with HTML comments OK).

For each project `stories.md` and experience/global `stories.md`: document the story field list in a short comment + empty `## Stories` section.

For each `artifacts.md`:

```markdown
# Artifacts — <Project Name>

| URL | Problem solved | I'd do differently (or decisions.md anchor) | Good for |
|-----|----------------|-----------------------------------------------|----------|
|     |                |                                               |          |
```

For each `_ingest_index.json`:

```json
{
  "schemaVersion": 1,
  "projectId": "<id>",
  "sessions": []
}
```

`identity.md`: short placeholders for voice notes / OPT one-liner / bans (optional content).

- [ ] **Step 4: Write validator**

Create `scripts/validate_knowledge_skeleton.py` that:

1. Lists `gpt/projects/*.md` stems as required project ids  
2. Asserts each required path under `knowledge/projects/<id>/` exists  
3. Asserts experience + global stories + README exist  
4. Asserts each `_ingest_index.json` parses and has `sessions` list  
5. Prints `OK` or lists missing paths; exit 1 on failure  

- [ ] **Step 5: Run validator**

Run: `python3 scripts/validate_knowledge_skeleton.py`  
Expected: `OK`

- [ ] **Step 6: Stop for user review** (commit only if user asks)

---

### Task 2: Cursor skill — Job OS router

**Files:**
- Create: `.cursor/skills/job-os-router/SKILL.md`
- Modify: `README.md` — add Job OS row pointing to spec + `experimental/job-os-router.md`

**Interfaces:**
- Consumes: `experimental/job-os-router.md`
- Produces: skill that triggers on Job OS / answers+outreach routing / update-knowledge mentions

- [ ] **Step 1: Write skill frontmatter + body**

```markdown
---
name: job-os-router
description: >-
  Route Shubh Kapadia's Job OS modes (answers, linkedin, linkedin-message,
  update-knowledge, resume). Use when the user names a Job OS mode, asks for
  application answers or LinkedIn outreach with KB grounding, or wants to
  update project knowledge from sessions.
---

# Job OS Router

1. Read `experimental/job-os-router.md` and follow it exactly.
2. Read `docs/superpowers/specs/2026-07-16-job-os-approach1-design.md` if behavior is ambiguous.
3. For answers/LinkedIn details, also follow the updated prompts under `prompts/` after Task 4–5 land.
```

- [ ] **Step 2: Add README quick lookup rows** for Job OS router, `knowledge/`, evals

- [ ] **Step 3: User review gate**

---

### Task 3: update-knowledge skill + ingest contract

**Files:**
- Create: `.cursor/skills/update-knowledge/SKILL.md`
- Create: `prompts/update-knowledge.md`

**Interfaces:**
- Consumes: `knowledge/projects/<id>/_ingest_index.json`, Coach/session inputs, existing A/B/stories/artifacts
- Produces: propose-only patch workflow documented for the agent

- [ ] **Step 1: Write `prompts/update-knowledge.md`**

Must include:

- Required input: `projectId` or experience id  
- Algorithm: list sessions → filter by index fingerprint → summarize new only → propose unified diff or section patches → stop  
- On approve: write markdown + append/update index records with fields: `sessionId`, `harness`, `workspace`, `lastMessageAt`, `contentFingerprint`, `ingestedAt`, `status`, `notes`  
- On reject: status `rejected_by_user`  
- Coach = discovery; raw dumps under `knowledge/_raw/` (gitignored)  
- Never invent decisions not supported by session/export text  

- [ ] **Step 2: Write skill pointing at that prompt**

- [ ] **Step 3: Dry-run checklist (manual test)**

Without real Coach data, run a fake propose: user pastes 1 paragraph “session note” for hearloop → agent must propose `decisions.md` entry and show index update **without writing** until approve.

Expected: proposal visible; files unchanged until user says approve.

---

### Task 4: Rewrite application-answers prompt + skill

**Files:**
- Modify: `prompts/application-answers.md`
- Modify: `.cursor/skills/application-answers/SKILL.md`
- Modify: `applications/README.md` (inputs + KB SoT)

**Interfaces:**
- Consumes: `knowledge/**`, `gpt/**`, JD, questions; optional `.tex`
- Produces: paste-ready answers + NEED/thin + trace stub

- [ ] **Step 1: Rewrite `prompts/application-answers.md` to match spec §6**

Replace “resume `.tex` required / only truth” with:

- Main SoT = `knowledge/` + `gpt/`  
- `.tex` optional  
- Length context-dependent; short and direct  
- Runtime overlap for Why-company  
- Story routing (technical vs behavioral)  
- Partial `[NEED:]` policy  
- Output includes trace stub  
- Point to `experimental/job-os-router.md` for shared rules  

Keep playbooks for common question types but remove rigid 50–90/120 as hard global max unless portal states a limit (bias short).

- [ ] **Step 2: Rewrite skill** to match (no refuse-on-missing-`.tex`)

- [ ] **Step 3: Manual test against Full Stack golden questions (Task 6)** once goldens exist; until then, smoke test with 2 questions and empty KB → expect thin/`[NEED:]`, no invention

---

### Task 5: LinkedIn connection-note update + linkedin-message

**Files:**
- Modify: `prompts/linkedin-connection-note.md`
- Modify: `.cursor/skills/linkedin-connection-note/SKILL.md`
- Create: `prompts/linkedin-message.md`
- Create: `.cursor/skills/linkedin-message/SKILL.md`
- Modify: `networking/README.md`

**Interfaces:**
- Connection note: 300/3-line contract unchanged structurally; grounding from KB; refuse generic if their hook missing  
- Post-connect: longer message contract  

- [ ] **Step 1: Update connection-note prompt** — them+you hard rule; KB metrics; `[NEED: their hook]`; trace stub; pointer to router  

- [ ] **Step 2: Write `prompts/linkedin-message.md`**

Inputs: same person fields + optional prior thread; length guidance (e.g. ~80–150 words default unless user says); voice B; grounded ask; no fake familiarity.

- [ ] **Step 3: Skills + networking README**

- [ ] **Step 4: Manual test** — connection note with thin “their experience” → must not produce generic pitch  

---

### Task 6: Role-lane goldens + run-log

**Files:**
- Create: `evals/golden/full-stack-engineer/questions.md`
- Create: `evals/golden/full-stack-engineer/expectations.md`
- Create: `evals/golden/backend-engineer/questions.md`
- Create: `evals/golden/backend-engineer/expectations.md`
- Create: `evals/golden/ai-engineer/questions.md`
- Create: `evals/golden/ai-engineer/expectations.md`
- Create: `evals/golden/software-engineer/questions.md`
- Create: `evals/golden/software-engineer/expectations.md`
- Create: `evals/README.md`
- Create: `governance/run-log.md`
- Optional: `evals/fixtures/sample-jds/full-stack-snippet.md` (thin, for overlap wiring only)

**Interfaces:**
- Consumes: role-typical work/approach questions (debug, artifact, ramp, constraints, ownership)  
- Produces: checklist expectations; no company-specific Why-us as golden spine  

- [ ] **Step 1: Write `evals/README.md`** — how to run a golden (paste questions into answers mode with a lane JD snippet); score expectations manually  

- [ ] **Step 2: Fill each lane `questions.md` with 4–6 work/approach prompts** (adapt wording slightly per lane; include debug + artifact + least-experience-stack + design-constraint + ownership/feedback)

- [ ] **Step 3: Fill `expectations.md` checklists** matching spec §8 (no invented debug; artifact from KB or NEED; short/direct; tone; KB SoT)

- [ ] **Step 4: Create `governance/run-log.md`** with header + table template for pasted trace stubs  

- [ ] **Step 5: Manual golden pass on full-stack-engineer** with current (possibly empty) KB — expect honest NEED/thin, pass checklist  

---

### Task 7: Wire docs (CONTEXT + applications/networking)

**Files:**
- Modify: `CONTEXT.md` — add Job OS section pointing to spec, router, knowledge/, evals; note resume remains §governance  
- Modify: `applications/README.md` and `networking/README.md` if not fully updated in Tasks 4–5  

- [ ] **Step 1: Add CONTEXT.md “Job OS” section** (problem → KB → modes → link spec)  
- [ ] **Step 2: Ensure no doc still says “refuse until `.tex`” for answers  
- [ ] **Step 3: User review — Phase 1–4 complete**  

---

## Spec coverage check

| Spec area | Task |
|-----------|------|
| KB layout A/B/stories/artifacts/experience/index | Task 1 |
| Router prompt | Done (`experimental/job-os-router.md`) + Task 2 |
| update-knowledge + ingest | Task 3 |
| Answers contract | Task 4 |
| LinkedIn connection + post-connect | Task 5 |
| Role-lane goldens + run log | Task 6 |
| Docs pointers | Task 7 |
| Resume P1 / email / interview | Out of this plan (Phases 5–6) |
| Coach auto-integration | Documented in Task 3; full Coach API wiring may need follow-up when workspace mapping is known |

## Placeholder / consistency review

- Project ids = `gpt/projects` stems (including `ClusterOps`)  
- Index schema fields match spec  
- No per-company folders in any task  
- Commit steps deferred to user request  

---

## Execution handoff

Plan complete and saved to `docs/superpowers/plans/2026-07-16-job-os-approach1.md`.

Ultimate router prompt: `experimental/job-os-router.md`.

**Two execution options:**

1. **Subagent-Driven (recommended)** — fresh subagent per task, review between tasks  
2. **Inline Execution** — run tasks in this session with checkpoints  

Which approach?
