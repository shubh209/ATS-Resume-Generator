# Hearloop

## Product

Hearloop is a multi-tenant voice micro-feedback platform. A **Partner** creates
a Capture link or embeds a capture surface; an **End user** records a short
audio response; Hearloop runs its asynchronous **Pipeline** and returns
structured **Insights** through the Partner dashboard, webhook delivery, or an
urgent-alert email path.

The primary capture surface is an in-person QR code or shared link that opens
Hearloop's Hosted capture page. The website widget and `@hearloop/react` SDK are
secondary surfaces for Partners with existing web traffic.

## Core terms

| Term | Meaning |
| --- | --- |
| **Partner** | The business account that owns credentials, settings, Sessions, and delivery configuration |
| **End user** | The person who records feedback and has no Hearloop account |
| **Capture link** | A durable Partner-created QR or shareable link that mints a fresh Session for each capture attempt |
| **Hosted capture** | Hearloop's public recording page, opened through a scoped Session token |
| **Session** | One feedback-capture attempt and its lifecycle from creation to completion, failure, or expiry |
| **Pipeline** | The asynchronous validate, transcribe, analyze, webhook-delivery, and expiry processing chain |
| **Insights** | The transcript and structured sentiment, topics, urgency, and flags produced for a Session |
| **Target** | The Partner-defined subject of feedback, such as a location, service bay, campaign, or product |
| **Business context** | Optional Partner-controlled text used to make analysis specific to the Partner's services |
| **Insights query** | A bounded Partner-only question over eligible Sessions; the current implementation is only a count demo |

## Status vocabulary

| Status | Meaning in this file |
| --- | --- |
| **Released** | Integrated or applied to the deployed environment with direct evidence |
| **Implemented** | Code exists and scoped verification passed; production activation is not implied |
| **Builder demo** | Implemented portfolio surface with explicit limitations; not a validated Partner product |
| **Planned** | Designed or approved but not confirmed working |
| **Retired** | Previously built and later removed |
| **Unknown** | No reliable evidence is recorded |

## Current state

- The deployed baseline supports Partner authentication, Capture links, Hosted
  capture, the widget/React SDK, signed S3 uploads, the asynchronous Pipeline,
  dashboard Insights, webhooks, and health checks.
- Capture-link Target attribution and the dashboard's real-data path are built.
- Business context is optional Partner-controlled text entered manually or
  from a starter template.
- The Crawl4AI/FastAPI website-import feature is **retired**. Its API routes,
  worker, UI, sidecar, dependencies, and spike artifacts were removed.
- S3 version-aware primitives and versioned upload-grant issuance are
  **implemented**, but the end-to-end media-pinning flow is incomplete.
- Neon migrations 010 and 011 are **released**. New Sessions still default to
  `legacy-v0`; the recorded production state had no `versioned-v1` Sessions,
  upload grants, finalize receipts, or pinned Recordings.
- Insights query slice 1 is an **implemented builder demo**: Partner-authenticated
  count queries only, feature flag off by default, at most a 90-day range,
  Partner-scoped completed `versioned-v1` Sessions, and a stub evidence URL.
  List, quote, real evidence browsing, and Partner rollout are not built.
- No production Partner count, live-business usage volume, or validated
  customer outcome is recorded.

## Tech stack

