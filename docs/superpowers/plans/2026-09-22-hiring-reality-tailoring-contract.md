# Hiring Reality and Tailoring Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the user's hiring assumptions and role keyword profiles persistent inputs to resume tailoring while making the tailoring report strictly opt-in.

**Architecture:** Two read-only reference files own market assumptions and role-profile vocabulary; verified candidate facts remain isolated in the existing fact masters. The live skill consumes both references, performs evidence checks internally, and exposes only the tailored resume unless a report is explicitly requested. Preflight protects the new read-set and output-contract invariants.

**Tech Stack:** Markdown, Python 3 standard library, `unittest`; LaTeX templates remain unchanged

**Spec:** `docs/superpowers/specs/2026-09-22-hiring-reality-tailoring-contract-design.md`

## Global Constraints

- Treat the user's September 2026 hiring statements as authoritative operating assumptions for this repository.
- Do not add external-source caveats or re-litigate those assumptions during a live tailoring run.
- Do not modify locked bullets, project facts, metrics, or files under `resume-system/templates/variants/`.
- Do not add the excluded evidence rules for production, scale, cross-functional work, technical communication, AI tooling, or MLOps.
- Do not add PDF extraction or `pdftotext` validation.
- Keep the existing DIRECT, TRANSFERABLE, ADJACENT, and GAP protections.
- Default output is the tailored resume only; a tailoring report is produced only when explicitly requested.
- A saved normal run contains `job-description.md` and `resume.tex`; `tailoring-report.md` is conditional on an explicit report request.
- Preserve all unrelated user changes in the dirty worktree.

## Review Focus

- A plain tailoring request must not emit a report, selection table, fact-check table, gaps table, or validation summary; Task 2 pins this in contract tests.
- An explicit report request must still resolve to the existing report schema and permit a third saved file; Task 2 pins this in skill and schema tests.
- Removing either market reference, or removing either reference from the live skill read set, must fail preflight; Tasks 1 and 2 pin both cases.
- The three supplied role profiles must remain guidance rather than candidate-fact authority; Tasks 1 and 3 test the headings and non-authority language.
- The auditor must use three-priority placement and must not retain the fixed 75% keyword rule; Task 3 tests the required and forbidden text.

---

### Task 1: Add persistent hiring and qualification references

**Files:**
- Create: `resume-system/reference/hiring-reality.md`
- Create: `resume-system/reference/qualification-taxonomy.md`
- Modify: `.agents/skills/resume-tailor/scripts/preflight.py`
- Modify: `tests/test_resume_preflight.py`

**Interfaces:**
- Consumes: The approved design spec and the existing `REQUIRED_FILES` preflight contract.
- Produces: Two immutable reference paths that the live skill and later contract tests can consume.

- [ ] **Step 1: Create complete reference fixtures and write failing tests**

Create both reference files with the Step 3 content, add both paths to `FIXTURE_PATHS`, and add:

```python
    def test_rejects_missing_hiring_reality_reference(self) -> None:
        fixture = self.make_fixture()
        (fixture / "resume-system/reference/hiring-reality.md").unlink()
        result = self.run_preflight(fixture)
        self.assert_rejected(result, "a missing hiring-reality reference")

    def test_rejects_missing_qualification_profile(self) -> None:
        fixture = self.make_fixture()
        path = fixture / "resume-system/reference/qualification-taxonomy.md"
        content = path.read_text(encoding="utf-8").replace(
            "## Go / Node.js Engineer",
            "## Backend Profile Removed",
        )
        path.write_text(content, encoding="utf-8")
        result = self.run_preflight(fixture)
        self.assert_rejected(result, "a taxonomy missing the Go / Node.js profile")
```

- [ ] **Step 2: Run the new tests and verify failure**

Run:

```bash
python3 -m unittest \
  tests.test_resume_preflight.ResumePreflightTest.test_rejects_missing_hiring_reality_reference \
  tests.test_resume_preflight.ResumePreflightTest.test_rejects_missing_qualification_profile -v
```

