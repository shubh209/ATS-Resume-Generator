# Job OS (Approach 1) — Design Spec

> Status: approved 2026-07-16  
> Date: 2026-07-16  
> Owner: Shubh Kapadia  
> Scope: Cursor-first personal Job OS — knowledge base + single router; P0 = application answers + outreach; P1 = resume tailor (existing governance)

---

## 1. Problem

The current system has strong **resume facts** (`gpt/`) and resume governance, but application answers and outreach are shallow because they lack **process context** (decisions, mistakes, walkthroughs, reusable stories, artifacts). Agents stall (e.g. demand `.tex` + inventable debug stories) or produce generic AI-toned copy.

**Root cause:** missing knowledge base and weak contracts for answers/outreach — not primarily “need a better resume tailor.”

**Success criteria (priority order):**

1. **Defendability** — claims exist in facts/KB; no invented stories  
2. **Human tone** — conversational-careful (voice B); send-as-is bar  
3. Speed is a side effect, not the design target  
4. No application volume limit as a constraint  

---

## 2. Goals and non-goals

### Goals

- Single **router** in Cursor with **explicit modes** (no assumed full application pack)  
- Durable **file knowledge base** for process + stories + artifacts  
- **Application answers** and **LinkedIn** (connection note + post-connect message) as P0 surfaces  
- **Update-knowledge** curator using AI Engineer Coach / sessions with **ingest index** (avoid re-tokenizing old sessions)  
- Runtime **company overlap** from JD + KB (no per-company files)  
- Role-lane **golden evals** focused on work/approach questions  
- Email + interview later on the same memory  
- Resume tailor remains available (P1); may later cite KB decisions  

### Non-goals (Approach 1)

- Multi-agent mesh, Temporal/LangGraph, hosted SaaS, vector DB as requirements  
- Per-company application folders  
- Replacing resume `OUTPUT_CONTRACT` / FACT_RULES in the first cut  
- Auto-writing KB without user approval  

### Production principles applied (video → this system)

| Principle | Approach 1 mapping |
|-----------|-------------------|
| Memory vs state | `gpt/` + `knowledge/` = memory; JD/questions/overlap this run = state |
| Tool contracts | Path + schema + propose/approve for writes |
| Orchestration | Procedural checklist in router prompt / skills |
| Evaluation | Role-lane goldens + run-log stubs |
| Approval | KB mutations propose → approve → write |

---

## 3. Architecture

```text
You: explicit mode + inputs
        │
        ▼
┌──────────── ROUTER (single agent / skill) ────────────┐
│ parse → retrieve memory → (runtime overlap) → draft   │
│ → tone gate → emit + [NEED:]/thin → optional propose  │
└───────────────────────────────────────────────────────┘
        │
        ├── knowledge/ + gpt/     (memory)
        └── surfaces: answers, linkedin*, update-knowledge,
                      resume (P1), email/interview (later)
```

**AI Engineer Coach:** discovery aid for sessions when updating KB — not the answer brain. Session detail APIs are truncated; full depth comes from source logs/exports summarized into approved markdown.

---

## 4. Knowledge base

### 4.1 Layout

```text
knowledge/
  README.md
  identity.md                      # optional voice / constraints
  stories.md                       # behavioral only
  projects/<id>/                   # one per gpt/projects entry
    decisions.md                   # A
    walkthrough.md                 # B
    stories.md                     # technical stories for this project
    artifacts.md                   # file/commit/PR for this project
    _ingest_index.json             # sessions already processed
  experience/
    einfochips/
      stories.md
    asu-academic-records/
      stories.md
```

**Facts remain in `gpt/projects/*.md` and `gpt/work-experience.md`.** KB adds process; do not duplicate metrics as a second SoT for numbers (metrics still sourced from facts unless explicitly promoted into KB with care).

**Project ids (initial):** mirror `gpt/projects/` filenames without `.md` (e.g. `hearloop`, `seo-audit-engine`, `youtube-ads-compliance-pipeline`, `ClusterOps`). Prefer kebab-case for any new folders; do not rename existing fact files in Phase 1.

### 4.2 Schemas (fields)

**A — `decisions.md`:** Decision; Alternatives; Why stuck with it; Mistake/dead end; I’d do differently now; Source + date  

**B — `walkthrough.md`:** One-minute pitch; How it works; Constraints designed for; Hard parts; Demo/repo pointers  

**C — technical `projects/*/stories.md`:** id; Type; Situation; What you did; Root cause/outcome; Tool/log/technique (if debug); Use when  

**C — behavioral `stories.md` + `experience/*/stories.md`:** same shape; types like feedback, ownership, collaboration, ambiguity  

**Artifacts — `projects/*/artifacts.md`:** URL (file/commit/PR); Problem solved; I’d do differently (prefer pointer to A); Good for  

**No `applications/` company tree.** Overlap (D) is computed at draft time from JD + memory and discarded (unless user later opts into saving — out of scope).

### 4.3 Empty content policy

Empty sections are allowed. Agent writes **thin** answers from available memory and labels **`[NEED: …]`** or “thin”. Do not invent. Block entire forms only if user explicitly says so.

### 4.4 Update path (`update-knowledge`)

