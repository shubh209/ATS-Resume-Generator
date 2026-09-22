# Golden JD — Software Engineer, Early Career (Commure, real posting)

**Use for regression:** Early-career, multi-team software engineering posting at an AI-native healthcare company, spanning AI/agents, clinical product, revenue-cycle management, platform/infrastructure, and product engineering. Dominant emphasis is AI systems (LLM inference/orchestration pipelines, evaluation infrastructure) layered on strong full-stack and backend/distributed-systems work.
**Source:** Real Commure early-career Software Engineer posting. Captured September 2026.
**Note on seniority:** Explicitly early-career (recent or upcoming graduate). Accepts internships, research, open-source, coursework, startups, and personal projects. The tailoring system should emphasize demonstrated fundamentals, shipped projects, AI-tool fluency, and high ownership without inflating the candidate into an experienced engineer.

---

## Software Engineer, Early Career — Commure

### Company overview

Commure builds an AI-native operating system for healthcare spanning the care journey: ambient AI and dictation at the point of care, agents automating patient and revenue workflows, and autonomous revenue-cycle management processing claims, integrated with 60+ EHRs. Stated scale: 500,000+ clinicians, 500+ healthcare organizations, $25B+ in annual claims, 200M+ patient interactions. Recent $70M raise at a $7B valuation.

### Job overview

Early-career engineers work alongside experienced engineers across backend, frontend, mobile, and infrastructure while owning production systems and product features. Team placement varies. Example teams: AI & Agents (AI-powered admin-automation workflows), Clinical (reduce clinician documentation time), Revenue Cycle Management (automate billing workflows), Platform & Infrastructure (reliability, observability, scalability), Product Engineering (end-to-end React/API/backend/DB features).

### What you'll do

- Build product features across web, mobile, and backend, including offline-first experiences.
- Develop reliable APIs and backend services for high-volume clinical workflows.
- Build data-processing pipelines for complex, high-volume healthcare data.
- Build and improve AI systems: inference pipelines, orchestration (fallbacks, retries, async workflows), and quality evaluation infrastructure.
- Improve monitoring, observability, alerting, debugging, performance, and reliability.
- Design internal tools that make engineers faster and production systems easier to operate.
- Work directly with product, design, clinical, and customer-facing teams.

### What you have

- Bachelor's or Master's in CS/Engineering or related, recent or upcoming graduate.
- Strong fundamentals in algorithms, data structures, operating systems, databases, networking, or distributed systems.
- Experience building software through internships, research, open-source, coursework, startups, or personal projects, ideally something substantial beyond coursework.
- Clean, maintainable code; strong cross-layer debugging; curiosity about whole systems; care for reliability and performance; high ownership; willingness to learn quickly; preference for ownership over narrow tickets; strong communication.

### Technical environment

- **Languages & frameworks:** Python, TypeScript, Dart, Swift, Kotlin, Flutter, React, native mobile.
- **Infrastructure & data:** PostgreSQL, Redis, cloud object storage, Kubernetes, containers, distributed queues, data-processing pipelines.
- **AI systems:** LLM inference and orchestration pipelines, AI evaluation infrastructure.
- **Observability & testing:** monitoring, logging, tracing, production observability, automated testing.

### Candidate-fit notes for regression testing

- **Expected lane:** AI Engineer by default. The dominant emphasis is LLM inference/orchestration (fallbacks, retries, async workflows) and AI evaluation infrastructure, which centers the AI lane per the routing table. Backend or Full Stack are legitimate alternates when the user's intent or a specific team placement (Platform/Infrastructure, RCM, Product Engineering) supports it.
- **Strongest AI-lane project match:** Video Compliance Pipeline — LangGraph orchestration, LLMs, RAG, multi-model architecture, and a 104-case golden evaluation dataset with holdout testing. This directly matches "orchestration (fallbacks, retries, async workflows)" and "quality evaluation infrastructure." Hearloop adds an async LLM pipeline with a validate-and-reroute fallback workflow. Fake Review Detector adds ML/transformers.
- **Orchestration + eval evidence:** Hearloop's LLM fallback workflow (validate each classification, reroute invalid results) and Video Compliance's golden-dataset evals are the strongest matches for the AI orchestration and evaluation-infrastructure asks. Keep eval framing at design/harness level; do not claim production classifier accuracy.
- **Backend / distributed-systems alternate:** Distributed Caching (Go, gRPC, Raft, PostgreSQL, cache-aside, Prometheus/Grafana) and ClusterOps (Go, Kafka, Redis, observability) map to the platform/infrastructure and data-pipeline asks. Note: Distributed Caching metrics need a re-run before citing fresh (see its master); the Get/Set data race has been fixed.
- **Full-stack / product alternate:** Hearloop and SEO Audit provide React/TypeScript + Node + PostgreSQL + REST + async processing for the Product Engineering path.
- **Data-pipeline match:** DAS (PostgreSQL ingestion/reconciliation on Azure) and ASU (Python/SQL data pipeline with validation) map to "data processing pipelines for complex, high-volume healthcare data" as transferable, non-healthcare evidence.
- **AI-tool fluency:** Claude Code documented at DAS; AI-assisted development across projects. Directly relevant to a company that deploys daily and expects AI-tool use.
- **Observability match:** Azure Monitor (DAS), CloudWatch (eInfochips), Prometheus/Grafana/OpenTelemetry/Jaeger (ClusterOps, Distributed Caching) cover the monitoring/logging/tracing asks.
- **Real gaps to handle honestly:** No verified Dart, Flutter, Swift, Kotlin, native mobile, or Kubernetes experience. Redis is verified (Hearloop, ClusterOps, SEO Audit). Do not present mobile or Kubernetes as held experience; frame as learnable-on-the-job, which this early-career posting explicitly welcomes.
- **Adjacent evidence only:** Docker/containers are verified but Kubernetes is not. Distributed queues are covered by BullMQ and Kafka (adjacent to Commure's "distributed queues"). No healthcare-domain or EHR experience; treat healthcare as domain to learn, not claimed expertise.
- **Tailoring behavior to test:** Route to AI lane, lead with Video Compliance orchestration + evaluation evidence, surface AI-tool fluency and high-ownership shipping (DAS live system), keep prototype framing honest, and report the mobile/Kubernetes gaps rather than cramming all five example teams into one resume.
- **Application-fit assessment:** Strong early-career fit on AI-orchestration/evaluation, full-stack, backend/distributed-systems, data pipelines, observability, and AI-tool fluency. Genuine gaps in mobile (Dart/Flutter/Swift/Kotlin) and Kubernetes, and no healthcare-domain experience, all of which the posting's early-career, learn-fast framing accommodates.
