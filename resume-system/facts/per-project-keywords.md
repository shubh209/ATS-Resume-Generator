# Keyword Mapping — Per-Project Coverage

> Routing reference only. This file does not authorize facts, metrics, skills, project counts, or selection of a project without a current locked bullet bank. The live rules are in `.agents/skills/resume-tailor/SKILL.md`.

## Role Keyword Requirements (Reference)

**Full Stack:** Degree, TypeScript, JavaScript, HTML, CSS, REST API, SQL (any),
Cloud (AWS/Azure/GCP), Backend (Python/Java/Go/C#), React/Angular/Node.js/Vue.js (any),
DevOps, CI/CD, Agile, Git. Extra credit: Large scale, AI tools, cross functional

**Backend:** Degree, Agile, Go/Golang, Fiber/Node.js/Next.js (any), SQL, MongoDB,
Redis, REST API, Cloud, Git, CI/CD, Kafka, RabbitMQ, Docker, Kubernetes, C++, OOP

**SDET:** Degree, Testing methodologies (functional/e2e/regression/stress/load/smoke - any),
Database testing/SQL, Agile/Scrum, CI/CD, Git, Jenkins, bug communication, coding language,
Playwright/Cypress/Selenium (any), test management tools (TestRail/Azure DevOps/Jama)

**AI Engineer:** Degree, Backend language, ML, LLMs, Cloud, production systems,
Agentic systems, Claude Code/Cursor/Codex (any), LangGraph/LangChain/Google ADK (any),
technical communication to non-technical stakeholders, MLOps, AI architecture,
AI orchestration. Rare: industry experience, SQL, RAG, Git, NumPy

---

## Recommended Resume Projects

AI Engineer uses the locked projects-first structure with four projects and `3 / 2 / 2 / 2` bullets. Other lanes follow their own templates.

### Full Stack SWE

| Order | Project | Bullets |
|-------|---------|---------|
| 1 | Hearloop | 3 |
| 2 | SEO Audit Engine | 3 |
| 3 | Crypto Market Simulator | 2 |
| 4 | ClusterOps | 2 |

**Bench:** Video Compliance Pipeline (9/13) · Fake Review Detector (6/13) · Distributed Caching (5/13 — no JS/TS frontend framework)

### Backend SWE

| Order | Project | Bullets |
|-------|---------|---------|
| 1 | Distributed Caching System | 3 |
| 2 | ClusterOps | 3 |
| 3 | Hearloop | 2 |
| 4 | Video Compliance Pipeline | 2 |

**Bench:** SEO Audit Engine (7/16) · Crypto Market Simulator (6/16) — swap in for Video Compliance on serverless/edge JDs  
**Exclude:** Fake Review Detector (3/16)

### AI Engineer

| Order | Project | Bullets |
|-------|---------|---------|
| 1 | Video Compliance Pipeline | 3 |
| 2 | Fake Review Detector | 2 |
| 3 | Hearloop | 2 |
| 4 | ClusterOps | 2 |

**Exclude:** SEO Audit (1/13) · Crypto Market Simulator (2/13)

### Dad Friend / General SWE Handoff

Locked July 2026 for a general referral handoff resume.

| Order | Project | Bullets |
|-------|---------|---------|
| 1 | Hearloop | 3 |
| 2 | Video Compliance Pipeline | 3 |
| 3 | Distributed Caching System | 2 |

**Reason:** Balanced full-stack product, AI/RAG systems, and backend/distributed-systems depth without crowding the expanded Experience section.

### Cross-role appearance

| Project | Full Stack | Backend | AI Engineer |
|---------|:----------:|:-------:|:-----------:|
| Hearloop | ✓ | ✓ | ✓ |
| ClusterOps | ✓ | ✓ | ✓ |
| Video Compliance Pipeline | bench | ✓ | ✓ |
| SEO Audit Engine | ✓ | bench | |
| Distributed Caching System | | ✓ | bench |
| Crypto Market Simulator | ✓ | | |
| Fake Review Detector | | | ✓ |

---

## Hearloop

| Technology Used | Primary Keyword Match | Alternative Keyword Match |
|---|---|---|
| TypeScript | TypeScript (Full Stack) | Backend language (AI Engineer) |
| Node.js | Node.js (Full Stack, Backend) | Backend language (AI Engineer) |
| Fastify | Fiber/Node.js (Backend) | REST API framework |
| Next.js | Next.js/React (Full Stack) | Frontend framework |
| React | React (Full Stack) | — |
| PostgreSQL | SQL (Full Stack, Backend, SDET) | Database testing (SDET) |
| Redis | Redis (Backend) | Caching |
| BullMQ | Job queue (Backend) | Async pipeline |
| AWS EC2/S3/ECR | Cloud (Full Stack, Backend, AI Engineer) | — |
| Docker | DevOps (Full Stack) | Docker (Backend) |
| GitHub Actions | CI/CD (all roles) | DevOps (Full Stack) |
| Jest | Testing (SDET) | Unit testing |
| k6 | Load/stress/soak testing (SDET) | — |
| OWASP ZAP | Security testing (SDET) | — |
| REST API | REST API (Full Stack) | — |
| Groq Whisper / AWS Bedrock | LLMs, ML (AI Engineer) | AI orchestration |
| Prometheus/Grafana | Observability (Backend) | MLOps (AI Engineer) |
| Kafka (covered by ClusterOps) | Kafka now lives in ClusterOps | Event streaming (AI Engineer orchestration) |

**Coverage:** Full Stack 8/13 · Backend 7/16 · SDET 6/10 · AI Engineer 4/13 (locked bullets strong; no LangGraph/RAG)

**Resume use:** Full Stack #1 · Backend #3 (2 bullets) · AI Engineer #4 (2 bullets)

---

## SEO Audit Engine

| Technology Used | Primary Keyword Match | Alternative Keyword Match |
|---|---|---|
| JavaScript | JavaScript (Full Stack) | Coding language (SDET) |
| HTML/CSS | HTML/CSS (Full Stack) | — |
| Node.js | Node.js (Full Stack, Backend) | — |
| Express.js | REST API framework | Node.js (Backend) |
| BullMQ | Job queue (Backend) | Async pipeline |
| PostgreSQL (Neon) | SQL (Full Stack, Backend, SDET) | Database testing (SDET) |
| Redis (Upstash) | Redis (Backend) | Caching |
| Playwright | Playwright (SDET) | E2E testing |
| axe-core | Accessibility testing (SDET) | — |
| Jest / Supertest | Testing (SDET) | Unit / API testing |
| Render / Cloudflare Pages | Cloud (Full Stack, Backend, AI Engineer) | — |
| GitHub Actions | CI/CD (all roles) | DevOps (Full Stack) |
| REST API | REST API (Full Stack) | — |
| SSE | Real time / async | — |

**Coverage:** Full Stack 8/13 · Backend 7/16 · SDET 7/10 · AI Engineer 1/13 (do not use for AI roles)

**Resume use:** Full Stack #2 · Backend bench

---

## Fake Review Detector

| Technology Used | Primary Keyword Match | Alternative Keyword Match |
|---|---|---|
| Python | Backend language (Full Stack, AI Engineer) | Coding language (SDET) |
| JavaScript | JavaScript (Full Stack) | — |
| HTML/CSS | HTML/CSS (Full Stack) | — |
| Flask / Gunicorn | REST API (Full Stack) | Backend (Python), production systems (AI Engineer) |
| REST API | REST API (Full Stack) | — |
| TensorFlow / PyTorch | ML (AI Engineer) | — |
| Hugging Face Transformers | LLMs / ML (AI Engineer) | — |
| BERT / RoBERTa | ML, LLMs (AI Engineer) | — |
| scikit-learn | ML (AI Engineer) | — |
| NumPy / pandas | NumPy (AI Engineer rare) | ML data prep |
| Render / Railway / Docker | Cloud (Full Stack, Backend, AI Engineer) | Docker (Backend) |
| Confidence-score UI | Technical communication to non-technical stakeholders (AI Engineer) | — |
| GitHub | Git (all roles) | — |

**Coverage:** Full Stack 6/13 · Backend 3/16 (weak) · SDET 2/10 (weak) · AI Engineer 7/13

**Gaps (do not claim):** MLOps, agentic systems, LangGraph/RAG, enterprise cloud (AWS/Azure/GCP)

**Resume use:** AI Engineer #2 only

---

## Video Compliance Pipeline

| Technology Used | Primary Keyword Match | Alternative Keyword Match |
|---|---|---|
| Python | Backend language (Full Stack, AI Engineer) | Coding language (SDET) |
| JavaScript | JavaScript (Full Stack) | — |
| HTML/CSS | HTML/CSS (Full Stack) | — |
| FastAPI | REST API (Full Stack, Backend) | Backend (Python) |
| SQLAlchemy / Alembic | SQL (Full Stack, Backend, SDET) | Database testing (SDET) |
| Neon PostgreSQL (serverless) | SQL (Full Stack, Backend) | Cloud (serverless) |
| LangGraph / LangChain | LangGraph/LangChain (AI Engineer) | Agentic systems, AI orchestration |
| Azure OpenAI GPT-4o | LLMs (AI Engineer) | ML, policy reasoning |
| Azure AI Foundry (Phi-4-mini-instruct) | LLMs, ML (AI Engineer) | Multi-model architecture, cost optimization |
| Azure AI Search (RAG) | RAG (AI Engineer rare) | AI architecture, vector search |
| Azure OpenAI Embeddings | ML (AI Engineer) | — |
| cross-encoder/ms-marco-MiniLM-L-6-v2 | ML (AI Engineer) | Retrieval evaluation, reranking |
| Whisper (Azure OpenAI) | Production systems (AI Engineer) | Audio transcription, ingestion pipeline |
| Azure Storage Queue + Worker | Message queues (Backend) | Async processing, production systems (AI Engineer) |
| Azure Blob Storage | Cloud (Backend) | File uploads, caching |
| Azure Container Apps (API + Worker) | Cloud (Full Stack, Backend, AI Engineer) | — |
| Docker | DevOps (Full Stack) | Docker (Backend) |
| GitHub Actions + pytest gate | CI/CD (all roles) | DevOps (Full Stack) |
| GitHub Container Registry | CI/CD (Backend) | DevOps |
| OpenTelemetry / Application Insights | MLOps (AI Engineer) | Observability (Backend) |
| Microsoft Entra ID (JWT) | Backend auth / security | — |
| Human review workflow + admin UI | Technical communication to non-technical stakeholders (AI Engineer) | — |
| Golden evaluation dataset | MLOps (AI Engineer) | Retrieval evaluation, testing |
| Firecrawl (structured extraction) | Production systems (AI Engineer) | Data pipeline, ingestion |
| youtube-transcript-api / yt-dlp / YouTube Data API | Production systems (AI Engineer) | Ingestion pipeline |
| Git | Git (all roles) | — |

**Coverage:** Full Stack 9/13 · Backend 9/16 · SDET 4/10 · AI Engineer 13/13 (strongest — full coverage)

**Gaps (do not claim):** TypeScript, React/Node frontend, Redis (planned for rate limiting), Kafka, Kubernetes

**Resume use:** Full Stack bench · Backend #4 (3 bullets) · AI Engineer #1 (3 bullets)

**Doc status:** Locked Full Stack (3) + Backend (3) + AI (3) bullets in PROJECT.md


---

## Crypto Market Simulator

| Technology Used | Primary Keyword Match | Alternative Keyword Match |
|---|---|---|
| TypeScript | TypeScript (Full Stack) | Backend language (AI Engineer) |
| JavaScript | JavaScript (Full Stack) | — |
| Python | Backend language (Full Stack, AI Engineer) | Coding language (SDET) |
| React Native | React (Full Stack alt) | — |
| Cloudflare Workers | Cloud (Full Stack, Backend, AI Engineer) | Backend (serverless) |
| Hono | Node.js framework (Full Stack, Backend) | — |
| Cloudflare D1 | SQL (Full Stack, Backend, SDET) | Database testing (SDET) |
| Cloudflare KV | Redis equivalent (Backend) | Caching |
| REST APIs | REST API (Full Stack) | — |
| Jest | Testing (SDET) | Unit testing |
| GitHub Actions | CI/CD (all roles) | DevOps (Full Stack) |
| Clerk | Auth / product engineering | — |

**Coverage:** Full Stack 8/13 · Backend 6/16 · SDET 4/10 · AI Engineer 2/13 (weak)

**Resume use:** Full Stack #3 (2 bullets) · Backend bench only

---

## Distributed Caching System

| Technology Used | Primary Keyword Match | Alternative Keyword Match |
|---|---|---|
| Go | Go/Golang (Backend primary) | Backend language (Full Stack, AI Engineer) |
| REST API / gRPC / Protocol Buffers | REST API (Backend) | Backend (distributed systems) |
| PostgreSQL | SQL (Full Stack, Backend, SDET) | Database testing (SDET) |
| Docker / Docker Compose | Docker (Backend) | DevOps (Full Stack) |
| Prometheus / Grafana | Observability (Backend) | MLOps (AI Engineer) |
| Git / Make | Git (all roles) | CI/CD-ready |
| go test race detector | Unit testing (SDET) | Concurrency testing |
| Python / NumPy | NumPy (AI Engineer rare) | Backend language (AI Engineer) |
| LLM prefix caching module | ML / LLMs (AI Engineer) | AI architecture |
| RAG pipeline simulation | RAG (AI Engineer rare) | LangChain-style retrieval |
| [PLANNED] Kubernetes | Kubernetes (Backend) | DevOps (Full Stack) |

**Coverage:** Full Stack 5/13 (weak — no JS/TS/HTML/CSS) · Backend 6/16 (strongest Go story; Kubernetes pending)
· SDET 3/10 (weak) · AI Engineer 5/13 (infra/simulation angle)

**Resume use:** Backend #1 · AI Engineer #3 (2 bullets)

---

## ClusterOps

| Technology Used | Primary Keyword Match | Alternative Keyword Match |
|---|---|---|
| Go | Go/Golang (Backend) | Backend language (AI Engineer) |
| Kafka | Kafka, event streaming (Backend) | Streaming/orchestration (AI Engineer) |
| PostgreSQL | SQL (Full Stack, Backend) | Database |
| Redis | Redis, caching (Backend) | — |
| REST API | REST API (Full Stack, Backend) | — |
| TypeScript | TypeScript (Full Stack) | — |
| React | React (Full Stack) | Frontend framework |
| HTML/CSS | HTML/CSS (Full Stack) | — |
| Docker | Docker (Backend) | DevOps (Full Stack) |
| Docker Compose | Containerization (Backend) | DevOps |
| GitHub Actions | CI/CD (all roles) | DevOps (Full Stack) |
| Prometheus/Grafana | Observability (Backend) | MLOps (AI Engineer) |
| GPU telemetry (simulated) | Distributed systems, infra (Backend) | ML infrastructure (AI Engineer) |
| [SWAP-IN] LLM failure analysis | — | LLMs, RAG (AI Engineer, planned) |

**Coverage:** Full Stack 8/13 (TS/React frontend + Go/Redis backend) · Backend 9/16 (Go + Kafka + Redis + observability + CI/CD) · SDET 3/10 (weak) · AI Engineer 6/13 (infra/MLOps angle; rule-based assistant only)

**Resume use:** Backend #2 (3 bullets) · Full Stack #4 (2 bullets) · AI Engineer bench (MLOps/infra JDs)

**Status caveat:** Local prototype with simulated GPU telemetry. No real GPUs, Kubernetes, LLM, or cloud deployment. All metrics are ESTIMATE/UNKNOWN — see `resume-system/facts/projects/ClusterOps.md` Never Claim section.

---

## Cross-Project Summary

| Role | Top 4 (in order) | Strongest single project | Weakest among all 7 |
|---|---|---|---|
| Full Stack | Hearloop → SEO Audit → Crypto → ClusterOps | Hearloop, SEO Audit (8–9/13) | Distributed Caching (5/13) |
| Backend | Distributed Caching → ClusterOps → Hearloop → Video Compliance | ClusterOps (9/16) | Fake Review Detector (3/16) |
| SDET | SEO Audit → Hearloop → Crypto → Video Compliance | SEO Audit (7/10) | Fake Review Detector (2/10) |
| AI Engineer | Video Compliance → Fake Review → Hearloop → ClusterOps | Video Compliance (13/13) | SEO Audit (1/13) |

**Pending upgrades:** Distributed Caching Kubernetes · Video Compliance Backend locked bullets · ClusterOps MEASURED metrics + repo URL

*Last updated: 2026-06-23 — Added ClusterOps (Backend #2, Full Stack #4); Kafka coverage moved to ClusterOps; SEO Audit dropped to Backend bench and Video Compliance to Full Stack bench.*
