# SEO Audit Engine

## Tagline

One URL in, one unified audit out — async SEO, performance, and accessibility reports for small teams who shouldn't need three paid tools and an afternoon per client site.

## Tech Stack (Languages / Frameworks / Infrastructure / Tools)

**Languages:** JavaScript (ES modules), HTML, CSS, SQL

**Frameworks / Libraries:** Node.js, Express.js, BullMQ, Playwright, axe-core, Jest, Supertest, jsPDF

**Infrastructure:** Render (API + worker services, free tier), Cloudflare Pages (static frontend), Neon PostgreSQL, Upstash Redis

**Tools:** Git, GitHub Actions (CI/CD + scheduled keep-alive), REST API, Server-Sent Events (SSE)

## Problem

Small agencies and freelance marketers audit client websites constantly — before pitches, during onboarding, and after launches. Enterprise tools like Ahrefs, SEMrush, and bundled PageSpeed workflows cost **$99–299/month** at entry tiers [ESTIMATE], and even free alternatives force teams to **context-switch across three or more surfaces**: performance checkers, separate WCAG tools, and manual SEO spreadsheets for title tags, meta descriptions, and heading structure.

That fragmentation creates operational costs hiring managers recognize without reading code:

1. **Time lost:** Each client site review takes an estimated **15–20 minutes** of tool-hopping before anyone can say "here's what to fix first." [ESTIMATE]
2. **Inconsistent deliverables:** Different team members run different checks in different orders — weakening agency credibility on client calls.
3. **Blocked workflows:** A synchronous "submit URL, wait 60 seconds, hope it doesn't timeout" model fails when an agency queues **10–50 URLs** for a Monday morning review batch.

Without a unified pipeline, agencies either pay for subscriptions they barely use or burn billable hours on manual audits that don't scale with client load.

## Solution

A **distributed audit platform** where users submit a URL through a vanilla JavaScript web UI, the Express REST API enqueues the job on BullMQ, and workers run a five-stage analysis pipeline asynchronously on Render. Users see **real-time progress** via **SSE** (with polling fallback) as each stage completes (crawl → performance → accessibility → SEO → report), then receive a scored report with optional **PDF export**.

Repeat audits of the same URL within 24 hours return cached results in **<1s** [MEASURED] — so agencies re-checking a staging site after fixes skip a full crawl cycle.

Live deployment: frontend on Cloudflare Pages (`seo-audit-engine.pages.dev`), API and worker on Render, backed by Neon PostgreSQL and Upstash Redis. **$0/month** infrastructure on free tiers; GitHub Actions cron pings services every 14 minutes to reduce Render spin-down.

## My Role

Solo full-stack owner across a **6-week** portfolio build for job search — no prior README or team handoff; architecture, implementation, deployment, and CI owned end-to-end.

- **Architecture:** Designed the API/worker split with BullMQ so Playwright crawls never block HTTP threads — the async pattern agencies need for batch URL reviews.
- **Backend (Node.js / Express):** Built REST endpoints for job submission, status polling, cursor-paginated history, and SSE streaming; implemented 24-hour PostgreSQL URL deduplication and Redis result caching (86400s TTL).
- **Worker pipeline:** Implemented five sequential stages — Playwright DOM extraction with resource blocking, response-time performance scoring, axe-core WCAG 2.1 analysis (run on live DOM), seven custom SEO rules, and JSONB report aggregation in PostgreSQL.
- **Frontend (vanilla JavaScript):** Built submit → live stepper → scored report UI with circular score rings, step timing display, recent-audit history (localStorage), and client-ready PDF via jsPDF — deployed as static assets on Cloudflare Pages.
- **Infrastructure & DevOps:** Deployed API and worker to Render free tier, frontend to Cloudflare Pages, configured CORS, added worker health server, API keep-alive pings, and GitHub Actions scheduled keep-alive workflow; wired GitHub Actions CI gating merges on **52 passing Jest tests** (18 API + 34 worker).
- **Engineering tradeoffs:** Renamed performance module to `runPerformanceCheck.js` after dropping Google Lighthouse for reliability on Render free-tier workers; optimized pipeline from ~24s to **~5s** warm audits without paid hosting.

## Impact

### Locked resume bullets

Use the set that matches the role on your resume. Full text also in `seo-audit-engine-keyword-mapping.md`.

