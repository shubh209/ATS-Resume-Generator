# Golden JD — Software Engineer, Billing (Cursor / Anysphere, real posting)

**Use for regression:** Specialized, deeply technical backend IC role centered on usage-based billing: metering pipelines, subscription/entitlement systems, Stripe payment integration, and a financial ledger layer. Explicitly not a backend-generalist role and not a finance-ops role.
**Source:** Real Cursor (Anysphere) Software Engineer, Billing posting. Captured September 2026.
**Note on seniority/fit:** This is a mid-to-senior specialist posting. The "you may be a fit if" list assumes the candidate has already shipped a usage-based billing system in production, integrated deeply with Stripe, and built or maintained a financial ledger. Treat this primarily as a **seniority/specialization-mismatch regression case**: the tailoring system should surface the adjacent payment/reconciliation and correctness evidence honestly, and must NOT inflate an early-career candidate into someone who has owned production billing or a ledger.

---

## Software Engineer, Billing — Cursor (Anysphere)

### Company overview

Cursor builds an AI coding tool for professional programmers, combining research, design, and engineering. Flat org, small talent-dense team; values truth-seeking, spirited debate, and shipping code.

### Role overview

Evolve the systems that power how Cursor charges and reconciles revenue across millions of developers and enterprise teams. Work across the billing stack: usage metering pipelines, subscription and entitlement systems, payment integrations, and the ledger layer, to make billing accurate, scalable, and transparent. A deeply technical IC role, explicitly not finance ops and not a backend generalist wearing a billing hat.

### What you'll do

- Implement usage and billing system changes end-to-end, from UI updates and raw usage events at the edge to invoiced amounts in Stripe, including the metering pipeline, aggregation logic, entitlement enforcement, and ledger.
- Evolve the ledger system that is the source of truth for customer balances, credits, overages, and adjustments, with the correctness guarantees financial systems require.
- Integrate deeply with Stripe: subscriptions, usage records, invoices, webhooks, and edge cases like mid-cycle plan changes, prorations, and failed-payment recovery.
- Build billing APIs and internal tooling for product, finance, and customer success to query customer state, issue credits, and investigate anomalies.
- Improve observability across the billing pipeline: metering lag, reconciliation discrepancies, invoice accuracy.
- Partner with product, infrastructure, and finance to ship new pricing models with minimal operational risk.
- Own usage & limits, payments (Stripe + daily jobs), grants & promotions, ledger, and internal data insights. Not tax compliance or general finance infrastructure unless it intersects the billing system.

### You may be a fit if

- Shipped a usage-based billing system in production; opinions on metering architecture, idempotency, and exactly-once semantics.
- Integrated deeply with Stripe; understand its data model; handled erroring webhooks.
- Built or maintained a financial ledger and understand why it's required.
- Care about correctness so customers don't manually review invoices.
- Hold the tension between "move fast" and "do not lose revenue or trust."
- Comfortable shipping end-to-end, from scaling infrastructure to tweaking a UI component.

### Candidate-fit notes for regression testing

- **Expected lane:** Backend by domain (APIs, services, databases, pipelines, ledger, correctness). But see the fit caveat below; this is a specialist posting, not a general backend role.
- **Overall fit: STRETCH / likely mismatch.** The must-have bar (production usage-based billing, a maintained financial ledger, deep Stripe idempotency/exactly-once experience) exceeds the candidate's verified evidence. The honest system behavior is to present the strongest adjacent evidence and clearly report the gaps, not to manufacture billing/ledger ownership.
- **Strongest adjacent evidence (payment + reconciliation correctness):** DAS payment-reconciliation pipeline (Node.js, PostgreSQL, Stripe and Zeffy webhooks, mismatch routed to human review before it changes member status) is the closest real match. It demonstrates payment-webhook integration and correctness-before-side-effect thinking, but it is nonprofit membership reconciliation, NOT a usage-based billing system or a ledger. eInfochips payment-tracking APIs (10,000+ records, RBAC, PostgreSQL transactions) add financial-data correctness and transactional integrity as further adjacent evidence.
- **Stripe evidence:** Real but shallow. DAS used Stripe (and Zeffy) webhooks for reconciliation. The candidate has NOT worked with Stripe subscriptions, usage records, invoices, prorations, mid-cycle plan changes, or failed-payment recovery. Do not imply deep Stripe billing-model experience.
- **Correctness / idempotency / exactly-once:** Partial adjacent evidence only. PostgreSQL transactions (eInfochips), mismatch-to-human-review (DAS), and cache-aside/consistency work (Distributed Caching) show correctness thinking, but there is no verified metering pipeline, idempotency-key, or exactly-once semantics work. Report as a gap.
- **Ledger:** GAP. No verified experience building or maintaining a financial ledger. Do not claim it.
- **Observability match:** Azure Monitor (DAS), CloudWatch (eInfochips), Prometheus/Grafana (ClusterOps, Distributed Caching) map to the billing-pipeline observability asks as transferable evidence.
- **End-to-end / full-stack shipping:** Verified (DAS live system, projects), which matches the "scale infra to tweak a UI component" expectation.
- **Real gaps to handle honestly:** production usage-based billing, financial ledger, deep Stripe billing model (subscriptions/invoices/prorations/usage records), metering pipeline, idempotency/exactly-once semantics. All GAP. This is the core of the role, so the honest assessment is a weak fit despite good adjacent payment/correctness evidence.
- **Tailoring behavior to test:** Lead with DAS payment reconciliation and eInfochips transactional integrity as the closest adjacent evidence, frame correctness/observability transferably, and REPORT the billing/ledger/Stripe-depth gaps plainly rather than disguising them. The system should not turn "used Stripe webhooks for reconciliation" into "shipped a usage-based billing system." A red-flag/fit check should flag this as a stretch application before spending it.
- **Application-fit assessment:** Weak-to-moderate fit. Strong adjacent payment-reconciliation and financial-data-correctness evidence, but the role's defining requirements (production billing, ledger, deep Stripe) are genuine gaps for an early-career candidate. Useful regression case for testing honest gap-reporting and mismatch detection.
