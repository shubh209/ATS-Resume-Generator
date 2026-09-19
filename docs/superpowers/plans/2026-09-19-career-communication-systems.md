# Career Communication Markdown Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Improve the Markdown prompts, rules, guardrails, and skill routers for LinkedIn connection notes, application answers, and cover letters.

**Architecture:** One shared Markdown standard owns the decision rules used by all three systems. Each channel keeps its own focused prompt and thin Cursor skill. Markdown example cases document what good and bad judgment look like; no Python tooling or application-tracking system is added.

**Tech Stack:** Markdown only

**Spec:** `docs/superpowers/specs/2026-09-19-career-communication-systems-design.md`

## Constraints

- Modify only Markdown files under `career-tools/`, `.cursor/skills/`, and `docs/superpowers/`.
- Do not modify `resume-system/` or the live resume-tailoring skill.
- Candidate facts come only from `resume-system/facts/` and obey `resume-system/governance/FACT_RULES.md`.
- Never use `career-stories/_drafts/` as a source.
- Candidate-facing output stays in chat unless the user explicitly asks to save it.
- Do not add an `applications/` folder, Python validator, test module, dependency, or automated evaluation framework.

---

### Task 1: Write the shared decision standard

**Files:**
- Create: `career-tools/reference/candidate-communication-standard.md`

- [ ] Write the ordered decision process: identify reader and desired response, extract the reader's problem, generate verified candidate angles, reject weak angles, rank remaining angles, choose one primary angle, draft, and run a final rejection pass.
- [ ] Define evidence ranking around relevance, standalone clarity, credibility, usefulness, and word or character cost.
- [ ] State that unexplained project names, technical benchmarks, and metrics are omitted when the reader needs hidden context to understand them.
- [ ] Define the clarification threshold: ask only when missing information materially changes the output and there is no safe default.
- [ ] Define the truth boundary using `resume-system/facts/`, `FACT_RULES.md`, prototype framing, and the ban on `_drafts/` sources.
- [ ] Define the human-voice review using `career-tools/reference/humanizer.md` internally while returning only final copy.
- [ ] Add the shared final rejection checklist for unsupported claims, invented motivation, generic praise, overstated overlap, context-poor metrics, indirect answers, and reusable AI-sounding prose.
- [ ] Review the file for duplicated channel-specific rules and keep those rules in their channel prompt.
- [ ] Commit the shared standard.

---

### Task 2: Rewrite the LinkedIn connection-note system

**Files:**
- Modify: `career-tools/linkedin/linkedin-connection-note.md`
- Modify: `.cursor/skills/linkedin-connection-note/SKILL.md`
- Create: `career-tools/linkedin/examples.md`

- [ ] Change the objective from earning an accepted request to earning a reply.
- [ ] Set the standard input to name, job title, company, About section when available, and LinkedIn Experience section.
- [ ] Remove the mandatory intent/reason form, exact-three-line rule, and mandatory project-plus-metric rule.
- [ ] Default unstated intent to reply-oriented networking. Preserve explicit referral or application context only when the user supplies it.
- [ ] Define recipient handling for recruiters, hiring managers, engineers, and founders.
- [ ] Require one profile-specific observation, one concise connection to Shubh, and one low-friction question answerable in one sentence.
- [ ] Allow two or three lines while preserving the 300-character hard limit.
- [ ] Omit metrics by default. Allow one only when it is independently understandable and improves the reason to reply.
- [ ] Ban first-contact referral requests, generic praise, `Would love to connect` as the only ask, copied profile facts without an observation, multiple questions, unexplained project names, and essay-sized questions.
- [ ] Add an output format that exposes a short internal decision summary outside the copy block and returns one ready-to-paste note.
- [ ] Rewrite the Cursor skill as a thin router to the LinkedIn prompt, shared standard, candidate profile, relevant fact files, fact rules, and humanizer.
- [ ] Add Markdown examples covering a detailed recruiter, sparse recruiter, close engineer overlap, adjacent overlap, career transition, founder, context-poor metric, and profile too sparse for safe personalization.
- [ ] For each example, record the input, chosen angle, evidence allowed, what to reject, and acceptance criteria. Include a few acceptable and rejected notes without treating one exact sentence as mandatory.
- [ ] Manually count every acceptable example to confirm it stays within 300 characters and uses only one question.
- [ ] Commit the LinkedIn Markdown changes.

