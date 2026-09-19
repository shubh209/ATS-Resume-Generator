# Internship Master Story — Internal Accounting Tool (2024)

This document is a personal reference, not a script. Goal: refresh full context before any interview, technical or behavioral, without blanking. Items marked **[unconfirmed]** were logical guesses discussed in prep, not things explicitly recalled — verify before stating as fact.

---

## 1. The Problem

Accounting team manually entered payment data (name, date, amount, method) from PDFs, faxed documents, old Excel sheets, and old bank statements. Each accountant kept their own spreadsheet — no sync between them. If one accountant needed data another had, they had to contact that person directly. As payment/document volume grew, this became unworkable.

Core issue: **no single source of truth**, and this mattered more than usual because it was financial data — accuracy and accountability were non-negotiable.

## 2. Team & Role

- Team: supervisor (senior, tech dept) + 2 interns (you + 1 other).
- Supervisor assigned tickets via Jira, did all PR reviews. Code review sessions twice a week.
- You: backend — building APIs to fetch/insert data under RBAC constraints, dashboard read speed, data correctness against accountant queries.
- Other intern: frontend.
- Collaboration point: connecting frontend/backend per business logic from stakeholders.
- Some pairing sessions happened directly with supervisor.
- Project was prototype/pilot stage when internship ended — actively used and given feedback by 7 real accountants, not just a demo. Considered **staging**, not full production.
- Architecture/full build was not completed within internship duration.
- **Internship dates: January 2024 – May 2024.**
- **Pilot sequence:** started with senior team members testing on mock/dummy data, then moved to real usage by 7 accountants with 10,000+ real records later in the internship.
- **Self-initiated contributions (not just assigned Jira tickets):** proposed the idea of OCR integration; proposed various improvements at different pipeline stages; proposed how to customize observability/logging for the system.

## 3. Architecture (Detailed)

**Diagram:**

<svg width="100%" viewBox="0 0 680 460" role="img">
<title>Final confirmed architecture of the internal accounting tool</title>
<desc>Accountant logs in through a React frontend on S3 and CloudFront, hits a Node/Express backend on Elastic Beanstalk with validation and RBAC layers, writes through a single transaction to Postgres RDS with an audit log table, backed by Secrets Manager and CloudWatch, deployed through GitHub Actions</desc>
<defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="black" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker></defs>

<g>
<rect x="190" y="30" width="300" height="52" rx="8" stroke="black" fill="none" stroke-width="1"/>
<text x="340" y="47" text-anchor="middle" dominant-baseline="central" font-size="14" font-weight="bold">Accountant</text>
<text x="340" y="64" text-anchor="middle" dominant-baseline="central" font-size="12">Email + password login</text>
</g>
<line x1="340" y1="82" x2="340" y2="106" stroke="black" stroke-width="1.5" marker-end="url(#arrow)"/>

<g>
<rect x="190" y="106" width="300" height="52" rx="8" stroke="black" fill="none" stroke-width="1"/>
<text x="340" y="123" text-anchor="middle" dominant-baseline="central" font-size="14" font-weight="bold">React Frontend</text>
<text x="340" y="140" text-anchor="middle" dominant-baseline="central" font-size="12">S3 + CloudFront, MUI forms</text>
</g>
<line x1="340" y1="158" x2="340" y2="182" stroke="black" stroke-width="1.5" marker-end="url(#arrow)"/>

<g>
<rect x="190" y="182" width="300" height="52" rx="8" stroke="black" fill="none" stroke-width="1"/>
<text x="340" y="199" text-anchor="middle" dominant-baseline="central" font-size="14" font-weight="bold">Node/Express API</text>
<text x="340" y="216" text-anchor="middle" dominant-baseline="central" font-size="12">AWS Elastic Beanstalk</text>
</g>
<line x1="340" y1="234" x2="340" y2="258" stroke="black" stroke-width="1.5" marker-end="url(#arrow)"/>

<g>
<rect x="190" y="258" width="300" height="52" rx="8" stroke="black" fill="none" stroke-width="1"/>
<text x="340" y="275" text-anchor="middle" dominant-baseline="central" font-size="14" font-weight="bold">Validation + RBAC</text>
<text x="340" y="292" text-anchor="middle" dominant-baseline="central" font-size="12">Route and data-layer checks</text>
</g>
<line x1="340" y1="310" x2="340" y2="334" stroke="black" stroke-width="1.5" marker-end="url(#arrow)"/>

