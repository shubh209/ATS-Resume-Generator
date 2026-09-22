# YouTube Ads Compliance Pipeline

## Tagline

Upload a video or paste a YouTube ad link and get a pass or fail compliance report with cited policy findings and severity levels. Built to show how a marketing or compliance team could screen ads before launch instead of catching problems after spend is already live.

## Tech Stack (Languages / Frameworks / Infrastructure / Tools)

**Languages:** Python 3.12, JavaScript, HTML/CSS

**Frameworks & Libraries:** FastAPI, LangGraph, LangChain, Pydantic, Uvicorn, SQLAlchemy, Alembic

**AI & Data:** Azure OpenAI (GPT-4o for reasoning), Azure AI Foundry (Phi-4-mini-instruct for claim extraction), Azure OpenAI Embeddings (text-embedding-3-small), Azure AI Search (hybrid vector RAG with semantic reranking fallback), Whisper (audio transcription), Tesseract OCR (on-screen text from sampled video frames, V2 upload path), cross-encoder/ms-marco-MiniLM-L-6-v2 (reranking), youtube-transcript-api, Firecrawl (structured policy extraction)

**Infrastructure:** Azure Container Apps (API + Worker), Neon PostgreSQL (serverless), Azure Blob Storage (video uploads + policy cache), Azure Storage Queue (async job processing), GitHub Container Registry, Docker

**Auth & Security:** Microsoft Entra ID (JWT), team API keys (SHA-256 hashed), CORS allowlist, Postgres-backed rate limiting (sliding window, persists across restarts/deploys)

**Tools & Practices:** Git, GitHub Actions (CI/CD with pytest gate), OpenTelemetry, Azure Application Insights, Swagger UI, golden dataset evaluation

## Problem

Marketing and compliance teams often check YouTube ads by hand before launch. Someone reads the title, description, tags, and claims, then flips through long policy PDFs for YouTube rules and FTC disclosure requirements. Different reviewers reach different conclusions. Work piles up when ad volume spikes. A bad call can mean pulled campaigns, wasted spend, or platform strikes. Additionally, policies change frequently across platforms (YouTube, Meta, TikTok, X, FTC) and keeping up manually is unsustainable.

## Solution

Solo-built end-to-end compliance pipeline with two ingestion paths: paste a YouTube URL for quick screening, or upload a video file for full audio transcription and compliance audit. Policy rules from YouTube, Meta, TikTok, X, and FTC are scraped via structured extraction, chunked per-rule, and indexed into Azure AI Search. Each audit extracts discrete claims via Phi-4-mini, retrieves relevant policy chunks with query expansion and reranking, then reasons violations through GPT-4o with chain-of-thought. Results include severity levels (HIGH/MEDIUM/LOW), policy citations with source excerpts, and are persisted for human review override. Includes a web audit UI, admin dashboard, async worker for video processing, and automated Azure deployment.

**Project status:** Working prototype for demos and interviews. Shows how an internal company tool could operate. Not a live customer rollout.

## Project Status

**demo prototype** — portfolio / interview piece. Not a live customer rollout.

## Verified Metrics

| Metric | Value | Label | Source |
|--------|-------|-------|--------|
| Policy source URLs indexed | 35 (YouTube, Meta, TikTok, X, FTC) | MEASURED | policy_sources.py |
| Platforms covered | 5 (YouTube, Meta, TikTok, X, FTC) | MEASURED | policy_sources.py |
| Golden eval accuracy (v1, 10-case) | 80% (8/10 test cases pass) | MEASURED | evals/eval_results.json |
| Golden eval dataset v2 size | 104 cases (72 FAIL / 32 PASS) | MEASURED | evals/golden_dataset_v2.json |
| Champion baseline accuracy (v2, pre-fix) | 76.9% (80/104), 68.8% false-positive rate | MEASURED | commit 9c777e3 |
| Accuracy after round-1 prompt fix (improvement set) | 93.3% (from 72.5%), FP 9.1% (from 73.7%) | MEASURED | commit 1a3f046 |
| Eval accuracy on unseen cases (v2) | 88.2% (30/34) | MEASURED | evals/round2_holdout_run.log, commit fb4e983 |
| False positives on compliant ads (v2, unseen) | 0% (0/9 compliant cases flagged) | MEASURED | holdout run, commit fb4e983 |
| pytest tests in CI gate | 57 | MEASURED | GitHub Actions |
| CI deploy on push to main | Yes | MEASURED | deploy.yml |
| Models in pipeline | 2 (GPT-4o reasoning + Phi-4-mini extraction) | MEASURED | nodes.py |
| Ingestion paths | 2 (URL metadata + file upload with Whisper) | MEASURED | Architecture |

