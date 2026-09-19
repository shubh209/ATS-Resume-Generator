# Digital Aid Seattle — Rainbow City MMS Master Story (2026)

Personal reference for interview prep. Status: architecture completed; the user subsequently
confirmed that the MMS implementation was completed and deployed to production. The locked resume
bullets below reflect that direct confirmation and supersede the earlier design-only audit status.

Items marked **[unconfirmed]** are logical inferences or facts stated once in conversation but not
yet built out with enough detail to write a bullet — verify before stating as fact or escalating to
a resume claim. See `resume-system/governance/FACT_RULES.md` (design-vs-build verbs, metric legibility) for the
rules this file must follow.

---

## 1. The Problem

Rainbow City is a Seattle performing-arts nonprofit running 12 ensembles for 400 active
members. Staff tracked membership, ensemble participation, and payment status across fragmented
systems: Band.us (communication, not a reliable roster source), spreadsheets, Zeffy (legacy
payment processor), and manual PDF/Excel handoffs. No single system showed who was active, who
had paid, or who needed follow-up. This caused duplicate records, delayed decisions, and
reconciliation overhead for volunteer-run staff with limited time.

Core issue: no single source of truth for member participation and payment status, compounded by
an unreliable communication-platform API (Band.us does not expose full roster/attendance data) and
a nonprofit's real constraint: a $2,000/year Azure credit ceiling.

## 2. Role

DAS (Digital Aid Seattle) is a volunteer software organization; Rainbow City is one of its client
engagements. Confirmed contribution: designed the MMS architecture and delivery plan for this
engagement — both the technical solution architecture (data model, state machine, security model,
integration design) and the delivery blueprint (phased rollout plan, governance/RACI, slice-by-slice
acceptance criteria). This was iterative: 10 rounds of design revision recorded in an iteration log,
plus an independent model-driven review specifically designed to reject the design if it found
unsourced requirements, security gaps, or scope violations.

Work was delivered through Agile sprints — **confirmed real**, not design-only, distinct from most
of the rest of this file.

**Current status:** The user confirmed that the MMS was implemented and deployed to production.
Confirmed implementation includes payment reconciliation, PostgreSQL persistence, shared
TypeScript API interfaces, and Azure Monitor metrics, logs, and audit trails.

## 3. Architecture (Designed)

**Stack (designed, not yet confirmed built):** React + MUI frontend, TypeScript Azure Functions/API,
Supabase (Postgres + Auth + Row Level Security) as a separate service from Azure, Stripe for
payments, read-only QuickBooks reconciliation, Forminator (WordPress) for intake, Mailchimp for
communication-preference lookup, Azure Key Vault for secrets, GitHub Actions for CI/CD.

**Data model (designed):** Member, MemberSensitive (Super-Admin-only), EnsembleInterest,
EnsembleMembership, PaymentRecord, PaymentCheckoutLink, AccessGrant/AccessRequest,
NotificationAttempt, ReconciliationException, AuditEvent, AdminUser, RoleAssignment. (12 entities —
flagged under Metric Legibility below; not used as a resume metric without approval.)

**Lifecycle state machine (designed):** Two independent state dimensions.
- Participation: Interested -> Active (manager records one attended practice) -> Inactive
  (six weeks unpaid, or manual).
- Payment: Not due (<3 weeks) -> Due (3-6 weeks) -> Paid (Stripe confirms) or
  Refunded/Failed (routes to exception review).
Kept deliberately separate so a payment failure never silently changes participation status.

**Security model (designed):** Dual-layer authorization — backend role/ensemble-scope check AND
independent Supabase Row Level Security at the database layer, so a bug in one layer doesn't expose
data. Sensitive fields (including accessibility data) isolated in a separate table, Super-Admin-only.
Every sensitive read, role change, access grant, and status change designed to produce an audit
event.

**Integration reliability (designed):** Durable Postgres-backed work/event ledger (idempotency keys,
attempt-state tracking) chosen over Azure Service Bus, deferred until measured throughput need
justifies the added operational surface — a deliberate build-vs-buy tradeoff under a real cost
ceiling. Stripe webhooks designed for signature verification + idempotent event-ID storage.
QuickBooks reconciliation designed as stable-reference-first matching; any ambiguous match becomes
an exception record rather than a silent guess.

**Delivery blueprint (designed):** 8 thin vertical slices (auth/RBAC shell -> intake queue ->
activation/roster -> Stripe payment mirror -> lifecycle reminders -> sensitive-field/export
isolation -> QuickBooks reconciliation -> operational hardening/handoff), each with its own
acceptance criteria and test coverage plan. Includes a RACI-style responsibility map and a
governance/quality plan (traceability, security review cadence, accessibility target WCAG 2.2 AA).

## 4. Process / Rigor Story (real differentiator)