| Area | Verified technology | Role |
| --- | --- | --- |
| Languages | TypeScript, JavaScript, SQL, HTML, CSS | Shared monorepo implementation |
| API | Node.js 20, Fastify 5, Kysely | HTTP routes, authentication, Partner scoping, and database access |
| Web | Next.js 15 App Router, React 19 | Hosted capture, dashboard, docs, and settings |
| Async | BullMQ, Upstash Redis | Pipeline queues and workers |
| Data | PostgreSQL 16 on Neon | Partner, Session, Recording, Insights, delivery, and grant state |
| Media | AWS S3, MediaRecorder API | Browser recording, signed upload, and private audio storage |
| AI | Groq Whisper, AWS Bedrock Nova Lite, Claude Haiku fallback | Transcription and structured classification |
| Infrastructure | AWS EC2, ECR, CloudWatch, Vercel, Caddy | API/workers, images, metrics, frontend, and TLS |
| Delivery and security | HMAC, bcrypt, Node crypto, AWS SES | Webhook signatures, credentials, dashboard sessions, and urgent alerts |
| Operations | Docker, GitHub Actions, Pino, k6, OWASP ZAP, Turborepo, npm workspaces | Build, deploy, logging, testing, and monorepo orchestration |

Python, FastAPI, and Crawl4AI are not current stack entries. They belonged to
the retired website-import sidecar.

## Problem and value

Traditional feedback forms ask customers to choose a rating or type into a
text box after a service interaction. Many customers skip that work, leaving
businesses with shallow ratings, spreadsheet exports, or voicemails that are
slow to interpret.

Hearloop lets an End user speak for a few seconds. The Partner receives a
transcript and structured labels such as sentiment, topics, urgency, and
flags. Target attribution can associate a Session with the location, service,
campaign, counter, or other subject selected by the Partner's Capture link.

This is a product hypothesis supported by a working portfolio system, not by
recorded paying-customer or live-business adoption data.

## My role

Solo builder responsible for product scope, architecture, implementation,
testing, and deployment, with AI coding tools used as assistants.

- Designed the Partner/End-user boundary, Session lifecycle, public-token
  capture flow, Target attribution, and dashboard behavior.
- Built the Fastify API, PostgreSQL data model, BullMQ Pipeline, Groq
  transcription, Bedrock classification, webhook delivery, and health paths.
- Built the Next.js dashboard and Hosted capture surface, `widget.js`,
  `@hearloop/react`, and the QuickLube reference site.
- Built the Docker/ECR/EC2 deployment path and used Neon, Upstash, Vercel, S3,
  k6, and ZAP to keep the portfolio deployment inexpensive and observable.
- Implemented media-pinning prerequisites: schema, S3 version-aware operations,
  and replay-safe upload grants. Did not complete or activate the full protocol.
- Implemented Insights query slice 1 as a feature-flagged builder demo. Did not
  complete the approved count/list/quote product or its Partner launch gates.
- Retired the website importer after deciding its maintenance and product value
  did not justify keeping the Crawl4AI/FastAPI sidecar.

## Verified capabilities

| Capability | Status | Verified boundary |
| --- | --- | --- |
| Partner signup and dashboard login | Released baseline | Email/password dashboard session; optional server-side Partner secret key |
| Capture links and QR codes | Implemented and API-E2E verified | Mint Hosted capture Sessions with Target metadata |
| Target-aware dashboard | Implemented | Real API payloads; no dashboard mock arrays remain |
| Hosted capture | Released baseline | Public-token recorder reached from a Capture link or direct share |
| Website widget and React SDK | Released baseline | Browser-safe embed key plus allowed-origin checks |
| Signed S3 direct upload | Released baseline | Audio bypasses the API process |
| Pipeline | Released baseline | Validate, transcribe, analyze, webhook delivery, and expiry |
| Structured Bedrock analysis | Implemented | Forced tool output; transcript, business context, and Target remain separate inputs |
| Partner webhooks | Released baseline | HMAC signatures, retry identity, SSRF protections, and retry handling |
| Urgent-alert email | Implemented code path | SES delivery remains constrained by sender/sandbox configuration |
| Manual/template business context | Implemented | Optional Partner-controlled text used during analysis |
| Website business-context import | Retired | No current route, worker, UI, sidecar, or dependency |
| S3 version-aware storage operations | Implemented, inactive foundation | Checksum-aware signed PUT and exact-version HEAD, GET, and DELETE |
| Versioned upload grants | Implemented, inactive foundation | Public/authenticated issuance, safe replay, conflict handling, legacy compatibility |
| Media-pinning database schema | Released | Migrations 010 and 011 applied; production Sessions remained `legacy-v0` |
| End-to-end media pinning | Planned | Finalize pinning, worker reads, exact deletion, abandoned-upload cleanup, clients, telemetry, and rollout remain |
| Insights query count demo | Builder demo | Flagged Partner-only count path over completed pinned Sessions; evidence URL is a stub |
| Insights query list/quote/evidence product | Planned | Evaluation gates, evidence browsing, list/quote retrieval, and rollout remain |
| RAG, MCP access, adaptive follow-up | Planned or discussed | No confirmed implementation |

