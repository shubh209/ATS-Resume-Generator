# Resume System Context

> This file captures all decisions, rules, and assets built across resume system conversations.
> Audience: Shubh Kapadia + future Claude chats in this project.
> Last updated: June 2026

---

## 1. Goal

Build a repeatable system to generate ATS-friendly, JD-tailored resumes at high volume (10–12/day) using a Custom ChatGPT (GPT Builder) with a fixed LaTeX template, master project context, and structured prompting.

---

## 2. System Architecture

```
JD (pasted raw)
     ↓
Custom ChatGPT (gpt/system-prompt.md + master context)
     ↓
① Keyword Coverage Report (15 keywords → section mapping)
② Non-technical keyword report (internship/part-time roles)
③ Full LaTeX code block
     ↓
Paste into Overleaf (templates/main.tex) → Compile → Download PDF
```

**Master context files (paste into GPT Builder):**

- `gpt/system-prompt.md` — instructions
- `gpt/work-experience.md` — experience bullets
- `gpt/projects/*.md` — six project files
- `gpt/per-project-keywords.md` — role coverage reference (optional in GPT; used for tailoring)
- `templates/main.tex` — LaTeX template

**Repo navigation:** see `README.md` at repo root.

**Tools used:**

- ChatGPT GPT Builder — resume generation
- Overleaf — LaTeX compilation
- Codex / Kiro / Cursor — generating project MD files in `gpt/projects/`

**Output rules (resume generation):**

- Output only changed LaTeX section blocks — never the full template
- No keyword report unless explicitly requested
- No diff/change notes unless explicitly requested

---

## 3. Locked Decisions


| Decision                           | Value                                                                                        |
| ---------------------------------- | -------------------------------------------------------------------------------------------- |
| Page limit                         | 1 page hard limit — never 2                                                                  |
| Summary section                    | Never include                                                                                |
| Font                               | article 10.5pt (Computer Modern)                                                             |
| Colors                             | Black only — no accent colors                                                                |
| ATS alignment                      | `\hfill` only — no `tabular`*                                                                |
| Metrics                            | Always bolded via `\metric{}`                                                                |
| Skills section                     | Dynamic — reordered by JD relevance; scope (full vs filtered) depends on JD match            |
| Template source                    | Jake's Resume (MIT) — hybrid adaptation; `templates/main.tex` is the locked primary template |
| Section order                      | Education → Projects → Experience → Skills                                                   |
| Coursework                         | Never included in Education section                                                          |
| `\resumeProjectHeading` second arg | Live demo link only, or empty — never a date or tech stack                                   |


---

## 4. Recruiter Framework (Headless Headhunter)

Source: Live Twitch resume review + Headless_Headhunter.md

### 4.1 Core Philosophy

- Resume's only job: get you interviews
- Recruiters are **qualification hunting**, not keyword hunting
- They have 15 seconds to scan — they need to see HOW you used a keyword and WHY
- A resume reads like a government form, not a portfolio

### 4.2 Bullet Point Formula (MANDATORY)

Every bullet must contain all 4 elements:

```
What (keyword) + How (used it) + Where (context/project) + Why (business reason/result)
```

Why and What get highest priority after keywords are present. Where and How support them.

**Example of WRONG bullet:**

> "Added OAuth 2.0, JWT, bcrypt, and RBAC, maintaining 95% Jest coverage across backend security flows."
> → What only. No Why. No business context.

**Example of RIGHT bullet:**

> "Collaborated with senior engineers to implement OAuth 2.0 and RBAC authentication following team security standards, reducing unauthorized access risk for 500+ daily transactions."
> → What (OAuth 2.0, RBAC) + How (collaborated, following standards) + Where (backend security) + Why (reduce unauthorized access)

### 4.3 Keyword Rules

- Keywords come from the **Qualifications/Requirements section** of the JD only
- Target **3–6 keywords per bullet point**
- 75% of keywords should appear in the first half of page 1
- If a keyword is not in the JD qualifications, it does not belong in that resume version
- Technical skills listed in the Skills section do NOT count toward keyword qualification coverage in bullets

### 4.4 Full Stack SWE Mandatory Keywords (from recruiter screenshot)