<g>
<rect x="190" y="334" width="300" height="52" rx="8" stroke="black" fill="none" stroke-width="1"/>
<text x="340" y="351" text-anchor="middle" dominant-baseline="central" font-size="14" font-weight="bold">Postgres RDS</text>
<text x="340" y="368" text-anchor="middle" dominant-baseline="central" font-size="12">Single txn, entries + audit log</text>
</g>

<line x1="220" y1="386" x2="130" y2="410" stroke="black" stroke-width="1.5" marker-end="url(#arrow)"/>
<line x1="460" y1="386" x2="550" y2="410" stroke="black" stroke-width="1.5" marker-end="url(#arrow)"/>

<g>
<rect x="20" y="410" width="220" height="52" rx="8" stroke="black" fill="none" stroke-width="1"/>
<text x="130" y="427" text-anchor="middle" dominant-baseline="central" font-size="14" font-weight="bold">Secrets Manager</text>
<text x="130" y="444" text-anchor="middle" dominant-baseline="central" font-size="12">DB credentials, keys</text>
</g>
<g>
<rect x="440" y="410" width="220" height="52" rx="8" stroke="black" fill="none" stroke-width="1"/>
<text x="550" y="427" text-anchor="middle" dominant-baseline="central" font-size="14" font-weight="bold">CloudWatch</text>
<text x="550" y="444" text-anchor="middle" dominant-baseline="central" font-size="12">Access + error logs</text>
</g>
</svg>



**Repo:** Single monolith repo, backend + frontend in one codebase, deployed as separate AWS services (not one instance).

**Frontend:** React + MUI. Static build served via S3 + CloudFront. Conditionally renders fields/buttons based on user role — UX convenience only, never the real security boundary.

**Backend:** Node.js + Express + TypeScript. Runs on **AWS Elastic Beanstalk** (confirmed). Layered:
- **Auth layer** — email/password login, role attached to session at login.
- **RBAC middleware** — runs on every request; checks role before both the route AND the data-shaping layer (this second check was added after a real bug — see Section 5).
- **Validation layer** — required fields, types, business rules (amount > 0, valid date) before DB insert. Built validation covering multiple business rules for financial data entry (avoid citing an exact count — not a relevant metric here).
- **Business logic layer** — duplicate detection and Excel bulk import (row-by-row validation, partial success with per-row error reporting instead of failing the whole batch). Split transactions with distinct transaction IDs were ingested correctly as separate payment records. The later failure was in reporting, where the system could not determine whether separate records were independent payments or parts of one invoice.

**Database:** PostgreSQL on AWS RDS. Separate instances for staging vs production.
- Tables (likely 5–7): `users`, `roles` (or role field on users), `entries`/`payments` (name, date, amount, method, source ref, entered_by, timestamps), `documents` (tracks original PDF/fax/Excel source), `audit_log` (confirmed built).
- Foreign keys: `entries.entered_by` → `users.id`; `entries.source_document_ref` → `documents.id`.
- Indexes (logical, for search): `entries.date`, `entries.name`, `entries.amount`, `users.email`.

**Transactions:** Multi-table writes (e.g. entry + linked document ref) wrapped in a single atomic Postgres transaction — all-or-nothing, no orphaned records. (You personally found and fixed a bug here — Section 5, Option 3.)

