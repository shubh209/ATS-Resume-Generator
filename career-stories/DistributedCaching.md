# Distributed Caching (distributed-caching-go) — Engineering Story Bank

Personal reference, not a script. Purpose: recall real, defensible engineering episodes before an interview or when answering application questions, without inventing anything. Mined from the project's git history, code, ADR, and Kiro specs, and cross-checked against `resume-system/facts/projects/distributed-caching.md`. No AI-session transcripts exist for this project, so there are no agent-dialogue episodes.

## Concurrency status — data race FOUND AND FIXED
- The Get/Set data race that failed `TestCache_ConcurrentAccess_NoRace` under `-race` has been fixed: `Get()` now reads the mutable fields while the lock is held (computes `expired` under RLock, copies `Value` under the write lock) instead of reading them after unlocking.
- After the fix, `go test ./internal/cache/ -race` passes and `go test -race ./...` is clean across all packages, so the `INTERVIEW_QA.md` Q33 claim (CI runs `-race` cleanly) is now actually true.
- This is a legitimate "found and fixed a concurrency bug" story. Frame it honestly as a quick find-and-fix, not a multi-session hunt.

## Never-claim / confidence guardrails (carry into any answer)
- All throughput/hit-rate numbers (10,600 req/s, 98.7% hit rate, 163ms Raft election, 92.3% prefix-cache hit, etc.) come from the author's own simulation scripts and were NOT re-run during mining. Treat as **[UNVERIFIED — confirm by re-running]** before citing fresh.
- Many tradeoff episodes below are grounded in `INTERVIEW_QA.md` quoting the code, not the code read directly. Those are labeled UNVERIFIED — open the cited file to confirm before stating specifics.
- No AI-agent-error episode and no collaboration episode exist (no transcripts, solo repo).

---

## Debugging episodes

### Data race between Get (lazy expiry) and Set (upsert) — found and fixed
- **What:** `TestCache_ConcurrentAccess_NoRace` was failing under `-race`. `Get` read the entry pointer under RLock, unlocked, then read `IsExpired()` and `Value` with no lock held while a concurrent `Set` mutated that entry under Lock. The double-checked-locking comment only guarded the delete, not the initial field reads.
- **Method:** Reproduced with `go test ./internal/cache/ -run TestCache_ConcurrentAccess_NoRace -race`; detector pointed at Set()'s upsert racing IsExpired() via Get().
- **Outcome:** Fixed by reading mutable fields while the lock is held: compute `expired := exists && entry.IsExpired(time.Now())` inside the RLock section and copy `value := entry.Value` inside the hit-path write-lock section. After the fix, `go test ./internal/cache/ -race` passes and `go test -race ./...` is clean, so INTERVIEW_QA.md Q33 is now true.
- **Evidence:** fix in cache.go Get; cache_test.go:146-161; before-fix race output; after-fix `go test -race ./...` all ok.
- **Confidence:** VERIFIED (reproduced the failure, applied the fix, confirmed the suite passes under -race).

### Reverse proxy was caching 404s; restricted to 2xx
- **What:** Proxy cached 404 responses, so it kept serving "not found" after a product was later created.
- **Method:** Documented as found during live testing; fix guards the cache-write path to 2xx only.
- **Outcome:** Caching restricted to `StatusCode >= 200 && < 300`, with a comment on why transient states must not be cached. Regression test `TestProxy_404Response_NotCached` passes (re-run during mining).
- **Evidence:** proxy.go:79-85; proxy_test.go:212-232; docs/distributed_caching.md:64.
- **Confidence:** VERIFIED that guard, comment, and passing test exist. **[UNVERIFIED — confirm]** that it was found via live testing; guard and test landed together in commit 8d96db1, so no before/after commit shows the bug.