## Never Claim

GPT and resume tailoring must **not** invent or imply:

- Production customer rollout or paying compliance customers
- React or TypeScript frontend (UI is vanilla JavaScript)
- URL-path full transcript (captions blocked by YouTube bot detection on server; upload path uses Whisper)
- Live SOC2 or enterprise compliance certification
- Measured end-to-end audit latency as a performance guarantee
- Volume tested at scale
- An automated self-improving eval loop (the v2 prompt-improvement rounds were run and verified manually, not by an autonomous system)
- Eval accuracy above the recorded 88.2% on unseen cases (or 93.3% on the improvement set) without a fresh eval run; the 93.3% improvement-set number is measured on cases used for tuning and must not be presented as generalization
- That the v2 reasoning-prompt changes are live in production unless a deploy after commit fb4e983 is confirmed

Use **Interview Framing** below when discussing scope in interviews.

## My Role

- Owned the full build alone, from problem framing through Azure deployment, so there was no gap between the idea and something a reviewer could actually click through.
- Designed a four-stage LangGraph workflow (claim extraction, per-claim retrieval with reranking, GPT-4o policy reasoning, report synthesis) so each run follows a repeatable sequence and fails cleanly when a step breaks.
- Chose a multi-model architecture (GPT-4o for reasoning, Phi-4-mini for extraction) to keep token cost low while maintaining accuracy on compliance judgment.
- Built two ingestion paths (URL metadata screening and file upload with Whisper transcription) so the tool works both for quick pre-launch checks and for full video audits.
- Indexed policy rules from five advertising platforms into Azure AI Search with structured extraction and per-rule chunking so violations cite the actual rule text, not model memory.
- Built an async worker on Azure Container Apps with blob storage and queue processing so video uploads don't block the API and users get immediate confirmation.
- Created a golden evaluation dataset to measure pipeline accuracy against labeled test cases so improvements are tracked against a repeatable baseline.
- Expanded evaluation to a 104-case labeled dataset with a fixed train/holdout split, then added explicit compliant-language and disclosure rules to the GPT-4o reasoning prompt so the pipeline stops flagging properly qualified ads while still catching real violations.
- Fixed the evaluation runner so per-case timeouts actually fire (thread-based timeout replacing a signal handler that did not interrupt blocking LLM calls) so eval runs complete reliably instead of hanging.
- Wired GitHub Actions CI/CD to Azure Container Apps with a pytest gate so deploys stay tied to passing tests.

## Impact

- **Grounded audits in policy rules from five advertising platforms** (YouTube, Meta, TikTok, X, FTC), indexed as per-rule chunks in Azure AI Search **[MEASURED]**, so findings tie back to written regulatory language instead of generic model guesses.
- **Stored every audit in Neon PostgreSQL** with team scoping, AI status, final status after human review, and ingestion source, so compliance history lives in one place instead of scattered email threads.
- **Returned severity-ranked PASS/FAIL reports with policy citations** (source document + excerpt per violation + risk level), so reviewers see what to fix before spend goes live and can point to the rule behind each flag.
- **Built a golden evaluation dataset** with synthetic ad transcripts and expected violation labels **[MEASURED: 80% baseline]**, so pipeline accuracy is measurable and regressions are caught before deploy.
- **Deployed API and worker on Azure Container Apps with CI/CD on every push to `main`** **[MEASURED]**, so the tool stays current when code or policy indexing changes without manual server work.
- **Added human review overrides** that preserve the original AI recommendation, so teams can disagree with the model without losing the audit trail.
- **Implemented multi-model cost optimization** using Phi-4-mini for extraction tasks and GPT-4o only for reasoning, so the pipeline stays within free-tier budget constraints.

## How It Works

### Architecture (high level)

```
Video File (upload) OR YouTube URL
    → Indexer (skip if transcript pre-provided by worker)
    → Enrich (youtube-transcript-api / yt-dlp fallback / metadata-only)
    → Auditor:
        Stage 1: Claim extraction (Phi-4-mini-instruct)
        Stage 2: Per-claim retrieval + rerank (Azure AI Search + cross-encoder)
        Stage 3: Policy reasoning (GPT-4o, chain-of-thought)
        Stage 4: Report synthesis (Phi-4-mini-instruct)
    → Persist (Neon PostgreSQL audit record)
    → PASS/FAIL Report with severity + citations
         ↑
   Azure AI Search (35 policy URLs, structured extraction, per-rule chunks)
```

### Step by step