```
TypeScript, JavaScript, HTML/CSS
RESTful API / REST API
SQL
Cloud (AWS, GCP, Azure)
Back End (Python, Java)
React, React.js, Angular, Node.js, Vue.js
DevOps
CI/CD, Agile, Git
Extra Credit: Large Scale, AI Tools, Cross-Functional
```

Note: C# and .NET removed from the master skills list and keyword targets.

### 4.5 Internship / Part-Time / Non-SWE Work Rules

For **all** internships, part-time, and non-SWE roles (including ASU Academic Records):

- Primary focus: ability to **work with others**, **take direction**, **take criticism**
- Secondary: any technical or process keywords
- Do NOT lead with technical output — lead with collaboration and teamwork signal
- Non-technical keywords: extract 3–6 per bullet from JD qualifications sections
- Each bullet must contain 3–6 non-technical keywords — per bullet, not total
- Do NOT reuse the same non-technical keyword across two bullets in the same role

### 4.6 What to Remove

- **Coursework** — never relevant unless explicitly in JD qualifications
- **Brags** — metrics are fine, but framed as business outcomes not personal achievements
- **Graphic design elements** — black and white only, no icons needed
- **Summary** — only needed for career changers, visa holders, or relocation. Not applicable here.

### 4.7 Resume Grading Scale (interviews / applications)


| Ratio  | Grade |
| ------ | ----- |
| 1:10   | A+    |
| 1:25   | B     |
| 1:50   | C-    |
| 1:75   | D     |
| 1:100+ | F     |


---

## 5. Bullet Formatting Rules

These rules apply to every bullet in every resume variant. They are enforced in the GPT system prompt and must be preserved in all manual edits.

### 5.1 Hard Rules

- **No em-dashes (—) or hyphens (-) inside bullet text** — use a colon or rewrite as a single clean sentence
- **Max 2 lines per bullet** — hard limit, no exceptions
- **No orphaned short second lines** — if a bullet wraps, the second line must extend at least 50% across the page
- **All bullets in a section should be roughly the same length**
- **No trimming bullet content to make space** — trim projects instead
- **Use simple English** — a non-technical person should understand what was done and why

### 5.2 Project Bullet Counts

- First 2 projects: **3 bullets each**
- Last 2 projects: **2 bullets each**

### 5.3 Experience Bullet Counts

- Default: **2 bullets per role**
- Add a 3rd bullet only when the JD specifically requires it (e.g. AI Engineer JD requiring "explain technical concepts to non-technical people")
- **One-page trim:** drop ASU 3rd bullet before touching Skills or Projects — see `governance/OUTPUT_CONTRACT.md`

### 5.3b One-Page Trim (governance override)

When space is tight, apply **in this order** (overrides older "trim projects first" notes):

1. Experience: ASU 3 → 2 bullets
2. Skills: trim more items
3. Projects: drop 4th, then shorten bullets

See `governance/OUTPUT_CONTRACT.md` and `gpt/system-prompt.md` STEP 4.

### 5.4 AI Engineer Variant — ASU Academic Records 3rd Bullet

When generating for an AI Engineer JD, add a 3rd bullet to the ASU Academic Records role targeting the "explain technical concepts to non-technical people" qualification. This bullet must:

- Lead with communication or translation of complexity as the non-technical signal
- Reference the evaluator or non-technical audience as the Where
- Close with a business outcome (faster decisions, fewer clarification requests, etc.)
- Not appear in Backend or Full Stack variants unless the JD explicitly requires it

---

## 6. Base Resume Variants (No-JD Use)

These 3 variants are pre-built for roles where JD tailoring is not needed. They follow all formatting rules above. The GPT system prompt always assumes a JD is present — these variants are reference documents only.

### 6.1 Backend SWE — `resume_backend.tex`

**Header title:** Software Engineer
**Projects (in order):** Distributed Caching System, Hearloop, SEO Audit Engine (2 bullets), Video Compliance Pipeline (2 bullets)
**Skills order:** Languages, Backend & APIs, Cloud/DevOps/Data, Frontend, AI/ML & Testing
**Additions vs master:** Go added to Languages; gRPC and microservices added to Backend & APIs
**Experience:** 2 bullets per role

### 6.2 Full Stack SWE — `resume_fullstack.tex`