Two independent audits were run against this design — one checking every architecture claim
against source-of-truth documents line by line, one checking against source code (finding none)
before any implementation claim was made. The design survived both without a rejected requirement.
This mirrors the "Independent review instructions" section built into the architecture document
itself: explicit adversarial review criteria a second model must apply before approving the design
— unsourced requirements, Band.us dependency creep, missing dual-layer auth, missing cost evidence,
missing client-ownership gates.

## 5. Metrics Ledger

| Metric | Value | Label |
|---|---|---|
| Design iteration rounds (Iteration Log) | 10 | [MEASURED — count of logged iterations] |
| Delivery blueprint slices | 8 | [MEASURED — count of designed slices] |
| Data model entities designed | 12 | [MEASURED — count in data model; **flagged, fails metric legibility check, not used in a bullet without explicit approval**] |
| Azure annual budget ceiling designed against | $2,000 | [MEASURED — stated client constraint; **flagged, needs tradeoff stated in-sentence to pass legibility, not used bare**] |
| Production user scale | 400 active members across 12 ensembles | [USER-CONFIRMED — September 18, 2026] |
| Acceptance criteria defined | 17 | [MEASURED — count of defined test criteria, all status Pending] |
| Lines of code / commits / test coverage | Not recorded | [UNKNOWN — do not invent] |
| Production deployment | Completed | [USER-CONFIRMED] |

## 6. Never Claim

- Do not claim load, latency, throughput, error-reduction, or time-savings metrics that were not
  measured. Production implementation and deployment are user-confirmed, but performance numbers
  remain unknown.
- Do not claim the $2,000 Azure budget was met — the source document calls this a future gate, not
  an achieved result.
- Do not use "12 entities" or "$2,000 budget" as a bare bullet metric — both flagged under Metric
  Legibility; only usable with explicit user approval and, for the budget figure, an in-sentence
  tradeoff.
- Do not claim solo authorship of the underlying business requirements (Rainbow City stakeholders,
  DAS product/process roles) — the design consolidates pain points and decisions from multiple named
  roles (PM, SA, PDM, QA) per the project's RACI map; confirmed personal contribution is the
  architecture and delivery-blueprint authorship itself, not the org's requirements gathering.
- Do not merge the React component-library ticket stream into the MMS story. The user confirmed
  they were separate DAS workstreams under the same role.

## 7. Confirmed Resume Bullets

### Full Stack lane (2 bullets, locked)

**Bullet 1 — tech: Postgres, dual layer authorization, Row Level Security · non-tech: ownership, cross-functional**
> Designed a Postgres data model and dual layer authorization architecture with Supabase Row Level Security and TypeScript Azure Functions for a membership and payment platform, splitting participation from payment status so a failed Stripe payment could not silently deactivate a paying member.

**Bullet 2 — tech: React, MUI, REST APIs, GitHub Actions CI/CD · non-tech: initiative, detail-oriented**
> Architected a React and MUI admin interface backed by REST APIs on Azure with a GitHub Actions CI/CD pipeline, scoping every screen to role based ensemble access so a manager could only ever query and view their own ensemble's members and payment status.

### Backend lane (4 bullets, locked)

**Bullet 1 — lifecycle data model and APIs**
> Designed a SQL data model and TypeScript REST APIs that kept member status changes consistent, allowing ensemble managers to see who was active or overdue without checking records manually.

**Bullet 2 — payment reconciliation**
> Built a payment reconciliation pipeline using Node.js, PostgreSQL, and webhooks from Stripe and Zeffy to match payments with member records and route mismatches to ensemble managers before they affected member status.

**Bullet 3 — shared API interfaces**
> Created shared TypeScript interfaces for member and payment data across the React frontend and Node.js backend, ensuring consistent API formats and reducing integration errors and development rework.

**Bullet 4 — production observability**
> Instrumented payment and member-data workflows with Azure Monitor metrics, logs, and audit trails, allowing developers to identify the exact stage of a production failure and trace changes to member records.

### AI Engineer lane

Not yet drafted.

## 8. Open Items / Not Yet Finalized

- **Debugging-in-production story.** User stated this happened at DAS and wanted to discuss it, but
  no concrete details (what bug, what environment, how caught, how fixed) were ever given. Cannot
  write a bullet or story section from this yet.
- **Academic Records async jobs.** User stated async jobs were used in the Academic Transfer Credit
  Solutions role and wanted to discuss it, but this is unconnected to the locked Academic Records
  Raw Context in `resume-system/facts/work-experience.md` (which only covers manual research + a *proposed*
  web-scraping automation). No concrete facts were ever given. Do not add to either role's file
  until resolved.
- **Full Stack set.** Four revised bullets are being reviewed separately; do not replace the two
  locked Full Stack bullets in this file until the user locks the complete revised set.
- **AI Engineer lane.** Zero bullets exist. If needed, draft from confirmed facts only (data model as
  provenance/evaluation-corpus framing, the iteration/independent-review process) — not from the
  rejected Claude-authored AI Engineer bullets, which describe unbuilt "AI sidecar" proposals as
  shipped work. See `career-stories/_drafts/DAS-unverified-draft-bullets.md` for what NOT to reuse.
