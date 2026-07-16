# Full Stack Resume Template — LOCKED

> **Status:** Locked June 2026 by user directive.  
> **Canonical file:** `templates/main.tex`  
> **Lane:** Full Stack Software Engineer (also used when header title is **Software Engineer**)

---

## Rule

**Do not edit `templates/main.tex`** unless the user explicitly requests a change in chat.

This includes:

- Typography (Arial, font sizes, line spacing)
- Header layout (Software Engineer, two-row contact)
- Education line format
- Project order, bullet count, and bullet text
- Experience bullets
- Skills rows
- LaTeX preamble macros and spacing

---

## Full Stack project order (this template)

| # | Project | Bullets |
|---|---------|---------|
| 1 | Hearloop | 3 |
| 2 | SEO Audit Engine | 2 |
| 3 | Crypto Market Simulator | 2 |
| 4 | Video Compliance Pipeline | **1** (trim ladder) |

---

## JD tailoring workflow

For Full Stack JDs:

1. **Base template:** `templates/variants/fullstack-engineer.tex` (agent reads this; outputs **changed LaTeX sections only**).
2. **Locked canonical:** `templates/main.tex` — do not edit unless user updates the lock.
3. **Agent skill:** `.cursor/skills/fullstack-resume-tailor/SKILL.md`
4. **Contract:** `governance/OUTPUT_CONTRACT.md` (Project Selection → Fact Check → changed sections).
5. Application answers: use the `.tex` actually submitted for that role (`prompts/application-answers.md`).

When user says “tailor for full stack,” start from `fullstack-engineer.tex`, not `main.tex`.

---

## Related files

| File | Role |
|------|------|
| `templates/main.tex` | **Locked** Full Stack canonical template |
| `templates/variants/fullstack-engineer.tex` | **Tailoring base** for Full Stack JDs |
| `templates/main-one-page.tex` | Mirror of locked `main.tex` |
| `templates/variants/backend-faang.tex` | Backend lane (separate) |
| `templates/variants/ai-engineer-faang.tex` | AI Engineer lane (separate) |
| `gpt/per-project-keywords.md` | Project order reference for GPT |

---

## Compiler

XeLaTeX or LuaLaTeX (Arial via `fontspec`).
