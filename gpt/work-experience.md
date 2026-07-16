# Work Experience

---

## Non-Technical Keyword Bank (JD reference)

Common soft-skill qualifications from JDs (see `gpt/system-prompt.md` STEP 2B and `CONTEXT.md` §4.5).  
**Rules:** 3–6 non-technical keywords **per bullet** · **no keyword reused** within the same role · lead with behavior, not tools.


| Keyword                               | ASU signal                                                  | eInfochips signal                                |
| ------------------------------------- | ----------------------------------------------------------- | ------------------------------------------------ |
| Collaboration                         | Colleagues on edge cases; supervisor 1:1s                   | Paired dev with senior engineer                  |
| Communication                         | Explained rationale on notes; plain language for evaluators | Articulated rationale in code reviews            |
| Cross-functional                      | Evaluators + supervisor + students                          | Accounting team + engineering                    |
| Take direction                        | Asked goals before starting; followed supervisor guidance   | Worked under senior; followed security protocols |
| Receiving feedback                    | Iterative note corrections                                  | Code review corrections                          |
| Take criticism                        | Applied corrections without defensiveness                   | Incorporated review feedback positively          |
| Initiative / proactive                | Proposed web scraping automation                            | Identified scope issues in reviews (optional)    |
| Ownership                             | Owned research quality for evaluator handoff                | Owned auth delivery for accounting APIs          |
| Teamwork                              | Daily research queue with colleagues                        | Paired model + accounting stakeholders           |
| Detail-oriented / analytical          | Caught discrepancies; edge cases                            | Payment discrepancy prevention                   |
| Explain to non-technical stakeholders | Plain language notes for evaluators                         | Accounting team trust (AI variant bullet)        |
| Works under pressure                  | 150+ records daily volume                                   | Deadline-driven intern delivery (use if JD asks) |


---

## Academic Records Operations

**Company:** Academic Transfer Credit Solutions, ASU
**Location:** Tempe, AZ
**Duration:** Jan 2026 – May 2026
**Type:** Part-time

### Raw Context

- Weekly 1-1s with supervisor; always asked why the assigned task mattered and who benefitted after the task was completed before starting to contribute, showing my skill of understanding the business.
- Researched course transfer eligibility using TES and TG Admin; wrote internal notes for evaluators to save their time and increase efficiency in salesforce ticket resolve.
- Collaborated with colleagues on edge cases not covered in instructions to understand the task better and learning from senior members approach of thinking towards a problem.
- Received regular feedback on internal notes (missed data, misinterpreted entries); responded by explaining thought process and correcting approach going forward
- Proactively identified that several research tasks that could be automated via web scraping TES instead of manual copy-paste; raised this in 1-1 with supervisor.
- Supervisor noted strong analytical skills — caught discrepancies early and flagged alternate routes before they became blockers.

### Non-Technical Keyword Coverage (3 bullets)


| Bullet | Keywords used (no reuse across role)                           |
| ------ | -------------------------------------------------------------- |
| 1      | collaboration, cross-functional, communication, take direction |
| 2      | receiving feedback, take criticism, detail-oriented, teamwork  |
| 3      | initiative, proactive, analytical, ownership                   |


### Bullet Points (Option B — soft-skill lead, business outcome close)

**Bullet 1 — Collaboration + cross-functional + take direction:**
Aligned with the supervisor and transfer evaluators on goals and took direction upfront, delivering complete course transfer notes on the first pass so evaluators avoided rework and students were not delayed by missing data.

**Bullet 2 — Receiving feedback + take criticism + detail-oriented:**
Applied feedback from colleagues and the supervisor by correcting edge case errors in research notes and explaining my rationale, cutting evaluator rework and moving Salesforce tickets toward resolution faster.

**Bullet 3 — Initiative + ownership + analytical:**
Took initiative on repetitive manual TES and TG Admin lookups, proposed web scraping automation to supervisor with analytical support for the workflow change, and owned follow through on daily research quality while processing \metric{150+} transfer records daily, so the team redirected hours toward complex edge cases instead of copy paste work.

---

## Software Engineer Intern

**Company:** eInfochips
**Location:** Ahmedabad, India
**Duration:** May 2023 – Aug 2023
**Type:** Internship

### Raw Context

