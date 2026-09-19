# Work Experience

---

## Non-Technical Keyword Bank (JD reference)

Common soft-skill qualifications from JDs. Live selection and ordering rules are in `.agents/skills/resume-tailor/SKILL.md`.
**Rules:** **3–4 technical + 1–2 non-technical keywords per bullet** · **no non-technical keyword reused** within the same role · lead with the technical build, weave in 1–2 non-technical keywords.


| Keyword                               | DAS signal                                                       | ASU signal                                                  | eInfochips signal                                |
| ------------------------------------- | ---------------------------------------------------------------- | ----------------------------------------------------------- | ------------------------------------------------ |
| Collaboration                         | Maintainer-facing volunteer contribution flow                    | Colleagues on edge cases; supervisor 1:1s                   | Paired dev with senior engineer                  |
| Communication                         | Asked process questions before code; clarified access blockers   | Explained rationale on notes; plain language for evaluators | Articulated rationale in code reviews            |
| Cross-functional                      | Volunteer engineering across repos and org process               | Evaluators + supervisor + students                          | Accounting team + engineering                    |
| Take direction                        | Read docs, followed DAS-style planning, avoided drive-by diffs   | Asked goals before starting; followed supervisor guidance   | Worked under senior; followed security protocols |
| Receiving feedback                    | PR checklist and maintainer-review mindset                       | Iterative note corrections                                  | Code review corrections                          |
| Take criticism                        | Ordered revert when workflow started wrong                       | Applied corrections without defensiveness                   | Incorporated review feedback positively          |
| Initiative / proactive                | Spec-first approach before React and UI ticket work              | Built and improved automated data-quality checks            | Identified scope issues in reviews (optional)    |
| Ownership                             | Owned ramp-up and ticket planning before implementation          | Owned research quality for evaluator handoff                | Owned auth delivery for accounting APIs          |
| Teamwork                              | Contributed inside existing nonprofit repos                      | Daily research queue with colleagues                        | Paired model + accounting stakeholders           |
| Detail-oriented / analytical          | Traced setup, auth, build, test, lint, and E2E requirements      | Caught discrepancies; edge cases                            | Payment discrepancy prevention                   |
| Explain to non-technical stakeholders | Not primary signal                                               | Plain language notes for evaluators                         | Accounting team trust (AI variant bullet)        |
| Works under pressure                  | Not primary signal                                               | Not a primary signal                                        | Deadline-driven intern delivery (use if JD asks) |


---

## Software Engineer

**Company:** Digital Aid Seattle
**Location:** Remote
**Duration:** June 2026 – Present
**Type:** Volunteer

### Raw Context

- New to DAS; needed to contribute as a junior without tribal knowledge.
- DAS work covered two separate workstreams: React component-library maintenance and the Rainbow City membership management system (MMS).
- Cloned `component-library` and `program-management`; used a repo understanding pass to learn why the library exists and how to contribute.
- Worked through local setup friction with Node, yarn, and corepack.
- For ET-126, "Update to latest React versions", stopped unplanned coding, ordered a full revert, and required DAS-style flow: read docs, plan upgrade to React 19.x, PR checklist, install, build, test, tsc, lint, E2E, codemods locally before PR, and solid PR description.
- Diagnosed GitHub write access issues with `gh auth status` and clarified the need for maintainer-granted repo write access before forcing a broken publish path.
- For a loading indicator ticket, stopped immediate coding and required a spec/design plan first.
- Implemented and deployed the MMS to production for 400 active members across 12 ensembles.
- Implemented a third-party client-data pipeline into PostgreSQL, shared TypeScript interfaces between the React frontend and Node.js backend, and Azure Monitor metrics, logs, and audit trails across processing stages.
- Built payment reconciliation with PostgreSQL and webhooks from Stripe and Zeffy; mismatches were routed to ensemble managers for review.
- Used Claude Code during implementation and verified functions against acceptance criteria and production metrics.

### Non-Technical Keyword Coverage (2 bullets)

| Bullet | Keywords used (no reuse across role)                                      |
| ------ | ------------------------------------------------------------------------- |
| 1      | collaboration, communication, take direction, ownership                   |
| 2      | initiative, detail-oriented, receiving feedback, teamwork                 |

### Locked Resume Bullets — Full Stack (4-Bullet Set)

Preserve these four bullets for the Full Stack base resume. Tailoring may reorder them but must not rewrite them.