### docker compose startup: Prometheus volume path + Postgres port conflict + bad go.mod revision
- **What:** Stack didn't come up: colon-in-path on the Prometheus config volume, host Postgres port conflict on 5432, invalid pgservicefile module revision breaking go mod.
- **Method:** One fix commit enumerating each cause and fix.
- **Outcome:** Prometheus config moved to inline Docker `configs:`; Postgres remapped 5432→5433:5432; pgservicefile pinned to a valid revision and go.sum regenerated.
- **Evidence:** commit 8f91267 and its diff.
- **Confidence:** VERIFIED.

### Len() over-counted expired entries; added LiveLen()
- **What:** `Len()` returned `len(entries)` including expired-but-uncleaned entries, so any accurate live count was wrong.
- **Outcome:** Added `LiveLen()` (scans under RLock, counts non-expired, O(n)); kept `Len()` as the cheap approximate count for metrics/logging.
- **Evidence:** commit ba7b4e6 diff cache.go:152-178; callers at cacheserver.go:83, proxy.go:191,197, eviction.go:96-98.
- **Confidence:** VERIFIED. **[UNVERIFIED — confirm]** whether a concrete bug was observed or it was preventive hardening.

---

## AI-agent episodes

### Rewrote a docs write-up to strip AI writing patterns and an inflated claim (prose, not code)
- **What:** A project write-up doc was rewritten to remove AI-writing tells and soften an inflated tagline ("reduce GPU compute cost by up to 98%" → "measures LLM prefix caching savings using real transformer math").
- **Outcome:** 56 insertions / 39 deletions on one file; superlatives toned down.
- **Evidence:** commit 44deb66; docs/distributed_caching.md:1-9.
- **Confidence:** VERIFIED that the rewrite happened. **[UNVERIFIED — confirm]** that the original prose was AI-generated. This is a prose cleanup, NOT an agent-wrote-buggy-code episode.

### Spec-driven scaffolding exists, but no captured agent missteps
- **What:** Built spec-first via Kiro specs (requirements/design/tasks) for both the Go cache and the Python module. Planning artifacts, not session logs; no recorded agent-error-and-correction.
- **Evidence:** .kiro/specs/python-llm-rag-simulation/design.md:636-666; .kiro/specs/distributed-caching-go/design.md.
- **Confidence:** VERIFIED specs exist. No agent-error episode recoverable.

---

## Evals & tests

### Python Hypothesis suite — 24 correctness properties
- **What:** Property-based tests, one per numbered design property (e.g. Property 2: vectorized cost == scalar within rtol=1e-9; Property 10: LRU eviction; Property 24: monthly projection arithmetic), plus example/unit tests.
- **Evidence:** test_models.py:42, :85-88; test_prefix_cache.py:308-341; test_rag.py:312-316; design.md:636-666.
- **Confidence:** VERIFIED the suite and property tagging exist. **[UNVERIFIED — confirm]** the "206 tests all passing" count (not re-run; run `pytest` in python/).

### 17 Go unit tests for the LLM prefix-cache module
- **What:** FLOP-math scaling (manually verified Llama3-70B case), cost ordering, deterministic hashing, cache hit/miss + LRU, scenario sanity.
- **Evidence:** commit dd0f607 ("17/17 pass").
- **Confidence:** VERIFIED commit and enumerated intent. **[UNVERIFIED — confirm]** current pass count (not re-run).

### TestProxy_404Response_NotCached — regression eval for the 404 bug
- **What:** Mock upstream returns 404, two identical GETs, asserts upstream hit twice (no cache serve). Guards the 404 episode above.
- **Evidence:** proxy_test.go:212-232; re-run during mining: PASS.
- **Confidence:** VERIFIED (re-run).

### Cache-Control semantics eval
- **What:** Tests assert the proxy honors max-age=300 (cache), no-store, no-cache, max-age=0 (no cache), counting upstream calls.
- **Evidence:** proxy_test.go:104-197.
- **Confidence:** VERIFIED tests exist. **[UNVERIFIED — confirm]** current pass/fail (not individually re-run).

---

## Tradeoffs (system-design material — this project's strength)