Expected: both fail because current preflight neither requires the references nor checks their headings.

- [ ] **Step 3: Populate the references**

Write `resume-system/reference/hiring-reality.md`:

```markdown
# Hiring Reality — Operating Assumptions

> Authoritative internal guidance supplied by the user. Apply it during tailoring. It is not a source of candidate facts and is not routine output.

## Application strategy
- Resume automation saves time; reinvest it in profile improvement, application-volume feedback, and networking.
- Referrals beat cold applications.
- The economy is in recession and the hiring market is the toughest it has been; roles that once took tens of applications may take hundreds.
- A resume must be in the top one percent of what the reviewer reads and surface the requested qualifications immediately.

## Qualification evidence
- A qualification needs WHAT, HOW, WHY, and WHERE.
- Skills sections and summaries do not count as qualification evidence because they lack WHERE.
- Use the posting's exact words when they truthfully describe verified experience.
- Never rely on implication for an explicitly requested qualification.
- Pair technical detail with a plain-English reason.
- Prefer concrete verbs and legible scale over vague language or context-free percentages.
- The first bullet of the most recent relevant role is the highest-value line.
- For students and interns, keep education near the top and prove teamwork, ability to take direction, and response to criticism alongside technical knowledge.

## ATS and recruiter behavior
- An ATS is primarily a filing cabinet with search and workflow features.
- The employer's configured knockout questions are the automatic rejection path.
- Applications commonly enter a list, recruiters search by literal keyword, skim the upper portion, and stop when they have enough candidates.
- Either a person opened the application and did not find the required qualification, or nobody opened it.
- No ATS calculates a universal resume match score. Consumer ATS scores are invented keyword-overlap diagnostics, not hiring probabilities or standards to beat.

## Format and application conventions
- Prefer one page below roughly five years of experience and allow two afterward.
- Use a single-column, plain, text-selectable PDF without photos or heavy graphics.
- Cover letters are low value for engineering roles unless requested.
- The exact six-second claim is invented precision, although skimming is real.
- Paid resume writers have no demonstrated outcome advantage.
- The LinkedIn Open to Work banner has no demonstrated positive or negative effect.
- Do not use hidden white text or tiny keyword stuffing.
- Read every knockout question carefully and apply early to fresh postings.
```

Write `resume-system/reference/qualification-taxonomy.md`:

```markdown
# Qualification Taxonomy — Role Profiles

> Authoritative market vocabulary supplied by the user. This file guides matching and tie-breaking but never authorizes a candidate fact, skill, metric, or resume claim.

## Full Stack Software Engineer
- Degree
- TypeScript, JavaScript, HTML, CSS
- RESTful API or REST API
- SQL; cloud using AWS, GCP, or Azure
- Backend using Python, C#/.NET, or Java
- React or React Native
- Git or GitHub
- CI/CD, Agile, DevOps
- Extra credit: AI tools, infrastructure user counts, cross-functional work
- Development tools such as Claude, Cursor, and GitHub Copilot

## Go / Node.js Engineer
- Degree and Agile
- Go/Golang, Fiber, Node.js, NestJS, SQL, MongoDB, Redis
- Cloud, CI/CD, Git, Kafka, RabbitMQ
- Docker and Kubernetes
- Additional language such as C#, C++, or Java
- OOP

## AI Engineer
- Degree, Python or another backend language, ML, and LLMs
- Cloud using GCP, Azure, or AWS; production systems; agentic systems or multi-agent systems
- Agentic coding using Claude Code, OpenAI Codex, or Cursor
- LangGraph, LangChain, Google ADK, or OpenAI Agents SDK
- Communicating technical details to a nontechnical audience
- MLOps, AI architectures, and AI orchestration
- Less common differentiators: industry experience, SQL, RAG, Git, and NumPy

## Literal wording variants
- Go / Golang
- REST API / RESTful API
- CI/CD / CICD
- Git / GitHub when the JD accepts either
```

- [ ] **Step 4: Add preflight reference validation**