## How the released capture path works

1. A Partner configures a Capture link, Hosted capture URL, or website embed.
2. The End user opens a scoped Session and records audio in the browser.
3. The browser receives a signed URL and uploads directly to private S3.
4. Finalize submits the Session and returns without waiting for AI work.
5. EC2 BullMQ workers validate the audio, transcribe it through Groq, classify
   it through Bedrock, persist Insights in PostgreSQL, and attempt delivery.
6. The Partner reads the result in the dashboard or receives signed webhook
   JSON; qualifying negative and urgent Insights can enter the email path.

The Next.js application on Vercel proxies browser HTTPS requests to the EC2 API.
The API and workers currently share one EC2 instance.

## Implemented but inactive media path

For a Session explicitly marked `versioned-v1`, the upload routes can validate
the proposed media description, create a checksum-aware S3 upload grant, store
the authoritative response, safely replay the same request, and reject
conflicting retries. The storage module can address an exact S3 VersionId.

This does not yet make a Session's Recording immutable evidence. Finalize does
not pin the uploaded version, workers do not read from a pin, cleanup does not
own every abandoned version, capture clients do not implement the new contract,
and production Session creation still uses `legacy-v0`.

## Insights query builder demo

The current slice exposes a feature-flagged Partner dashboard panel and
authenticated count route. It accepts bounded count filters, enforces Partner
scope, requires completed `versioned-v1` Sessions, returns a valid zero count,
and refuses unsupported intents or invalid ranges.

The demo does not provide real evidence browsing. Its evidence URL is a stub,
the production query corpus was empty at the recorded migration state, and the
larger Cited-answer design remains unfinished.

## Measurements and claim policy

Measurements are evidence, not automatic resume material. Agents may use a
number in downstream writing only when the target document's metric rules
accept it and the number communicates recognizable scale, performance, risk,
or business value. Verification counts and internal implementation vocabulary
belong in engineering evidence unless the user explicitly approves them.

### Recruiter-legible measured results

| Measurement | Result | Scope |
| --- | --- | --- |
| Load test | 200 concurrent users, 149 ms p95, 0% errors | k6 against the live API |
| Soak test | 20 virtual users for 10 minutes, 116 ms p95 | k6 stability check |
| Deployment time | About 15 minutes manually to about 60 seconds automated | GitHub Actions deployment workflow |
| Docker runtime CVEs | 46 to 0 | Production runner image scan |
| Redis health-check command volume | About 36,000/day to about 7,000/day | Cache and queue-count correction after exhausting the free-tier cap |
| EC2 root volume | 100% used to 18% used | Image cleanup plus deploy-time pruning |
| ECR storage | 9,772 MB to about 75 MB | 91 images reduced to one retained image |

### Engineering evidence; not automatic resume metrics

- Production migrations 010 and 011 were applied while 1,882 existing Sessions
  remained `legacy-v0`; this proves compatibility at the schema release, not
  adoption of the new protocol.
- The last recorded full API suite for the Insights-query work was 240 passed,
  2 pre-existing environment-fixture failures, and 1 skipped. The suite was not
  fully green.
- Insights query slice 1 added 21 dedicated test cases across six files. This is
  verification evidence, not user impact.
