# Career Communication Systems Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a shared decision standard, revised LinkedIn and application-answer workflows, a new cover-letter workflow, and repeatable regression checks that produce concise, factual, human candidate communications.

**Architecture:** One shared reference owns evidence selection, clarification, truth, and voice decisions. Three channel playbooks own channel-specific inputs and output contracts, while thin model-invoked Cursor skills route requests to those playbooks. Markdown fixtures capture judgment expectations, and a dependency-free Python validator checks deterministic output constraints without enforcing exact prose.

**Tech Stack:** Markdown prompt and skill files, Python 3 standard library, `unittest`

**Spec:** `docs/superpowers/specs/2026-09-19-career-communication-systems-design.md`

**Scope decision:** Keep one plan because the three channel workflows share the same evidence-ranking and clarification interface. Tasks 3-5 remain independently reviewable after Tasks 1-2 establish that shared contract and validator.

## Global Constraints

- Work stays under `career-tools/`, `.cursor/skills/`, `tests/`, and `docs/superpowers/`.
- Do not modify the live resume-tailoring pipeline under `resume-system/`.
- Candidate facts come only from current authoritative files under `resume-system/facts/` and obey `resume-system/governance/FACT_RULES.md`.
- Never use `career-stories/_drafts/` as a source.
- All candidate-facing workflows return output in chat and write no files unless the user explicitly asks to save.
- Do not add an `applications/` folder or application tracking.
- Do not add a package or dependency; validation uses Python 3 standard-library code.
- Human-readable regression cases evaluate decisions and banned outcomes, not exact prose snapshots.
- Preserve the confirmed eInfochips facts: Software Engineer Intern, Jan-May 2024, React/MUI, TypeScript/Node/Express/PostgreSQL, email/password sessions, and RBAC. Never restore Angular, OAuth/JWT, Kubernetes, 5+ APIs, a 40% metric, or a 2023 date.

## Review Focus

- A sparse LinkedIn profile must trigger one focused clarification instead of fabricated personalization; pin this in Task 3.
- A profile or JD that tempts an impressive but context-poor metric must produce a capability statement or no metric; pin this in Tasks 3, 4, and 5.
- A mixed-lane JD must yield one dominant angle rather than a Full Stack/Backend/AI keyword collage; pin this in Tasks 4 and 5.
- A personal, legal, salary, relocation, or work-authorization question without an authoritative answer must trigger clarification; pin this in Task 4.
- A company with thin or generic context must produce honest role-focused writing rather than invented passion or praise; pin this in Tasks 4 and 5.

---

### Task 1: Shared candidate-communication standard

**Files:**
- Create: `career-tools/reference/candidate-communication-standard.md`
- Create: `tests/test_career_tool_contracts.py`

**Interfaces:**
- Consumes: `resume-system/governance/FACT_RULES.md`, `career-tools/reference/humanizer.md`, and the approved design spec.
- Produces: a shared Markdown contract referenced by all three channel playbooks and their Cursor skill wrappers.

- [ ] **Step 1: Write a failing shared-standard contract test**

Create `tests/test_career_tool_contracts.py` with the following foundation:

```python
from __future__ import annotations

import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    return (REPO / relative).read_text(encoding="utf-8")


class SharedCommunicationStandardTest(unittest.TestCase):
    def test_shared_standard_defines_decision_and_clarification_contracts(self) -> None:
        content = read("career-tools/reference/candidate-communication-standard.md")

        required = (
            "## Decision sequence",
            "## Evidence ranking",
            "## Clarification threshold",
            "## Truth boundary",
            "## Human voice",
            "## Final rejection pass",
            "resume-system/governance/FACT_RULES.md",
            "career-tools/reference/humanizer.md",
        )
        for marker in required:
            with self.subTest(marker=marker):
                self.assertIn(marker, content)

        self.assertIn("Ask only when", content)
        self.assertIn("Omit the metric", content)
        self.assertIn("one primary angle", content)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the test and verify the missing-file failure**

Run:

```bash
python3 -m unittest tests.test_career_tool_contracts.SharedCommunicationStandardTest -v
```

Expected: `ERROR` with `FileNotFoundError` for `career-tools/reference/candidate-communication-standard.md`.

- [ ] **Step 3: Write the shared standard**

Create `career-tools/reference/candidate-communication-standard.md` with these sections and rules:

```markdown
# Candidate communication standard

> Shared decision rules for LinkedIn notes, application answers, and cover letters. Channel playbooks own their inputs, length, structure, and output format.

## Decision sequence

1. Identify the reader and the response the writing should earn.
2. Extract the reader's most relevant problem from the supplied profile or JD.
3. Generate candidate angles from verified facts.
4. Reject angles that need hidden context, force irrelevant metrics, exaggerate overlap, repeat what the reader knows, or work unchanged for many recipients.
5. Rank the remaining angles by relevance, standalone clarity, credibility, usefulness, and space cost.
6. Choose one primary angle. Add supporting evidence only when the channel or question requires it.
7. Draft for the channel, then run the final rejection pass.

## Evidence ranking

Prefer, in order: a directly relevant work outcome; a directly relevant implementation decision; an adjacent capability described honestly; a project or metric only when it is understandable without hidden context. Omit the metric when the reader needs project background or a technical baseline to understand why it matters.

## Clarification threshold