1. **Reviewer submits a URL or uploads a video** via the web UI (`/`), admin page (`/admin`), or `POST /audit` / `POST /audit/upload`. Entra JWT or team API key required unless `AUTH_DISABLED=true` for local dev.
2. **Upload path:** File goes to Azure Blob Storage, job queued to Azure Storage Queue, worker picks it up, transcribes with Whisper, then runs the audit pipeline with the transcript pre-provided.
3. **URL path:** Indexer node pulls public metadata from YouTube Data API v3. Enrich node tries youtube-transcript-api for captions (fallback: yt-dlp, then metadata-only).
4. **Auditor node Stage 1:** Phi-4-mini extracts discrete checkable claims from the transcript.
5. **Auditor node Stage 2:** Each claim is expanded into policy terminology, then per-claim vector search retrieves relevant policy chunks from Azure AI Search. Cross-encoder reranks for relevance.
6. **Auditor node Stage 3:** GPT-4o receives claims + retrieved policy chunks and reasons violations with chain-of-thought. Returns structured JSON with severity, citations, and risk level.
7. **Auditor node Stage 4:** Phi-4-mini synthesizes a human-readable report from the violations.
8. **API persists the audit** to Neon PostgreSQL: team, user, AI status, violations, policy version, ingestion source.
9. **Human reviewer** can override via `POST /audits/{id}/review`. AI status stays unchanged; `final_status` updates.
10. **Admin** can reindex policies (`POST /admin/policies/reindex`), manage team API keys, browse audit history, and export CSV/PDF reports.
11. **GitHub Actions** runs pytest, then builds and deploys to Azure Container Apps on push to `main`.

### Key technical decisions

| Decision | Why | Tradeoff |
|---|---|---|
| Two ingestion paths (URL + upload) | Upload gives full transcript via Whisper; URL gives quick metadata check | URL path limited by YouTube bot detection on cloud IPs |
| Multi-model (GPT-4o + Phi-4-mini) | Extraction is cheap on small model; reasoning needs GPT-4o accuracy | Two models to manage, different failure modes |
| Per-claim retrieval with query expansion | Each claim gets its own relevant policy chunks | More API calls per audit than bulk retrieval |
| Cross-encoder reranking | Improves precision of retrieved chunks | Adds latency per retrieval step |
| Structured policy extraction (Firecrawl) | Per-rule chunks with metadata enable filtered search | Higher Firecrawl credit cost per reindex |
| Neon PostgreSQL (serverless) | Free tier, scales to zero, no Azure Postgres cost | Cold start adds latency on first connection |
| GPT-4o at temperature 0 | Same input should give the same PASS/FAIL | Reports read mechanically |
| Vanilla JS UI (no React) | Faster to ship audit + admin pages | Less polished than a component library |

### API surface (v3.0.0)

| Method | Path | Purpose |
|---|---|---|
| POST | `/audit` | Run compliance audit (URL) |
| POST | `/audit/upload` | Upload video for async audit |
| GET | `/audits`, `/audits/{id}` | Team scoped audit history and detail |
| POST | `/audits/{id}/review` | Human override (reviewer/admin) |
| GET | `/audits/{id}/export?format=csv\|pdf` | Download report |
| GET/POST | `/admin/policies/*`, `/admin/api-keys` | Policy reindex and API key management |
| GET | `/auth/me` | Verify auth token |
| GET | `/health` | Health check |
| GET | `/`, `/admin` | Audit UI and admin dashboard |

## Locked Resume Bullets (Full Stack Roles)

### Version 0 (superseded — kept for reference, do not use unless reverting)

*Locked 2026-06-05.*

**Bullet 1:** Built an ad auditing website with JavaScript, HTML, CSS, and REST APIs for a company marketing team to generate YouTube and FTC compliance reports so teams could catch policy issues before launch instead of facing legal exposure after ads go live.

Keywords: [JavaScript, HTML, CSS, REST API]

Metric type: N/A

Business outcome: Catch policy issues before launch, not legal exposure after ads go live.

---

**Bullet 2:** Built backend services with Python, SQL, and Docker on Azure for the compliance team to store audit history and human review decisions in one place instead of losing findings in email threads.

Keywords: [Python, SQL, Docker, Azure]

Metric type: N/A

Business outcome: Audit history and review decisions live in one place, not lost in email.

---

**Bullet 3:** Automated service releases with DevOps, CI/CD, and Azure so the compliance tool could stay running and current when advertising rules change without manual server updates before each demo or review.

Keywords: [DevOps, CI/CD, Azure]

Metric type: **[MEASURED]** (deploy on every push to `main`)

