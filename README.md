# ATS Resume Generator

Repeatable system for JD-tailored, ATS-friendly LaTeX resumes via Custom ChatGPT + Overleaf.

**Start here** → then read [`CONTEXT.md`](CONTEXT.md) for all rules and decisions.

---

## Directory map

```
ATS Resume Generator/
├── README.md                 ← you are here
├── CONTEXT.md                ← rules, bullet formula, base resume variants
├── governance/               ← tailoring contract (authoritative for JD runs)
│   ├── OUTPUT_CONTRACT.md    ← what GPT outputs and how it selects content
│   ├── DEFINITION_OF_DONE.md ← your checklist before Overleaf
│   ├── FACT_RULES.md         ← metrics, claims, Never Claim
│   ├── auditor-prompt.md     ← second-pass FAIL-only review
│   └── feedback-log.md       ← log failures over time
│
├── gpt/                      ← paste these into ChatGPT GPT Builder
│   ├── system-prompt.md      ← Configure → Instructions (main prompt)
│   ├── work-experience.md    ← master context block
│   ├── per-project-keywords.md
│   └── projects/             ← one file per portfolio project (6 total)
│       ├── hearloop.md
│       ├── seo-audit-engine.md
│       ├── crypto-market-simulator.md
│       ├── distributed-caching.md
│       ├── fake-review-detector.md
│       └── youtube-ads-compliance-pipeline.md
│
├── templates/
│   ├── main.tex              ← Full Stack (default); LaTeX template for GPT/Overleaf
│   └── variants/
│       ├── fullstack-engineer.tex   ← Full Stack JD tailoring base
│       ├── backend-faang.tex
│       └── ai-engineer-faang.tex
│
├── prompts/                  ← auxiliary prompts (not the main GPT)
│   ├── application-answers.md
│   ├── linkedin-connection-note.md
│   ├── networking.md
│   └── system-prompt-patch.md
│
├── reference/                ← read-only guides (do not paste into GPT)
│   ├── headless-headhunter.md
│   └── humanizer.md
│
├── applications/
│   └── README.md             ← hub: short portal question answers
│
├── networking/
│   ├── README.md             ← hub: connection note + script library
│   ├── candidate-profile.md  ← metrics for outreach (synced from gpt/)
│   └── scripts.md            ← LinkedIn / outreach message templates
│
├── .cursor/skills/
│   ├── application-answers/SKILL.md
│   └── linkedin-connection-note/SKILL.md
│
├── handoffs/                 ← agent session notes between Cursor chats
│   └── 2026-06-05-youtube-compliance.md
│
├── golden-jds/               ← regression test job descriptions (3 lanes)
│   ├── README.md
│   ├── full-stack-software-engineer.md
│   ├── backend-software-engineer.md
│   └── ai-software-engineer.md
│
├── _vendor/                  ← third-party repos (not part of workflow)
│   └── skills-main/
│
└── Resume+Template.pdf       ← compiled reference PDF
```

---

## Daily workflow

1. **Tailor a resume** — paste a JD into your Custom GPT (built from `gpt/system-prompt.md` + master context).
2. **Compile** — copy changed LaTeX sections into Overleaf using `templates/main.tex`.
3. **Edit project truth** — update files in `gpt/projects/` when a repo changes; re-paste into GPT Builder.
4. **Check keywords** — use `gpt/per-project-keywords.md` for project order and role coverage.

---

## GPT Builder setup (one-time / after edits)

Paste into **Configure → Instructions** in this order:

| Block | Source file |
|-------|-------------|
| System prompt | `gpt/system-prompt.md` |
| Work Experience | `gpt/work-experience.md` |
| Projects | all 6 files in `gpt/projects/` (concatenate) |
| LaTeX template | `templates/main.tex` (Full Stack default) |
| **Locked Full Stack template (do not edit)** | `governance/FULL_STACK_TEMPLATE.md` · `templates/main.tex` |
| **Tailor Full Stack to a JD** | `templates/variants/fullstack-engineer.tex` · `.cursor/skills/fullstack-resume-tailor/` |
| **Pre-built FAANG lane resumes** | `templates/variants/fullstack-engineer.tex` · `backend-faang.tex` · `ai-engineer-faang.tex` |

Skills list lives inside `gpt/system-prompt.md` already.

---

## Quick lookup

| I need… | Go to… |
|---------|--------|
| Bullet rules (What/How/Where/Why) | `CONTEXT.md` §4–5 |
| **JD tailoring contract** | `governance/OUTPUT_CONTRACT.md` |
| **Before you accept GPT output** | `governance/DEFINITION_OF_DONE.md` |
| Which 4 projects per role | `gpt/per-project-keywords.md` |
| Locked resume bullets | each file in `gpt/projects/` |
| Work experience LaTeX | `gpt/work-experience.md` |
| Recruiter framework | `reference/headless-headhunter.md` |
| De-AI prose when editing MDs | `reference/humanizer.md` |
| **LinkedIn connection note (300 chars)** | `prompts/linkedin-connection-note.md` or `networking/README.md` |
| **Application questions (short answers)** | `prompts/application-answers.md` or `applications/README.md` |
| Outreach / networking (20 scripts) | `prompts/networking.md` · `networking/scripts.md` |
| Pending agent tasks | `handoffs/` (latest file) |
| Regression test JDs | `golden-jds/` |

---

## Path migration (June 2026)

| Old path | New path |
|----------|----------|
| `gpt_system_prompt.md` | `gpt/system-prompt.md` |
| `work_experience.md` | `gpt/work-experience.md` |
| `Per-Project Keyword.md` | `gpt/per-project-keywords.md` |
| `Projects/*.md` | `gpt/projects/*.md` (kebab-case names) |
| `main.tex` | `templates/main.tex` |
| `networking_system_prompt.md` | `prompts/networking.md` |
| `SCRIPTS.md` | `networking/scripts.md` |
| `Headless Headhunter.md` | `reference/headless-headhunter.md` |
| `skills-main/Humanizer.md` | `reference/humanizer.md` |
| `HANDOFF_2026-06-05.md` | `handoffs/2026-06-05-youtube-compliance.md` |

---

## JD paste shortcut

```
Tailor per governance/OUTPUT_CONTRACT.md
```
