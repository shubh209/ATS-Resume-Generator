# Golden JD — Software Engineer I, Data Platform (Abnormal AI, real posting)

**Use for regression:** Early-career backend/infrastructure role on a Data Platform team at an AI-native cybersecurity SaaS company. Centers on scalable storage, batch/stream data processing, orchestration, and internal tooling. Backend/distributed-systems/infrastructure lane with a data-platform emphasis.
**Source:** Real Abnormal AI Software Engineer I, Data Platform posting. Captured September 2026.
**Note on seniority:** Titled Software Engineer I and framed for someone "eager to learn," but asks for "1+ years of professional experience" (backend/distributed systems/infrastructure preferred). Slightly above pure new-grad. Accepts school/personal/work experience for the programming skills. Emphasize Go/backend fundamentals and distributed-systems projects without inflating into a data-platform specialist.

---

## Software Engineer I, Data Platform — Abnormal AI

### Company overview

Abnormal AI builds AI-native, data-intensive SaaS products that stop cybercrime for enterprises. The Data Platform team builds and operates the core infrastructure powering the company's most data-heavy workloads, providing storage, processing, and orchestration to all of engineering and data science, plus tooling to make it easy to operate and integrate.

### What you'll do

- Contribute to the design, development, and operation of core data-platform components.
- Build tools and services that make it easy for other teams to adopt and scale data systems.
- Automate infrastructure and operations for reliability, performance, and scalability.
- Apply GenAI techniques to build smarter developer and operator experiences.
- Collaborate across engineering teams on scalability and reliability challenges.
- Own projects, delivering features end-to-end with guidance from senior engineers.

### What you bring

- 1+ years of professional software engineering experience: backend, distributed systems, or infrastructure preferred.
- Solid programming in Python, Go, or similar (school, personal, or work all count).
- Strong fundamentals: data structures, clean code, testing, debugging.
- Interest in learning AWS, Databricks, and the stack (databases, streaming, orchestration).
- Curiosity, problem-solving, willingness to ask questions, independent and team work, strong communication.

### Nice to have

- Kafka, Kinesis, or Flink.
- Cloud platforms (AWS, GCP, Azure).
- Large-scale or data-intensive systems exposure.

### Technical environment

Storage: PostgreSQL, OpenSearch, Redis, RocksDB, DynamoDB. Processing: Kafka, Spark. Orchestration: Airflow, DBT. Cloud: AWS, Databricks.

### Candidate-fit notes for regression testing

- **Expected lane:** Backend. The work centers on storage systems, stream/batch processing, orchestration, and infrastructure tooling.
- **Overall fit: MODERATE.** Genuine backend/distributed-systems project evidence maps to the core, but the data-platform specialty stack (Spark, Airflow, DBT, RocksDB, DynamoDB, OpenSearch, Databricks) is mostly unheld, and the "1+ year professional" bar sits just above new-grad. Present the strong adjacent evidence; report the data-platform-tooling gaps honestly.
- **Strongest project matches:** Distributed Caching (Go, gRPC, Raft, PostgreSQL, cache-aside, Prometheus/Grafana, Docker) is the best fit; it demonstrates backend/distributed-systems fundamentals and Go, the JD's preferred language. Note: its metrics need a re-run before citing fresh, and its Get/Set data race has been fixed (see master). ClusterOps (Go, Kafka, Redis, PostgreSQL, observability, event pipeline) is the second-strongest and directly matches the streaming (Kafka) and reliability/observability asks.
- **Language match:** Go and Python both verified (Go in Distributed Caching/ClusterOps; Python in ASU, Fake Review, Video Compliance). Directly matches "Python, Go, or similar."
- **Streaming / queues:** Kafka verified (ClusterOps), Redis verified (ClusterOps, Hearloop, SEO Audit, Distributed Caching). Kinesis and Flink are gaps. Kafka is a genuine nice-to-have match.
- **Storage breadth:** PostgreSQL and Redis strong and verified. OpenSearch, RocksDB, and DynamoDB are gaps. Do not imply experience with them.
- **Data processing / orchestration:** Spark, Airflow, DBT, Databricks are all gaps. The closest adjacent evidence is the Python/SQL data pipelines at ASU and DAS and the Distributed Caching Python simulation, which show data-pipeline thinking but not these specific tools. Report as a gap, not a match.
- **Observability match:** Prometheus/Grafana/OpenTelemetry (ClusterOps, Distributed Caching), Azure Monitor (DAS), CloudWatch (eInfochips) map to the reliability/operations asks.
- **Cloud:** AWS verified at a basic level (eInfochips Elastic Beanstalk/S3/CloudWatch, Hearloop EC2/S3), Azure (DAS, Video Compliance). Databricks is a gap.
- **GenAI-for-tooling angle:** Video Compliance (LangGraph/RAG/evals) and AI-coding-tool fluency (Claude Code at DAS) map to "apply GenAI to build smarter developer/operator experiences" as a differentiator.
- **Real gaps to handle honestly:** Spark, Airflow, DBT, Databricks, RocksDB, DynamoDB, OpenSearch, Kinesis, Flink, and 1+ year of professional backend experience (candidate is early-career with an internship plus a current volunteer role). Frame these as learnable, which the posting explicitly invites ("but you can also learn here").
- **Tailoring behavior to test:** Route to Backend, lead with Distributed Caching (Go/distributed systems) and ClusterOps (Kafka/Redis/observability), surface Go + Python + Kafka + PostgreSQL + observability, and report the data-platform-tooling and professional-experience gaps plainly rather than implying Spark/Airflow/Databricks experience.
- **Application-fit assessment:** Moderate fit. Strong Go/backend/distributed-systems and Kafka/observability evidence; genuine gaps in the data-processing/orchestration stack and the professional-experience bar. A reasonable stretch application given the posting's learn-here framing.