Extend `REQUIRED_FILES` with both new paths, then add:

```python
REQUIRED_REFERENCE_HEADINGS = {
    "resume-system/reference/hiring-reality.md": (
        "## Application strategy",
        "## Qualification evidence",
        "## ATS and recruiter behavior",
        "## Format and application conventions",
    ),
    "resume-system/reference/qualification-taxonomy.md": (
        "## Full Stack Software Engineer",
        "## Go / Node.js Engineer",
        "## AI Engineer",
        "## Literal wording variants",
    ),
}
```

After required-file validation, add:

```python
    for relative, headings in REQUIRED_REFERENCE_HEADINGS.items():
        path = root / relative
        if not path.is_file():
            continue
        content = path.read_text(encoding="utf-8")
        for heading in headings:
            if heading not in content:
                errors.append(f"{relative} missing required heading: {heading}")
```

- [ ] **Step 5: Run Task 1 verification**

```bash
python3 -m unittest tests.test_resume_preflight -v
python3 .agents/skills/resume-tailor/scripts/preflight.py
```

Expected: all tests pass and preflight reports that deterministic sources satisfy invariants.

- [ ] **Step 6: Commit Task 1**

```bash
git add resume-system/reference/hiring-reality.md \
  resume-system/reference/qualification-taxonomy.md \
  .agents/skills/resume-tailor/scripts/preflight.py \
  tests/test_resume_preflight.py
git commit -m "feat: add hiring reality references"
```

---

### Task 2: Make tailoring reports explicitly opt-in

**Files:**
- Modify: `.agents/skills/resume-tailor/SKILL.md`
- Modify: `.agents/skills/resume-tailor/references/tailoring-report-schema.md`
- Modify: `.agents/skills/resume-tailor/scripts/preflight.py`
- Modify: `tests/test_resume_preflight.py`

**Interfaces:**
- Consumes: The references created by Task 1 and the existing report schema.
- Produces: A resume-only default contract with a preserved explicit-report path.

- [ ] **Step 1: Add skill contract files to test fixtures**

Add to `FIXTURE_PATHS`:

```python
    Path(".agents/skills/resume-tailor/SKILL.md"),
    Path(".agents/skills/resume-tailor/references/tailoring-report-schema.md"),
    Path("resume-system/governance/auditor-prompt.md"),
```

- [ ] **Step 2: Write failing contract tests**

```python
    def test_rejects_skill_without_hiring_reality_read_set(self) -> None:
        fixture = self.make_fixture()
        path = fixture / ".agents/skills/resume-tailor/SKILL.md"
        content = path.read_text(encoding="utf-8").replace(
            "5. `resume-system/reference/hiring-reality.md`\n",
            "",
        )
        path.write_text(content, encoding="utf-8")
        result = self.run_preflight(fixture)
        self.assert_rejected(result, "a live skill missing hiring reality from its read set")

    def test_rejects_skill_without_report_opt_in_contract(self) -> None:
        fixture = self.make_fixture()
        path = fixture / ".agents/skills/resume-tailor/SKILL.md"
        content = path.read_text(encoding="utf-8").replace(
            "Do not produce a tailoring report unless the user explicitly requests one.",
            "Always produce a tailoring report.",
        )
        path.write_text(content, encoding="utf-8")
        result = self.run_preflight(fixture)
        self.assert_rejected(result, "a live skill without report opt-in")

    def test_rejects_report_schema_without_opt_in_boundary(self) -> None:
        fixture = self.make_fixture()
        path = fixture / ".agents/skills/resume-tailor/references/tailoring-report-schema.md"
        content = path.read_text(encoding="utf-8").replace(
            "Use this schema only when the user explicitly requests a tailoring report.",
            "Use this schema for every tailoring run.",
        )
        path.write_text(content, encoding="utf-8")
        result = self.run_preflight(fixture)
        self.assert_rejected(result, "a report schema without its opt-in boundary")
```

- [ ] **Step 3: Run the contract tests and verify failure**