**End-to-end data flow:**
Accountant logs in (email/password) → React form submit → Node/Express API (behind AWS load balancer, no separate API gateway — internal tool, small user base doesn't need one) → validation layer → RBAC check → single DB transaction (multi-table write) → Postgres RDS → Dashboard (nightly auto-refresh, or manual refresh) / Search (direct query, no caching layer).

**Why no caching on search:** decided after direct conversation with the accounting team — once an accountant accessed a record, low chance they'd access it again soon. Not an assumption, a decision informed by actual user behavior.

**Secrets:** AWS Secrets Manager — DB credentials, API keys. Not hardcoded, not plain `.env`.

**Logging/monitoring:** Custom access logging at middleware level — captures user identity, resource accessed, HTTP method/status, response time. Feeds CloudWatch. Built deliberately this granular because financial data needs an audit trail of who touched what, not just error debugging. No manual-process error-rate baseline existed before this system (there was nothing to compare against) — instead, the system was designed to measure each step itself as it ran: data insertion outcomes, failed cases, etc., rather than retroactively measuring improvement over the old manual process.

**CI/CD:** GitHub Actions. Triggers on merge to main. Steps: install deps → lint/build → deploy to staging. Backend deploys to AWS Elastic Beanstalk; frontend deploys to S3 + CloudFront. No formal automated test suite in the pipeline (see Testing, Section 6).

**Security policy:** Role changes require re-login to take effect (no real-time permission propagation). Password rotation every 3 months.

## 4. Data Ingestion & Edge Cases

**Sources:** legacy Excel sheets, PDFs, faxed documents, old bank statements. (Not sensitive to disclose — just old/manual paperwork formats.)

**Manual entry → OCR (partial):**
- Started with manual form entry to nail down consistency logic first.
- OCR introduced in final month of internship, did not get to fully build/integrate it before internship ended (see Section 7 — missed deadline story).

**Excel bulk import (logical structure):**
- Bulk upload endpoint, not one-by-one.
- Each row validated with same rules as manual entry.
- Failed rows flagged, don't block whole batch — partial success + error report.
- Valid rows inserted in transaction(s).

**Edge cases explicitly considered** (raised directly by accounting team while discussing their real workflow):
- **Split payments in reports** — an invoice total could arrive as several transactions with distinct transaction IDs and otherwise matching vendor information. Ingestion correctly stored each transaction separately, but stakeholder reports needed the transactions grouped under the invoice's total amount.
- **True duplicates** — same name, date, amount, method — accidental double entry, needs a check before insert.
- **Partial refunds** — negative amounts, needs sign validation.
- **Same-day/same-amount coincidences** — hard to distinguish from data alone; may need accountant confirmation.
- **Late corrections** — accountant realizes an amount was wrong after entry — ties to audit trail concept.
- **Concurrent entry** — two accountants entering same transaction near-simultaneously — race condition risk, needs DB constraint or optimistic locking **[unconfirmed if actually implemented]**.

**Core theme to repeat in interviews:** every edge case was treated as a **data integrity risk**, not just a UX inconvenience, because this was financial data — "finance is the most important part of the business."

## 5. Bug / Mistake Stories (candidates — pick per interview)

### Option 2 — RBAC gap (caught by supervisor in code review)
**Situation:** Supervisor flagged in review that a new-hire role could view financial fields it shouldn't, because the permission check was only at the route level, not the nested data-shaping layer.
**Task:** Fix the gap, make sure the pattern didn't repeat elsewhere.
**Action:** Audited every endpoint returning entry data, moved permission checks to the data-shaping layer, asked supervisor to re-review since this touched security.
**Result:** Fixed before pilot rollout. Learned RBAC needs enforcement at every layer touching sensitive data, not just the route entry point.

### Option 3 — Multi-table transaction bug (caught by self, during testing)
**Situation:** Testing split-payment flow, found that if the second table write failed mid-operation, the first write stayed committed — orphaned record, no linked document reference.
**Task:** Fix before this became a real data consistency risk.
**Action:** Wrapped the multi-table insert in a single Postgres transaction. Deliberately forced a failure mid-write to confirm rollback actually worked, didn't just assume it.
**Result:** No orphaned records reached pilot. Reinforced why atomic transactions matter specifically for financial systems.

### Option 4 — Split-payment reporting failure (reported by an accountant)
**Situation:** The ingestion system correctly stored each transaction from a split invoice because every transaction had its own ID. The problem appeared when an accountant prepared a stakeholder report. The system showed the transactions separately even though the accountant needed one vendor-level invoice total. For example, four transactions from a $100 invoice appeared as four report entries instead of one $100 total.
**Task:** Resolve a granularity mismatch: preserve transaction-level records during ingestion while rolling related transactions up to the invoice level for reporting.
**Root cause:** The source included an invoice ID, but the original system had no invoice-level table and did not store that identifier. Without an invoice entity or shared identifier, the reporting layer could not reliably distinguish several transactions from one invoice from independent payments by the same vendor. Independent payments had different invoice IDs.
**Options considered:**

1. **SQL view.** Group transactions by invoice ID when the report is queried. This required no schema change, avoided synchronization bugs, and was fast to ship. It would recompute the aggregation on each query, become slower at higher volume, leave no natural home for invoice-only fields, and bury business logic in SQL.
2. **Parent-child model.** Make the invoice a first-class parent record with transaction children. This would support faster reads, invoice-level fields, payment matching, and future partial-payment features. It required a schema migration, more complex insertion logic, and protection against parent-child synchronization errors.

**Tradeoff:** The SQL view favored immediate simplicity but carried future query and modeling costs. The parent-child model required more work upfront but gave the domain a structure that could support additional invoice features and higher volume.

**Decision:** Proposed the parent-child model because invoices were likely to support more features and records over time. The higher upfront cost was justified by clearer domain structure, room for invoice-level fields, and more scalable report reads.

**Approval and ownership:** The supervisor approved the proposed parent-child design. The user personally implemented the schema migration, wrote the business logic, and tested the result with SQL queries.

**Confirmed implementation:** Added an `invoices` table and an `invoice_id` foreign key to the transaction records, then changed the reporting path to work at invoice granularity. Historical records did not contain invoice IDs, so the backfill grouped them using available business fields such as name, date, payment method, and amount, with manual checking where needed.

**Completed implementation and validation:**

1. Create the invoice schema and transaction foreign key.
2. Backfill historical transactions into invoice groups.
3. Update ingestion to create or append to an invoice.
4. Point reports to the invoice table.
5. Add a reconciliation job comparing transaction sums with invoice totals.
6. Run the new path beside the old path behind a feature flag and compare outputs.
7. Cut reports over to the invoice table and monitor a reporting cycle.
8. Remove the old grouping logic after the new path is stable.

Testing covered creation and append behavior, totals, duplicate transaction IDs, end-to-end ingestion and reporting, foreign-key enforcement, backfill spot checks, intentional reconciliation failures, partial and late invoices, refunds, invalid invoice IDs, concurrent inserts, and old-versus-new report comparisons. The full rollout plan and test plan were completed.
**Result:** The accountant who raised the issue verified that the resulting report showed the required invoice-level total. Confirm any additional observable result or measured impact before drafting.

## 6. Testing

- Primarily manual endpoint testing (e.g. Postman), not a formal automated test suite — typical for an intern-built prototype under time constraints.
- Separate staging DB/environment before pilot accountants touched anything.
- Given the financial-data edge cases (duplicates, splits, negative amounts), these specific scenarios were manually tested more deliberately than a typical prototype would be, even without formal test coverage.
- Excel bulk import tested against real sample sheets from accountants — real-world malformed data was the actual risk, not synthetic test data.
- Real QA loop was pilot feedback — accountants using it live surfaced bugs faster than internal testing alone.
- Likely pilot bugs **[unconfirmed specifics]**: date format mismatches (Excel vs Postgres date types), incomplete search matches, an RBAC edge case caught by an accountant.
- Honest gap to name in interviews: no formal automated test suite / error-path coverage. Good "what I'd do differently" answer.

## 7. Non-Technical / Behavioral Stories

### Story A — RBAC mistake, disagreement, and how you handled being wrong
Based on your requirements understanding, you believed your original RBAC approach covered all cases. Supervisor was skeptical upfront but let you proceed, asking you to report back failures as you hit them rather than shutting the idea down outright. You explained your reasoning given company constraints and limited resources. The approach worked fine on the happy path but failed under error-path testing — latency issues and HTTP 429 failures under certain access patterns. You owned the gap, rebuilt with those edge cases considered.
**Core lesson:** think about how something breaks in production, not just whether it works for the expected case. There will always be more experienced/smarter people in the room — own your work, stay open to learning at any career stage, keep self-respect intact on both sides of a disagreement.
**LP fit:** Learn and Be Curious, Ownership, Earn Trust.

### Story B — OCR missed deadline, conflict with colleague, and resolution
You and the other intern were both assigned to research OCR integration, but roles weren't clearly split upfront, causing overlapping research and a disagreement: your approach favored latency/performance, colleague's favored cost. Both reasonable given real constraints. Lack of early alignment ate into time meant for the MVP research report — deadline missed.
**Resolution:** You and your colleague went back to first principles — revisited actual requirements/scope rather than defending individual approaches. Brought in supervisor for pipeline-design guidance specific to your use case. Went directly to the accounting department to understand which parts of their workflow were repetitive/automatable, and critically, what accuracy threshold OCR needed to clear versus human error — the real tradeoff, not just latency vs cost in isolation.
**Final decision:** Hybrid approach — prioritized cost and data accuracy over latency, since the system wasn't event-driven and could tolerate slower responses, but financial fields (company, transaction ID, amount, type, date) needed high extraction accuracy.
**Deadline recovery:** Expedited the next sprint, increased working hours including weekends, to complete the task before the final internship deadline — not out of obligation, but to follow through on ownership after already having missed once, and to leave a strong final impression.
**LP fit:** Are Right A Lot (grounded decision in data/user input), Dive Deep, Ownership, Deliver Results.

### Story C — Working style difference with the other intern [flagged, not fully developed]
Different core ideologies: colleague focused on UX — fewer clicks, attractive display, ease of use. You focused on storage/retrieval performance, latency, throughput, reliability, consistency. Colleague would sometimes propose features without considering system performance impact; tension between compromising reliability/speed vs. UX friction.
**Note:** This overlaps with Story B and was not separately developed into a full STAR story — revisit if needed for a specific "differing working styles" question.

### Story D — Accounting dept wanted a display feature that hurt latency [skipped, not developed]
Mentioned once: accounting wanted to display data in a way that worsened latency, prioritizing ease of use over performance/integrity. Not built out into a full story — revisit if a "conflicting stakeholder requirements" question needs a dedicated example beyond Story B.

## 8. Stakeholder Communication (general point, usable across multiple questions)

Biggest non-technical learning: constant communication with non-technical, cross-functional stakeholders (accounting dept). They didn't care which database or language/framework was used — they cared about data security, data integrity, and RBAC (new employees having less access). Learned to translate technical decisions into business-relevant terms (security, accuracy, accountability) rather than technical jargon.

## 8b. Metrics Ledger (for resume use)

- **7 accountants** — MEASURED. Confirmed pilot user count (Section 2).
- **10,000+ real records** — MEASURED. Confirmed pilot data volume (Section 2).
- **40% invoice processing time reduction** — **RETIRED ESTIMATE; do not use in resume bullets.** There was no formal manual-process baseline, and the locked full-stack set now uses observable workflow impact instead.

---

## 8c. Locked Resume Bullets — Full Stack (3-bullet set)

Locked wording. Tailor a resume by reordering these bullets, not rewriting them. Every bullet ends with business impact. Facts are sourced above (§3, §5, §6, §8b).

**Bullet 1 — end-to-end application and shared payment state**
> Integrated React and Material UI workflows with TypeScript, Node.js, Express, REST APIs, and PostgreSQL, centralizing access to 10,000+ payment records for seven accountants and reducing spreadsheet handoffs that caused inconsistent payment states.

**Bullet 2 — data-entry and retrieval workflow**
> Co-developed an Excel bulk-import workflow with a senior engineer and implemented payment validation, search, and dashboard APIs, reducing manual record entry and cross-checking while giving accountants one place to retrieve current payment status.

**Bullet 3 — UAT and application reliability**
> Conducted UAT with accountants during prototype demonstrations, traced invalid-input failures across React and Express, and standardized API error contracts, preventing workflow interruptions during user testing and reducing rework between the accounting, frontend, and backend teams.

Metrics: 7 accountants and 10,000+ records = MEASURED (§8b). Auth = email/password session, not OAuth/JWT. Frontend = React + Material UI, not Angular.

## 8d. Locked Resume Bullets — Backend (3-bullet set)

Locked wording. Tailor a resume by reordering these bullets, not rewriting them. Every bullet ends with business impact.

**Bullet 1 — REST APIs and shared payment state**
> Built payment creation and retrieval services using TypeScript, Node.js, Express, REST APIs, PostgreSQL, and AWS, centralizing 10,000+ records so seven accountants could access consistent payment status without coordinating across separate Excel sheets.

**Bullet 2 — security and transactional integrity**
> Secured payment data with role-based access control (RBAC), input validation, and PostgreSQL transactions, ensuring only authorized accountants could access records and incomplete updates did not affect reconciliation or reporting.

**Bullet 3 — delivery, monitoring, and UAT**
> Automated staging deployments with GitHub Actions and AWS, instrumented access and error monitoring through CloudWatch, and supported UAT with accounting users, helping the team diagnose backend failures before broader pilot use and reducing interruptions to payment workflows.

## 8e. Locked Resume Bullets — AI Engineer Supporting Experience (3-bullet set)

Locked wording. Tailor a resume by reordering these bullets, not rewriting them. These bullets demonstrate supporting data, reliability, and cloud engineering without claiming that the internship involved AI.

**Bullet 1 — data ingestion and structured storage**
> Built TypeScript and Node.js REST APIs and an Excel ingestion workflow that validated and stored 10,000+ payment records in PostgreSQL, giving seven accountants a consistent dataset instead of fragmented spreadsheets with conflicting payment states.

**Bullet 2 — data quality and traceability**
> Improved payment-data quality with duplicate checks, role-based access control, PostgreSQL transactions, and CloudWatch audit logging, preventing incomplete or unauthorized changes from affecting financial reconciliation and reporting.

**Bullet 3 — cloud delivery and user validation**
> Automated staging deployments on AWS with GitHub Actions and conducted UAT with accountants, resolving API error-handling failures so the team could iterate on the prototype without repeatedly disrupting payment-entry workflows.

---

## 9. Open Items / Not Yet Finalized

- Story C and Story D above are flagged as underdeveloped — revisit if you want dedicated STAR versions.
- Whether `audit_log` table was actually built during your internship — confirmed built (Section 3 table list can be treated as fact, not guess).
- Whether optimistic locking/concurrency handling was actually implemented is still unconfirmed.
- Specific pilot bugs beyond the three named bug stories are logical guesses, not confirmed incidents.
- Number of API endpoints intentionally not tracked — not a metric you want to use in bullets.