- The React SDK's last recorded baseline was 69 of 72 tests passing, with three
  stale `apiKey` versus `embedKey` expectation failures.
- The classifier synthetic diagnostic was 17 of 23. It is not a launch gate,
  production accuracy result, or Partner outcome.
- Historical classification cost and latency were based on a very small live
  sample. Do not generalize them as production-scale performance.
- The infrastructure change from roughly $35/month to $9.60/month is factual,
  but the earlier architecture was self-selected. Do not turn it into a resume
  impact claim without explicit user approval.

### Unknown or unvalidated

- Paying customer count and production Partner count
- Real completed Sessions from live businesses at meaningful scale
- Production webhook success rate and Session completion rate at scale
- Voice-versus-form completion lift
- Staff time saved per feedback item
- Partner demand for Insights query, evidence browsing, or webhook replay
- Pilot-safe privacy, retention, alert-delivery, and operational outcomes

## Never claim

- Paying customers, production usage, adoption, retention improvement, or
  validated customer outcomes.
- Website business-context import, Crawl4AI, or the FastAPI scraper sidecar as a
  current capability. The feature was retired.
- End-to-end media-evidence pinning or active `versioned-v1` production usage.
- Insights query as a launched Partner product. Only a count-only builder demo
  exists, the feature flag defaults off, and its evidence URL is a stub.
- Query list/quote retrieval, real citations, RAG, MCP access, adaptive
  follow-up, a knowledge graph, fine-tuning, or a feedback knowledge base.
- A completed automotive service-recovery workflow. Hearloop does not identify
  the customer/order or track acknowledgement, assignment, resolution, and outcome.
- A fully green API or React SDK suite, or exhaustive CI enforcement, until
  fresh evidence replaces the recorded failures.
- Pilot-safe or broadly production-ready operation merely because the deployed
  baseline and health endpoints respond.
- Universal prompt-injection resistance or production classifier accuracy from
  local contracts and a synthetic diagnostic.
- Full production webhook or urgent-email delivery success.
- The website widget as Hearloop's only or primary capture surface.

## Tradeoffs

- The asynchronous Pipeline keeps capture fast but means Insights arrive later
  through the dashboard or delivery channels.
- Direct S3 upload keeps audio off the small API instance but adds a browser-to-
  storage step and makes media ownership/integrity a separate protocol concern.
- Nova Lite keeps model cost low; Haiku is used only after primary structured
  output fails validation.
- Neon and Upstash reduce always-on infrastructure cost but add cold-start and
  Redis-quota constraints.
- The API and workers share one EC2 instance, which is appropriate for a
  portfolio deployment but not evidence of broad-production resilience.
- Excluding `legacy-v0` Sessions from Insights query protects evidence quality
  but leaves the production query corpus empty until media pinning and rollout
  are completed.


## Locked Resume Bullets — Full Stack Roles

### Version 0 (superseded — kept for reference, do not use unless reverting)

Canonical bullets for full stack resume versions. Each follows What + How + Where + Why. No keyword repeats across bullets in this set.

**Bullet 1 (frontend / capture):**
Built an embeddable voice feedback capture flow and dashboard with TypeScript, React, REST APIs, HTML, and CSS on AWS so businesses collect spoken customer feedback instead of forms most people refuse to finish.

Keywords: [TypeScript, React, REST API, HTML, CSS, AWS]
Metric type: [ESTIMATE]
Business outcome: Businesses hear from more customers because speaking takes seconds while forms get skipped.

---

**Bullet 2 (back end):**
Built an async back end with Node.js, JavaScript, SQL, and Redis that processes voice feedback into stored analysis so businesses understand customer complaints without reading survey exports, chasing voicemails, or guessing from star ratings.

Keywords: [Node.js, JavaScript, SQL, Redis]
Metric type: [MEASURED] (~$0.00003/classification session; ~1.2 s analysis latency under normal conditions)
Business outcome: Managers get organized complaint signal without manual exports, voicemails, or star rating guesswork.