#### Full Stack

1. Built an audit submission flow and scored report dashboard with JavaScript, HTML, CSS, REST API, and Cloud so client teams deliver one standardized site assessment per engagement that supports clear recommendations in sales and onboarding conversations.

2. Built server side audit processing with Node.js, SQL, Redis, and CI/CD so client teams finish onboarding site reviews on time, improving new account retention by avoiding the backlog that builds when one slow website blocks the entire review queue.

3. Automated production deploys with Git, CI/CD, and DevOps so client teams keep a reliable site review workflow on live accounts, improving retention by avoiding the outages and delays manual releases introduce.

#### Backend

*Bullets 1–2 locked 2026-06-15 (reason-first, plain-English `because`). Used in `templates/variants/backend-faang.tex`.*

1. **LOCKED:** Built server side audit processing with Node.js, REST API, SQL, Redis, and PostgreSQL because agency teams onboarding multiple new accounts each week had no single stored site assessment to share on sales calls and kickoffs without rebuilding the report from scratch every time.

2. **LOCKED:** Built async audit queues with Node.js, REST API, SQL, Redis, and BullMQ keeping the Express REST API under 400ms because one slow client website can take several minutes to check and agency teams miss onboarding deadlines when every other account must wait in line behind it.

3. Automated service releases with Git, CI/CD, and DevOps so audit scores and checklist results stay accurate on the live platform, protecting client trust and account retention when teams present site review findings in sales calls and onboarding kickoffs.

#### SDET

1. Built automated audit scoring tests with Jest, JavaScript, SQL, and functional testing so every site review applies the same checklist standards regardless of who runs it, protecting client trust and account retention when teams present findings in sales calls and onboarding kickoffs.

2. Validated REST API flows with Supertest, CI/CD, and Git so site review submission and status updates are verified before client teams use them during live onboarding engagements, protecting new account retention by catching broken workflows before they surface in a client meeting.

3. Built production browser crawls with Playwright and accessibility testing so accessibility findings appear in the same site assessment shared at onboarding kickoffs, protecting client trust and retention by surfacing compliance issues before clients raise them in follow up meetings.

### Supporting context (portfolio doc — not all for resume line)

- **Designed a BullMQ worker on Render (concurrency: 1 on free tier)** using Redis-backed job queuing so the Express REST API returns in **<400ms** [MEASURED] while audits run in the background — preventing one slow client site from blocking the HTTP thread.

- **Implemented dual-layer caching (PostgreSQL 24-hour URL dedup + Redis job-result cache)** so repeat staging-site checks skip full Playwright crawls — returning cached URLs in **<1s** instead of a full **~5s** warm audit [MEASURED].

- **Consolidated response-time performance scoring, axe-core accessibility checks, and seven custom SEO rules into one PDF-exportable report** — replacing an estimated **15–20 minute** multi-tool workflow per client site with a single standardized deliverable. [ESTIMATE]

- **Shipped 52 Jest unit tests with GitHub Actions CI/CD** (18 API including SSE route tests, 34 worker) — blocking regressions before production deploys so live demo audits stay trustworthy during interviews.

- **Optimized the worker pipeline** (shared Chromium, axe on live DOM, WCAG 2.1 tag scope, duplicate fetch removal): warm audits dropped from **~24s to ~5s** [MEASURED]; per-step timings persisted to PostgreSQL for observability.

## How It Works

### Architecture

```
[Cloudflare Pages — vanilla JS frontend]
        │  POST /api/jobs  ·  GET /api/stream/:id (SSE, poll fallback)
        ▼
[Render — Express REST API]
        │  INSERT job (Neon PostgreSQL)  ·  24hr URL dedup
        │  auditQueue.add() ──► [Upstash Redis / BullMQ]
        ▼
[Render — BullMQ Worker, concurrency: 1]
        │  5-stage pipeline  ·  axe runs on live crawl DOM
        ▼
[Neon PostgreSQL]  ← status enum + JSONB report + per-step timings
        ▲
        │  GET /api/stream/:id (SSE)
[Frontend stepper — real-time progress + step timings]

[GitHub Actions cron */14] ──► ping API /health + worker (free keep-alive)
```

The system splits into **two Node.js services** on Render: a lightweight API container and a CPU-heavy worker (Playwright + axe-core). BullMQ on Redis decouples acceptance from execution — the same pattern used by CI runners and payment processors: accept work in milliseconds, finish slow work in the background.