Business outcome: Tool stays running and current without manual server updates when rules change.

---

### Version 1 (current — use this)

Drafted Aug 2026 to match the causal-chain density of the reworked work-experience bullets: each
outcome names a business risk avoided, not a feature or UX description. Incorporates the v2 golden
evaluation dataset work (104 cases, 88.2% holdout accuracy, 0% false positives). Sourced only from
this file's Verified Metrics, My Role, and Impact sections.

**Bullet 1:** Built an audit platform using JavaScript, HTML, CSS, and REST APIs on Azure that lets a reviewer paste a URL or upload a video to catch a policy violation before spend is already committed instead of discovering it after a campaign is live.

Keywords: [JavaScript, HTML, CSS, REST API, Azure]

Metric type: N/A

Business outcome: Team catches a violation before spend is committed instead of discovering it after the campaign is live and the money is already gone.

---

**Bullet 2:** Built backend services with Python, SQL, and PostgreSQL on Azure that persist every audit with its AI status, human review outcome, and policy version, so a compliance team can prove why an ad was approved months later instead of having no record to defend the decision if it is challenged.

Keywords: [Python, SQL, PostgreSQL, Azure]

Metric type: N/A

Business outcome: Team can defend an approval decision later instead of having no record if it is ever challenged.

---

**Bullet 3:** Automated deployments to Azure Container Apps with GitHub Actions and a pytest gate on every push to main, so the tool enforced current advertising rules instead of quietly running stale policy logic that gives a team false confidence in a compliance check that no longer matches reality.

Keywords: [GitHub Actions, CI/CD, Azure, pytest]

Metric type: [MEASURED] (deploy on every push to `main`)

Business outcome: Tool enforces current rules instead of giving false confidence from a stale check that no longer matches reality.

---

## Locked Resume Bullets (AI Engineer Roles)

### Version 0 (superseded — kept for reference, do not use unless reverting)

*Locked 2026-07-14.*

**Bullet 1:** Built a multi-stage ad compliance pipeline with LangGraph, RAG, LLMs, and AI orchestration on Azure to extract claims from video transcripts and match them against indexed policy rules so marketing teams catch compliance issues before launch instead of facing pulled campaigns and wasted spend after ads go live.

Keywords: [LangGraph, RAG, LLMs, AI orchestration, Azure, compliance]

Business outcome: Catch compliance issues before launch instead of pulled campaigns and wasted spend.

---

**Bullet 2:** Designed a multi-model AI architecture with GPT-4o for policy reasoning and Phi-4-mini for claim extraction on Azure AI Foundry, with MLOps tracing and a golden evaluation dataset, so the team knows whether the tool is getting better or worse before trusting it with real ad spend decisions.

Keywords: [AI architecture, MLOps, LLMs, ML, Cloud, evaluation]

Business outcome: Team knows if tool is improving before trusting it with real ad spend decisions.

---

**Bullet 3:** Indexed policy rules from multiple advertising platforms using structured extraction, vector search, and semantic reranking in a production systems RAG pipeline on Azure AI Search so reviewers can point to the exact written rule behind each flag when a stakeholder asks why an ad was rejected.

Keywords: [RAG, production systems, Azure, ML, vector search, agentic systems]

Business outcome: Reviewers point to exact written rule when stakeholder asks why an ad was rejected.

---

### Version 1 (current — use this)

Locked September 2026 for the projects-first AI Engineer format.

**Bullet A1:** Designed a LangGraph AI orchestration pipeline using LLMs, RAG, Azure AI Search, and vector search to check advertising claims against policies across multiple platforms and reduce the risk of ads being flagged before launch.

Keywords: [LangGraph, LLMs, RAG, Azure AI Search, vector search]

Metric type: N/A

Business outcome: Reduce the risk of ads being flagged by policies across multiple platforms before launch.

---

**Bullet A2:** Designed a multi-model LLM architecture that separated claim extraction from policy reasoning, using the higher-cost model only for complex decisions to limit inference costs while preserving stronger reasoning for policy checks.

Keywords: [multi-model LLM architecture, inference cost, policy reasoning]

Metric type: N/A

Business outcome: Limit inference costs while preserving stronger reasoning for complex policy checks.

---

**Bullet A3:** Built a 104-case golden evaluation dataset with holdout testing and prompt engineering, reaching 88.2% accuracy with zero false positives on unseen cases and reducing the risk of compliant ads being wrongly flagged for manual review.

Keywords: [evaluation, golden dataset, prompt engineering, holdout testing]