---

**Bullet 3 (DevOps / deployment):**
Automated DevOps deployments with Docker, Git, CI/CD, and AWS through GitHub Actions to ECR and EC2 so businesses keep collecting customer complaints the same day a fix ships instead of losing days of feedback to slow manual deploys.

Keywords: [DevOps, Docker, Git, CI/CD, AWS]
Metric type: [MEASURED] (~15 min manual deploy → ~60 s automated; CI 0% → 100% after validate gate)
Business outcome: Feedback collection resumes quickly after a break instead of a multi-day blind spot.

---

### Version 1 (current — use this; locked September 2026)

Drafted Aug 2026 to match the causal-chain density of the reworked work-experience bullets. Sourced only from `hearloop.md` Product / Tech stack / Verified capabilities / Recruiter-legible measured results sections. No metric used that failed the legibility check.

**Bullet 1 (capture flow):**
Built a voice-feedback capture flow and dashboard with TypeScript, React, HTML, CSS, and REST APIs on AWS, designed to surface detailed service issues beyond star ratings and scattered voicemails.

Keywords: [TypeScript, React, HTML, CSS, REST APIs, AWS]
Metric type: N/A
Intended business reason: Capture detailed customer concerns and surface service issues beyond shallow star ratings or scattered voicemails.

---

**Bullet 2 (pipeline):**
Built an asynchronous pipeline with Node.js, BullMQ, Redis, PostgreSQL, and AWS Bedrock to turn voice recordings into sentiment, topics, and urgency, making service issues easier to prioritize.

Keywords: [Node.js, BullMQ, Redis, AWS Bedrock, PostgreSQL]
Metric type: N/A
Intended business reason: Turn raw recordings into structured signals that make service issues easier to prioritize.

---

**Bullet 3 (deployment):**
Automated AWS deployments with Docker, GitHub Actions, and CI/CD, reducing release time from about 15 minutes to 60 seconds and shortening how long the voice-feedback service remains on outdated or faulty code.

Keywords: [AWS, Docker, GitHub Actions, CI/CD]
Metric type: [MEASURED] (~15 min manual → ~60 sec automated; source recorded in this master)
Intended business reason: Release fixes quickly so the feedback service does not remain on outdated or faulty code.

---

## Locked Resume Bullets — Backend Roles

### Version 0 (superseded — kept for reference, do not use unless reverting)

Canonical bullets for backend resume versions. Each follows What + How + Where + Why. No keyword repeats across bullets in this set.

**Bullet B1 (server / storage):**
Built server side voice processing with Node.js, REST API, SQL, Redis, and AWS to store analyzed feedback for each business so managers see what customers said without reading survey exports, chasing voicemails, or guessing from star ratings.

Keywords: [Node.js, REST API, SQL, Redis, AWS]
Metric type: [MEASURED] (~$0.00003/classification session; ~1.2 s analysis latency under normal conditions)
Business outcome: Managers see customer voice in one place instead of scattered manual follow up.

---

**Bullet B2 (service releases):**
Automated service releases with Docker, Git, CI/CD, and DevOps through GitHub Actions so businesses keep collecting customer complaints the same day a server fix ships instead of losing days of feedback to manual deploys.

Keywords: [Docker, Git, CI/CD, DevOps]
Metric type: [MEASURED] (~15 min manual deploy → ~60 s automated; CI 0% → 100% after validate gate)
Business outcome: Feedback collection resumes the same day a fix ships instead of a multi-day blind spot.

---

**Bullet B3 (load testing):**
Stress tested the business logic with JavaScript, SQL, AWS, and load testing for 200 concurrent users at 149ms response time so businesses collect spoken feedback during rush hours without customers abandoning a slow or frozen capture flow.