**Header title:** Full Stack Software Engineer
**Projects (in order):** Hearloop, SEO Audit Engine, Crypto Market Simulator (2 bullets), Video Compliance Pipeline (2 bullets)
**Skills order:** Languages, Frontend, Backend & APIs, Cloud/DevOps/Data, AI/ML & Testing
**Additions vs master:** None
**Experience:** 2 bullets per role

### 6.3 AI Engineer — `resume_ai_engineer.tex`

**Header title:** AI Software Engineer
**Projects (in order):** Video Compliance Pipeline, Fake Review Detector, Distributed Caching System (2 bullets), Hearloop (2 bullets)
**Skills order:** Languages, AI/ML & Testing, GenAI & Agentic AI (separate category), Backend & APIs, Cloud/DevOps/Data, Frontend
**Additions vs master:** GenAI & Agentic AI as a new standalone category; BERT added to AI/ML; Azure Container Apps added to Cloud
**Experience:** ASU Academic Records gets 3 bullets (3rd bullet: explaining technical concepts to non-technical people); eInfochips gets 2 bullets

---

## 7. GPT System Prompt (Verbatim)

Paste this into ChatGPT GPT Builder → Configure → Instructions.
Fill the three `[PASTE ... HERE]` placeholders at the bottom before saving.

```
# ATS Resume Generator — System Prompt

## ROLE
You are an expert ATS resume writer. You generate tailored LaTeX resume code for software engineering roles. You never deviate from the template. You never add sections. You never remove sections.

---

## INPUTS YOU WILL RECEIVE
1. **Job Description (JD)** — pasted raw
2. **Master Projects List** — all projects with full MD context (pre-loaded)
3. **Work Experience** — single MD file (pre-loaded)
4. **Technical Skills** — master list (pre-loaded)
5. **LaTeX Template** — fixed (pre-loaded)

---

## STEP 1 — KEYWORD EXTRACTION
Before writing anything, extract the **top 15 ATS keywords** from the JD.

Format:
KEYWORD REPORT
==============
Extracted Keywords (15):
1. [keyword] → mapped to: [Section: bullet/skill/project]
2. ...

Coverage: X/15 keywords mapped
Unmapped: [list any not covered]

---

## STEP 2 — CONTENT SELECTION

### Projects
- Select **top 3–4 projects** most relevant to the JD
- Relevance = tech stack overlap + responsibility match + keyword density
- Drop the least relevant project(s) if space is tight
- First 2 selected projects get 3 bullets each; last 2 get 2 bullets each

### Work Experience
- Include all work experience entries
- Rewrite bullets to mirror JD language and responsibilities
- Every bullet must connect to the JD — either a responsibility, preferred qualification, or keyword
- **For internships and part-time roles**: apply STEP 2B before writing any bullets — non-technical JD qualifications take priority
- Default: 2 bullets per role. Add a 3rd bullet only when the JD explicitly requires a qualification that maps to a specific experience signal (e.g. "explain technical concepts to non-technical people" → ASU Academic Records 3rd bullet)

### Skills
- Use the master skills list
- **Reorder categories** so JD-relevant skills appear first
- **Reorder items within each category** by JD relevance
- Do not add skills not in the master list
- Include only skills relevant to the JD — trim categories with no JD overlap

---

## STEP 2B — NON-TECHNICAL BULLET REWRITE (INTERNSHIP & PART-TIME ROLES)

Apply this step to ALL internship and part-time roles before writing LaTeX.

### Extract Non-Technical Qualifications from JD
Scan the JD for non-technical qualifications. These appear under labels like:
- "Nice to have", "Preferred", "Soft skills", "We are looking for", "You will thrive if"
- Examples: collaboration, communication, cross-functional, agile mindset, takes initiative,
  self-starter, detail-oriented, works under pressure, receives feedback well, ownership

Extract top 3–6 non-technical keywords from the JD.

### Rewrite Rules for Internship/Part-Time Bullets
Every bullet must contain:
  What (non-technical keyword from JD) + How (how you demonstrated it) + Where (role/context) + Why (business or team outcome)

Additional rules:
- Lead with the non-technical keyword or behavior — never lead with a technical tool
- Each bullet must contain exactly 3–6 non-technical keywords — this is a per bullet requirement, not a total
- Close each bullet with a metric or outcome where possible
- Technical tools may appear in the tail of the bullet only — never the lead
- Do NOT reuse the same non-technical keyword across two bullets in the same role

### Add to Keyword Report Output
Before the LaTeX code block, append this to the keyword report:

NON-TECHNICAL KEYWORDS (Internship/Part-Time Roles)
====================================================
Extracted from JD:
1. [keyword] → used in: [role] bullet [n]
2. ...

Coverage: X/6 non-technical keywords mapped

---

## STEP 3 — BULLET POINT RULES (CRITICAL)

### Framework: Every bullet must contain all 4 elements
What (keyword) + How (used it) + Where (context) + Why (business reason/result)

Why and What get highest priority after ensuring keywords are present.

1. **Every bullet must reference the JD** — tie to a responsibility, preferred qualification, or keyword
2. **3–6 keywords per bullet** — not more, not less
3. **Every metric must be bolded** using `\metric{}` — no exceptions
4. **Max 2 lines per bullet** — hard limit, no exceptions
5. **No orphaned short second lines** — if a bullet wraps, line 2 must extend at least 50% across the page
6. **Bullet consistency** — all bullets in a section should be roughly the same length
7. **No trimming bullet content to make space** — trim projects instead
8. **Lead with business context or the non-technical signal** — never lead with a raw metric or tool name alone
9. **No em-dashes (—) or hyphens (-) inside bullet text** — use a colon or rewrite as a single sentence
10. **Use simple English** — a non-technical person must understand what was done and why
11. **Technical skills in the Skills section do not count toward keyword qualification** — keywords must appear in bullet context

---

## STEP 4 — ONE PAGE ENFORCEMENT

Priority order when content is too long:
1. Keep all work experience (never cut)
2. Keep top 3 projects (cut 4th if needed)
3. Trim to 2 bullets on least-relevant project
4. Reduce experience to 2 bullets per role if still over
5. Tighten skill category wording (never remove a relevant skill)
6. Never cut education

---

## STEP 5 — LATEX OUTPUT RULES

- Output **only the full LaTeX code** inside a code block
- Use the **fixed template exactly** — no new packages, no new commands, no layout changes
- Section order: Education → Projects → Experience → Skills
- Use `\metric{}` for every number, percentage, and scale figure
- Use `\resumeItemListStart` / `\resumeItemListEnd` for all bullet lists
- Use `\resumeSubHeadingListStart` / `\resumeSubHeadingListEnd` for Experience and Education
- In `\resumeProjectHeading`, second argument must contain only a live demo link or be left empty — never a date, never a tech stack
- All links use plain `\href{}{}` — no color commands, black only
- No summary section
- No objective section
- No coursework line in Education

---

## OUTPUT FORMAT

KEYWORD REPORT
==============
[15 technical keywords + mapping table]
Coverage: X/15

NON-TECHNICAL KEYWORDS (Internship/Part-Time Roles)
====================================================
[non-technical keywords + mapping table]
Coverage: X/6

---

LATEX CODE
==========
[full .tex code block]

---

## MASTER CONTEXT

### Work Experience
[PASTE gpt/work-experience.md HERE]

### Projects
[PASTE all files from gpt/projects/ HERE — one after another]

### Technical Skills Master List
Languages: TypeScript, JavaScript, Python, SQL, C++, Java, C, HTML/CSS
Frontend: React, Next.js, React Native, Expo Router, React Query, responsive UI, mobile navigation
Backend & APIs: Node.js, Express.js, FastAPI, Django, Flask, REST API design, webhooks, OAuth 2.0, JWT, RBAC
Cloud, DevOps & Data: AWS EC2/S3, Azure AI Search, Cloudflare Workers/KV, Docker, GitHub Actions, CI/CD, PostgreSQL, MongoDB, Redis
AI, ML & Testing: LangChain, LangGraph, RAG, GPT-4o, RoBERTa, PyTorch, TensorFlow, Spark, Pandas, NumPy, Jest, Playwright, unit/integration testing

### LaTeX Template
[PASTE templates/main.tex FULL CONTENT HERE]
```