```bash
python3 -m unittest \
  tests.test_resume_preflight.ResumePreflightTest.test_rejects_skill_without_hiring_reality_read_set \
  tests.test_resume_preflight.ResumePreflightTest.test_rejects_skill_without_report_opt_in_contract \
  tests.test_resume_preflight.ResumePreflightTest.test_rejects_report_schema_without_opt_in_boundary -v
```

Expected: failures because the live skill still requires a report and omits the references.

- [ ] **Step 4: Update the live skill read set and priority handling**

Use this read-set order:

```markdown
1. `resume-system/governance/FACT_RULES.md`
2. `resume-system/facts/work-experience.md`
3. `resume-system/facts/per-project-keywords.md`
4. Every file in `resume-system/facts/projects/*.md`
5. `resume-system/reference/hiring-reality.md`
6. `resume-system/reference/qualification-taxonomy.md`
7. `resume-system/reference/jd-red-flags.md`
8. Exactly one lane template from the routing table below
```

After priority extraction, add:

```markdown
Classify relevant requirements internally as eligibility, technology, responsibility, collaboration, or optional tooling. Use the role profiles as vocabulary and tie-breaking context, never as authority for a candidate claim.

Place the strongest truthful evidence for the three priorities as early as the locked lane structure permits. Give special weight to the first bullet of the most recent relevant role. Do not change locked wording to force placement.
```

- [ ] **Step 5: Replace the output and completion contracts**

The new `## Output` must contain:

```markdown
Default: return only the complete tailored `resume.tex`, or only the specifically requested answer when the request is narrower than a resume.

Do not produce a tailoring report unless the user explicitly requests one. Do not append a selection table, fact-check table, gaps table, validation summary, or ATS explanation to the default response. Report an actual blocker, failed invariant, or material fact-integrity warning when necessary.
```

For saved output, require:

```markdown
- Always write `job-description.md` and `resume.tex`.
- Write `tailoring-report.md` only when the user explicitly requests a tailoring report.
```

Keep internal validation. Change completion so a default run completes when the tailored resume or requested answer is delivered after internal validation. Use the report schema only for explicit report requests.

- [ ] **Step 6: Mark the report schema opt-in**

Below its title, add:

```markdown
> Use this schema only when the user explicitly requests a tailoring report. Never append it to a default tailoring response.
```

- [ ] **Step 7: Add preflight contract validation**

Add:

```python
REQUIRED_CONTRACT_TEXT = {
    ".agents/skills/resume-tailor/SKILL.md": (
        "resume-system/reference/hiring-reality.md",
        "resume-system/reference/qualification-taxonomy.md",
        "Do not produce a tailoring report unless the user explicitly requests one.",
        "Write `tailoring-report.md` only when the user explicitly requests a tailoring report.",
    ),
    ".agents/skills/resume-tailor/references/tailoring-report-schema.md": (
        "Use this schema only when the user explicitly requests a tailoring report.",
    ),
}
```

Validate every snippet and emit `missing required contract text` on absence.

- [ ] **Step 8: Run Task 2 verification**

```bash
python3 -m unittest tests.test_resume_preflight -v
python3 .agents/skills/resume-tailor/scripts/preflight.py
```

Expected: all tests and preflight pass.

- [ ] **Step 9: Commit Task 2**

```bash
git add .agents/skills/resume-tailor/SKILL.md \
  .agents/skills/resume-tailor/references/tailoring-report-schema.md \
  .agents/skills/resume-tailor/scripts/preflight.py \
  tests/test_resume_preflight.py
git commit -m "feat: make tailoring reports opt in"
```

---

### Task 3: Align keyword mapping and auditor placement

**Files:**
- Modify: `resume-system/facts/per-project-keywords.md`
- Modify: `resume-system/governance/auditor-prompt.md`
- Modify: `.agents/skills/resume-tailor/scripts/preflight.py`
- Modify: `tests/test_resume_preflight.py`

**Interfaces:**
- Consumes: The qualification taxonomy and three-priority model.
- Produces: Project coverage vocabulary aligned to the supplied profiles and a priority-first audit rule.

- [ ] **Step 1: Write failing tests**

```python
    def test_rejects_fixed_keyword_percentage_in_auditor(self) -> None:
        fixture = self.make_fixture()
        path = fixture / "resume-system/governance/auditor-prompt.md"
        content = path.read_text(encoding="utf-8").replace(
            "The three JD priorities must appear in the earliest available truthful evidence allowed by the lane's locked structure.",
            "<75% JD keywords likely in first half of page 1",
        )
        path.write_text(content, encoding="utf-8")
        result = self.run_preflight(fixture)
        self.assert_rejected(result, "the retired fixed placement percentage")

    def test_rejects_keyword_map_that_authorizes_facts(self) -> None:
        fixture = self.make_fixture()
        path = fixture / "resume-system/facts/per-project-keywords.md"
        content = path.read_text(encoding="utf-8").replace(
            "This file does not authorize facts, metrics, skills, project counts, or selection",
            "This file authorizes facts, metrics, skills, project counts, and selection",
        )
        path.write_text(content, encoding="utf-8")
        result = self.run_preflight(fixture)
        self.assert_rejected(result, "a keyword map claiming fact authority")
```

- [ ] **Step 2: Run the new tests and verify failure**

```bash
python3 -m unittest \
  tests.test_resume_preflight.ResumePreflightTest.test_rejects_fixed_keyword_percentage_in_auditor \
  tests.test_resume_preflight.ResumePreflightTest.test_rejects_keyword_map_that_authorizes_facts -v
```

Expected: failures because neither contract is enforced yet.

- [ ] **Step 3: Replace the role keyword block**

Preserve the non-authority warning and replace `## Role Keyword Requirements (Reference)` with:

```markdown
## Role Qualification Profiles

The authoritative market profiles live in `resume-system/reference/qualification-taxonomy.md`:

- Full Stack Software Engineer
- Go / Node.js Engineer, routed through the Backend lane
- AI Engineer

Use the target JD for live priorities. Use this file only to map verified project evidence to that vocabulary.
```

Keep project tables and recommendations. Reconcile these misleading rows without editing any project master:

```markdown
| Fastify | Node.js backend framework (Full Stack, Go / Node.js) | REST API framework |
| React Native | React Native (Full Stack) | Mobile frontend framework |
| Hono | Backend framework (Full Stack, Go / Node.js) | Serverless REST API framework |
```

- [ ] **Step 4: Replace the auditor placement rule**

Use:

```markdown
**PLACEMENT** — The three JD priorities must appear in the earliest available truthful evidence allowed by the lane's locked structure. A supported priority is buried beneath less relevant evidence.
```

- [ ] **Step 5: Add required and forbidden preflight text**

Extend `REQUIRED_CONTRACT_TEXT`:

```python
    "resume-system/facts/per-project-keywords.md": (
        "This file does not authorize facts, metrics, skills, project counts, or selection",
        "resume-system/reference/qualification-taxonomy.md",
    ),
    "resume-system/governance/auditor-prompt.md": (
        "The three JD priorities must appear in the earliest available truthful evidence allowed by the lane's locked structure.",
    ),
```

Add and validate:

```python
FORBIDDEN_CONTRACT_TEXT = {
    "resume-system/governance/auditor-prompt.md": (
        "<75% JD keywords likely in first half of page 1",
    ),
}
```

Emit `contains forbidden contract text` when found.

- [ ] **Step 6: Run Task 3 verification**

```bash
python3 -m unittest tests.test_resume_preflight -v
python3 .agents/skills/resume-tailor/scripts/preflight.py
```

Expected: all tests and preflight pass.

- [ ] **Step 7: Commit Task 3**

```bash
git add resume-system/facts/per-project-keywords.md \
  resume-system/governance/auditor-prompt.md \
  .agents/skills/resume-tailor/scripts/preflight.py \
  tests/test_resume_preflight.py
git commit -m "feat: align qualification matching rules"
```

---

### Task 4: Document the live workflow

**Files:**
- Modify: `README.md`

**Interfaces:**
- Consumes: Final paths and behavior from Tasks 1–3.
- Produces: A discoverable maintainer entry point without runtime changes.

- [ ] **Step 1: Update the directory map**

```markdown
│   └── reference/            ← hiring-reality.md · qualification-taxonomy.md · jd-red-flags.md
```

- [ ] **Step 2: Update the live workflow**

Add:

```markdown
5. Return the tailored resume only. Produce a tailoring report only when the user explicitly asks for one.
```

- [ ] **Step 3: Update quick lookup**

```markdown
| Hiring-market operating assumptions | `resume-system/reference/hiring-reality.md` |
| Role qualification profiles | `resume-system/reference/qualification-taxonomy.md` |
| Optional tailoring-report schema | `.agents/skills/resume-tailor/references/tailoring-report-schema.md` |
```

- [ ] **Step 4: Verify documentation**

```bash
rg -n "hiring-reality|qualification-taxonomy|tailoring-report|resume only" README.md .agents/skills/resume-tailor/SKILL.md resume-system/reference
git diff --check -- README.md
```

Expected: new paths appear, the report is opt-in, and `git diff --check` prints nothing.

- [ ] **Step 5: Commit Task 4**

```bash
git add README.md
git commit -m "docs: document resume tailoring assumptions"
```

---

### Task 5: Verify the complete tailoring contract

**Files:**
- Verify only: files changed by Tasks 1–4

**Interfaces:**
- Consumes: The complete implementation.
- Produces: Verification evidence and no new interface.

- [ ] **Step 1: Run the full regression suite**

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Expected: all tests pass.

- [ ] **Step 2: Run live preflight**

```bash
python3 .agents/skills/resume-tailor/scripts/preflight.py
```

Expected: deterministic source invariants pass for every live lane.

- [ ] **Step 3: Check formatting and changed paths**

```bash
git diff --check HEAD~4..HEAD
git diff --name-only HEAD~4..HEAD
```

Expected implementation paths:

```text
.agents/skills/resume-tailor/SKILL.md
.agents/skills/resume-tailor/references/tailoring-report-schema.md
.agents/skills/resume-tailor/scripts/preflight.py
README.md
resume-system/facts/per-project-keywords.md
resume-system/governance/auditor-prompt.md
resume-system/reference/hiring-reality.md
resume-system/reference/qualification-taxonomy.md
tests/test_resume_preflight.py
```

Pre-existing dirty files may still appear in `git status`; do not stage, restore, or modify them.

- [ ] **Step 4: Inspect the final contract diff**

```bash
git diff HEAD~4..HEAD -- \
  .agents/skills/resume-tailor/SKILL.md \
  .agents/skills/resume-tailor/references/tailoring-report-schema.md \
  resume-system/reference/hiring-reality.md \
  resume-system/reference/qualification-taxonomy.md \
  resume-system/facts/per-project-keywords.md \
  resume-system/governance/auditor-prompt.md
```

Confirm:

- Default output forbids routine reports.
- Explicit report requests remain supported.
- Both references are in the immutable read set.
- Candidate fact authority still belongs to fact masters.
- The 75% placement rule is gone.
- No excluded evidence rule or PDF extraction rule was added.

- [ ] **Step 5: Commit only if verification required a correction**

If a correction was necessary:

```bash
git add .agents/skills/resume-tailor/SKILL.md \
  .agents/skills/resume-tailor/references/tailoring-report-schema.md \
  .agents/skills/resume-tailor/scripts/preflight.py \
  README.md \
  resume-system/facts/per-project-keywords.md \
  resume-system/governance/auditor-prompt.md \
  resume-system/reference/hiring-reality.md \
  resume-system/reference/qualification-taxonomy.md \
  tests/test_resume_preflight.py
git diff --cached --name-only
git commit -m "fix: satisfy tailoring contract verification"
```

If no correction was needed, do not create an empty commit.