### Request lifecycle

1. **Submit:** Frontend POSTs `{ url }` to `/api/jobs`. API validates the URL, checks PostgreSQL for a completed audit within 24 hours (dedup hit → return existing `jobId` with `cached: true`), otherwise inserts `queued` and enqueues on the `seo-audits` BullMQ queue.

2. **Process:** Worker runs five sequential steps, writing status to PostgreSQL after each: `crawling` → `scoring_performance` → `checking_accessibility` → `checking_seo` → `building_report` → `complete`. Failures set `failed` with `failed_step` for UI error display.

3. **Progress:** Frontend streams via SSE at `/api/stream/:id`; falls back to polling `GET /api/jobs/:id` every 2s if SSE disconnects. Step timings (`crawl_ms`, `a11y_ms`, etc.) display as each stage completes.

4. **Deliver:** Completed jobs persist scores, `processing_time_ms`, per-step timings, `checks_run`, and full JSONB report. Redis caches terminal payloads for 24 hours (`job:v2:*` key). Frontend renders tabbed results; jsPDF generates a branded client handoff PDF.

### Pipeline stages and tradeoffs

| Stage | Implementation | Decision |
|-------|----------------|----------|
| **Crawl + a11y** | Playwright Chromium, `domcontentloaded`, 45s timeout, blocks images/fonts/media/stylesheets; axe-core runs on live DOM before page close | Avoids second page load + `setContent`; WCAG 2.1 A/AA tags only |
| **Performance** | Score derived from crawl `loadTimeMs` | **Tradeoff:** Lighthouse removed after Render hangs; honest response-time labeling |
| **Accessibility** | axe-core via Playwright on crawled DOM | Industry-standard WCAG engine; violations include severity and element counts |
| **SEO** | 7 custom rules (title, meta, H1, alt text, canonical, viewport, lang) | Rule engine written from scratch; weighted scoring (−15 fail, −5 warn); **100%** unit test coverage |
| **Report** | Average of three category scores → JSONB | Single source of truth for history API, recent sidebar, and PDF export |

### Caching (two layers, two business purposes)

- **PostgreSQL URL dedup (24hr):** Prevents re-queuing the same client URL.
- **Redis job cache (24hr TTL, `job:v2` key):** Serves completed job payloads during polling/SSE without hammering PostgreSQL.

### CI/CD and reliability

GitHub Actions runs **34 worker + 18 API tests** in parallel on push/PR to `main`. A separate **keep-alive workflow** pings API and worker every 14 minutes (free tier, no cost). Render free tier still cold-starts after long idle — warm the app once before live demos.

Production data [MEASURED 2026-06-05]: **11 completed audits**, median **20.3s** (pre-optimization baseline); post-optimization warm audits **~4–5s** on example.org.

### Scale headroom

Architecture supports queued submissions without blocking the API. Worker concurrency is **1** on Render free tier (512MB RAM); increase to 2–3 only on 1GB+ paid compute.

## Keywords

### By target role (see `seo-audit-engine-keyword-mapping.md` for full matrix)

**Full Stack (8/13 JD keywords matched):** JavaScript, HTML/CSS, Node.js, REST API, SQL, PostgreSQL, Cloud, CI/CD, Git, DevOps

**Backend (7/16 matched):** Node.js, REST API, SQL, Redis, Azure, Cloud, CI/CD, Git, caching

**SDET (7/10 matched):** Playwright, Jest, Supertest, SQL, CI/CD, Git, functional testing, accessibility testing, regression testing

**AI Engineer (1/13 — do not lead with this project):** Cloud only; pair with Video Compliance Pipeline for AI roles

### Project keyword list

JavaScript, HTML/CSS, Node.js, Express.js, REST API, SQL, PostgreSQL, Redis, Cloud, Azure, Render, Cloudflare, Playwright, axe-core, Jest, Supertest, CI/CD, Git, GitHub Actions, DevOps, accessibility testing, functional testing, regression testing, WCAG, SEO analysis

### ATS keyword expansion

RESTful API, Job Queue, Server-Sent Events, Real-Time Updates, Unit Testing, Full Stack, Backend, Microservices, Caching, Async Processing, PDF Export, Web Crawling, Accessibility, Portfolio Project