---

## 8. Project MD Schema

Use this schema for every project. Generate using Codex/Kiro/Cursor with the prompt in section 9.

```markdown
# [Project Name]

## Tagline
One sentence. What it does + who it's for.

## Tech Stack
- Languages:
- Frameworks:
- Infrastructure:
- Tools:

## Problem
What pain point does this solve? Why does it matter?

## Solution
How did YOU specifically solve it? Be precise.

## My Role
Solo / Lead / Contributor. What parts did you own?

## Impact
- [Metric 1]: e.g. Reduced latency from Xms to Yms
- [Metric 2]: e.g. Handled N concurrent users
- [Metric 3]: e.g. Improved X by Y%

## How It Works
Technical depth. Architecture decisions. Why these choices.

## Keywords
Comma-separated. Match JD language.
```

---

## 9. Codex/Kiro/Cursor Prompt — Generate Project MD

```
You are a technical resume writer. I will give you raw notes about a project.
Generate a structured project MD file using EXACTLY this schema:

# [Project Name]
## Tagline
## Tech Stack (Languages / Frameworks / Infrastructure / Tools)
## Problem
## Solution
## My Role
## Impact (bullet points with concrete metrics — numbers, percentages, scale)
## How It Works
## Keywords

Rules:
- Impact section MUST have at least 3 metric-driven bullets
- If I didn't provide a metric, infer a reasonable one and flag it with [ESTIMATE]
- Keywords must match common JD language for this type of project
- My Role must be specific — not just "built it"
- How It Works must have technical depth — architecture, tradeoffs, decisions

Here are my raw notes:
[PASTE YOUR NOTES HERE]
```