**Bullet 1 — membership application and shared status:**
Built and deployed a membership management application with React, TypeScript, HTML, and CSS for a nonprofit serving \metric{400} active members across \metric{12} ensembles, replacing scattered forms and spreadsheets with one place to track member status.

**Bullet 2 — payment reconciliation:**
Built a payment reconciliation workflow with Node.js, PostgreSQL, REST APIs, and payment webhooks, matching payments to member records and routing mismatches to ensemble managers before they changed member status.

**Bullet 3 — shared API interfaces:**
Created shared TypeScript interfaces for member and payment data across the React frontend and Node.js backend, ensuring consistent API formats and reducing integration errors and development rework.

**Bullet 4 — production observability:**
Instrumented payment and member-data workflows with Azure Monitor metrics, logs, and audit trails, allowing developers to identify the exact stage of a production failure and trace changes to member records.

### Locked Resume Bullets — Backend (4-Bullet Set)

**Bullet 1 — lifecycle data model and APIs:**
Designed a SQL data model and TypeScript REST APIs that kept member status changes consistent, allowing ensemble managers to see who was active or overdue without checking records manually.

**Bullet 2 — payment reconciliation:**
Built a payment reconciliation pipeline using Node.js, PostgreSQL, and webhooks from Stripe and Zeffy to match payments with member records and route mismatches to ensemble managers before they affected member status.

**Bullet 3 — shared API interfaces:**
Created shared TypeScript interfaces for member and payment data across the React frontend and Node.js backend, ensuring consistent API formats and reducing integration errors and development rework.

**Bullet 4 — production observability:**
Instrumented payment and member-data workflows with Azure Monitor metrics, logs, and audit trails, allowing developers to identify the exact stage of a production failure and trace changes to member records.

### Locked Resume Bullets — AI Engineer Supporting Experience (3-Bullet Set)

Preserve these three bullets in this order. They support AI Engineer applications through data pipelines, human review, and production observability without implying that the DAS role involved building an AI model.

**Bullet 1 — data ingestion and traceability:**
Built a PostgreSQL data pipeline on Azure to ingest and trace third-party records for \metric{400} active members across \metric{12} ensembles, creating a consistent data foundation for payment reconciliation, reporting, and future automation.

**Bullet 2 — reconciliation and human review:**
Built a payment reconciliation pipeline using Node.js, PostgreSQL, and Stripe and Zeffy webhooks to match payments with member records and route mismatches for human review before incorrect payment data changed member status.

**Bullet 3 — production observability:**
Instrumented production payment and member-data workflows with Azure Monitor metrics, logs, and audit trails, making failures traceable to the exact processing stage and preserving a history of changes to member records.

---

## Data Management Intern

**Company:** Academic Transfer Credit Solutions, ASU
**Location:** Tempe, AZ
**Duration:** Jan 2026 – May 2026
**Type:** Part-time

### Raw Context

- Maintained a data pipeline using Python and SQL to process, sanitize, and ingest course records, university information, and transfer rules from Arizona colleges and universities.
- Built, improved, and monitored automated data-quality checks that flagged anomalies for human review before the records reached evaluators and prospective students.
- Exported case data to Excel and used SQL queries to identify a recurring process issue.
- Helped validate the resulting process improvement; average review time fell from seven to four minutes and related support tickets fell by approximately 30%.

### Locked Resume Bullets — Shared 3-Bullet Set

Use all three bullets for Full Stack and Backend resumes. AI Engineer resumes use the first two to preserve the locked one-page format. Do not rewrite, substitute, or reorder them during JD tailoring.

**Bullet 1 — case analysis and measured process improvement:**
Analyzed student transfer-credit cases using Excel and SQL queries to uncover a recurring process issue, helping cut average review time from 7 to 4 minutes and reduce related support tickets by approximately 30%.

**Bullet 2 — data pipeline maintenance:**
Maintained a data pipeline using Python and SQL to clean course and transfer-rule records from Arizona colleges and universities, helping evaluators provide prospective students with accurate transfer-credit information.

**Bullet 3 — automated data validation:**
Automated data validation with Python and SQL to catch missing or inconsistent course information and flag questionable records for human review, helping evaluators keep transfer-credit results accurate.

---

## Software Engineer Intern

**Company:** eInfochips
**Location:** Ahmedabad, India
**Duration:** Jan 2024 – May 2024
**Type:** Internship

### Raw Context