Ask only when missing information would materially change the output and no safe default exists. Do not ask merely because several facts fit, the JD spans lanes, a company is ordinary, or a metric must be omitted. Ask when personalization would otherwise be fabricated or when the answer depends on an unstored personal, legal, salary, relocation, or work-authorization preference.

## Truth boundary

Candidate claims come only from `resume-system/facts/work-experience.md`, current selectable files under `resume-system/facts/projects/`, and `resume-system/governance/FACT_RULES.md`. Treat side projects as prototypes unless their master says otherwise. Never join unrelated facts into a fictional story. Never use `_drafts/` files.

## Human voice

Use `career-tools/reference/humanizer.md` as an internal review reference. Return only the final candidate-facing copy, not the humanizer's draft and audit. Prefer direct sentences, normal words, natural contractions, and details Shubh can explain aloud. Avoid generic praise, inflated significance, JD mimicry, rule-of-three padding, em or en dashes, and ceremonial closings.

## Final rejection pass

Rewrite when the output does not answer the reader's likely question, needs missing context, contains unsupported motivation or facts, uses a context-poor metric, overstates overlap, sounds reusable across recipients, or reads like a polished AI blob rather than Shubh.
```

- [ ] **Step 4: Run the shared-standard test**

Run:

```bash
python3 -m unittest tests.test_career_tool_contracts.SharedCommunicationStandardTest -v
```

Expected: `OK`, one test passing.

- [ ] **Step 5: Commit the shared standard**

```bash
git add career-tools/reference/candidate-communication-standard.md tests/test_career_tool_contracts.py
git commit -m "feat: add candidate communication standard"
```

---

### Task 2: Deterministic output-contract validator

**Files:**
- Create: `career-tools/evals/validate_output.py`
- Modify: `tests/test_career_tool_contracts.py`

**Interfaces:**
- Consumes: plain candidate-facing body text with no metadata wrapper.
- Produces: `ValidationResult(ok: bool, errors: tuple[str, ...])` through `validate_linkedin`, `validate_application`, and `validate_cover_letter`.

- [ ] **Step 1: Add failing validator unit tests**

Append the following imports and test class to `tests/test_career_tool_contracts.py`:

```python
import importlib.util
import sys