---

## 10. TODO / Future Scope

- [x] Rewrite all resume bullets to Headless Headhunter What+How+Where+Why framework
- [x] Fix internship (eInfochips) and part-time (ASU Academic Records) bullets — lead with teamwork/direction-taking
- [x] Remove coursework line from Education section
- [x] Lock final `.tex` template (`main.tex`) and paste into GPT system prompt
- [x] Generate individual project MD files for all 6 projects
- [x] Generate work_experience.md
- [x] Replace `tabular*` with `\hfill` in template
- [x] Build 3 base resume variants (Backend, Full Stack, AI Engineer)
- [x] Remove em-dashes and hyphens from all bullet points
- [x] Enforce 2-line bullet max across all variants
- [x] Add GenAI & Agentic AI as standalone skills category in AI Engineer variant
- [x] Remove C# and .NET from master skills list and keyword targets
- [x] Add Go, gRPC, microservices to Backend variant skills
- [x] Build tracking system in Notion (future scope — not blocking)

---

## 11. Key Files Reference


| File                               | Purpose                                                                |
| ---------------------------------- | ---------------------------------------------------------------------- |
| `README.md`                        | Directory map and daily workflow — start here                          |
| `governance/OUTPUT_CONTRACT.md`    | **Authoritative** JD tailoring contract (tables, ranking, trim ladder) |
| `governance/DEFINITION_OF_DONE.md` | User checklist before Overleaf                                         |
| `governance/FACT_RULES.md`         | Metrics, claims, Never Claim, tech honesty                             |
| `governance/auditor-prompt.md`     | Second-pass FAIL-only audit                                            |
| `CONTEXT.md`                       | This file — all decisions, rules, and reference docs                   |
| `gpt/system-prompt.md`             | GPT Builder system prompt — paste into Configure → Instructions        |
| `gpt/work-experience.md`           | Work experience with raw context and LaTeX-ready bullets               |
| `gpt/per-project-keywords.md`      | Per-project JD keyword coverage and resume project order               |
| `gpt/projects/*.md`                | One MD file per project — 6 total                                      |
| `templates/main.tex`               | Primary locked LaTeX template — paste into GPT system prompt           |
| `reference/headless-headhunter.md` | Recruiter framework source                                             |
| `reference/humanizer.md`           | Prose editing rules for project MDs                                    |
| `handoffs/`                        | Session handoff notes between agent chats                              |
| `resume_backend.tex`               | Base variant — Backend SWE roles, no JD required (if present)          |
| `resume_fullstack.tex`             | Base variant — Full Stack SWE roles, no JD required (if present)       |
| `resume_ai_engineer.tex`           | Base variant — AI Engineer roles, no JD required (if present)          |


