# Hearloop — Engineering Story Bank

Personal reference, not a script. Purpose: recall real, defensible engineering episodes before an interview or when answering application questions, without inventing anything. Every episode is grounded in a commit or file:line. Mined from the project's own build history and cross-checked against `resume-system/facts/projects/hearloop.md`.

## Never-claim guardrails (carry into any answer)
- No paying customers, production usage, or validated customer outcomes.
- The eval-harness and partner-action work is eval/graders design with tests green. Production analysis stayed unchanged and the live Bedrock evaluation was explicitly not run. Do not claim a production classifier accuracy number or a launched Insights product.
- The outline-batch episode below is about content/documentation output, not application code. Do not stretch it into "an agent handed me buggy code."

---

## Debugging episodes

### Redis command-quota diagnosis, revised twice to the real root cause (strongest debugging story)
- **What happened:** Redis command volume was blowing through the Upstash free-tier quota.
- **Method:** First hypothesis was worker duplication; added a workersStarted guard but documented it as insufficient. Second hypothesis was idle polling; increased drainDelay and checked the Upstash command counter. The remaining command rate led to the real root cause: persistent Queue connections created by the connection architecture, where Queue instances and Workers could not share the connection arrangement.
- **Outcome:** Workers got dedicated connections; Queue instances became per-enqueue resources closed immediately, so no Queue instance stayed alive between jobs. (Master records the measured effect: ~36,000 → ~7,000 commands/day.)
- **Evidence:** context/METRICS.md:297, :303, :467; commits f04ef694 and a2c1a84.
- **Confidence:** VERIFIED. Good "first guess was wrong, kept digging" narrative.

### Production capture page 404 while the pipeline worked via curl
- **What happened:** The live Vercel `/capture/:token` page returned 404 even though the public pipeline completed when hit directly with curl.
- **Method:** Separated the hosted page from the backend pipeline, then traced the page request to NEXT_PUBLIC_API_URL ending in `/api/v1` while the server fetch also appended `/public/session`. Fixes routed server capture calls through a same-origin proxy and derived the base from the request host.
- **Outcome:** Immediate fix removed `/v1` from the env value; later commits hardened production capture routing.
- **Evidence:** career/interview-prep/coverage/03-e2e-flows.md:283; commits dd40132c and 7b3a0ff8.
- **Confidence:** VERIFIED.

### Shared BullMQ queue caused a handler race
- **What happened:** A single shared queue let workers complete jobs without executing their handlers, because jobs were pulled through the wrong concurrency slot.
- **Method:** Identified the queue topology as the failure boundary; replaced the shared queue with dedicated queues per job type.
- **Outcome:** Transcription, analysis, and other stages each got their own queue.
- **Evidence:** context/DECISIONS.md:33.
- **Confidence:** VERIFIED.

---

## AI-agent episodes

### Rejected an outline-only prep batch and changed the workflow (content, not code)
- **What happened:** The agent produced an outline-only interview-prep batch that did not meet the bar; rejected it.
- **Method:** Recorded the rejection, captured the expected structure in a _TEMPLATE.md, and rewrote the section as a full document.
- **Outcome:** Workflow changed from outline-only batches to a template-backed full format.
- **Evidence:** career/interview-prep/INTERVIEW_PREP.md:415.
- **Confidence:** VERIFIED. Honest framing: this is "agent output missed the bar and I corrected the process," about documentation output, NOT buggy application code.

---

## Evals

### Partner-action holdout eval (design-level)
- **What happened:** The existing 23-case contract-and-safety set was judged insufficient to prove classifier output matched the action a shop owner should take.
- **Method:** Added deterministic page_now / follow_up_today / ignore_for_ops holdout labels, kept injection cases critical, required complete holdout and critical passes for promotion, and tested graders and partitions without calling analyzeTranscript.
- **Outcome:** Graders, sets, and tests recorded green; runner reported three slices. Production analysis stayed unchanged; live Bedrock eval explicitly not run.
- **Evidence:** docs/superpowers/specs/2026-08-16-insights-partner-action-eval-design.md:3, :149, :169; commit a41decaa.
- **Confidence:** VERIFIED. Use as eval-design evidence only, not a production-accuracy claim.

### Engineering-harness eval (agent-safety scenarios)
- **What happened:** Evaluated whether the repo's engineering harness prevented unsafe agent behavior across six scenarios (architectural ambiguity, missing skills, locked decisions, excluded scope, completion claims, dirty worktrees).
- **Method:** One isolated read-only trial per scenario against a pre-harness control and the harness treatment, recording failed predicates and excerpts.
- **Outcome:** Control failed 4 of 6 and passed 2; the harness report says all six required scenarios passed. Codex and Kiro runs remained not_run.
- **Evidence:** docs/agents/evals/results/2026-08-15-codex-baseline.md:18; docs/agents/evals/results/2026-08-15-codex-harness.md:16; commits 2bde2146 and ebf4d57b.
- **Confidence:** VERIFIED.

---

## Tradeoffs

### Hybrid EC2 workers instead of fully serverless
- **What happened:** Chose persistent EC2-hosted BullMQ workers with managed data and frontend services rather than a fully serverless design.
- **Method:** Rejected Lambda for long-running queue consumers; rejected proxying audio through the API in favor of direct S3 uploads; accepted the single-EC2 operations burden with CI/CD, monitoring, and load-test mitigation.
- **Outcome:** Locked a hybrid, cost-optimized architecture: always-on compute for the async pipeline, managed/serverless services where they cut ops and idle cost.
- **Evidence:** career/interview-prep/INTERVIEW_PREP.md:232, :404.
- **Confidence:** VERIFIED.

---

## Gaps
- None flagged by the mining pass. Reversal, tradeoff, eval, bug, and one agent_error episode are all present and grounded.
