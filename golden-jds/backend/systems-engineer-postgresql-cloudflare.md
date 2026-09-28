# Golden JD — Systems Engineer, PostgreSQL Platform (Cloudflare, real posting)

**Use for regression:** Backend / Database Systems lane, production PostgreSQL platform,
automation, reliability, observability, and infrastructure operations.
**Source:** Real Cloudflare posting for its internal multi-region PostgreSQL platform team.
Captured September 2026.
**Locations:** Austin, New York, or San Francisco.
**Note on seniority:** Although the posting gives no explicit years requirement, its must-haves
expect direct experience operating large-scale, multi-tenant PostgreSQL clusters in production,
including high availability, failover, and disaster recovery. Treat those as substantive experience
requirements rather than keywords that can be satisfied by application-level PostgreSQL use.

---

## Systems Engineer — PostgreSQL Platform

### About Cloudflare

Cloudflare is building a better Internet through a global network that protects and accelerates
millions of websites and Internet properties, ranging from individual publishers and small
businesses to Fortune 500 companies. Its network improves performance and reduces spam and attacks
without requiring customers to install hardware or software or change application code.

Cloudflare values builders who identify normalized problems, use AI-native tools to create
solutions, iterate quickly, and share improvements with the wider team. The culture emphasizes
curiosity, practical shipping, and using AI as a partner in solving difficult Internet-scale
problems.

### About the team

The team manages an internal, multi-region PostgreSQL platform that enables engineers to build,
deploy, and operate services quickly. Its mission is to provide a highly available, stable,
self-service database platform with clear operational visibility. The Systems Engineer works with
database engineers, developers, application teams, and infrastructure teams to evolve database
architecture, automation, scale, and reliability.

### Responsibilities

- Build, deploy, and manage PostgreSQL database clusters in production environments.
- Develop and maintain database tooling for automation, monitoring, and performance tuning.
- Implement high-availability, backup, and disaster-recovery solutions.
- Integrate database tooling with infrastructure and application teams.
- Build proactive observability for database health.
- Optimize database performance, indexes, and queries.

### Must-have skills

- Experience building, scaling, and managing large-scale, multi-tenant PostgreSQL clusters,
  including high-availability failover and disaster-recovery strategies.
- Infrastructure as code using Terraform, Ansible, or Salt.
- Python or Bash scripting for automation.
- Database tooling for automation and monitoring.
- Docker and Kubernetes.
- PostgreSQL performance optimization and query tuning.
- Alerting and monitoring with Prometheus, Grafana, or Kibana.

### Nice-to-have skills

- Software development in Go, Ruby, or C/C++.
- Contributions to PostgreSQL or relevant open-source projects.
- Automated schema migrations using Flyway, Liquibase, goose, or similar tooling.
- Connection pooling with PgBouncer or HAProxy.
- Distributed and time-series databases such as Cassandra or Timescale, and key-value stores such
  as Redis.

### Candidate-fit notes for regression testing

- **Expected lane:** Backend / Database Systems. If the system only supports the standard three
  lanes, propose Backend and explain that this is a database-infrastructure specialization.
- **Strongest supporting project:** ClusterOps provides Go, PostgreSQL, Redis, Docker, Prometheus,
  Grafana, OpenTelemetry, event ingestion, and operational visibility. Its telemetry is simulated,
  it runs locally in Docker Compose, and it does not provide real Kubernetes or production database
  operations experience.
- **Additional supporting project:** Distributed Caching provides Go, PostgreSQL, Redis, Docker,
  Prometheus/Grafana, performance testing, and distributed-systems reasoning. Use only documented
  measurements and do not convert application benchmarking into PostgreSQL cluster-administration
  experience.
- **Professional supporting evidence:** eInfochips includes PostgreSQL on AWS RDS, atomic
  transactions, schema work, RBAC, audit logging, AWS deployment, and CI/CD. It supports
  application-level database correctness and migration experience after the role's conflicting
  dates, frontend framework, and metric claims are reconciled.
- **Real hard gaps:** No verified experience currently shows operating large-scale or multi-region
  PostgreSQL clusters, multi-tenancy at the database-platform level, replication, high-availability
  failover, backup/restore operations, disaster recovery, Terraform, Ansible, Salt, Kubernetes,
  PgBouncer, HAProxy, Cassandra, Timescale, Flyway, Liquibase, goose, or PostgreSQL open-source
  contributions.
- **Adjacent evidence only:** Docker Compose is not Kubernetes. PostgreSQL application schemas and
  transactions are not cluster administration. Redis caching is relevant but does not satisfy
  distributed or time-series database experience. GitHub Actions deployment is not infrastructure
  as code.
- **Tailoring behavior to test:** The system should surface Go, Python, PostgreSQL, Redis, Docker,
  Prometheus, and Grafana evidence while classifying production cluster management and IaC as
  genuine gaps. A high keyword count must not produce a high fit score when the central operational
  requirements are absent.
- **Application decision:** This is currently a stretch role because the core must-have is direct
  production PostgreSQL platform operation. The workflow should flag that before generating an
  aggressively tailored resume.
- **Location flag:** Austin, New York, or San Francisco. Confirm location and relocation fit before
  spending an application slot.

