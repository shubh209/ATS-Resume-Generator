# ATS Resume Generator

Repeatable system for JD-tailored, ATS-friendly LaTeX resumes, plus the career tools around them (LinkedIn notes, application answers, interview prep).

> **CURRENT LIVE ENTRY POINT:** `.agents/skills/resume-tailor/SKILL.md`. Its three lane templates under `resume-system/templates/variants/` are the only live resume-generation bases.

---

## Directory map

```
ATS Resume Generator/
├── README.md                 ← you are here
├── AGENTS.md · CLAUDE.md     ← per-tool entry pointers to the resume-tailor skill
│
├── resume-system/            ← the live tailoring pipeline
│   ├── facts/                ← current work and project masters (source of truth)
│   │   ├── work-experience.md
│   │   ├── per-project-keywords.md
│   │   └── projects/         ← seven project masters; only valid locked banks are selectable
│   │       ├── hearloop.md · seo-audit-engine.md · crypto-market-simulator.md
│   │       ├── distributed-caching.md · fake-review-detector.md
│   │       └── youtube-ads-compliance-pipeline.md · ClusterOps.md
│   ├── governance/           ← fact and audit rules
│   │   ├── FACT_RULES.md · auditor-prompt.md · feedback-log.md
│   ├── templates/variants/   ← lane templates (fullstack / backend / ai-engineer + non-live extras)
│   └── reference/            ← jd-red-flags.md (read during tailoring)
│
├── career-tools/             ← human-facing systems around the resume
│   ├── linkedin/             ← connection-note prompt, candidate-profile, scripts
│   ├── networking/           ← broad outreach prompt + README
│   ├── application-answers/  ← short application-answer prompt
│   ├── cover-letters/        ← (planned) cover-letter system
│   ├── discovery/            ← experience-discovery interview prompt
│   ├── interview/            ← interview-prep prompts and roadmaps
│   └── reference/            ← headless-headhunter.md, humanizer.md
│
├── career-stories/           ← deep master-story files, one per role
│   ├── DigitalAidSeattle.md · eInfochips.md
│   └── _drafts/              ← unverified draft bullets, never a source of truth
│
├── golden-jds/               ← regression-test job descriptions
│
├── tests/                    ← test_resume_preflight.py (preflight regression suite)
├── docs/                     ← superpowers plans/specs
├── archive/                  ← non-system material (Amazon-LP, old audits, old PDFs)
└── _vendor/                  ← third-party repos (not part of workflow)
```

---

## Live workflow

1. Provide the JD and request resume tailoring.
2. Follow `.agents/skills/resume-tailor/SKILL.md`.
3. Start from the lane template it selects under `resume-system/templates/variants/`.
4. Run `.agents/skills/resume-tailor/scripts/preflight.py` before completion.

---

## Quick lookup

| I need… | Go to… |
|---------|--------|
| **JD tailoring contract** | `.agents/skills/resume-tailor/SKILL.md` |
| **Validation** | `.agents/skills/resume-tailor/scripts/preflight.py` |
| Bullet and fact rules | `resume-system/governance/FACT_RULES.md` |
| Locked resume bullets | each file in `resume-system/facts/projects/` |
| Work experience LaTeX | `resume-system/facts/work-experience.md` |
| Lane templates | `resume-system/templates/variants/` |
| JD red flags | `resume-system/reference/jd-red-flags.md` |
| Recruiter framework | `career-tools/reference/headless-headhunter.md` |
| De-AI prose when editing MDs | `career-tools/reference/humanizer.md` |
| **LinkedIn connection note (300 chars)** | `career-tools/linkedin/linkedin-connection-note.md` |
| **Application questions (short answers)** | `career-tools/application-answers/application-answers.md` |
| Outreach / networking | `career-tools/networking/networking.md` · `career-tools/linkedin/scripts.md` |
| Interview prep | `career-tools/interview/` |
| Regression test JDs | `golden-jds/` |
| Preflight regression tests | `tests/test_resume_preflight.py` |

---

## JD paste shortcut

```
Tailor using .agents/skills/resume-tailor/SKILL.md
```