1. Target project or experience id  
2. List Coach/sessions for that workspace  
3. Skip sessions in `_ingest_index.json` with unchanged fingerprint  
4. Summarize only new/changed sessions  
5. **Propose** patch to A/B/stories/artifacts + index updates  
6. On **approve** → write files and update index  
7. Rejected proposals: mark sessions `rejected_by_user` (default) to avoid repeat spam  

Raw chat dumps: **gitignored**; only approved markdown + index in repo.

Index record fields: `sessionId`, `harness`, `workspace`, `lastMessageAt`, `contentFingerprint`, `ingestedAt`, `status` (`ingested` | `skipped_low_signal` | `rejected_by_user`), `notes`.

---

## 5. Router modes

| Mode | Priority | Behavior |
|------|----------|----------|
| `answers` | P0 | Questionnaire / portal answers from KB + facts |
| `linkedin` / `connection-note` | P0 | ≤300 chars, 3 lines, them+you |
| `linkedin-message` | P0 | Post-connect longer message; same grounding/tone |
| `update-knowledge` | P0 (enabler) | Curator propose → approve → write |
| `resume` | P1 | Existing OUTPUT_CONTRACT; later optional cite decisions |
| `email` | Later | Same memory |
| `interview` | Later | Same memory |

User always states the mode. No auto full pack.

---

## 6. Answers contract

- **Main SoT:** `knowledge/` + `gpt/` (KB may include detail not on the one-page resume)  
- **Never invent** metrics, debug stories, or artifacts  
- **Length:** context-dependent (company, role, stated limit, question type); bias **short and direct**  
- **Voice B:** conversational-careful; no em dashes; no cover-letter AI register; humanizer gate (tone research may refine later)  
- **Why company:** runtime overlap from JD + your work only; no fake passion; use themes already in the JD (no web research unless asked)  
- **Story routing:** technical → `projects/*/stories.md`; behavioral → `stories.md` / `experience/*/stories.md`  
- **Partial forms OK:** answer what is grounded; `[NEED:]` on blocked items  
- **OPT/visa:** only if asked or user requests  
- **Multi-question:** one reply, per-question sections  
- **`.tex`:** optional if this application’s resume differs from master; not required to start  

---

## 7. LinkedIn contracts

### Connection note (`linkedin`)

- Name, title, experience-at-company when possible; intent `network` | `ask` | `referral`; JD optional  
- Exactly 3 lines, ≤300 characters; no Hi Name  
- Them hook + you hook required; if their side thin → do not ship generic; ask or `[NEED: their hook]`  
- One person per run  
- No OPT/H1-B; no portfolio URLs in the note  
- Line 2 metric/decision phrase from facts/KB; keep short  
- Same structure for recruiter vs engineer; ask line differs  

### Post-connect (`linkedin-message`)

- Longer than 300 chars allowed  
- Still them+you, grounded, voice B  
- Not a substitute for `email` mode (email later for formal threads)  

---

## 8. Evaluation and observability

### Goldens (by role lane, not company)

```text
evals/golden/
  full-stack-engineer/
  backend-engineer/
  ai-engineer/
  software-engineer/
```

Focus: work/approach questions (debug, artifact + do differently, ramp, design under constraints, ownership). Company-specific “why us” is runtime-only, not the golden spine.

Optional thin JD snippets under `evals/fixtures/sample-jds/` only to exercise overlap wiring.

### Run log

Agent always emits a one-line trace stub (mode, role/company if any, NEED count, thin flags). User ratings optional (`send` / `edit` / `reject` or 1–5). Append to `governance/run-log.md` (or dated files).

### Metrics (informal)

Invent rate; send-as-is rate; NEED rate; tone fail rate; generic outreach rate.

### Human scoring

Manual golden pass when system/prompts/schemas change (E1). Not every application.

---

## 9. Build order

| Phase | Deliverable |
|-------|-------------|
| 0 | This spec + ultimate router prompt draft |
| 1 | KB skeleton (empty templates + README) |
| 2 | `update-knowledge` curator + ingest index |
| 3 | Answers + LinkedIn skill/prompt rewrite |
| 4 | Role-lane goldens + run-log stub |
| 5 | Email + interview modes |
| 6 | Resume optional cite from decisions (P1) |

**First useful cut = Phases 1–4.**

---

## 10. Locked decisions log (grill)

- Explicit mode every run; JD-driven for now; cold/founders later on same system  
- Approach 1 (file KB + single Cursor router)  
- P0 answers + outreach; P1 resume  
- KB SoT for answers; empty OK; propose→approve→write  
- Session ingest index for token control  
- Coach as discovery, not SoT  
- No per-company KB files; artifacts per project; behavioral + per-project technical stories; experience tree  
- Voice B now; samples later (voice C)  
- Role-lane goldens; E1/E2 as above  

---

## 11. Open items (post-spec, not blockers for Phase 1)

- Exact Coach → workspace mapping for each project folder  
- Tone research pass for voice B examples  
- Resume citing decisions (Phase 6 detail)  

---

## 12. Out of scope reminders

Do not treat Intramotev (or any single company) as the regression golden. Do not build multi-agent infrastructure before KB has real content.