Keywords: [JavaScript, SQL, AWS, load testing]
Metric type: [MEASURED] (200 concurrent users, 149ms response time, 0% errors on k6 load test)
Business outcome: Rush hour customers finish feedback without hitting a slow or frozen capture flow.

---

### Version 1 (superseded — discard; replaced by Version 2 after user confirmation)

Drafted Aug 2026. Sourced only from confirmed backend facts in this file. No metric used that failed the legibility check.

**Bullet B1 (data layer):**
Built the Fastify API and Kysely data layer over PostgreSQL that stores Partner, Session, and Insights state with Partner scoped queries enforced at the data access layer, so one business could never read another business's feedback records.

Keywords: [Fastify, Kysely, PostgreSQL, Node.js]
Metric type: N/A
Business outcome: One Partner's feedback data stays isolated from every other Partner sharing the same platform.

---

**Bullet B2 (webhook security):**
Built signed webhook delivery with HMAC signatures, retry identity, and SSRF protections so a Partner's CRM or Slack integration receives verified Insights without exposing their own endpoint to spoofed or malicious requests.

Keywords: [HMAC, webhook security, SSRF protection, retry logic]
Metric type: N/A
Business outcome: Partner's integration trusts every delivered result instead of risking a spoofed or malicious payload.

---

**Bullet B3 (load testing):**
Load and soak tested the API with k6 at 200 concurrent users, holding a 149 millisecond p95 response time with zero errors, so a Partner's dashboard stayed responsive during a real traffic spike instead of timing out.

Keywords: [k6, load testing, REST API, AWS]
Metric type: [MEASURED] (200 concurrent users, 149ms p95, 0% errors; recruiter-legible measured result)
Business outcome: Dashboard stays responsive under a real spike instead of timing out on Partners checking results.

---

### Version 2 (current — use this; locked September 2026)

Use both bullets together for the Backend resume. They preserve the multi-tenant data-isolation and measured load-test facts without claiming real customer adoption or traffic.

**Bullet B1 (multi-tenant data layer):**
Built a multi-tenant REST API with Node.js, Fastify, Kysely, and PostgreSQL, enforcing partner-scoped queries at the data layer to keep each business's feedback records isolated on a shared platform.

Keywords: [Node.js, Fastify, Kysely, PostgreSQL, REST API]
Metric type: N/A
Intended business reason: Keep each business's feedback records isolated on a shared platform.

---

**Bullet B2 (load testing):**
Load and soak tested the AWS API with k6 at 200 concurrent users, holding 149 ms p95 latency with zero errors to verify the feedback dashboard remains responsive as simulated request volume increases.

Keywords: [AWS, REST API, k6, Load Testing]
Metric type: [MEASURED] (200 concurrent users, 149 ms p95, 0% errors; source recorded in this master)
Intended business reason: Verify the feedback dashboard remains responsive as request volume increases.

---

## Locked Resume Bullets — AI Engineer Roles

### Version 0 (superseded — kept for reference, do not use unless reverting)

Canonical bullets for AI engineer resume versions. Each follows What + How + Where + Why. Keywords aligned to ML, LLMs, cloud, production systems, MLOps, and AI architecture used in this project.

**Bullet A1 (voice to insight pipeline):**
Built a production voice to insight pipeline with ML, LLMs, AWS Bedrock, and SQL using AI orchestration from speech input to labeled feedback to help business owners understand their customers better without manually reading every transcript line by line.

Keywords: [ML, LLMs, AWS Bedrock, SQL, AI orchestration, production systems]
Metric type: [ESTIMATE] (qualitative; pipeline verified E2E in production deploy)
Business outcome: Owners understand customers without line by line transcript review.

---

**Bullet A2 (LLM cost and access):**
Fine-tuned LLM inference on AWS Bedrock with MLOps token controls on AWS EC2 cloud production systems to help small local businesses turn customer voice into usable insights without hiring engineers to build AI integrations they cannot afford.