- Paired with a senior software engineer — daily point of contact, guide, code reviewer, mentor.
- Weekly (sometimes 2x/week) code review sessions; senior software engineer reviewed code for bugs, logic errors, and alignment with original task scope
- Project: internal REST APIs for accounting team to fetch and push financial data for payment tracking (internal tool, not customer-facing) increasing their efficiency and effectiveness resulting in less payment errors.
- Pilot scale: 7 real accountants using it live against 10,000+ real payment records.
- Stack (confirmed per eInfochips.md master story): Node.js, Express.js, TypeScript, React + MUI (frontend), PostgreSQL on AWS RDS, AWS (Elastic Beanstalk, S3/CloudFront, Secrets Manager, CloudWatch), GitHub Actions CI/CD. Auth is email/password session with role attached at login (NOT OAuth/JWT). Multi-table writes wrapped in atomic Postgres transactions. RBAC enforced at both route and data-shaping layer.
- Took criticism positively, iterated on feedback, did what was instructed — as expected in an internship
- Biggest personal takeaway: how teams work, how projects are scoped, how to give and receive feedback, how to work with teams from different department.

### Non-Technical Keyword Coverage (3 bullets)


| Bullet | Technical keywords (3–6) | Business / collaboration signal |
| ------ | ------------------------- | ------------------------------- |
| 1 | React, Material UI, TypeScript, Node.js, REST APIs, PostgreSQL | shared payment state, reduced handoffs |
| 2 | Excel bulk import, validation, search, dashboard APIs | senior collaboration, reduced manual work |
| 3 | UAT, React, Express, API error contracts | stakeholder testing, reduced workflow interruption and rework |


*Locked rule: internship bullets lead with the technical build, include 3–6 relevant terms naturally, and end with explicit business impact. Auth is email/password session, not OAuth/JWT. Frontend is React + MUI, not Angular.*

### Locked Resume Bullets — Full Stack (3 Bullet Set)

Tailor by reordering these approved bullets, not rewriting them.

**Bullet 1 — end-to-end application and shared payment state:**
Integrated React and Material UI with TypeScript, Node.js, REST APIs, and PostgreSQL, centralizing \metric{10{,}000+} payment records for \metric{7} accountants and reducing spreadsheet handoffs that caused conflicting payment states.

**Bullet 2 — data-entry and retrieval workflow:**
Co-developed an Excel bulk-import workflow with a senior engineer and built validation, search, and dashboard APIs, reducing manual data entry while giving accountants one place to retrieve current payment status.

**Bullet 3 — UAT and application reliability:**
Conducted UAT with accountants during prototype demonstrations, traced invalid-input failures across React and Express, and standardized API error contracts, preventing workflow interruptions during user testing and reducing rework between the accounting, frontend, and backend teams.

### Locked Resume Bullets — Backend (3 Bullet Set)

Tailor by reordering these approved bullets, not rewriting them.

**Bullet 1 — REST APIs and shared payment state:**
Built payment creation and retrieval services using TypeScript, Node.js, Express, REST APIs, PostgreSQL, and AWS, centralizing \metric{10{,}000+} records so \metric{7} accountants could access consistent payment status without coordinating across separate Excel sheets.

**Bullet 2 — security and transactional integrity:**
Secured payment data with role-based access control (RBAC), input validation, and PostgreSQL transactions, ensuring only authorized accountants could access records and incomplete updates did not affect reconciliation or reporting.

**Bullet 3 — delivery, monitoring, and UAT:**
Automated staging deployments with GitHub Actions and AWS, instrumented access and error monitoring through CloudWatch, and supported UAT with accounting users, helping the team diagnose backend failures before broader pilot use and reducing interruptions to payment workflows.

### Locked Resume Bullets — AI Engineer Supporting Experience (3 Bullet Bank; use first 2)

Tailor by reordering these approved bullets, not rewriting them. Do not imply that the internship involved AI or machine learning.

**Bullet 1 — data ingestion and structured storage:**
Built TypeScript and Node.js REST APIs with an Excel ingestion workflow to validate and store \metric{10{,}000+} payment records in PostgreSQL, so \metric{7} accountants could track payment status in one system instead of separate spreadsheets.

**Bullet 2 — data quality and traceability:**
Improved payment-data quality with duplicate checks, role-based access control, PostgreSQL transactions, and CloudWatch audit logging, preventing incomplete or unauthorized changes from affecting financial reconciliation and reporting.