### Raft for leader election only, NOT write replication (ADR 0001)
- **What:** Chose Raft for leader election only (data stays on one node via consistent hashing) over full write replication. Rationale: it's a cache, not source of truth; a dead node's keys miss and fall through to PostgreSQL, acceptable for a learning sandbox. Consequence accepted: node failure = cache miss, no durability/HA.
- **Evidence:** docs/adr/0001-raft-for-leader-election-only.md; INTERVIEW_QA.md Q18.
- **Confidence:** VERIFIED (ADR states the tradeoff). **[UNVERIFIED — confirm]** the exact rpc.go missing-log-fields detail.

### Write-behind invalidation DELETEs the key instead of SETting the new value
- **What:** The delayed write-behind task deletes the entry rather than writing the new value, because ~100ms later a concurrent read may have re-populated with fresh DB data and a SET would overwrite the newer value. DELETE forces a correct re-fetch at the cost of one miss.
- **Evidence:** INTERVIEW_QA.md Q15, Q13 (writeBehindDelay=100ms, writeBehindDeadline=5s).
- **Confidence:** **[UNVERIFIED — confirm]** in internal/invalidation/writebehind.go.

### Cache-write error after DB write treated as non-fatal
- **What:** If the cache update/invalidation fails after the DB write committed, the request still succeeds; DB is source of truth, so the next read just misses and fetches correctly.
- **Evidence:** INTERVIEW_QA.md Q14 (middleware.go UpdateProduct `_ = ca.strategy.OnWrite(...)`).
- **Confidence:** **[UNVERIFIED — confirm]** in internal/api/middleware.go.

### 150 virtual nodes per physical node on the hash ring
- **What:** 150 vnodes per node to even out key distribution across only 3 physical nodes; more vnodes = more memory + longer sorted slice.
- **Evidence:** INTERVIEW_QA.md Q5 (defaultVirtualNodes=150; distribution test).
- **Confidence:** **[UNVERIFIED — confirm]** in ring.go / cluster_test.go.

### FNV-1a over a cryptographic hash for the ring
- **What:** FNV-1a (fast, allocation-free, deterministic) over SHA-256/SipHash; crypto strength unnecessary on a private Docker network. Acknowledged weakness to adversarial hash-flooding; public-facing would use SipHash.
- **Evidence:** INTERVIEW_QA.md Q6 (hashKey uses fnv.New32a()).
- **Confidence:** **[UNVERIFIED — confirm]** in ring.go.

### Inline idempotent SQL migration instead of a migration tool
- **What:** Schema runs inline on startup (CREATE TABLE IF NOT EXISTS, INSERT ON CONFLICT DO NOTHING); dependency-free for a sandbox, no version-tracked migrations. Would use a real tool in production.
- **Evidence:** INTERVIEW_QA.md Q26 (postgres.go migrate()); internal/db/migrations/001_products.sql exists.
- **Confidence:** **[UNVERIFIED — confirm]** the migrate() body in postgres.go.

### Separate proxy and API services — accepted an extra network hop
- **What:** Proxy (:8080, cross-cutting HTTP) and API (:8081, business/cache-aside logic) are separate binaries; extra hop accepted for a sandbox, would measure against P99 in production.
- **Evidence:** cmd/proxy and cmd/api exist in the repo tree; INTERVIEW_QA.md Q2.
- **Confidence:** VERIFIED both binaries exist. **[UNVERIFIED — confirm]** the reasoning as a discrete decision moment.

---

## Gaps (no defensible evidence)
- **Multi-session debugging saga with a paper trail** — the reproducible data race was found during mining, not by a recorded hunt, and is unfixed; the 404 bug has no before/after commit.
- **agent_error** — no transcripts; closest is a prose cleanup, not code.
- **Design reversal** — ADR records a decision + rejected alternative, but nothing was implemented then reverted.
- **Defended tradeoff with re-verified numbers** — all metrics are from the author's own sim scripts, not re-run.
- **Collaboration / disagreement** — single-author repo, no PR reviews.