Keywords: [LLM, AWS Bedrock, MLOps, AWS EC2, cloud, production systems]
Metric type: [ESTIMATE] (cost optimized via token limits and lighter primary model; no headline dollar figure on resume)
Business outcome: Small local businesses get AI insights without building their own integration team.

---

**Bullet A3 (company knowledge base):**
Configured company knowledge base for AWS Bedrock LLM classification with SQL and AI architecture using voice inputs stored on AWS S3 so business owners understand their customers and inform retention strategy from analyzed feedback instead of vague summaries they cannot act on.

Keywords: [AWS Bedrock, LLM, SQL, AI architecture, AWS S3]
Metric type: [ESTIMATE] (qualitative relevance lift from business context in prompts)
Business outcome: Retention strategy informed by feedback that reflects each business, not generic summaries.

---

**Bullet A4 (business context import):**
Built a website import feature with Python, LLMs, AWS Bedrock, and SQL that reads a business's public site and drafts its profile for review so owners get feedback analysis tuned to their own services without writing setup copy they usually skip.

Keywords: [Python, LLMs, AWS Bedrock, SQL]
Metric type: [MEASURED] (import feasibility spike: 5/5 homepages, 572 ms p95 local / 358 ms EC2 Docker)
Business outcome: Owners get analysis tuned to their services without writing the setup copy they usually skip.

Interview detail (not on resume): Groq Whisper for STT; Nova Lite primary with Haiku fallback; business context is prompt injection, not RAG; import crawls with Crawl4AI behind an SSRF guard; built solo with AI assisted development tools.

**Note on Version 0 Bullet A4:** references the website-import feature, which the Current State
section of this file marks **Retired**. Do not use A4 even if reverting to Version 0 for A1–A3 —
replace it with Version 1's A3 or draft a new one from currently active capabilities.

---

### Version 1 (current — use this; 2-bullet AI set)

Locked September 2026 for the projects-first AI Engineer format. Sourced only from confirmed facts in this file.

**Bullet A1 (voice to insight):**
Built an asynchronous AI pipeline for a multi-tenant voice-feedback platform using Groq Whisper, AWS Bedrock, and structured LLM outputs to convert recordings into transcripts, sentiment, topics, and urgency, designed to help teams identify negative feedback and prioritize issues requiring attention.

Keywords: [asynchronous AI pipeline, Groq Whisper, AWS Bedrock, structured LLM outputs]
Metric type: N/A
Business outcome: Make negative and urgent feedback easier to identify and prioritize.

---

**Bullet A2 (fallback reliability):**
Designed an LLM fallback workflow on AWS Bedrock that validates each classification response and reroutes invalid results to a secondary model, allowing recordings to still produce usable insights when the first model fails.

Keywords: [LLM fallback, AWS Bedrock, structured outputs, reliability]
Metric type: N/A
Business outcome: Preserve usable insights when the primary classification attempt returns invalid output.

---

## SELF CRITIQUE (Version 0 — original pass, retained for reference)

**Rule 1: PASS** — All five non-technical value statements contain no technical terms (no API, async, webhook, JSON, queue, etc.). "Dashboard" and "voice feedback" are plain product language a hiring manager understands.

**Rule 2: PASS** — All five resume bullets have exactly 5 keywords each (within 3–6 range).

**Rule 3: PASS** — No hyphens appear inside any non-technical value statement or resume bullet.

**Rule 4: PASS** — No bullet uses [UNKNOWN] metrics. Bullet 3 uses [ESTIMATE] for form abandonment lift; bullets 1, 2, 4, 5 use [MEASURED] values only.

**Rule 5: PASS** — Every resume bullet ends with a plain English business outcome stated in the Business outcome field and reflected in the bullet closing clause.

**Rule 6: PASS** — Each non-technical value statement starts with a person or role (business owners, location managers, shop staff, company leaders, customers) and describes a before/after a non-technical reader can follow without follow up.

**Overall: 6/6 passed. Output is READY.**
