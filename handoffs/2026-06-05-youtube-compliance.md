# Handoff: ATS Resume Generator (from YouTube Compliance Pipeline session)

> **Purpose:** Carry context from the agent chat in the `Youtube-Ads-Compliance-Pipeline` workspace into this `ATS Resume Generator` project.
> **How to use:** `@handoffs/2026-06-05-youtube-compliance.md` + `@CONTEXT.md` + `@gpt/system-prompt.md`

---

## Repo layout (updated June 2026)

See `README.md` for full map. GPT paste bundle lives in `gpt/`.

```
gpt/system-prompt.md
gpt/work-experience.md
gpt/per-project-keywords.md
gpt/projects/*.md
templates/main.tex
CONTEXT.md
```

---

## What this session was about

Two related threads:

1. **YouTube Ads Compliance Pipeline** — updated project docs, humanized prose, locked resume bullets, Tier 1+2 features (Postgres, Entra, k=8 RAG, human review, etc.).
2. **ATS Resume Generator** — how project MDs should work as GPT master context, what assumptions to fix, and how to add a real verification feedback loop.

---

## Critical finding: stale master context

| File | Status |
|---|---|
| `Development/AI:LLM/Youtube-Ads-Compliance-Pipeline/YouTube_Ads_Compliance_Pipeline.md` | **Source of truth** in dev repo |
| `gpt/projects/youtube-ads-compliance-pipeline.md` | **Synced** (v3, locked FS + AI bullets) |
| `gpt/per-project-keywords.md` → Video Compliance section | **Synced** (June 2026) |

GPT reads **`gpt/` in this Applications folder**, not the dev repo. Re-sync after major project changes.

---

## How this ATS system actually works

Not a vector RAG app. It is **Custom ChatGPT (GPT Builder)** with pasted master context:

```
JD → Custom GPT (gpt/system-prompt.md)
       ├── gpt/projects/*.md
       ├── gpt/work-experience.md
       ├── gpt/per-project-keywords.md
       └── templates/main.tex + rules in CONTEXT.md
     → Validation Summary + changed LaTeX sections
     → Paste into Overleaf
```

---

## What each project MD should contain (target schema)

Extend beyond `CONTEXT.md` section 8:

```markdown
## Project Status
demo prototype | production | academic

## Verified Metrics
[MEASURED only — table with labels]

## Never Claim
- bullets GPT must not invent

## Locked Resume Bullets (Full Stack)
[verbatim, copy to resume]

## Locked Resume Bullets (AI Engineer)
[verbatim]

## Bullet Atoms
### atom-id
Roles: [...]
Keywords: [...]
What / How / Why / Metric label

## Tagline / Tech Stack / Problem / Solution / My Role / Impact / How It Works / Keywords
```

**YouTube locked bullets:** see `gpt/projects/youtube-ads-compliance-pipeline.md`

**Interview framing:** Working prototype for pre launch screening. Built for demos and interviews, not live customer rollout.

**YouTube [MEASURED] metrics:** 2 policy PDFs, 37 chunks, RAG k=8, 9 pytest tests, CI deploy on push to main, API v3.0.0.

**YouTube Never Claim:** production customer rollout; React/TypeScript frontend; measured latency/accuracy; ~30 sec review time; ~95% metadata success; 80 videos tested.

---

## Assumptions to clear (replace in prompts + CONTEXT.md)

| Wrong assumption | Replace with |
|---|---|
| GPT self-validates 40/40 | Validation Summary is draft only; user + Overleaf + optional script are gates |
| Never reuse bullets verbatim | Rewrite wording for JD; **lock facts** from Verified Metrics / Locked bullets |
| Infer `[ESTIMATE]` in project MDs | Only `[MEASURED]` numbers get `\metric{}` in LaTeX |
| JD keyword = add any skill | JD keyword only if supported by project MD or `gpt/work-experience.md` |
| One prompt behavior | Single output contract (see below) |
| Project score is computed | Require **Project Selection table** before LaTeX |
| Success = keyword report | **Definition of Done** = compile, 1 page, fact check clean |

---

## Pending work (pick up in this project)

### P0 — Sync truth
- [x] Replace `gpt/projects/youtube-ads-compliance-pipeline.md` from dev repo
- [x] Update `gpt/per-project-keywords.md` Video Compliance row
- [x] Add Verified Metrics, Never Claim to Compliance MD
- [x] Add locked Backend bullets to Compliance MD
- [ ] Add Bullet Atoms sections (optional; defer)

### P1 — Governance
- [x] `governance/OUTPUT_CONTRACT.md`
- [x] `governance/DEFINITION_OF_DONE.md`
- [x] `governance/FACT_RULES.md`
- [x] `governance/auditor-prompt.md`
- [x] `governance/feedback-log.md` (template)
- [x] Align `gpt/system-prompt.md` with above

### P2 — Regression
- [x] `golden-jds/` with 3 sample JDs
- [ ] Optional `verify_resume_tex.py`

### P3 — GPT Builder
- [ ] Re-paste updated `gpt/` files into Configure → Instructions
- [ ] Test one golden JD end to end in Overleaf

---

## Source files in dev repo (copy from)

```
/Users/shubhkapadia/Desktop/Development/AI:LLM/Youtube-Ads-Compliance-Pipeline/YouTube_Ads_Compliance_Pipeline.md
/Users/shubhkapadia/Desktop/Development/AI:LLM/Youtube-Ads-Compliance-Pipeline/YouTube_Ads_Compliance_Pipeline_Context.md
/Users/shubhkapadia/Desktop/Development/AI:LLM/Youtube-Ads-Compliance-Pipeline/Youtube-Ads-Compliance-Pipeline/docs/SETUP_TESTING.md
```

---

## Suggested next prompt

```
@golden-jds/full-stack-software-engineer.md @governance/OUTPUT_CONTRACT.md

Run a regression tailor. Verify Selection + Fact Check + LaTeX against DEFINITION_OF_DONE.
```