def load_validator():
    path = REPO / "career-tools/evals/validate_output.py"
    spec = importlib.util.spec_from_file_location("career_output_validator", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load validator from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class OutputValidatorTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_validator()

    def test_linkedin_accepts_two_lines_and_one_question(self) -> None:
        text = (
            "Your move from product APIs into platform work at Acme stood out.\n"
            "I'm finishing my MS at ASU and building backend job systems. What changed most in that move?"
        )
        self.assertTrue(self.validator.validate_linkedin(text).ok)

    def test_linkedin_rejects_four_lines_and_two_questions(self) -> None:
        text = "One\nTwo\nThree?\nFour?"
        result = self.validator.validate_linkedin(text)
        self.assertFalse(result.ok)
        self.assertIn("LinkedIn note must contain 2 or 3 non-empty lines", result.errors)
        self.assertIn("LinkedIn note must contain exactly one question mark", result.errors)

    def test_application_honors_word_and_character_limits(self) -> None:
        text = "I built a concise answer from verified experience."
        self.assertTrue(
            self.validator.validate_application(text, max_words=12, max_chars=80).ok
        )
        self.assertFalse(
            self.validator.validate_application(text, max_words=5, max_chars=80).ok
        )

    def test_application_rejects_multiple_paragraphs(self) -> None:
        result = self.validator.validate_application("First paragraph.\n\nSecond paragraph.")
        self.assertIn("Application answer must contain one paragraph", result.errors)

    def test_cover_letter_accepts_two_short_paragraphs(self) -> None:
        text = "First paragraph connects the role to experience.\n\nSecond paragraph proves it and asks for a conversation."
        self.assertTrue(self.validator.validate_cover_letter(text).ok)

    def test_cover_letter_rejects_wrong_paragraph_count_and_dash(self) -> None:
        result = self.validator.validate_cover_letter("Only one paragraph — with a dash.")
        self.assertIn("Cover letter must contain exactly 2 paragraphs", result.errors)
        self.assertIn("Output must not contain em or en dashes", result.errors)
```

- [ ] **Step 2: Run the validator tests and verify they fail**

Run:

```bash
python3 -m unittest tests.test_career_tool_contracts.OutputValidatorTest -v
```

Expected: `ERROR` with `FileNotFoundError` for `career-tools/evals/validate_output.py`.

- [ ] **Step 3: Implement the validator**

Create `career-tools/evals/validate_output.py`:

```python
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass


WORD = re.compile(r"\b[\w']+\b")
PARAGRAPH_BREAK = re.compile(r"\n\s*\n")


@dataclass(frozen=True)
class ValidationResult:
    errors: tuple[str, ...]

    @property
    def ok(self) -> bool:
        return not self.errors


def _word_count(text: str) -> int:
    return len(WORD.findall(text))


def _paragraphs(text: str) -> list[str]:
    stripped = text.strip()
    return [part.strip() for part in PARAGRAPH_BREAK.split(stripped) if part.strip()]


def _dash_error(text: str) -> list[str]:
    return ["Output must not contain em or en dashes"] if "—" in text or "–" in text else []


def validate_linkedin(text: str, max_chars: int = 300) -> ValidationResult:
    body = text.strip()
    lines = [line for line in body.splitlines() if line.strip()]
    errors: list[str] = []
    if len(lines) not in (2, 3):
        errors.append("LinkedIn note must contain 2 or 3 non-empty lines")
    if len(body) > max_chars:
        errors.append(f"LinkedIn note exceeds {max_chars} characters")
    if body.count("?") != 1:
        errors.append("LinkedIn note must contain exactly one question mark")
    errors.extend(_dash_error(body))
    return ValidationResult(tuple(errors))


def validate_application(
    text: str,
    max_words: int = 120,
    max_chars: int | None = None,
) -> ValidationResult:
    body = text.strip()
    errors: list[str] = []
    if len(_paragraphs(body)) != 1:
        errors.append("Application answer must contain one paragraph")
    if _word_count(body) > max_words:
        errors.append(f"Application answer exceeds {max_words} words")
    if max_chars is not None and len(body) > max_chars:
        errors.append(f"Application answer exceeds {max_chars} characters")
    errors.extend(_dash_error(body))
    return ValidationResult(tuple(errors))


def validate_cover_letter(text: str, max_words: int = 200) -> ValidationResult:
    body = text.strip()
    errors: list[str] = []
    if len(_paragraphs(body)) != 2:
        errors.append("Cover letter must contain exactly 2 paragraphs")
    if _word_count(body) > max_words:
        errors.append(f"Cover letter exceeds {max_words} words")
    errors.extend(_dash_error(body))
    return ValidationResult(tuple(errors))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate candidate-facing output contracts")
    parser.add_argument("kind", choices=("linkedin", "application", "cover-letter"))
    parser.add_argument("--max-words", type=int)
    parser.add_argument("--max-chars", type=int)
    args = parser.parse_args()
    text = sys.stdin.read()

    if args.kind == "linkedin":
        result = validate_linkedin(text, max_chars=args.max_chars or 300)
    elif args.kind == "application":
        result = validate_application(
            text,
            max_words=args.max_words or 120,
            max_chars=args.max_chars,
        )
    else:
        result = validate_cover_letter(text, max_words=args.max_words or 200)

    if result.ok:
        print("PASS")
        return 0
    for error in result.errors:
        print(f"FAIL: {error}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run validator tests and a CLI smoke test**

Run:

```bash
python3 -m unittest tests.test_career_tool_contracts.OutputValidatorTest -v
```

Expected: all six validator tests pass.

Run:

```bash
printf 'Profile-specific observation.\nRelevant bridge. What changed most?' | python3 career-tools/evals/validate_output.py linkedin
```

Expected: `PASS` and exit code `0`.

- [ ] **Step 5: Commit the validator**

```bash
git add career-tools/evals/validate_output.py tests/test_career_tool_contracts.py
git commit -m "test: add career output contract validator"
```

---

### Task 3: Reply-oriented LinkedIn connection-note workflow

**Files:**
- Modify: `career-tools/linkedin/linkedin-connection-note.md`
- Modify: `.cursor/skills/linkedin-connection-note/SKILL.md`
- Create: `career-tools/evals/linkedin-connection-note-cases.md`
- Modify: `tests/test_career_tool_contracts.py`

**Interfaces:**
- Consumes: name, job title, company, optional About section, LinkedIn Experience section, shared communication standard, candidate profile, authoritative project facts when needed, fact rules, and humanizer.
- Produces: one two- or three-line note of at most 300 characters with exactly one reply-oriented question, or one focused clarification when honest personalization is impossible.

- [ ] **Step 1: Add failing LinkedIn wiring and contract tests**

Append:

```python
class LinkedInWorkflowTest(unittest.TestCase):
    def test_playbook_uses_reply_oriented_contract(self) -> None:
        content = read("career-tools/linkedin/linkedin-connection-note.md")
        for marker in (
            "earn a reply",
            "Name",
            "Job title",
            "Company",
            "About section",
            "Experience section",
            "Two or three",
            "300 characters",
            "exactly one question",
            "Omit metrics by default",
            "career-tools/reference/candidate-communication-standard.md",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, content)
        self.assertNotIn("Exactly 3 lines", content)
        self.assertNotIn("one project + one metric", content)

    def test_skill_routes_to_shared_rules_and_reply_goal(self) -> None:
        content = read(".cursor/skills/linkedin-connection-note/SKILL.md")
        self.assertIn("earn a reply", content)
        self.assertIn("career-tools/reference/candidate-communication-standard.md", content)
        self.assertIn("career-tools/linkedin/linkedin-connection-note.md", content)
        self.assertIn("career-tools/evals/validate_output.py linkedin", content)

    def test_linkedin_fixture_covers_review_focus(self) -> None:
        content = read("career-tools/evals/linkedin-connection-note-cases.md")
        for case_id in (
            "LI-01 detailed recruiter",
            "LI-02 sparse recruiter",
            "LI-03 close engineer overlap",
            "LI-04 adjacent engineer overlap",
            "LI-05 career transition",
            "LI-06 founder",
            "LI-07 context-poor metric",
            "LI-08 unsafe personalization",
        ):
            with self.subTest(case_id=case_id):
                self.assertIn(case_id, content)
```

- [ ] **Step 2: Run the LinkedIn tests and verify failures**

Run:

```bash
python3 -m unittest tests.test_career_tool_contracts.LinkedInWorkflowTest -v
```

Expected: failures for the old mandatory three-line/project-metric rules and missing fixture file.

- [ ] **Step 3: Rewrite the LinkedIn playbook around the reply goal**

Replace the existing playbook with focused sections in this order:

```markdown
# LinkedIn connection note

> Goal: earn a reply from the recipient. An accepted request without a reply is useful but incomplete.

## Standard input
Name, Job title, Company, About section when available, and Experience section. Infer a reply-oriented networking intent unless the user explicitly provides another goal.

## Before writing
Read the shared standard, candidate profile, fact rules, relevant authoritative fact file only when needed, and humanizer. Never use a metric or project fact without checking its authoritative source.

## Recipient decision
Classify recruiter, hiring manager, engineer, or founder. Select one current-work detail, meaningful transition, technical/product area, or company-history detail. Connect it to one plain-language part of Shubh's background.

## The question
End with exactly one question that the recipient can answer in one sentence, is informed by the profile, is not answered by the company website, and does not ask for a referral, application review, or meeting on first contact.

## Shape
Two or three non-empty lines and at most 300 characters including line breaks. Combine elements when natural. Use one recipient-specific observation, one concise bridge, and one low-friction question.

## Evidence
Prefer capabilities to project names and problems solved to tool lists. Omit metrics by default. Include one only when it is independently meaningful inside the note and improves the reason to reply. Describe adjacent overlap as adjacent.

## Clarification
Generate without asking when job title, company, and Experience provide an honest hook. Ask one focused question when the profile is too sparse to personalize without invention or when a referenced job opening makes applied/not-applied status material.

## Reject and rewrite
Reject generic praise, copied profile facts without an observation, `Would love to connect` as the only ask, first-contact referrals, multiple questions, unexplained project names or benchmarks, long introductions, essay questions, and notes reusable across recipients.

## Output
Return brief decision metadata outside the copy block: recipient type, angle, evidence used or `none`, and omitted metric with reason when relevant. Put only the ready-to-paste note in the copy block. Count the copy with `python3 career-tools/evals/validate_output.py linkedin` before returning it.
```

Include one good and one rejected example. The good example must use a fictional profile and a profile-informed question. The rejected example must show why an unexplained benchmark plus `Would love to connect` fails.

- [ ] **Step 4: Thin the LinkedIn Cursor skill into a router**

Keep model invocation enabled and update its description to trigger on connection notes, recruiter or engineer outreach, and LinkedIn profile details. Its body must:

1. Read `career-tools/linkedin/linkedin-connection-note.md`.
2. Read `career-tools/reference/candidate-communication-standard.md`.
3. Read `career-tools/linkedin/candidate-profile.md`.
4. Read `resume-system/governance/FACT_RULES.md` and only the relevant fact file when evidence is selected.
5. Read `career-tools/reference/humanizer.md` as an internal review.
6. Apply the reply goal and clarification threshold.
7. Validate the copy with `python3 career-tools/evals/validate_output.py linkedin`.
8. Return one final note, not alternatives.

Remove duplicated project-selection, mandatory metric, exact-three-line, and old network/ask/referral default tables from the wrapper.

- [ ] **Step 5: Add eight LinkedIn decision fixtures**

Create `career-tools/evals/linkedin-connection-note-cases.md`. Give every case the headings `Input`, `Expected decision`, `Allowed evidence`, `Reject`, and `Acceptance`. Use these concrete cases:

| ID | Input summary | Expected decision |
|---|---|---|
| LI-01 detailed recruiter | Maya Patel, Senior Technical Recruiter at AtlasPay; About says she hires API and payments-platform engineers; Experience shows three years recruiting platform teams. | Bridge to Shubh's Node/PostgreSQL payment workflows; ask what differentiates early-career backend candidates on that team; omit the 10,000-record metric because it is unnecessary. |
| LI-02 sparse recruiter | Chris Lee, Technical Recruiter at Northstar; no About; Experience says software hiring across backend and frontend. | Use the stated backend/frontend hiring scope, briefly position Shubh as an MS CS candidate with full-stack and backend work, and ask which side the current early-career hiring favors. |
| LI-03 close engineer overlap | Daniel Kim, Senior Platform Engineer at CrawlWorks; Experience mentions Redis queues and browser workers. | Bridge to the async audit workflow without naming SEO Audit Engine first; ask one tradeoff question about isolating browser work from request handling. |
| LI-04 adjacent engineer overlap | Priya Shah, Senior ML Platform Engineer at ModelDock; Experience mentions training infrastructure and observability. | Describe Shubh's cluster-observability prototype as adjacent, not equivalent; ask about the hardest transition from application to ML platform work. |
| LI-05 career transition | Luis Romero, Staff Engineer at Acme; Experience shows frontend engineer to backend to platform. | Lead with the transition and Shubh's current backend direction; do not force a project or metric. |
| LI-06 founder | Erin Brooks, founder of a voice-workflow startup; About is product-focused with no open role. | Use adjacent voice/AI pipeline capability, avoid claiming the same problem, and ask one product-engineering question rather than requesting a call. |
| LI-07 context-poor metric | Recruiter for an infrastructure company; profile gives no benchmark context. | Omit ClusterOps estimates and unexplained throughput language; use the observable capability of tracing simulated cluster failures. |
| LI-08 unsafe personalization | Sam Chen, Senior Software Engineer at Acme; no About and Experience contains only title/company. | Ask the user for one additional profile detail or the person's visible technical focus; do not generate a generic note. |

For LI-01 and LI-07, include a rejected sample and a short explanation. For LI-03, include one acceptable sample that passes the validator. Keep all companies and recipients explicitly labeled fictional.

- [ ] **Step 6: Run LinkedIn and validator tests**

Run:

```bash
python3 -m unittest tests.test_career_tool_contracts.LinkedInWorkflowTest tests.test_career_tool_contracts.OutputValidatorTest -v
```

Expected: all LinkedIn and validator tests pass.

- [ ] **Step 7: Commit the LinkedIn workflow**

```bash
git add career-tools/linkedin/linkedin-connection-note.md .cursor/skills/linkedin-connection-note/SKILL.md career-tools/evals/linkedin-connection-note-cases.md tests/test_career_tool_contracts.py
git commit -m "feat: optimize LinkedIn notes for replies"
```

---

### Task 4: JD-driven application-answer workflow

**Files:**
- Modify: `career-tools/application-answers/application-answers.md`
- Modify: `.cursor/skills/application-answers/SKILL.md`
- Create: `career-tools/evals/application-answer-cases.md`
- Modify: `tests/test_career_tool_contracts.py`

**Interfaces:**
- Consumes: JD, verbatim application questions, shared standard, authoritative work and project facts, fact rules, and humanizer.
- Produces: one direct final answer per question, normally one paragraph and at most 120 words, or a focused clarification for an unstored personal answer.

- [ ] **Step 1: Add failing application workflow tests**

Append:

```python
class ApplicationAnswerWorkflowTest(unittest.TestCase):
    def test_playbook_uses_jd_and_questions_without_resume_paste(self) -> None:
        content = read("career-tools/application-answers/application-answers.md")
        for marker in (
            "JD",
            "Questions",
            "Backend, Full Stack, AI, or mixed",
            "No artificial minimum",
            "120 words",
            "resume-system/facts/work-experience.md",
            "resume-system/facts/projects/",
            "career-tools/reference/candidate-communication-standard.md",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, content)
        self.assertNotIn("Resume (.tex)", content)
        self.assertNotIn("Refuse to generate", content)

    def test_skill_routes_to_master_facts_and_validator(self) -> None:
        content = read(".cursor/skills/application-answers/SKILL.md")
        self.assertIn("career-tools/reference/candidate-communication-standard.md", content)
        self.assertIn("resume-system/facts/work-experience.md", content)
        self.assertIn("resume-system/facts/projects/", content)
        self.assertIn("career-tools/evals/validate_output.py application", content)
        self.assertNotIn("Resume (.tex)", content)
        self.assertNotIn("Require a pasted resume", content)

    def test_application_fixture_covers_review_focus(self) -> None:
        content = read("career-tools/evals/application-answer-cases.md")
        for case_id in (
            "APP-01 ordinary company",
            "APP-02 misleading AI keyword",
            "APP-03 mixed lane",
            "APP-04 missing technology",
            "APP-05 collaboration",
            "APP-06 technical challenge",
            "APP-07 short character limit",
            "APP-08 personal clarification",
            "APP-09 story diversity",
            "APP-10 one-sentence answer",
        ):
            with self.subTest(case_id=case_id):
                self.assertIn(case_id, content)
```

- [ ] **Step 2: Run application tests and verify failures**

Run:

```bash
python3 -m unittest tests.test_career_tool_contracts.ApplicationAnswerWorkflowTest -v
```

Expected: failures because the old playbook requires a pasted resume and the fixture is missing.

- [ ] **Step 3: Rewrite the application-answer playbook**

Replace the current playbook with sections implementing this exact contract:

```markdown
# Application question answers

> Goal: answer the literal application question with the smallest relevant, verified evidence in Shubh's natural voice.

## Standard input
Require the JD and at least one verbatim question. Company and role may be inferred from the JD. A pasted resume is not required.

## Before writing
Read the shared standard, fact rules, work experience, current selectable project masters, and humanizer. Classify the JD as Backend, Full Stack, AI, or mixed. Extract the work owned, technical priorities, product/customer problem, and expected independence. The question's evaluation goal overrides the lane.

## Evidence
Use one evidence unit by default. Add a second only when the question asks for multiple dimensions. Never combine unrelated facts, revive superseded project wording, or upgrade prototype work.

## Length
No artificial minimum. Use one sentence for simple facts, about 40-80 words for motivation or fit, and about 60-110 words for technical or behavioral answers. Default hard maximum is 120 words. A stated portal limit wins. Use one paragraph unless the prompt explicitly requests parts or a list.

## Strategies
Define direct strategies for Why this company, Why fit, Tell us about yourself, technical project, behavioral, missing skill, and personal/preference questions exactly as specified in the design.

## Voice
Answer in the first sentence. Use natural contractions and varied structures. Do not restate the prompt, mimic the JD, invent passion, end repeatedly with `This aligns with...`, or write miniature cover letters.

## Clarification
Ask only for an unstored personal, salary, relocation, legal, or work-authorization answer. Choose among relevant verified stories without asking the user.

## Output
Return each verbatim question as a heading, one paste-ready answer, and a word or applicable character count outside the answer. Validate each answer body with `python3 career-tools/evals/validate_output.py application` plus `--max-words` or `--max-chars` when the portal supplies a limit.
```

Add a compact good example for a fictional backend JD and a rejected example that repeats company values, lists technologies, and invents passion.

- [ ] **Step 4: Thin the application-answer Cursor skill into a router**

Keep model invocation enabled. Its description must trigger when the user supplies application questions, supplemental questions, or asks for Greenhouse, Lever, or Workday answers. Its ordered steps must read:

1. `career-tools/application-answers/application-answers.md`
2. `career-tools/reference/candidate-communication-standard.md`
3. `resume-system/governance/FACT_RULES.md`
4. `resume-system/facts/work-experience.md`
5. current selectable files under `resume-system/facts/projects/`
6. `career-tools/reference/humanizer.md`

Then classify the JD, answer each question, validate each answer body, and return one final answer per question. Remove the pasted-resume requirement and duplicated word, truth, and voice rules that now belong in the playbook or shared standard.

- [ ] **Step 5: Add ten application-answer decision fixtures**

Create `career-tools/evals/application-answer-cases.md` with the same five fixture headings used for LinkedIn. Use these cases:

| ID | Input summary | Expected decision |
|---|---|---|
| APP-01 ordinary company | FleetCore backend JD for maintenance scheduling; question: `Why FleetCore?` | Discuss reliable operational workflows and connect to payment/member reconciliation; do not claim passion for fleet maintenance or quote values. |
| APP-02 misleading AI keyword | Backend JD mentions `AI-powered` marketing once but responsibilities are Node APIs, PostgreSQL, and queues. | Classify Backend; use DAS/eInfochips or SEO async-work evidence, not the compliance AI project. |
| APP-03 mixed lane | JD splits React UI, TypeScript APIs, PostgreSQL, and background jobs. | Classify mixed with Full Stack primary; choose one end-to-end example instead of listing all lanes. |
| APP-04 missing technology | JD requires Rust; question asks about Rust experience. | State no verified Rust experience, then connect Go/TypeScript systems work only as adjacent evidence; do not add Rust to skills. |
| APP-05 collaboration | Question asks for collaboration with a nontechnical team. | Use accountant UAT or ensemble-manager payment review; focus on Shubh's action and result. |
| APP-06 technical challenge | Question asks about a difficult backend problem. | Use async browser-job isolation, payment reconciliation, or durable cache fallback based on JD priority; explain the decision, not a tool list. |
| APP-07 short character limit | `Why are you a fit? 300 characters maximum.` | Produce one or two direct sentences under 300 characters and run the character validator. |
| APP-08 personal clarification | Question asks desired salary and willingness to relocate; no answer is stored. | Ask Shubh for those preferences; do not infer them from the JD or location. |
| APP-09 story diversity | Three questions ask fit, collaboration, and technical challenge. | Use distinct evidence where possible; do not repeat the same project three times. |
| APP-10 one-sentence answer | Question asks whether Shubh has used PostgreSQL. | Answer directly in one evidence-backed sentence; do not pad to a target range. |

Include one acceptable answer for APP-01, one rejected answer for APP-02, and one acceptable sub-300-character answer for APP-07. Label all JDs and companies fictional.

- [ ] **Step 6: Run application and validator tests**

Run:

```bash
python3 -m unittest tests.test_career_tool_contracts.ApplicationAnswerWorkflowTest tests.test_career_tool_contracts.OutputValidatorTest -v
```

Expected: all application and validator tests pass.

- [ ] **Step 7: Commit the application workflow**

```bash
git add career-tools/application-answers/application-answers.md .cursor/skills/application-answers/SKILL.md career-tools/evals/application-answer-cases.md tests/test_career_tool_contracts.py
git commit -m "feat: make application answers JD driven"
```

---

### Task 5: Two-paragraph cover-letter workflow

**Files:**
- Create: `career-tools/cover-letters/cover-letter.md`
- Create: `.cursor/skills/cover-letter/SKILL.md`
- Create: `career-tools/evals/cover-letter-cases.md`
- Modify: `tests/test_career_tool_contracts.py`

**Interfaces:**
- Consumes: JD, shared standard, authoritative work/project facts, fact rules, and humanizer.
- Produces: one body-only cover letter with exactly two paragraphs and at most 200 words, delivered in chat by default.

- [ ] **Step 1: Add failing cover-letter workflow tests**

Append:

```python
class CoverLetterWorkflowTest(unittest.TestCase):
    def test_playbook_defines_jd_only_two_paragraph_contract(self) -> None:
        content = read("career-tools/cover-letters/cover-letter.md")
        for marker in (
            "JD only",
            "Exactly two paragraphs",
            "130-180 words",
            "200 words",
            "Body only",
            "career-tools/reference/candidate-communication-standard.md",
            "resume-system/facts/work-experience.md",
            "resume-system/facts/projects/",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, content)

    def test_cover_letter_skill_is_model_invoked_and_wired(self) -> None:
        content = read(".cursor/skills/cover-letter/SKILL.md")
        self.assertIn("name: cover-letter", content)
        self.assertIn("description:", content)
        self.assertNotIn("disable-model-invocation: true", content)
        self.assertIn("career-tools/cover-letters/cover-letter.md", content)
        self.assertIn("career-tools/reference/candidate-communication-standard.md", content)
        self.assertIn("career-tools/evals/validate_output.py cover-letter", content)

    def test_cover_letter_fixture_covers_review_focus(self) -> None:
        content = read("career-tools/evals/cover-letter-cases.md")
        for case_id in (
            "CL-01 backend scaling",
            "CL-02 broad full stack",
            "CL-03 vague AI",
            "CL-04 mixed lane",
            "CL-05 ordinary company",
            "CL-06 thin company context",
            "CL-07 missing technology",
            "CL-08 context-poor metric",
            "CL-09 early career",
            "CL-10 resume summary",
        ):
            with self.subTest(case_id=case_id):
                self.assertIn(case_id, content)
```

- [ ] **Step 2: Run cover-letter tests and verify missing-file errors**

Run:

```bash
python3 -m unittest tests.test_career_tool_contracts.CoverLetterWorkflowTest -v
```

Expected: `ERROR` for missing playbook, skill, and fixture files.

- [ ] **Step 3: Create the cover-letter playbook**

Create `career-tools/cover-letters/cover-letter.md` with this contract:

```markdown
# Cover letter

> Goal: make one concise argument connecting Shubh's verified experience to the work in the JD.

## Standard input
The standard input is the JD only. Infer company, job title, dominant lane, company/role problem, and strongest verified evidence. Ask only when the JD is missing or too incomplete to identify the role's work.

## Before writing
Read the shared standard, fact rules, work experience, current selectable project masters, and humanizer. Company claims come from the JD by default. Do not browse or invent a company problem unless the user requests research.

## Selection
Choose one central argument. Normally use one work experience and one project when they reinforce that argument. Use a third fact only for a distinct important requirement. Never mention three projects.

## Paragraph one
Open on the company's stated work or the role's concrete problem, connect it to relevant experience, and establish the central fit. When company context is thin, focus honestly on the role.

## Paragraph two
Support the fit with one or two concrete examples, explain the contribution they enable, and close with a direct invitation to discuss one specific responsibility.

## Output contract
Exactly two paragraphs. Target 130-180 words; hard maximum 200 words. Body only by default, with no address block, date, or generic salutation. Return one final version in chat and save nothing unless explicitly asked.

## Evidence and voice
Preserve prototype framing. Prefer decisions and capabilities to tool inventories. Explain a project before naming it. Use only standalone-legible metrics. Avoid generic openings, unsupported praise, lifelong passion, formal filler, adjective triplets, em/en dashes, and copied resume bullets.

## Reject and rewrite
Reject when the opening works for another company, paragraph one only paraphrases the JD, paragraph two is a resume list, more than one argument competes, praise exceeds evidence, a metric needs hidden context, the closing is stiff or entitled, or the output breaks the two-paragraph/200-word contract.

## Validation
Pass the body through `python3 career-tools/evals/validate_output.py cover-letter` before returning it.
```

Add one acceptable fictional example under 200 words and one rejected example annotated with the specific failure reasons.

- [ ] **Step 4: Create the model-invoked cover-letter skill**

Create `.cursor/skills/cover-letter/SKILL.md` with frontmatter:

```yaml
---
name: cover-letter
description: >-
  Write a short, human cover letter for Shubh Kapadia from a supplied job
  description. Use when the user asks for a cover letter, application letter,
  or a two-paragraph letter tailored to a role or company.
---
```

The body must route in this order:

1. Read `career-tools/cover-letters/cover-letter.md`.
2. Read `career-tools/reference/candidate-communication-standard.md`.
3. Read `resume-system/governance/FACT_RULES.md`.
4. Read `resume-system/facts/work-experience.md`.
5. Read current selectable files under `resume-system/facts/projects/`.
6. Read `career-tools/reference/humanizer.md`.
7. Infer the lane and one central argument from the JD.
8. Draft exactly two paragraphs, validate the body, and return one final version in chat.

State that the skill does not save a file or browse for company information unless the user explicitly requests it.

- [ ] **Step 5: Add ten cover-letter decision fixtures**

Create `career-tools/evals/cover-letter-cases.md` with the same five fixture headings. Use:

| ID | Input summary | Expected decision |
|---|---|---|
| CL-01 backend scaling | JD owns Node APIs, background work, PostgreSQL, and operational reliability. | Central argument: reliable asynchronous/backend workflows; choose the strongest coherent work/project pair. |
| CL-02 broad full stack | JD owns React UI, TypeScript API, and shared data contracts. | Use DAS end-to-end membership/payment work; avoid a technology inventory. |
| CL-03 vague AI | JD repeatedly says AI but concrete work is evaluation, retrieval, and traceable findings. | Use compliance-pipeline evaluation and cited findings; ignore marketing adjectives. |
| CL-04 mixed lane | JD combines frontend, APIs, and one AI feature. | Choose the dominant responsibility and mention the secondary capability only when it strengthens the same argument. |
| CL-05 ordinary company | Company sells routine operations software. | Open on the stated workflow problem; do not invent personal passion or prestige. |
| CL-06 thin company context | JD lists responsibilities but almost nothing about product or mission. | Focus on the role's work and avoid fabricated company specificity. |
| CL-07 missing technology | JD prefers Rust, which is not verified. | Do not claim Rust; use transferable backend design evidence without dwelling on the gap. |
| CL-08 context-poor metric | A ClusterOps estimate or test count is available but not meaningful to the reader. | Omit it and explain the failure-analysis or observability capability instead. |
| CL-09 early career | Senior-sounding JD could tempt leadership or production-scale overstatement. | Use confident contribution language while preserving intern/individual-contributor and prototype boundaries. |
| CL-10 resume summary | Several facts match and tempt a paragraph of bullets in prose. | Select one argument and at most one coherent work/project pair. |

Include one acceptable letter for CL-01 that passes the validator, one rejected generic letter for CL-05, and one rejected resume-summary letter for CL-10. Label all JDs and companies fictional.

- [ ] **Step 6: Run cover-letter and validator tests**

Run:

```bash
python3 -m unittest tests.test_career_tool_contracts.CoverLetterWorkflowTest tests.test_career_tool_contracts.OutputValidatorTest -v
```

Expected: all cover-letter and validator tests pass.

- [ ] **Step 7: Commit the cover-letter workflow**

```bash
git add career-tools/cover-letters/cover-letter.md .cursor/skills/cover-letter/SKILL.md career-tools/evals/cover-letter-cases.md tests/test_career_tool_contracts.py
git commit -m "feat: add concise cover letter workflow"
```

---

### Task 6: Evaluation guide and full-system verification

**Files:**
- Create: `career-tools/evals/README.md`
- Modify: `tests/test_career_tool_contracts.py`

**Interfaces:**
- Consumes: the three fixture files, validator CLI, and five qualitative dimensions from the design.
- Produces: one documented repeatable process for adding a case, generating an output, running deterministic checks, grading judgment, and deciding where a rule belongs.

- [ ] **Step 1: Add a failing evaluation-guide wiring test**

Append:

```python
class EvaluationGuideTest(unittest.TestCase):
    def test_evaluation_guide_documents_repeatable_loop(self) -> None:
        content = read("career-tools/evals/README.md")
        for marker in (
            "## Add a case",
            "## Generate one output",
            "## Run deterministic validation",
            "## Grade the decision",
            "Truth",
            "Judgment",
            "Standalone clarity",
            "Voice",
            "Contract",
            "pass, revise, or fail",
            "linkedin-connection-note-cases.md",
            "application-answer-cases.md",
            "cover-letter-cases.md",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, content)
```

- [ ] **Step 2: Run the guide test and verify the missing-file failure**

Run:

```bash
python3 -m unittest tests.test_career_tool_contracts.EvaluationGuideTest -v
```

Expected: `ERROR` with `FileNotFoundError` for `career-tools/evals/README.md`.

- [ ] **Step 3: Write the evaluation guide**

Create `career-tools/evals/README.md` with this process:

```markdown
# Career communication evaluations

These fixtures test judgment rather than exact wording. Each run receives `pass`, `revise`, or `fail`.

## Add a case
Copy the five-section case shape: Input, Expected decision, Allowed evidence, Reject, and Acceptance. Isolate one decision error. Put shared errors in the shared standard and channel-only errors in that channel's playbook.

## Generate one output
Run the relevant Cursor skill or apply its playbook to the case exactly as written. Save nothing by default. Keep only the candidate-facing body for deterministic validation.

## Run deterministic validation
Use one command:
`python3 career-tools/evals/validate_output.py linkedin < /tmp/linkedin-note.txt`
`python3 career-tools/evals/validate_output.py application < /tmp/application-answer.txt`
`python3 career-tools/evals/validate_output.py cover-letter < /tmp/cover-letter.txt`
Add `--max-chars N` or `--max-words N` for a portal-specific limit.

## Grade the decision
Grade Truth, Judgment, Standalone clarity, Voice, and Contract. `pass` means every dimension passes. `revise` means the facts and angle are usable but wording or contract needs another draft. `fail` means the system chose the wrong angle, invented or overstated a fact, ignored a required clarification, or produced channel-inappropriate writing.

## Fixture files
Link the LinkedIn, application-answer, and cover-letter case files.
```

- [ ] **Step 4: Run all career-tool tests**

Run:

```bash
python3 -m unittest tests.test_career_tool_contracts -v
```

Expected: every test in the new module passes.

- [ ] **Step 5: Run the existing resume regression suite**

Run:

```bash
python3 -m unittest tests.test_resume_preflight -v
```

Expected: all five existing resume preflight tests pass, confirming the live pipeline was not disturbed.

- [ ] **Step 6: Run repository-level consistency checks**

Run:

```bash
git diff --check
```

Expected: no output.

Run:

```bash
rg -n "Exactly 3 lines|one project \+ one metric|Resume \(\.tex\)|Refuse to generate" career-tools .cursor/skills
```

Expected: no stale live-rule matches in the three playbooks or their Cursor skills. If an evaluation fixture quotes a rejected old rule, label it explicitly as rejected and narrow this command to the live files.

Run:

```bash
rg -n "OAuth|JWT|Angular|Kubernetes|40%" career-tools/linkedin career-tools/application-answers career-tools/cover-letters .cursor/skills career-tools/evals
```

Expected: no candidate claim reintroduces retired eInfochips facts. A fixture may mention a banned claim only inside a clearly labeled `Reject` section.

- [ ] **Step 7: Commit the evaluation guide and final test wiring**

```bash
git add career-tools/evals/README.md tests/test_career_tool_contracts.py
git commit -m "docs: add career communication evaluation loop"
```

- [ ] **Step 8: Verify final repository state**

Run:

```bash
python3 -m unittest discover -s tests -v
git status --short
git log -7 --oneline
```

Expected: all tests pass; `git status --short` is empty; recent history contains the design commit plus the six implementation commits from this plan.