Metric type: [MEASURED] (88.2% accuracy on 30/34 unseen holdout cases, 0/9 false positives; source: evals/round2_holdout_run.log, commit fb4e983)

Business outcome: Reduce the risk of compliant ads being wrongly flagged for manual review.

---

## Locked Resume Bullets (Backend Roles)

### Version 0 (superseded — kept for reference, do not use unless reverting)

*Locked 2026-07-14.*

**Bullet 1:** Built async video processing with a Python FastAPI upload endpoint and Azure Storage Queue worker on Docker Container Apps to transcribe uploaded ads and run compliance audits without blocking the REST API so reviewers get results back without staring at a loading screen while the system processes their video.

Keywords: [FastAPI, Python, Azure, Docker, REST API, queue]

Business outcome: Reviewers get results without waiting on loading screen while system processes video.

---

**Bullet 2:** Stored audit history with human review overrides in PostgreSQL with team scoping, SQL migrations, and role-based access on Azure so compliance decisions live in one queryable system with full audit trail instead of getting lost across email threads and shared drives.

Keywords: [PostgreSQL, SQL, Python, Azure, database, security]

Business outcome: Compliance decisions in one system with audit trail instead of lost in email.

---

**Bullet 3:** Automated CI/CD deploys to Azure Container Apps with GitHub Actions, Docker builds, and a pytest gate with Git so the compliance tool stays available when advertising rules change without someone manually updating servers before each review cycle.

Keywords: [Docker, CI/CD, Azure, Git, DevOps, testing]

Business outcome: Tool stays available when rules change without manual server updates.

---

### Version 1 (current — use this)

Drafted Aug 2026. Bullet B3 replaces the Version 0 CI/CD bullet with the v2 eval work, since two
CI/CD-flavored bullets (FS3 and old B3) were redundant across lanes. Sourced only from this file's
Verified Metrics and My Role sections.

**Bullet B1:** Built an async video processing path with a FastAPI upload endpoint, Azure Storage Queue, and a worker that transcribes with Whisper, so the API stayed responsive under load instead of blocking on a slow upload and pushing reviewers to skip the compliance gate entirely under deadline pressure.

Keywords: [FastAPI, Azure Storage Queue, Whisper, async]

Metric type: N/A

Business outcome: API stays responsive instead of blocking, so reviewers do not skip the compliance gate under deadline pressure.

---

**Bullet B2:** Built human review overrides on top of PostgreSQL with team scoping and SQL migrations that preserve the original AI call next to the final human decision, so a team could defend an overridden compliance decision later instead of having no record if the ad in question was ever challenged.

Keywords: [PostgreSQL, SQL, migrations, RBAC]

Metric type: N/A

Business outcome: Team can defend an overridden decision later instead of having no record if the ad is ever challenged.

---

**Bullet B3:** Expanded a golden evaluation dataset to 104 labeled cases with a fixed train and holdout split, reaching 88.2 percent accuracy and zero false positives on compliant ads in the unseen holdout set, designed to catch prompt regressions before release instead of relying on a handful of convincing examples.

Keywords: [evaluation, golden dataset, holdout testing, LLM reasoning]

Metric type: [MEASURED] (104-case dataset, 88.2% accuracy on 30/34 unseen holdout cases, 0/9 false positives; source: evals/round2_holdout_run.log, commit fb4e983)

Business outcome: A regressing prompt change is caught before shipping instead of passing on convincing examples and failing quietly in production.

---

## Interview Framing

> I built a working prototype that shows how a compliance team could screen ads before launch. Upload a video or paste a URL, get a cited pass or fail with severity levels, store the audit, and let a human override if needed. It covers YouTube, Meta, TikTok, X, and FTC policies. Built for demos and interviews, not a live customer rollout yet.

Setup and smoke tests: see `Youtube-Ads-Compliance-Pipeline/docs/SETUP_TESTING.md`

## Keywords

Python, FastAPI, REST API, SQL, PostgreSQL, Neon, LangGraph, LangChain, RAG, Azure OpenAI, GPT-4o, Phi-4-mini, multi-model, Azure AI Search, embeddings, vector search, Whisper, audio transcription, video processing, async workers, YouTube Data API, Microsoft Entra ID, compliance automation, ad policy, FTC guidelines, Docker, Azure Container Apps, Azure Blob Storage, Azure Storage Queue, CI/CD, GitHub Actions, Git, DevOps, MLOps, Application Insights, JavaScript, HTML, CSS, human review, policy citations, structured extraction, Firecrawl, cross-encoder reranking, query expansion, chain-of-thought, golden dataset, evaluation, multi-platform compliance, full stack, AI tools, solo project, end to end ownership