**Bullet 3 — cloud delivery and user validation:**
Automated staging deployments on AWS with GitHub Actions and conducted UAT with accountants, resolving API error-handling failures so the team could iterate on the prototype without repeatedly disrupting payment-entry workflows.

---

## LaTeX-Ready Bullets

### Digital Aid Seattle

```latex
\resumeProjectHeading
  {Software Engineer, Digital Aid Seattle, Remote}{June 2026 -- Present}
\resumeItem{Built and deployed a membership management application with React, TypeScript, HTML, and CSS for a nonprofit serving \metric{400} active members across \metric{12} ensembles, replacing scattered forms and spreadsheets with one place to track member status.}
\resumeItem{Built a payment reconciliation workflow with Node.js, PostgreSQL, REST APIs, and payment webhooks, matching payments to member records and routing mismatches to ensemble managers before they changed member status.}
\resumeItem{Created shared TypeScript interfaces for member and payment data across the React frontend and Node.js backend, ensuring consistent API formats and reducing integration errors and development rework.}
\resumeItem{Instrumented payment and member-data workflows with Azure Monitor metrics, logs, and audit trails, allowing developers to identify the exact stage of a production failure and trace changes to member records.}
```

### Data Management Intern

```latex
\resumeItem{Analyzed student transfer-credit cases using Excel and SQL queries to uncover a recurring process issue, helping cut average review time from 7 to 4 minutes and reduce related support tickets by approximately 30\%.}
\resumeItem{Maintained a data pipeline using Python and SQL to clean course and transfer-rule records from Arizona colleges and universities, helping evaluators provide prospective students with accurate transfer-credit information.}
\resumeItem{Automated data validation with Python and SQL to catch missing or inconsistent course information and flag questionable records for human review, helping evaluators keep transfer-credit results accurate.}
```

### eInfochips

```latex
\resumeItem{Integrated React and Material UI with TypeScript, Node.js, REST APIs, and PostgreSQL, centralizing \metric{10{,}000+} payment records for \metric{7} accountants and reducing spreadsheet handoffs that caused conflicting payment states.}
\resumeItem{Co-developed an Excel bulk-import workflow with a senior engineer and built validation, search, and dashboard APIs, reducing manual data entry while giving accountants one place to retrieve current payment status.}
\resumeItem{Conducted UAT with accountants during prototype demonstrations, traced invalid-input failures across React and Express, and standardized API error contracts, preventing workflow interruptions during user testing and reducing rework between the accounting, frontend, and backend teams.}
```

### eInfochips — Backend

```latex
\resumeItem{Built payment creation and retrieval services using TypeScript, Node.js, Express, REST APIs, PostgreSQL, and AWS, centralizing \metric{10{,}000+} records so \metric{7} accountants could access consistent payment status without coordinating across separate Excel sheets.}
\resumeItem{Secured payment data with role-based access control (RBAC), input validation, and PostgreSQL transactions, ensuring only authorized accountants could access records and incomplete updates did not affect reconciliation or reporting.}
\resumeItem{Automated staging deployments with GitHub Actions and AWS, instrumented access and error monitoring through CloudWatch, and supported UAT with accounting users, helping the team diagnose backend failures before broader pilot use and reducing interruptions to payment workflows.}
```

### eInfochips — AI Engineer Supporting Experience

```latex
\resumeItem{Built TypeScript and Node.js REST APIs with an Excel ingestion workflow to validate and store \metric{10{,}000+} payment records in PostgreSQL, so \metric{7} accountants could track payment status in one system instead of separate spreadsheets.}
\resumeItem{Improved payment-data quality with duplicate checks, role-based access control, PostgreSQL transactions, and CloudWatch audit logging, preventing incomplete or unauthorized changes from affecting financial reconciliation and reporting.}
\resumeItem{Automated staging deployments on AWS with GitHub Actions and conducted UAT with accountants, resolving API error-handling failures so the team could iterate on the prototype without repeatedly disrupting payment-entry workflows.}
```

---

## Gaps (cannot honestly claim from Raw Context)


| JD keyword           | Status                                                                       |
| -------------------- | ---------------------------------------------------------------------------- |
| Agile / Scrum        | Not in either role — use project bullets (Hearloop, SEO Audit)               |
| Works under pressure | Not supported by the locked ASU bullets                           |
| Self-starter         | Covered by initiative / proactive at ASU                                     |
| Mentor others        | Not claimed — you were junior in both roles                                  |
| Conflict resolution  | Not in raw context — do not invent                                           |