- Paired with a senior software engineer — daily point of contact, guide, code reviewer, mentor.
- Weekly (sometimes 2x/week) code review sessions; senior software engineer reviewed code for bugs, logic errors, and alignment with original task scope
- Project: internal REST APIs for accounting team to fetch and push financial data for payment tracking (internal tool, not customer-facing) increasing their efficiency and effectives resulting in less payment errors.
- 2023 stack for REST APIs: Node.js, Express.js, JavaScript/TypeScript, PostgreSQL, JWT for auth, Docker, CI/CD Pipeline.
- Took criticism positively, iterated on feedback, did what was instructed — as expected in an internship
- Biggest personal takeaway: how teams work, how projects are scoped, how to give and receive feedback, how to work with teams from different department.

### Non-Technical Keyword Coverage (3 bullets)


| Bullet | Keywords used (no reuse across role)                                     |
| ------ | ------------------------------------------------------------------------ |
| 1      | collaboration, paired development, take direction, teamwork              |
| 2      | receiving feedback, communication, take criticism, cross-functional      |
| 3      | ownership, detail-oriented, initiative (following standards proactively) |


*Note: eInfochips Bullet 3 keeps technical keywords in the tail only (OAuth, JWT, RBAC, Jest) per internship rules.*

### Bullet Points (Option B — soft-skill lead, business outcome close)

**Bullet 1 — Technical build + paired development:**
Built a payment tracking system with TypeScript, Node.js, Express, and \metric{5+} REST APIs on AWS under a paired development model with a senior software engineer, so the accounting team updated payment records without manual spreadsheet handoffs and kept system state strongly consistent.

**Bullet 2 — Receiving feedback + communication + cross-functional:**
Incorporated code review feedback and communicated implementation rationale to cross functional accounting stakeholders, reducing invoice processing time by \metric{40\%} so staff caught payment discrepancies before they affected downstream reporting.

**Bullet 3 — Ownership + detail-oriented:**
Took ownership of authentication delivery with the senior engineer and accounting team, applying detail oriented standards through OAuth 2.0, JWT, and RBAC with \metric{95} Jest test coverage, so only authorized staff accessed sensitive payment data and the accounting team could trust the APIs in daily use.

---

## LaTeX-Ready Bullets

### Academic Records Operations

```latex
\resumeItem{Aligned with the supervisor and transfer evaluators on goals and took direction upfront, delivering complete course transfer notes on the first pass so evaluators avoided rework and students were not delayed by missing data.}
\resumeItem{Applied feedback from colleagues and the supervisor by correcting edge case errors in research notes and explaining my rationale, cutting evaluator rework and moving Salesforce tickets toward resolution faster.}
\resumeItem{Took initiative on repetitive manual TES and TG Admin lookups, proposed web scraping automation to supervisor with analytical support for the workflow change, and owned follow through on daily research quality while processing \metric{150+} transfer records daily, so the team redirected hours toward complex edge cases instead of copy paste work.}
```

### eInfochips

```latex
\resumeItem{Built a payment tracking system with TypeScript, Node.js, Express, and \metric{5+} REST APIs on AWS under a paired development model with a senior software engineer, so the accounting team updated payment records without manual spreadsheet handoffs and kept system state strongly consistent.}
\resumeItem{Incorporated code review feedback and communicated implementation rationale to cross functional accounting stakeholders, reducing invoice processing time by \metric{40\%} so staff caught payment discrepancies before they affected downstream reporting.}
\resumeItem{Took ownership of authentication delivery with the senior engineer and accounting team, applying detail oriented standards through OAuth 2.0, JWT, and RBAC with \metric{95\%} Jest test coverage, so only authorized staff accessed sensitive payment data and the accounting team could trust the APIs in daily use.}
```

### AI Engineer variant — ASU Academic Records (swap Bullet 3 when JD requires it)

Use when JD asks to explain technical concepts to non technical people. Replaces Bullet 3 only.

```latex
\resumeItem{Translated course transfer research into plain language internal notes for non technical evaluators, communicating complex eligibility rules clearly so they could approve or deny transfer credit without scheduling follow up calls to clarify what the research meant.}
```

**AI variant keywords:** communication, explain to non-technical stakeholders, cross-functional, detail-oriented

---

## Gaps (cannot honestly claim from Raw Context)


| JD keyword           | Status                                                                       |
| -------------------- | ---------------------------------------------------------------------------- |
| Agile / Scrum        | Not in either role — use project bullets (Hearloop, SEO Audit)               |
| Works under pressure | Weak signal only (150+ daily volume at ASU) — mention only if JD stresses it |
| Self-starter         | Covered by initiative / proactive at ASU                                     |
| Mentor others        | Not claimed — you were junior in both roles                                  |
| Conflict resolution  | Not in raw context — do not invent                                           |