---

### Task 3: Rewrite the application-answer system

**Files:**
- Modify: `career-tools/application-answers/application-answers.md`
- Modify: `.cursor/skills/application-answers/SKILL.md`
- Create: `career-tools/application-answers/examples.md`

- [ ] Change the standard input to the JD plus verbatim application questions. Remove the pasted-resume requirement.
- [ ] Make the system read authoritative work experience, current selectable project facts, `FACT_RULES.md`, the shared standard, and the humanizer.
- [ ] Define JD classification as Backend, Full Stack, AI, or mixed while making the literal question override the general lane.
- [ ] Require one evidence unit by default and a second only when the question asks for multiple dimensions.
- [ ] Remove the artificial 50-word minimum. Keep one sentence for simple facts, roughly 40-80 words for motivation or fit, roughly 60-110 words for technical or behavioral answers, and 120 words as the default maximum.
- [ ] Add focused strategies for `Why this company?`, `Why fit?`, `Tell us about yourself`, technical projects, behavioral questions, missing skills, and personal or preference questions.
- [ ] Require the literal answer in the first sentence and ban JD mimicry, invented passion, repeated `This aligns with...` conclusions, miniature-cover-letter cadence, and unnecessary story reuse across questions.
- [ ] Clarify only for unstored personal, salary, relocation, legal, or work-authorization answers.
- [ ] Rewrite the Cursor skill as a thin router to the application prompt, shared standard, fact rules, work experience, project facts, and humanizer.
- [ ] Add Markdown examples for an ordinary company, misleading AI keyword, mixed role, missing technology, collaboration, technical challenge, short character limit, personal clarification, multi-question story diversity, and a one-sentence factual answer.
- [ ] For each example, record the input, expected decision, allowed evidence, rejected behavior, and acceptance criteria. Include acceptable and rejected outputs for the most important failure modes.
- [ ] Manually verify example word or character limits and fact sourcing.
- [ ] Commit the application-answer Markdown changes.

---

### Task 4: Create the cover-letter system

**Files:**
- Create: `career-tools/cover-letters/cover-letter.md`
- Create: `.cursor/skills/cover-letter/SKILL.md`
- Create: `career-tools/cover-letters/examples.md`

- [ ] Set the standard input to the JD only.
- [ ] Make the prompt infer company, title, dominant lane, role problem, and strongest verified evidence from the JD and authoritative facts.
- [ ] Define one central argument rather than a resume summary.
- [ ] Use exactly two paragraphs, target 130-180 words, and enforce a 200-word maximum.
- [ ] Make paragraph one connect Shubh to the company's stated work or the role's concrete problem.
- [ ] Make paragraph two support the fit with one or two connected examples, explain the contribution, and close with a direct invitation to discuss the role.
- [ ] Default to body-only output without an address block, date, or generic salutation.
- [ ] Use the JD as the default source for company claims. When company context is thin, focus on the role instead of inventing specificity or browsing automatically.
- [ ] Preserve prototype framing and ban generic openings, unsupported praise, lifelong passion, formal letter filler, technology inventories, copied resume bullets, context-poor metrics, and stiff closings.
- [ ] Create a model-invoked Cursor skill that routes to the cover-letter prompt, shared standard, fact rules, work experience, project facts, and humanizer.
- [ ] Add Markdown examples for Backend, Full Stack, AI, mixed roles, ordinary companies, thin company context, missing technology, context-poor metrics, early-career boundaries, and resume-summary failure.
- [ ] Include at least one acceptable two-paragraph letter under 200 words and rejected examples showing generic praise and resume-summary prose.
- [ ] Manually verify paragraph count, word count, fact sourcing, and natural voice.
- [ ] Commit the cover-letter Markdown changes.

---

### Final verification

- [ ] Confirm every skill points to its channel prompt and the shared communication standard.
- [ ] Confirm no live file still requires a pasted resume for application answers.
- [ ] Confirm no live LinkedIn rule mandates exactly three lines or a project plus metric.
- [ ] Confirm every cover-letter example has exactly two paragraphs and no more than 200 words.
- [ ] Confirm acceptable examples contain no unsupported facts or retired eInfochips claims.
- [ ] Confirm `resume-system/` remains unchanged.
- [ ] Run `git diff --check` and inspect the final diff for duplicated or contradictory rules.
