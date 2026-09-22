# ClusterOps — Engineering Story Bank

Personal reference, not a script. Purpose: recall real, defensible engineering material before an interview or when answering application questions, without inventing anything. Mined from the project's own build history and cross-checked against `resume-system/facts/projects/ClusterOps.md`.

## Source honesty (read first)
No chat transcripts exist for this project, and git history is a single squashed initial commit (`1d6c739`), so there is no recorded diagnosis process or reverted-diff history to mine. The items below are grounded in committed project docs, code, comments, and config. They are mostly **design tradeoffs and design judgment**, not debugging narratives.

## Never-claim guardrails (carry into any answer)
- Local prototype with simulated GPU telemetry. No real GPUs, Kubernetes, LLM inference, or cloud deployment.
- All performance metrics are ESTIMATE or UNKNOWN. Do not cite measured latency, throughput, Kafka lag, or memory.
- These are tradeoffs and design decisions. Do NOT tell the two workarounds below as "a hard bug I debugged" — the outcome is recorded but the diagnosis process was never captured.

---

## Design workarounds (outcome recorded, diagnosis process NOT captured)

### Docker Desktop colon-path volume-parsing workaround
- **What:** Bind-mounting Prometheus/Grafana/OTel config into containers failed, attributed to a Docker Desktop bug where colons in the host path break volume-string parsing.
- **Outcome:** Removed the bind mounts; baked the configs into custom Docker images at build time (each observability service uses `build:` with its own Dockerfile).
- **Evidence:** docker-compose.yml:6-7 and :120-121; Dockerfile.otel/prometheus/grafana.
- **Confidence:** VERIFIED workaround and shape. Diagnosis steps UNVERIFIED (not recorded). Tell it as "I hit this constraint and worked around it," not as a debugging session.

### go:embed can't reach the project-root migrations directory
- **What:** Migrations lived at the project root, but go:embed can't embed files above the embedding package, so the store package couldn't reach them.
- **Outcome:** Duplicated the migration files into the store package and embedded them locally with `//go:embed migrations/*.sql`. The two directories were verified byte-identical.
- **Evidence:** backend/internal/store/db.go:17-18, :76, :90; ClusterOps-Context-Document.md.
- **Confidence:** VERIFIED (layout and directive in code). Diagnosis process not captured.

---

## Evals

### Rule-engine test suite built as a regression baseline for a future LLM swap
- **What:** A table-driven test suite validates that every job-failure and node-state scenario produces the correct classification, explicitly designed to double as an eval baseline so a future LLM's output can be diffed against the deterministic rule output.
- **Outcome:** engine_test.go asserts per-scenario RootCause, Severity, a minimum DebuggingSteps count, minimum Confidence, and non-empty Headline/Summary; runs dependency-free with zap.NewNop().
- **Evidence:** backend/internal/assistant/engine_test.go; CONTEXT.md Harness glossary entry.
- **Confidence:** VERIFIED that the suite and its intent exist. No captured run result or case count — do not cite a pass number.

---

## Tradeoffs

### SSE broker drops slow clients after 100ms instead of buffering
- **What:** The SSE broadcast wraps each client send in a select with a 100ms timeout; on timeout it unsubscribes and drops the client (which reconnects on its own), keeping memory flat under load.
- **Evidence:** backend/internal/api/sse.go broadcast(); ClusterOps-Context-Document.md.
- **Confidence:** VERIFIED.

### Rule-based assistant by design, as a swappable eval baseline
- **What:** The failure-analysis assistant is a deterministic rule engine, not an LLM call, so it can act as a verifiable baseline and be swapped for an LLM later without interface changes (mirrors retrieve→augment→generate with a swappable generate step). Phase-5 upgrade path (Ollama, pgvector) documented but not built.
- **Evidence:** backend/internal/assistant/engine.go package doc; CONTEXT.md.
- **Confidence:** VERIFIED. LLM absence is verifiable.

### Ingestion is the only DB writer; API is read-only
- **What:** Reads and writes split across two binaries; ingestion is the sole writer to PostgreSQL and Redis and the API only reads, to keep cache-invalidation logic simple.
- **Evidence:** backend/internal/ingestion/ingestion.go package doc; ClusterOps-Context-Document.md.
- **Confidence:** VERIFIED.

### Kafka consumer logs-and-skips on error instead of retrying
- **What:** On a failed Kafka message the consumer logs and moves on rather than retrying or dead-lettering; the accepted inconsistency window is corrected by later upserts and cache TTL expiry. Stated as appropriate for a demo.
- **Evidence:** backend/internal/kafka/consumer.go consume-loop comment.
- **Confidence:** VERIFIED.

---

## Gaps (no defensible evidence in this project)
- **Debugging narrative with a captured diagnosis process** — only outcomes recorded, not the diagnosis.
- **agent_error** — no transcripts, no reverted diffs, no comments describing a corrected agent output.
- **Eval with a captured run result** — harness exists, no recorded numbers.
- **Reversal** — single initial commit; nothing recorded as built then undone.
- **Collaboration / defended-tradeoff-against-pushback** — solo build, no recorded back-and-forth.
- **Measured performance** — API latency, Kafka lag, memory, fault-to-alert time all UNKNOWN/not measured.
