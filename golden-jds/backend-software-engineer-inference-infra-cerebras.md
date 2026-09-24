# Golden JD — Software Engineer, Inference Infrastructure (Cerebras, real posting)

**Use for regression:** Backend/platform role building high-performance, low-latency ML inference infrastructure at an AI-hardware company. Centers on Kubernetes orchestration, containerized inference services, autoscaling, multi-region/HA deployment, Python APIs, and observability-driven debugging. Not an ML-modeling role; it is the platform under inference.
**Source:** Real Cerebras Systems Software Engineer (inference infrastructure) posting. Captured September 2026.
**Note on seniority:** Minimum is a Master's in CS plus one year of experience (internship/part-time before/during/after grad studies counts). Candidate has an MS (2026) and early-career experience (internship + current volunteer SWE role), so this sits right at the edge of the minimum. Present real infra/observability evidence; do not inflate into a production-inference-infra specialist.

---

## Software Engineer, Inference Infrastructure — Cerebras

### Company overview

Cerebras builds the world's largest AI chip and delivers very high-speed training and inference. This role develops and maintains high-performance, low-latency inference infrastructure: deploying and optimizing scalable inference services, ensuring production-ready, reliable ML infrastructure.

### Responsibilities

- Implement infrastructure for high-performance, low-latency inference.
- Deploy and configure Kubernetes services for scalability and reliability of inference workloads.
- Optimize resource allocation and autoscaling to handle variable demand at minimal cost.
- Integrate inference services with Docker/Kubernetes-orchestrated containers.
- Ensure HA and fault tolerance via multi-region deployment and disaster recovery.
- Develop Python scripts and APIs for data preprocessing, inference execution, and post-processing.
- Collaborate with ML engineers to validate inference accuracy and latency.
- Triage/resolve defects via logs, metrics, and distributed traces; debug deployment, orchestration, and networking issues.
- Automate detection/mitigation of failure modes; author technical docs; track work in Jira/Git; join release planning.

### Required skills

Docker and Kubernetes; Java or C++; ActiveMQ and Kafka; Python or Groovy; JavaScript or TypeScript; Linux; SQL, OracleDB, and Redis; Git.

### Candidate-fit notes for regression testing

- **Expected lane:** Backend (platform/infrastructure). The work centers on orchestration, services, reliability, and observability.
- **Overall fit: MODERATE / stretch.** Genuine infra + observability + async-pipeline evidence maps to the reliability side, and ClusterOps's "ML infrastructure observability" framing is on-theme for inference infra. But the required-skills list has several hard gaps and the role is production-inference-infra, which the candidate has not done. Present adjacent evidence; report gaps plainly.
- **Strongest project matches:** ClusterOps (Go, Kafka, Redis, PostgreSQL, Prometheus/Grafana/OpenTelemetry/Jaeger, Docker; explicitly an ML-infrastructure observability prototype with simulated GPU telemetry) is the best thematic and technical match to inference-infra observability and Kafka/Redis. Distributed Caching (Go, Redis, cache-aside, PostgreSQL, Docker, Prometheus/Grafana; metrics need a re-run before citing, data race fixed) adds backend/caching/perf-benchmarking depth. Hearloop (Node async pipeline, Redis/BullMQ, k6 load test at 200 users / 149ms p95) adds latency/reliability-under-load evidence.
- **Language match:** Python and Go verified; JavaScript/TypeScript verified. Directly satisfies "Python or Groovy" and "JavaScript or TypeScript." Java or C++ is a GAP (candidate has neither in production).
- **Messaging:** Kafka verified (ClusterOps). ActiveMQ is a GAP. The JD asks for both.
- **Storage:** Redis and SQL/PostgreSQL verified. OracleDB is a GAP.
- **Observability:** strong, verified match, Prometheus, Grafana, OpenTelemetry, Jaeger (ClusterOps), Azure Monitor (DAS), CloudWatch (eInfochips). Directly supports "triage via logs, metrics, distributed traces."
- **Docker:** verified across projects. **Kubernetes:** GAP (Docker/Docker Compose only; no K8s). This is a lead required skill, so flag it clearly.
- **Latency/HA:** Hearloop k6 load/soak testing is the closest evidence for latency-under-load; no verified multi-region or DR experience (GAP).
- **Real gaps to handle honestly:** Kubernetes, Java/C++, ActiveMQ, OracleDB, multi-region/DR, and production inference-serving experience. Python + JS/TS + Kafka + Redis + observability + Docker + Git are genuine matches.
- **Tailoring behavior to test:** Route to Backend, lead with ClusterOps (ML-infra observability + Kafka/Redis) and Distributed Caching (caching/perf), surface observability and latency evidence, and report the Kubernetes / Java-or-C++ / ActiveMQ / OracleDB / multi-region gaps plainly. Do not imply Kubernetes or production inference-infra experience.
- **Application-fit assessment:** Moderate/stretch. Strong observability, Kafka/Redis, Python, and async-pipeline evidence with an on-theme ML-infra observability project, but multiple lead required skills (Kubernetes, Java/C++, ActiveMQ, OracleDB) and production-inference-infra experience are genuine gaps. Reasonable to apply if the candidate is explicit about the K8s and systems-language gaps.
