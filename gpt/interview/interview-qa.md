# Hearloop — Interview Q&A

Every answer is grounded in a real file. Every number came from the code.

---

## SYSTEM OVERVIEW

**Q: What is Hearloop? Describe it in one paragraph.**

Hearloop is a voice micro-feedback platform offered as a B2B API. A Partner (a business) embeds a widget or generates a QR code; an End User taps, speaks for up to 5 seconds, and the audio gets uploaded directly to object storage. The API then runs an async pipeline — validate → transcribe → analyze — and delivers structured Insights (transcript, sentiment, topics, urgency, summary, flags) to the Partner's webhook. Partners also get a web dashboard to review sessions.

Evidence: `CONTEXT.md`, `apps/api/src/index.ts`, `apps/api/src/jobs/`

---

## ARCHITECTURE & DESIGN

**Q: Walk me through the overall system architecture.**

Three main pieces:

1. **Fastify API** (`apps/api`) on an EC2 instance, port 3001. Handles HTTP routing, auth, and job enqueueing.
2. **BullMQ workers** — six named queues — running in-process alongside the HTTP server inside the same Docker container. Each worker has its own IORedis connection.
3. **Next.js web app** (`apps/web`) deployed on Vercel. Auth, dashboard, onboarding, and the hosted capture page.

Supporting infra: Cloudflare R2 (audio storage), Upstash Redis (BullMQ queues), PostgreSQL (data), AWS Bedrock (AI analysis), Groq (transcription), AWS CloudWatch (metrics).

Evidence: `apps/api/src/index.ts`, `apps/api/Dockerfile`, `.github/workflows/docker-image.yml`

---

**Q: Why run workers in the same process as the HTTP server instead of separating them?**

**Short answer:** simplicity at this scale. On a single EC2 instance, a separate worker process adds a Docker container, a separate CI job, and shared-state concerns with no real benefit until volume demands it.

- The risk accepted: a CPU-heavy job could slow HTTP response times. At 5-second clips the jobs are fast (Groq transcription + one Bedrock call), so this hasn't been a problem.
- `drainDelay: 600` (10 min idle poll), `concurrency: 1`, `stalledInterval: 600_000` — all tuned to stay well under Upstash's free-tier quota.
- Trade-off accepted: single point of failure. If the container crashes, both HTTP and workers go down together.

Evidence: `apps/api/src/index.ts` `startWorkers()`, `apps/api/src/lib/queue.ts` `WORKER_OPTIONS`

---

**Q: Why BullMQ + Redis instead of a managed queue like SQS?**

**Verdict:** BullMQ + Upstash Redis — fits free tier, gives visibility, retries, and backoff without extra AWS spend.

- SQS would mean another AWS service, IAM policy, and SDK. Upstash Redis is a single connection string and already needed for BullMQ.
- BullMQ gives per-job retry counts and exponential backoff out of the box. SQS needs separate DLQs and visibility-timeout tuning to achieve the same.
- What SQS does better: true at-least-once guarantee and infinite scale. BullMQ on Redis can lose a job if Redis goes down before persistence. Acceptable risk at this stage.

Evidence: `apps/api/src/lib/queue.ts`, `apps/api/package.json` (`bullmq`, `ioredis`)

---

**Q: Why does each BullMQ worker get its own IORedis connection?**

BullMQ workers use Redis blocking commands (`BZPOPMIN`, `RPOPLPUSH`) that monopolize a connection. Sharing one connection across workers causes them to fall back to active polling — which ignores `drainDelay` and burns Upstash's command quota. The comment in `queue.ts` quantifies it: active polling costs ~691K commands/day vs. the ~806-command budget at `drainDelay: 600`.

Enqueue helpers use a separate short-lived Queue instance + connection, closed immediately after `queue.add()` fires.

Evidence: `apps/api/src/lib/queue.ts` (top comment block + `makeWorkerConn()`)

---

**Q: What is the full job pipeline and what does each job do?**

```
finalize (HTTP) → validate-recording → transcribe → analyze → deliver-webhook
```

- **validate-recording**: checks mime type (allowlist of 7 types), verifies file size (1 KB min – 10 MB max), reads the first 12 bytes to check the audio header (EBML for webm, RIFF for wav, ftyp for mp4, ID3/sync for mp3, OggS for ogg). Enqueues transcribe on pass, marks session `failed` with a reason code on fail.
- **transcribe**: downloads audio from R2, calls Groq `whisper-large-v3-turbo` with `verbose_json`, extracts text, detected language, duration from segments, and confidence from `avg_logprob` (> -0.5 = high). Inserts into `analyses` table. Enqueues analyze.
- **analyze**: fetches partner's `business_context`, calls Bedrock Nova Lite (Haiku fallback on error/bad JSON), stores sentiment/topics/urgency/summary/flags. Marks session `completed`. Enqueues webhook delivery.
- **deliver-webhook**: builds full event payload, HMAC-signs it, POSTs to partner's webhook URL. Retries up to 7 times with exponential backoff starting at 5s. Dead-letters after 7 failures.
- **expire-session**: scheduled with a `delay` equal to the session TTL (30 min for API sessions, 24h for public/capture sessions). Deletes audio from R2, marks session `expired`.

Evidence: `apps/api/src/jobs/`

---

## DATABASE

**Q: What database do you use and why Kysely instead of Prisma?**

**Verdict:** PostgreSQL with Kysely — full TypeScript type safety without a generated client or Prisma DSL.

- Kysely works directly with the `pg` Pool. No build step for schema changes, no shadow database for migrations.
- Prisma's generated client is heavier. With mostly simple CRUD + one join per query, that overhead isn't worth it.
- Trade-off: Kysely is more verbose than Prisma's ActiveRecord-style API. Fine for this schema size.

Connection pool: `max: 10`, `idleTimeoutMillis: 30000`, `connectionTimeoutMillis: 5000`, SSL in production.

Evidence: `apps/api/src/lib/db.ts`, `apps/api/package.json`

---

**Q: Walk me through the database schema.**

Eight tables across 8 migrations:

| Table | Purpose |
|---|---|
| `partners` | Business accounts — email, bcrypt password_hash, webhook_url, allowed_origins, business_context |
| `api_keys` | SHA-256 hashed keys, type `secret`/`public`, revocation tracking |
| `sessions` | One capture attempt — 9-state lifecycle (`created` → `completed`/`failed`/`expired`) |
| `recordings` | Audio artifact metadata — storage_key, mime_type, sha256_hash, size_bytes |
| `analyses` | Transcription + AI output — transcript, sentiment, topics_json, moderation_json, token counts |
| `webhook_deliveries` | Delivery log — attempt_count, response_code, status `pending`/`delivered`/`failed`/`dead` |
| `session_create_tokens` | Short-lived (10 min), single-use tokens so the browser creates sessions without repeated embed-key exposure |
| `capture_links` | Durable QR/SMS tokens — target_label, target_key (normalized), soft-deleted with `active=false` |

Evidence: `packages/db/migrations/001_initial.sql`, `apps/api/src/lib/db.ts`

---

**Q: Why store `topics_json` and `moderation_json` as TEXT instead of JSONB?**

The JSON is always written and read as a unit — no need to query inside it with `->` operators — so the column type doesn't affect query performance. The schema was kept portable across PostgreSQL hosts (Neon, RDS, local). If cross-session topic filtering were needed, JSONB with a GIN index would be the upgrade path.

Evidence: `packages/db/migrations/001_initial.sql`

---

## AI / ML

**Q: What AI models do you use and why?**

Two AI calls per pipeline run:

1. **Transcription**: Groq `whisper-large-v3-turbo` via `groq-sdk`. Fast, cheap, Whisper-quality output with `verbose_json` for segment-level confidence and language detection. Temperature `0.0`. Partner can pass a `promptText` (up to 224 chars) for Whisper context priming.

2. **Analysis (classification)**: AWS Bedrock `us.amazon.nova-lite-v1:0` as primary, `us.anthropic.claude-haiku-4-5-20251001-v1:0` as fallback. Nova Lite is the cheapest Bedrock model (~$0.0001/call), sufficient for a fixed JSON classification schema with `maxTokens: 120` and `temperature: 0.0`.

Evidence: `apps/api/src/lib/groq.ts`, `apps/api/src/lib/claude.ts`

---

**Q: Why Bedrock instead of calling the Anthropic or OpenAI API directly?**

**Short answer:** AWS-native billing and credential consolidation.

- The infra already lives on AWS (EC2, IAM, CloudWatch). Bedrock reuses the same IAM credential chain — no separate API key.
- Nova Lite is extremely cheap. The transcript is capped at 800 chars (`MAX_TRANSCRIPT_CHARS`), output at 120 tokens.
- Trade-off: more complex SDK (InvokeModelCommand, manual JSON encoding) vs. the cleaner Anthropic SDK. The `@anthropic-ai/sdk` in `package.json` is a remnant from evaluation before Bedrock was chosen.

Evidence: `apps/api/src/lib/claude.ts`, `apps/api/package.json`

---

**Q: What is the Haiku fallback and when does it trigger?**

If Nova Lite returns invalid JSON (parse error after stripping markdown fences) or throws, `analyzeTranscript()` falls back to `us.anthropic.claude-haiku-4-5-20251001-v1:0`. Same system prompt, same 120-token cap, higher quality.

The model used (`"nova-lite"` or `"haiku-fallback"`) is stored in `analyses.model_used`. CloudWatch metrics are emitted with an `Outcome` dimension (`"success"` or `"fallback"`) to allow alarming on fallback rate.

Evidence: `apps/api/src/lib/claude.ts` `analyzeTranscript()`, `apps/api/src/jobs/analyze.ts`

---

**Q: Is this RAG? Is this an agent or agentic workflow?**

Neither.

- **Not RAG.** There's no vector store or retrieval step. The `business_context` string is fetched from the DB and injected directly into the user message as a prefix (`Business context: ...`). This is prompt injection / prompt context.
- **Not an agent.** There's no multi-step orchestration, tool calling, or state machine. It's two sequential LLM calls per session (Groq transcription, then Bedrock classification), each stateless and deterministic.

Evidence: `apps/api/src/lib/claude.ts` `analyzeTranscript()`, `apps/api/src/jobs/analyze.ts`

---

**Q: What does the analysis output look like and how is it validated?**

The model returns JSON: `sentiment` (positive/neutral/negative), `sentimentScore` (0–1), `topics` (array from an allowlist of 10 slugs), `urgency` (none/follow_up/urgent), `summary` (≤280 chars), `qualityFlags`, `moderationFlags`.

Validation in `parseAnalysis()`:
- Topics filtered against `VALID_TOPICS` (10 allowed values). Unknown values dropped. Empty → `["other"]`.
- Sentiment and urgency sanitized — any invalid value defaults to `"neutral"` / `"none"`.
- `sentimentScore` clamped to [0, 1].
- Transcript with fewer than 2 words skips the LLM entirely → `qualityFlags: ["too_short"]`.
- Empty transcript → `qualityFlags: ["inaudible"]`.

Evidence: `apps/api/src/lib/claude.ts` (`VALID_TOPICS`, `parseAnalysis`, `sanitizeSentiment`, `clamp`)

---

**Q: What is business context and how is it imported?**

Business context is a partner-supplied plain-text description (up to 500 chars) of their business — what they do, who their customers are, what feedback dimensions matter. It gets prepended to the Bedrock prompt so topics and summaries are more relevant.

Import flow:
1. Partner provides a website URL.
2. `assertPublicHttpsUrl` validates it (HTTPS only, no private IPs — SSRF guard).
3. A BullMQ job (`import-business-context`) fires with 1 attempt, 1-hour result TTL.
4. A Crawl4AI sidecar (`SCRAPER_URL`, default `http://127.0.0.1:11235`) fetches the page and converts it to Markdown. Timeout: 25 seconds.
5. Markdown truncated to 8,000 chars (`IMPORT_MARKDOWN_MAX_CHARS`), sent to Bedrock Nova Lite (`maxTokens: 180, temperature: 0.2`) to produce a ≤500-char summary.
6. Draft returned to the frontend. **Partner must click Save** to write it to the DB — the import never auto-saves.
7. Rate limit: 3 imports per partner per hour via Redis INCR + 3600s TTL.

Evidence: `apps/api/src/jobs/import-business-context.ts`, `apps/api/src/lib/scrape-via-crawl4ai.ts`, `apps/api/src/lib/summarize-business-context.ts`, `apps/api/src/lib/import-rate-limit.ts`

---

## AUTHENTICATION & SECURITY

**Q: Walk me through the authentication system.**

Three credential types:

1. **Partner secret key** (`sk-live_…`): server-side API calls. 32 random bytes (`randomBytes(24)`) prefixed with `sk-live_`. Stored as SHA-256 hash in `api_keys.key_hash`. Lookup hashes the incoming key, matches the hash, checks `revoked_at IS NULL` and `partners.status = 'active'`. Updates `last_used_at` on each use.

2. **Widget embed key** (`pk-live_…`): browser-safe. Same format but `type = 'public'`. Restricted to the `/public/sessions/create-token` route. Requires `allowed_origins` to be configured — requests from other origins are rejected with 403.

3. **Dashboard session token** (`hlps.{base64url-body}.{hmac-sig}`): issued after email+password login. HMAC-SHA256 over the base64url-encoded `{sub, exp}` payload using `PARTNER_SESSION_SECRET`. TTL: 30 days. Verified with `timingSafeEqual` to prevent timing attacks. No JWT library — built with Node's `crypto` module.

Evidence: `apps/api/src/lib/authenticate-partner.ts`, `apps/api/src/lib/create-api-key.ts`, `apps/api/src/lib/partner-session.ts`, `apps/api/src/lib/hash-api-key.ts`

---

**Q: Why store API keys as hashes?**

If the database is compromised, a hashed key can't be used to impersonate a partner. SHA-256 is sufficient here (unlike passwords) because the raw key has 192 bits of entropy from `randomBytes(24)` — brute force is infeasible. The `key_prefix` (first 12 chars) is stored in plaintext so the dashboard can show `sk-live_a3f…` for identification without exposing the full key.

Evidence: `apps/api/src/lib/create-api-key.ts`, `apps/api/src/lib/hash-api-key.ts`

---

**Q: How does webhook signing work?**

HMAC-SHA256 over `{timestamp}.{rawBody}` using `WEBHOOK_SIGNING_SECRET`. Signature format: `sha256=` + hex digest. Same scheme as Stripe.

Headers sent: `X-Hearloop-Event`, `X-Hearloop-Delivery`, `X-Hearloop-Timestamp`, `X-Hearloop-Signature`.

The partner's server reconstructs the signed string from the timestamp header + raw body and compares. Including the timestamp prevents replay attacks.

Evidence: `apps/api/src/jobs/deliver-webhook.ts` `signPayload()`

---

**Q: What is SSRF and how do you prevent it?**

SSRF (Server-Side Request Forgery): an attacker supplies a URL that makes the server fetch an internal resource — like `http://169.254.169.254/` (AWS metadata) or `http://localhost:5432` (the database).

Two guards:

1. **`assertPublicHttpsUrl()`** — sync check before any fetch. Rejects: non-HTTPS, embedded credentials, loopback (`127.*`, `::1`), RFC 1918 ranges (`10.*`, `192.168.*`, `172.16-31.*`), link-local (`169.254.*` — AWS metadata), IPv6 local (`fc*`, `fd*`), and `localhost`/`*.local`.

2. **Crawl4AI sidecar** — performs a second DNS-level check at fetch time (returns `blocked_resolved_ip` if the resolved IP is private, protecting against DNS rebinding).

Applied to: business-context import and webhook delivery.

Evidence: `apps/api/src/lib/assert-public-https-url.ts`, `apps/api/src/lib/blocked-hostname.ts`, `apps/api/src/lib/scrape-via-crawl4ai.ts`

---

**Q: How does rate limiting work?**

Two layers:

1. **API rate limit** (`@fastify/rate-limit`): 100 requests per minute. Keyed on the first 16 chars of the Bearer token (falls back to IP). Returns HTTP 429.

2. **Import rate limit**: Redis INCR on `hearloop:import-rate:{partnerId}` with a 3600s TTL. Max 3 imports per partner per hour. No library — just `INCR` + `EXPIRE`.

Evidence: `apps/api/src/index.ts`, `apps/api/src/lib/import-rate-limit.ts`

---

**Q: Why bcrypt with 12 rounds?**

12 rounds is ~300ms per hash on modern hardware — slow enough to defeat offline brute-force, fast enough not to hurt login UX. It's the standard recommendation and matches common production configurations. bcrypt automatically incorporates the salt into the stored hash, so no separate salt column is needed.

Evidence: `apps/api/src/routes/partners.ts` (`SALT_ROUNDS = 12`)

---

## SESSION LIFECYCLE

**Q: Walk me through a complete session from widget embed to webhook delivery.**

1. **Embed init**: widget calls `POST /v1/public/sessions/create-token` with the embed key. API validates origin against `allowed_origins`, issues a session-create token (32 random bytes, 10-min TTL, stored in DB).
2. **Session create**: widget exchanges the token for a session via `POST /v1/public/sessions`. Token is validated (expiry + `used_at` check), session created in `created` state.
3. **Open**: `POST /v1/public/session/:token/open` → `opened`.
4. **Upload URL**: `POST /v1/public/session/:token/upload-url` returns a pre-signed R2 PUT URL (900s TTL). Browser uploads audio directly — never through the API server.
5. **Finalize**: `POST /v1/public/session/:token/finalize` upserts the `recordings` row, moves session to `submitted`, enqueues `validate-recording`.
6. **Pipeline**: validate → transcribe → analyze → webhook. Session moves `submitted` → `processing` → `completed` (or `failed`).
7. **Webhook**: partner receives a signed `POST` with the full Insights payload.

Evidence: `apps/api/src/routes/public.ts`, `apps/api/src/routes/sessions.ts`

---

**Q: What is the session-create token and why does it exist?**

The embed key (`pk-live_…`) is long-lived. If the widget called `POST /sessions` directly on every page load, the embed key would appear in every network request visible in browser devtools.

The session-create token is single-use (marked `used_at` on consumption) and expires in 10 minutes. So the embed key only appears once per "capture intent" rather than on every session creation.

Evidence: `apps/api/src/routes/public.ts` `POST /public/sessions/create-token`

---

**Q: How does the expiry job work?**

When a session is created, `enqueueExpireSession(sessionId, delayMs)` enqueues a BullMQ job with a `delay` equal to the session's TTL. BullMQ holds the job in a delayed set in Redis and promotes it after the delay.

When the job runs, it checks if the session is already terminal (`completed`, `failed`, `expired`, `deleted`). If so, it's a no-op. Otherwise it deletes the audio from R2 and marks the session `expired`.

Evidence: `apps/api/src/jobs/expire-session.ts`, `apps/api/src/routes/sessions.ts`

---

## STORAGE & INFRA

**Q: Why Cloudflare R2 instead of S3?**

**Short answer:** zero egress fees.

The transcribe worker downloads audio from R2 and re-uploads to Groq — a full round-trip. S3 charges for that egress. R2 doesn't. The storage client uses the AWS S3 SDK pointed at the R2 endpoint (`STORAGE_ENDPOINT`) — R2 is S3-compatible, so no SDK change was needed.

Evidence: `apps/api/src/lib/storage.ts`, `apps/api/src/lib/env.ts`

---

**Q: How does direct-browser upload work and why not route audio through the API?**

The API issues a pre-signed PUT URL (`@aws-sdk/s3-request-presigner`, 900s TTL). The browser uploads audio directly to R2. The API never handles the audio bytes for upload.

Routing megabyte audio files through the API wastes bandwidth, increases latency, and strains the EC2 instance. Direct upload is the standard pattern for user-generated content.

Evidence: `apps/api/src/lib/storage.ts` `getUploadSignedUrl()`, `apps/api/src/routes/public.ts`

---

**Q: Walk me through the CI/CD pipeline.**

GitHub Actions on push to `main`:

1. **Validate job**: `tsc --noEmit` TypeScript check + Hadolint Dockerfile lint. Fast gate before any AWS spend.
2. **Deploy job** (only if validate passes):
   - Adds the GitHub runner's IP to EC2 Security Group `sg-0fdee87e11e224206` on port 22 (ephemeral firewall hole).
   - Authenticates to ECR, builds `--platform linux/amd64 --no-cache`, pushes to ECR.
   - SSH into EC2, pulls image, stops old container, starts new one with `--env-file /home/ec2-user/.env --restart unless-stopped`.
   - `docker image prune -af` — added after the root volume hit 14 GB (55 orphaned images).
   - Health check: `curl --fail --retry 3 /health` after 15s.
3. **Revoke runner IP** — always runs, even on failure. Cleans up the ephemeral firewall hole.

Evidence: `.github/workflows/docker-image.yml`

---

**Q: Why a 4-stage Dockerfile?**

```
base → deps (all deps + devDeps) → prod-deps (no devDeps) → builder (compiles TS) → runner (prod-only)
```

The `prod-deps` stage exists because devDependencies like `babel`, `jest`, `ts-jest` carry transitive CVEs but are never used at runtime. The final `runner` image copies from `prod-deps` + compiled `dist/` — smallest image, fewest vulnerabilities.

Evidence: `apps/api/Dockerfile`

---

**Q: How does CloudWatch observability work?**

After each successful Bedrock call, the analyze job calls `emitBedrockInvocation()` as fire-and-forget (`.catch()` swallows the error so a CloudWatch failure never blocks the pipeline).

Four metrics emitted in one `PutMetricDataCommand` to namespace `CLOUDWATCH_NAMESPACE`:
- `BedrockLatencyMs`
- `BedrockInputTokens`
- `BedrockOutputTokens`
- `BedrockInvocationCount`

Two dimensions: `ModelId` (full Bedrock model string) and `Outcome` (`"success"` for nova-lite, `"fallback"` for haiku). Enables alarming on fallback rate.

Evidence: `apps/api/src/lib/cloudwatch.ts`, `apps/api/src/jobs/analyze.ts`

---

## MONOREPO & TOOLING

**Q: Why a Turborepo monorepo?**

Three workspaces: `apps/api`, `apps/web`, `packages/db`. Turbo handles build ordering (`dependsOn: ["^build"]`) and output caching (`dist/**`). The `packages/db` migrations can be shared by both apps. Without Turbo, you'd manually coordinate build order across packages.

Evidence: `turbo.json`, root `package.json` workspaces

---

**Q: Why Fastify over Express?**

Type-safe request handling, a plugin system (`app.register()`) that makes route isolation clean, and faster JSON serialization. `@fastify/rate-limit` integrates natively as a plugin.

Trade-off: smaller ecosystem and less Stack Overflow coverage than Express. Not a real concern for a greenfield API this size.

Evidence: `apps/api/src/index.ts`, `apps/api/package.json` (`fastify@^5.8.3`)

---

**Q: What testing exists in this codebase?**

Jest with Babel transformer (`babel-jest`, `@babel/preset-typescript`). Test files in `__tests__/`:

- `jobs/__tests__/analyze.test.ts` — analyze job unit tests
- `lib/__tests__/assert-public-https-url.test.ts` — SSRF guard, includes property-based tests with `fast-check`
- `lib/__tests__/cloudwatch.test.ts`
- `lib/__tests__/env.test.ts`
- `lib/__tests__/partner-session.test.ts`
- `routes/__tests__/` — route-level tests

`fast-check` (`^3.23.2`) is used on the SSRF guard — generates arbitrary hostname inputs to verify the blocklist is exhaustive.

Evidence: `apps/api/package.json`, file tree

---

## CAPTURE LINKS & TARGETS

**Q: What is a capture link and how does it differ from the widget embed?**

A capture link is a durable token (32 random hex bytes, path `/c/{token}`) that creates a fresh session each time it's visited. It's printed as a QR code on a receipt or counter signage for in-person feedback — the primary capture surface for service businesses.

The widget embed (`pk-live_…`) is the online surface — a floating button on the partner's website.

Key differences:
- Capture link: durable, no JS, works as a plain URL, creates a new session per scan.
- Widget embed: tied to an origin (CORS check), requires JS, shorter-lived session-create token flow.

A capture link can carry a **Target** (`targetLabel` / `targetKey`) — a normalized slug identifying the thing being reviewed (location, service, staff member). Sessions created from the link carry the target in `metadata_json`. Dashboard groups sessions by `target_key` in the "By-Target" view.

Evidence: `apps/api/src/routes/capture-links.ts`, `apps/api/src/routes/public.ts` (`POST /public/capture/:linkToken/session`)

---

## KEY TRADE-OFF SUMMARY

| Decision | Chose | Passed On | Why |
|---|---|---|---|
| Query builder | Kysely | Prisma | No generated client, no build step, raw SQL control |
| Queue | BullMQ + Upstash Redis | SQS | Free tier fits, retries + backoff built in, single connection string |
| AI classification | AWS Bedrock Nova Lite | OpenAI / Anthropic direct | Same IAM credentials, ~$0.0001/call, no extra API key |
| Transcription | Groq Whisper | AWS Transcribe | Faster, cheaper, verbose_json gives confidence + language |
| Object storage | Cloudflare R2 | AWS S3 | Zero egress fees for the download-then-upload pattern |
| Worker topology | In-process with HTTP | Separate service | Simpler ops at current scale, easy to split later |
| Session tokens | Custom HMAC (crypto) | JWT library | No extra dependency, Node crypto is sufficient |
| Passwords | bcrypt 12 rounds | argon2 | Standard, well-audited, right cost factor for login UX |




# Technical And Trade-Off Interview Q/A

## Product Direction

### What is this project now?

**In one line:** It started as a fintech clone, but I intentionally narrowed it into a crypto and financial decision simulator.

- How it works: signed-in users use Simulation and Crypto tabs instead of fake banking screens.
- In this codebase: old Home, Activity, transaction storage, lock/passcode, and fake widgets were removed.
- Why that matters: fewer features, but much stronger correctness, data trust, and product focus.

Evidence: `docs/project-reference/README.md`, `docs/project-reference/issues.md`

### Why pivot away from the fintech clone?

**Short answer:** The old clone had shallow surfaces that looked real but did not create real user trust.

- The alternative I weighed: keep banking-style screens and polish them.
- Trade-off I accepted: the app looks narrower, but every remaining screen has a real backend/data story.
- If the use case changed: I would only add banking surfaces back if they served the simulator directly.

Evidence: `docs/project-reference/issues.md`

## Expo And React Native

### Why Expo Router instead of plain React Navigation?

**Verdict:** I used Expo Router because the app already maps cleanly to route files and authenticated route groups.

- Why it fits here: public auth screens and authenticated tabs are naturally separated by folders.
- What React Navigation is better at: lower-level custom navigation control.
- In this codebase: route wrappers live in `apps/frontend/app`, and real screens live under `apps/frontend/src/features`.
- Trade-off I accepted: Expo Router conventions shape the folder structure.

Evidence: `apps/frontend/app/_layout.tsx`, `docs/project-reference/architecture.md`

### Why React Native / Expo for this app?

**Short answer:** The product is mobile-first, and Expo let me build the simulator, auth, charts, storage, and native polish without owning native setup too early.

- The alternative I weighed: a web app first.
- Trade-off I accepted: native mobile dependencies add testing and build complexity.
- If the use case changed: for recruiter demos only, a web-first version would be faster to share.

Evidence: `package.json`, `apps/frontend/app/_layout.tsx`

## Auth

### Why Clerk?

**Short answer:** Clerk gave me real auth quickly, especially phone-based flows, without building identity infrastructure myself.

- The alternative I weighed: custom auth or Firebase Auth.
- Trade-off I accepted: vendor dependency and Clerk-specific app wiring.
- In this codebase: `ClerkProvider` wraps the app and uses a token cache.

Evidence: `apps/frontend/app/_layout.tsx`, `apps/frontend/src/features/auth/providers/clerkTokenCache.ts`

### How do auth redirects work?

**In one line:** Auth state is centralized so route screens stay thin.

- How it works: `_layout.tsx` calls `useAuthRedirects()` before rendering the stack.
- In this codebase: public screens are login/signup/help/verify, and signed-in users go to `(authenticated)/(tabs)`.
- Boundary: route files are wrappers; feature logic stays under `src/features/auth`.

Evidence: `apps/frontend/app/_layout.tsx`, `apps/frontend/src/features/auth/routing/useAuthRedirects.ts`

## Frontend Architecture

### Why feature folders?

**Verdict:** Feature folders fit this app because crypto, simulation, auth, and shared utilities have different ownership boundaries.

- Why it fits here: Simulation has API clients, storage, asset picker, screen logic, and tests.
- What flatter structure is better at: small apps with fewer domains.
- In this codebase: product code lives under `apps/frontend/src/features`.
- Trade-off I accepted: more folders, but easier to avoid mixing auth, crypto, and simulation logic.

Evidence: `docs/project-reference/architecture.md`

### Why keep route files thin?

**Short answer:** It keeps navigation separate from product behavior.

- The alternative I weighed: putting screen logic directly in `app/`.
- Trade-off I accepted: one extra wrapper file per route.
- If the use case changed: for a tiny prototype, direct route implementation would be okay.

Evidence: `docs/project-reference/architecture.md`, `apps/frontend/app/(authenticated)/(tabs)/simulation.tsx`

## React Query

### Why React Query?

**Verdict:** I used React Query because Simulation and Crypto screens are API-heavy and need loading/error/retry states.

- Why it fits here: historical prices, events, asset catalog, purchasing power, and crypto quotes are all remote queries.
- What simple `useEffect` is better at: very small one-off fetches.
- In this codebase: `QueryClientProvider` is global in `_layout.tsx`.
- Trade-off I accepted: more abstraction, but better cache and request state management.

Evidence: `apps/frontend/app/_layout.tsx`, `apps/frontend/src/features/simulation/screens/simulationScreen.tsx`

## Backend

### Why Cloudflare Workers?

**Verdict:** I used Workers because the backend is mostly API orchestration, validation, cache, and edge-friendly data access.

- Why it fits here: the Worker proxies provider APIs, reads KV fallback data, and queries D1.
- What a traditional server is better at: long-running jobs, heavy compute, complex background workflows.
- In this codebase: Hono routes mount crypto, purchasing-power, and simulation APIs.
- Trade-off I accepted: Worker runtime constraints.

Evidence: `apps/backend/src/index.ts`, `apps/backend/wrangler.jsonc`

### Why Hono?

**Short answer:** Hono is a small routing layer that fits Cloudflare Workers well.

- The alternative I weighed: raw Worker `fetch` handlers.
- Trade-off I accepted: one framework dependency, but cleaner domain route mounting.
- If the app grew: I would keep Hono unless middleware/routing needs outgrew it.

Evidence: `apps/backend/src/index.ts`, `apps/backend/src/domains/simulation/simulationRoutes.ts`

### Why keep API calls on the Worker instead of mobile?

**Verdict:** Provider secrets and validation belong on the backend, not in the mobile app.

- Why it fits here: mobile calls `EXPO_PUBLIC_API_BASE_URL`; it does not own CoinMarketCap, CoinGecko, D1, or raw CSV access.
- What mobile-owned handlers are better at: local-only prototypes.
- Trade-off I accepted: the app depends on deployed backend availability.
- In this codebase: tests ensure mobile-owned `app/api` crypto handlers are gone.

Evidence: `apps/frontend/src/features/crypto-market/api/getCryptoApiUrl.ts`, `apps/frontend/__tests__/cloud-backend-wiring.test.ts`

## Data Storage

### Why D1 for historical prices?

**Verdict:** D1 fits because historical price lookup is relational, date-based, and needs to run close to the Worker.

- Why it fits here: the Worker queries `HISTORICAL_PRICES_DB` for historical price rows.
- What Postgres is better at: larger operational workloads and richer indexing/query features.
- In this codebase: D1 binding is `HISTORICAL_PRICES_DB`, database `fintech-historical-prices`.
- Trade-off I accepted: D1 is more constrained than a full database.

Evidence: `apps/backend/wrangler.jsonc`, `apps/backend/src/domains/simulation/simulationPriceService.ts`

### Why Python for CSV ingestion but TypeScript for runtime?

**Verdict:** Python owns offline data processing, TypeScript owns app/runtime behavior.

- Why it fits here: CSV cleaning, OHLC repairs, quarantines, and SQL generation are data-engineering tasks.
- What TypeScript is better at here: shared API contracts and frontend/backend runtime consistency.
- In this codebase: historical import is in `scripts/historical_prices/import_historical_prices.py`.
- Trade-off I accepted: two languages, but each handles the job it is best at.

Evidence: `docs/project-reference/architecture.md`, `scripts/historical_prices/import_historical_prices.py`

### How much historical data does the simulator have?

**Short answer:** The docs report 176,348 imported rows across 84 ready assets and 16 unavailable assets.

- BTC starts at `2014-09-17`.
- ETH starts at `2017-11-09`.
- SOL starts at `2020-04-10`.
- Data runs through `2026-03-22` in the documented import.

Evidence: `docs/project-reference/architecture.md`

## Caching

### Why cache current prices?

**Verdict:** Current prices are reused across simulations, so a short cache reduces provider calls without making the app feel stale.

- Why it fits here: current Simulation USD prices come from CoinGecko Simple Price.
- What no cache is better at: absolute freshest data.
- In this codebase: current price cache TTL is `60_000` ms.
- Trade-off I accepted: prices can be up to about 60 seconds old.

Evidence: `apps/backend/src/domains/simulation/currentPriceCache.ts`

### Why KV fallback for crypto market data?

**Short answer:** KV gives the crypto screens a reliability fallback when live provider data fails or is malformed.

- The alternative I weighed: fail hard whenever CoinMarketCap fails.
- Trade-off I accepted: fallback data may be stale, so UI must expose source/freshness.
- If the use case changed: for trading, stale fallback would not be acceptable.

Evidence: `docs/project-reference/architecture.md`, `apps/backend/src/domains/crypto-market/cloudFallbackStore.ts`

## Simulation

### How does the basic simulation work?

**In one line:** The Worker compares a historical USD price from D1 against a current USD price from CoinGecko.

- How it works: amount divided by historical price gives implied quantity, then quantity times current price gives current value.
- In this codebase: `calculateResult()` computes implied quantity, current value, gain/loss dollars, and gain/loss percent.
- Boundary: it is hypothetical, not a trade or portfolio.

Evidence: `apps/backend/src/domains/simulation/simulationPriceService.ts`

### Why do simulation calculations live on the Worker?

**Verdict:** The Worker owns calculation because it also owns validation, D1 lookup, current price fetching, and data trust metadata.

- Why it fits here: the frontend should not query D1 or raw provider APIs.
- What frontend calculation is better at: purely local what-if calculators.
- Trade-off I accepted: simulation requires backend availability.
- In this codebase: frontend calls `getSimulationPrice`, Worker handles `/api/simulation/prices`.

Evidence: `apps/backend/src/domains/simulation/simulationRoutes.ts`, `apps/backend/src/domains/simulation/simulationPriceService.ts`

### What is date resolution?

**In one line:** Date resolution explains whether the simulator used the exact requested date or the next available valid historical price.

- How it works: missing or invalid source rows can resolve to the next valid date.
- In this codebase: responses include `requestedDate`, `resolvedDate`, and `dateResolution`.
- When it matters: it keeps results honest when historical data has gaps.

Evidence: `packages/shared/src/simulationTypes.ts`, `apps/backend/src/domains/simulation/simulationPriceService.ts`

## Event Simulation

### Why add event-based simulation?

**Short answer:** Date picking is useful, but events make the simulator feel like a real user decision: “what if I reacted to this news?”

- The alternative I weighed: only manual historical dates.
- Trade-off I accepted: curated event data needs source discipline.
- If the use case changed: live news ingestion would be a later version, not v1.

Evidence: `docs/project-reference/issues.md`, `apps/backend/migrations/0004_simulation_events.sql`

### How many events are seeded?

**Short answer:** The docs say 15 active BTC/ETH/SOL events with 30 source records.

- How it works: `/api/simulation/events` returns event cards.
- `/api/simulation/event-scenarios` resolves event plus reaction delay.
- Delays are `same_day`, `one_week`, and `one_month`.

Evidence: `docs/project-reference/issues.md`, `apps/frontend/src/features/simulation/screens/simulationScreen.tsx`

### Why deterministic risk metrics instead of AI-generated analysis?

**Verdict:** Risk numbers need to be reproducible and auditable.

- Why it fits here: max drawdown and underwater days come from static historical D1 rows.
- What AI is better at: summarizing or personalizing explanations.
- Trade-off I accepted: deterministic takeaways are less flexible, but more trustworthy.
- In this codebase: event scenario service computes risk metrics, not an LLM.

Evidence: `apps/backend/src/domains/simulation/simulationEventRiskMetrics.ts`, `apps/backend/src/domains/simulation/simulationEventScenarioService.ts`

## Purchasing Power

### Why include purchasing power comparisons?

**Short answer:** It turns abstract crypto gains/losses into real-life context.

- The alternative I weighed: just show percentage return.
- Trade-off I accepted: the current data is curated v1 data, not a live cost-of-living feed.
- If the use case changed: I would add cited datasets and update workflows before making stronger claims.

Evidence: `apps/backend/src/domains/purchasing-power/*`, `docs/project-reference/issues.md`

### Which cities are supported?

**Short answer:** Phoenix, San Francisco, New York, Austin, and Seattle.

- How it works: the frontend calls `/api/purchasing-power/comparisons`.
- In this codebase: these city IDs are defined in the Simulation screen.
- Boundary: these are curated estimates.

Evidence: `apps/frontend/src/features/simulation/screens/simulationScreen.tsx`, `apps/backend/src/domains/purchasing-power/purchasingPowerData.ts`

## Financial Harm Simulator

### What is the Financial Harm Simulator?

**In one line:** It compares one available amount across debt payoff, emergency savings, and risky investment.

- How it works: it calculates interest avoided, essentials coverage, stress-test downside, and simple down payment progress.
- In this codebase: `buildFinancialHarmScenario()` owns the pure calculation.
- Boundary: it is hypothetical and explicitly not financial advice.

Evidence: `packages/shared/src/financialHarmScenario.ts`

### Why build Financial Harm as shared logic?

**Verdict:** The formulas are business logic, not UI logic.

- Why it fits here: shared code can be unit tested without React Native.
- What keeping it in the screen is better at: faster one-off prototype work.
- Trade-off I accepted: extra shared files and exported types.
- In this codebase: tests cover the calculation separately.

Evidence: `packages/shared/src/financialHarmScenario.ts`, `packages/shared/src/financialHarmScenario.test.ts`

### Why use a 40% downside stress test when no crypto result exists?

**Short answer:** It gives the first local Life Impact slice a concrete downside scenario before a live simulation result is available.

- The alternative I weighed: block the feature until a crypto result exists.
- Trade-off I accepted: it is a simple stress test, not a forecast.
- If the use case changed: I would let users choose downside assumptions or pull asset-specific historical drawdowns.

Evidence: `apps/frontend/src/features/simulation/screens/simulationScreen.tsx`

## Decision Pattern Graph

### What is the Decision Pattern Graph?

**In one line:** It is a local-first record of decision events and user-confirmed pattern feedback.

- How it works: Life Impact scenarios create decision events, and Yes/No pattern responses create feedback edges.
- In this codebase: graph state stores `decisionEvents` and `patternFeedback`.
- Boundary: this is not a live AI knowledge graph yet.

Evidence: `apps/frontend/src/features/simulation/storage/decisionPatternGraphStore.ts`

### Is this actually AI or agentic?

**Short answer:** No, not yet. The current pattern loop is rule-based and user-confirmed.

- The alternative would be an LLM or graph reasoning engine.
- Trade-off I accepted: less intelligence, but more control and easier validation.
- If the use case changed: I would add AI after the graph events and feedback model are stable.

Evidence: `packages/shared/src/financialHarmScenario.ts`, `apps/frontend/src/features/simulation/storage/decisionPatternGraphStore.ts`

### Why local-first for the graph?

**Verdict:** The data is sensitive, so v1 should prove value privately before adding backend persistence.

- Why it fits here: user decision patterns can reveal debt stress, risk appetite, and financial pressure.
- What backend storage is better at: cross-device sync and analytics.
- Trade-off I accepted: local-only means no sync.
- In this codebase: graph state is stored through `expo-secure-store`.

Evidence: `apps/frontend/src/features/simulation/storage/decisionPatternGraphStore.ts`

### Why ask users to confirm patterns?

**Short answer:** I do not want the app silently labeling people.

- The alternative I weighed: infer behavior automatically and adapt immediately.
- Trade-off I accepted: a little more friction, but a more ethical feedback loop.
- If the product matured: I would use confidence scores, but still keep user correction.

Evidence: `packages/shared/src/financialHarmScenario.ts`, `apps/frontend/src/features/simulation/screens/simulationScreen.tsx`

## Data Trust

### What does Data Trust mean in this project?

**In one line:** Every important result should say where its data came from and whether fallback or date resolution was involved.

- How it works: shared API result metadata includes provider/source/fallback/freshness fields.
- In this codebase: simulation responses include historical source and current source/cache metadata.
- Boundary: the app avoids silently rendering stale or unclear data.

Evidence: `packages/shared/src/apiResult.ts`, `packages/shared/src/simulationTypes.ts`

## Validation

### Why shared validators/contracts?

**Verdict:** Shared contracts reduce drift between backend responses and frontend assumptions.

- Why it fits here: crypto and simulation payloads cross the Worker/mobile boundary.
- What independent DTOs are better at: strict separation between services.
- Trade-off I accepted: frontend and backend are coupled through the shared package.
- In this codebase: shared validators live in `packages/shared/src`.

Evidence: `packages/shared/src/index.ts`, `packages/shared/src/simulationValidators.ts`, `packages/shared/src/cryptoValidators.ts`

## Metrics

### How are metrics handled?

**In one line:** Metrics are currently local, lightweight, and testable.

- How it works: `recordMetric()` writes to an in-memory buffer capped at 200 events and logs outside tests.
- In this codebase: helpers include `recordMetric`, `timeAsync`, and `timeSync`.
- Boundary: this is instrumentation scaffolding, not production analytics yet.

Evidence: `apps/frontend/src/shared/metrics/metrics.ts`

### Why not add a full analytics platform?

**Short answer:** The product is still changing, so I wanted event discipline before vendor lock-in.

- The alternative I weighed: Segment, PostHog, or Firebase Analytics.
- Trade-off I accepted: no production dashboard yet.
- If the product matured: I would map these events to a real analytics sink.

Evidence: `apps/frontend/src/shared/metrics/metrics.ts`, `docs/project-reference/metrics.md`

## Testing

### What does the test suite cover?

**Short answer:** It covers frontend wiring, shared validators, simulation services, backend routes, storage, metrics, and cleanup regressions.

- In this codebase: the documented suite includes crypto API tests, simulation tests, event tests, D1 repository tests, and project-structure guards.
- Current full run from recent work passed 48 suites and 189 tests.
- Boundary: source-boundary tests are useful here, but they do not replace real end-to-end UI testing.

Evidence: `docs/project-reference/architecture.md`, recent `jest --runInBand --watchman=false` output

### Why source-boundary tests?

**Verdict:** They protect architectural decisions that normal unit tests might miss.

- Why it fits here: I wanted to ensure old fintech surfaces and mobile-owned API handlers do not come back.
- What behavioral tests are better at: proving actual user interactions.
- Trade-off I accepted: source tests can be brittle if names change.
- In this codebase: cleanup regressions and project-structure tests enforce removed surfaces.

Evidence: `apps/frontend/__tests__/product-cleanup-regressions.test.ts`, `tests/project-structure.test.ts`

## Security And Secrets

### Where are secrets kept?

**Short answer:** Provider secrets are backend/runtime environment concerns, not mobile code.

- Mobile uses `EXPO_PUBLIC_API_BASE_URL`, which is safe to expose as a public endpoint.
- Worker bindings include D1 and KV, and provider keys are read server-side.
- Clerk publishable key is public by design.

Evidence: `apps/frontend/src/features/crypto-market/api/getCryptoApiUrl.ts`, `apps/backend/wrangler.jsonc`, `apps/frontend/app/_layout.tsx`

### Is there server-side auth enforcement?

**Short answer:** The Worker config has Clerk issuer/JWKS vars, but from the files scanned, the shown route entrypoint does not demonstrate auth middleware on every API route.

- What I can honestly say: frontend routing is signed-in, and Clerk wraps the mobile app.
- What I should not claim: full backend authorization enforcement unless I point to middleware that validates Clerk JWTs.
- If pushed: I would say backend auth hardening is a next step.

Evidence: `apps/backend/wrangler.jsonc`, `apps/backend/src/index.ts`, `apps/frontend/app/_layout.tsx`

## Common Trade-Off Questions

### D1 vs Postgres?

**Verdict:** I chose D1 because the app is on Cloudflare Workers and needs date-based historical lookup close to the edge.

- Why it fits here: historical price records are read by Worker routes.
- What Postgres is better at: complex joins, mature tooling, heavy write workloads.
- In this codebase: D1 binding is `HISTORICAL_PRICES_DB`.
- Trade-off I accepted: less database maturity and fewer advanced features.

Evidence: `apps/backend/wrangler.jsonc`

### SecureStore vs AsyncStorage?

**Verdict:** I used SecureStore because saved simulations and decision patterns are user-specific financial context.

- Why it fits here: stored data includes simulated decisions, amounts, and pattern feedback.
- What AsyncStorage is better at: larger, less sensitive local app state.
- In this codebase: saved simulations and graph store use `expo-secure-store`.
- Trade-off I accepted: SecureStore is not ideal for large datasets.

Evidence: `apps/frontend/src/features/simulation/storage/savedSimulationsStore.ts`, `apps/frontend/src/features/simulation/storage/decisionPatternGraphStore.ts`

### React Query vs Redux?

**Verdict:** React Query fits because most state here is server state, not complex global client state.

- Why it fits here: crypto listings, simulation assets, history, events, and purchasing power are fetched data.
- What Redux is better at: complex cross-screen client workflows.
- In this codebase: React Query is globally provided in `_layout.tsx`.
- Trade-off I accepted: local UI state still lives in screen state for now.

Evidence: `apps/frontend/app/_layout.tsx`, `apps/frontend/src/features/simulation/screens/simulationScreen.tsx`

### Rule-based pattern detection vs LLM?

**Verdict:** I chose rule-based detection first because user trust matters more than cleverness.

- Why it fits here: the app only surfaces tentative patterns and asks for confirmation.
- What an LLM is better at: richer natural language reflection and more flexible pattern summaries.
- In this codebase: `buildTentativePatterns()` is deterministic.
- Trade-off I accepted: simple patterns, but explainable behavior.

Evidence: `packages/shared/src/financialHarmScenario.ts`

### Local graph vs backend graph database?

**Verdict:** I chose local graph state first because the product loop is not proven enough to justify backend graph infrastructure.

- Why it fits here: v1 only needs decision events and pattern feedback for one user.
- What Neo4j or a graph DB is better at: cross-user network analysis and complex graph traversal.
- In this codebase: graph state is arrays in SecureStore.
- Trade-off I accepted: no real graph query engine yet.

Evidence: `apps/frontend/src/features/simulation/storage/decisionPatternGraphStore.ts`

### Victory Native chart vs simpler chart rendering?

**Verdict:** Victory Native fits because the Simulation tab needs an interactive historical chart.

- Why it fits here: user can press and drag across chart points to select a buy date.
- What simpler UI is better at: fewer dependencies and easier rendering tests.
- In this codebase: `CartesianChart`, `Line`, and `useChartPressState` are used.
- Trade-off I accepted: more chart/rendering complexity.

Evidence: `apps/frontend/src/features/simulation/screens/simulationScreen.tsx`

### CoinGecko vs CoinMarketCap?

**Verdict:** The project uses both for different jobs: CoinMarketCap for crypto market browsing, CoinGecko Simple Price for current Simulation USD prices.

- Why it fits here: browsing and simulation have different provider paths.
- What one-provider architecture is better at: lower complexity.
- In this codebase: crypto-market domain uses CoinMarketCap, simulation current prices use CoinGecko.
- Trade-off I accepted: more provider integration surface.

Evidence: `docs/project-reference/architecture.md`, `apps/backend/src/domains/crypto-market/*`, `apps/backend/src/domains/simulation/current-prices/coinGeckoSimplePriceClient.ts`

## Gaps To Avoid Overclaiming

- Do not claim this is a production AI agent. Current pattern detection is deterministic.
- Do not claim RAG. There is no vector index retrieval feeding an LLM.
- Do not claim production analytics. Metrics are local/in-memory.
- Do not claim backend auth is fully enforced unless you point to JWT validation middleware.
- Do not claim live cost-of-living data. Purchasing power is curated v1 data.
- Do not claim real trading, banking, portfolio management, or money movement. The app explicitly avoids those.

Evidence: `apps/frontend/src/shared/metrics/metrics.ts`, `packages/shared/src/financialHarmScenario.ts`, `docs/project-reference/issues.md`


# Interview Q&A — SEO Audit Engine

> Answers grounded in real source files with concrete values.
> Every answer ends with an Evidence line pointing to the file that proves it.
> Read each answer out loud. Target 30–45 seconds.
> Likely follow-up printed under each answer — practice it before moving on.

---

## Stack & Key Decisions (quick reference)

| Layer | What | File proof |
|---|---|---|
| Language | JavaScript ES modules (Node 22) | `api/package.json` → `"type": "module"` |
| API framework | Express 5 | `api/package.json` → `"express": "^5.2.1"` |
| Queue | pg-boss 10 on Postgres — no Redis | `api/src/queue.js`, `worker/src/index.js` |
| Database | PostgreSQL via `pg` 8 | `api/package.json`, `infra/init.sql` |
| Crawling | Playwright 1.58 (Chromium) | `worker/package.json`, `worker/src/steps/crawlPage.js` |
| Accessibility | axe-core 4.11 | `worker/package.json`, `worker/src/steps/crawlPage.js:54` |
| CI | GitHub Actions — tests on every push to main | `.github/workflows/ci.yml` |
| Keep-alive | GH Actions cron every 14 min | `.github/workflows/keep-alive.yml` |
| Frontend | Vanilla JS, Cloudflare Pages | `frontend/` |
| Schema | 9 tables: jobs, users, businesses, keywords, rank_snapshots, gbp_posts, nap_audits, monthly_tips, monthly_tips | `infra/init.sql` |

**5 most interview-worthy design decisions:**
1. **pg-boss over BullMQ** — queue backed by Postgres, Redis dependency dropped entirely (`api/src/queue.js:8`)
2. **Browser singleton** — one Chromium instance reused across jobs, crash-reset on rejection (`worker/src/browser.js`)
3. **axe on live DOM** — accessibility runs on the same page before it closes, not a second `setContent` pass (`worker/src/steps/crawlPage.js:54`)
4. **URL normalisation before dedup** — `new URL()` strips hash + trailing slash so `example.com/` and `example.com/#s` deduplicate correctly (`api/src/routes/jobs.js:13`)
5. **Multi-tenancy schema** — `jobs.business_id` FK is nullable so legacy anonymous audits coexist with future user-scoped work (`infra/init.sql:40`)

---

## Architecture & Design

---

**Q: Walk me through the architecture.**

Three parts. A vanilla JS frontend on Cloudflare Pages, an Express REST API, and a separate worker process. A user submits a URL, the API validates it, normalises it, checks for a completed audit in the last 24 hours, inserts a job row, and sends the job ID to a pg-boss queue backed by Postgres. The worker polls that queue, picks up the job, and runs five stages in sequence: Playwright crawl, performance scoring, axe-core accessibility, seven custom SEO rules, then a report builder that writes scores and a JSONB report blob back to the jobs table. The frontend streams progress over SSE while the pipeline runs, then renders the scored report.

`Evidence: api/src/routes/jobs.js, worker/src/processor.js, worker/src/index.js`

> **Likely follow-up:** Why split the API and worker into separate processes?

The audit is slow and CPU-heavy — it launches a headless Chromium browser. Running that synchronously inside the API would block the HTTP thread for the entire crawl duration, typically 5–45 seconds. Separating them means the API returns a job ID immediately. The worker can also be restarted or scaled independently without touching the API.

---

**Q: Why split API and worker? Why not one process?**

Short answer: a Playwright crawl takes 5–45 seconds and runs Chromium. That cannot live on an HTTP request thread.

If I ran the audit inline, every concurrent request would block waiting for the previous crawl to finish. With a queue, the API inserts a job row and returns a job ID in milliseconds. The worker picks it up asynchronously. The concurrency is controlled by `WORKER_CONCURRENCY` which defaults to 1 in the worker code, right for a 512MB free-tier instance running one Chromium process.

`Evidence: worker/src/index.js:18 — CONCURRENCY = Number(process.env.WORKER_CONCURRENCY) || 1`

---

## Queue

---

**Q: Why pg-boss instead of BullMQ?**

Short answer: pg-boss stores the queue in the Postgres database I already had, so I could drop Redis entirely as a dependency.

BullMQ is excellent — I used it in Hearloop — but it requires Redis as its backing store. For this project, running a second service just for the queue was unnecessary cost and complexity. pg-boss creates a `pgboss` schema in the existing Postgres instance and handles retries, exponential backoff, and cron scheduling from there.

- The alternative I weighed: BullMQ on Upstash Redis — same pattern as Hearloop.
- Trade-off I accepted: pg-boss has less tooling. No built-in dashboard, smaller community. Fine at this scale.
- If the use case changed: multi-language workers, real-time dashboards, or fan-out routing — then BullMQ or SQS.

`Evidence: api/src/queue.js:8 — new PgBoss({ connectionString: process.env.DATABASE_URL })`

> **Likely follow-up:** How does pg-boss avoid two workers picking up the same job?

It uses `SELECT ... FOR UPDATE SKIP LOCKED` — a Postgres pattern where each worker locks the row it takes and other workers skip locked rows automatically. No coordination service needed.

---

**Q: What are the retry settings on jobs?**

Jobs are sent with `retryLimit: 3`, `retryDelay: 5` seconds, and `retryBackoff: true`, which means exponential backoff starting at 5 seconds. Jobs also have `expireInHours: 1` — if a job sits unprocessed for an hour it is abandoned rather than retried forever. On the pg-boss instance itself, completed jobs are deleted after 24 hours and failed jobs are archived for 7 days.

`Evidence: api/src/routes/jobs.js:66–71, api/src/queue.js:13–15`

---

## Database

---

**Q: Why PostgreSQL over MongoDB?**

Verdict: all the data in this project is relational and structured. Postgres fits better.

Jobs have fixed columns — URL, status enum, four score integers, step timings, a foreign key to businesses. That is a schema problem, not a document problem. When I needed flexibility for the audit report — which varies in structure per page — I stored it as a JSONB column inside the same Postgres table rather than adding a document store. MongoDB is genuinely better for deeply nested, fast-changing documents without a fixed schema. I did not have that problem.

`Evidence: infra/init.sql:23 — report JSONB column in jobs table`

---

**Q: What is JSONB and why did you use it here?**

In one line: JSONB is Postgres's binary JSON column type — it stores arbitrary JSON but lets you index and query inside it.

The audit report varies per page: different numbers of SEO checks, different violations, different metric values. Normalising that into joined tables would mean 10+ tables and complex queries just to render one report. Instead, scores and queryable metadata stay in typed columns (`seo_score INT`, `overall_score INT`), and the full rendered report goes in a JSONB column. The API returns it as a single JSON blob and the frontend renders it directly.

`Evidence: infra/init.sql:23 — report JSONB`

---

**Q: Explain the 24-hour deduplication.**

Before inserting a new job, the API queries for a completed job with the same normalised URL created within the last 24 hours. If one exists, it returns that job ID with `cached: true` and the frontend fetches the existing result — no crawl, no worker time. URLs are normalised first using the built-in `URL` constructor: the hash fragment is stripped and the trailing slash is removed. So `https://example.com`, `https://example.com/`, and `https://example.com/#section` all deduplicate against each other.

`Evidence: api/src/routes/jobs.js:13 (normaliseUrl), api/src/routes/jobs.js:34–47 (dedup query, INTERVAL '24 hours')`

---

**Q: What is the schema for jobs and why is business_id nullable?**

The jobs table has a UUID primary key, a URL text field, a custom `job_status` enum, four score integers, a JSONB report column, error fields, five step-timing INT columns, and a nullable `business_id` foreign key referencing the businesses table. The FK is nullable deliberately — all the existing anonymous audits that were created before the multi-tenancy migration have no associated business. Making it nullable means they coexist with future user-scoped audits without a data migration. New audits submitted through a business account will populate the FK.

`Evidence: infra/init.sql:35–55, infra/migrations/003_users_businesses_multi_tenancy.sql`

---

## Crawling

---

**Q: Why Playwright over fetch or Cheerio?**

Verdict: modern pages are JavaScript-rendered. A plain fetch gets raw HTML before JS executes — you miss everything a React or Next.js site renders client-side.

Playwright launches a real headless Chromium browser, runs the JavaScript, and gives you the final DOM — what Google actually indexes. I extract title, meta description, H1s, H2s, images with alt attributes, canonical tag, robots meta, viewport, and lang attribute from the live `document`. None of that is reliably available in raw HTML for a JS-heavy site. Cheerio is fast but it is an HTML parser, not a browser — no JS execution.

- Trade-off I accepted: Chromium adds ~150–300MB memory. On a 512MB free-tier worker, concurrency is kept at 1.

`Evidence: worker/src/steps/crawlPage.js:1, worker/package.json → "playwright": "^1.58.2"`

---

**Q: What optimisations did you make to the Playwright crawl?**

Three things. First, I block images, fonts, media, and stylesheets at the network level using `page.route()`. Those resources are irrelevant to DOM content and SEO checks but slow down page load on a real browser. Second, I run axe-core on the live DOM before closing the page — previously it opened a second page and called `setContent()` with the captured HTML, which doubled the Chromium work. Third, I use a browser singleton: one Chromium process is launched on worker startup and pages are opened and closed on it rather than launching a new browser per job.

`Evidence: worker/src/steps/crawlPage.js:8–14 (route blocking), crawlPage.js:54 (axe on live DOM), worker/src/browser.js (singleton)`

---

**Q: What is the crawl timeout?**

45 seconds, set via `waitUntil: 'domcontentloaded'`. I reduced it from 60 seconds after identifying it as a source of unnecessarily long failure waits. `domcontentloaded` fires when the HTML is parsed and the DOM is ready, without waiting for all images and iframes to finish loading — which is appropriate since I'm blocking those resources anyway.

`Evidence: worker/src/steps/crawlPage.js:20–23 — timeout: 45000, waitUntil: 'domcontentloaded'`

---

**Q: What is axe-core and how did you use it?**

axe-core is Deque's open-source WCAG accessibility rule engine. It runs inside a browser page and checks the live DOM against WCAG 2.1 rules. I inject it into the Playwright page using `addScriptTag` in `runAccessibility.js` and call it before closing the crawl page, so the same browser session does both the DOM extraction and the accessibility check. No second page, no re-parsing HTML.

`Evidence: worker/src/steps/crawlPage.js:54 — runAxeOnPage(page) called before page.close(), worker/package.json → "axe-core": "^4.11.1"`

---

**Q: Why not Lighthouse for performance scoring?**

Not used in this project. Lighthouse was attempted early on but proved unreliable on a Render free-tier worker with 512MB RAM — it occasionally crashed mid-audit or returned inconsistent scores under memory pressure. The replacement is response-time-based scoring: Playwright measures how long `page.goto()` takes to reach `domcontentloaded`, and that load time is mapped to a performance score. It is less rich than Lighthouse's Core Web Vitals but it is consistent and does not require a second browser pass or additional memory.

`Evidence: worker/src/steps/runPerformanceCheck.js, PERFORMANCE.md`

---

## Real-time Progress

---

**Q: Why SSE over WebSockets for the progress stream?**

Verdict: the updates are one-directional — server pushes status to client, client never sends anything back. SSE is purpose-built for that.

SSE is a persistent HTTP connection that streams `text/event-stream` events. It works over standard HTTP without a protocol upgrade, reconnects automatically on disconnect, and is simpler to implement server-side — just set the response headers and write events. WebSockets are bidirectional and require a handshake upgrade. That is the right tool when the client needs to send data back, which this use case does not need. I also implemented a polling fallback in the frontend — if SSE fails, the client polls `GET /api/jobs/:id` every 2 seconds.

`Evidence: api/src/routes/stream.js — Content-Type: text/event-stream, frontend/app.js:trackJobProgress()`

---

**Q: How does the SSE endpoint work technically?**

The API sets `Content-Type: text/event-stream`, flushes the headers without ending the response, then runs `setInterval` every 2 seconds to query the jobs table for the current status. Each poll result is written to the response as `data: <json>\n\n`. When the job reaches `complete` or `failed`, it sends a final event and calls `res.end()`. A heartbeat ping fires every 30 seconds — `event: ping\ndata: {}\n\n` — to prevent proxy timeouts on idle connections mid-crawl.

`Evidence: api/src/routes/stream.js`

---

## CI/CD & Testing

---

**Q: How is the CI pipeline set up?**

GitHub Actions runs two parallel jobs on every push and PR to main: `test-api` and `test-worker`. Each job installs dependencies on a fresh Ubuntu runner with Node 22, then runs `npm test`. The API tests run with `DATABASE_URL` set to a fake connection string and `NODE_ENV=test` — the DB and queue are mocked so no real Postgres or pg-boss connection is needed. Both jobs must pass before a `deploy-check` gate job runs, which currently just confirms the tests passed. There is no automated deploy step — Render auto-deploys on push to main via its GitHub integration.

`Evidence: .github/workflows/ci.yml`

---

**Q: What does the test suite cover?**

Four test files in `api/__tests__/`. `queue.test.js` verifies pg-boss is instantiated with the right options and that `boss.send()` is callable. `jobs.test.js` covers POST validation, URL normalisation (trailing slash stripped, hash stripped), the 24h cache hit path, and the new-job enqueue path. `stream.test.js` covers SSE headers and terminal status events. `history.test.js` covers pagination, the `hasMore` flag, and the cursor parameter. All dependencies — the DB pool and pg-boss — are mocked using Jest's `unstable_mockModule`.

`Evidence: api/__tests__/*.test.js`

---

**Q: What is the keep-alive workflow doing?**

Render's free tier spins services down after 15 minutes of inactivity. Cold starts can take 30–90 seconds. The `keep-alive.yml` workflow runs every 14 minutes via a cron trigger and makes two HTTP requests: a `curl` to `GET /health` on the API and a `curl` to the worker's health endpoint. Both use `--max-time` flags — 45 seconds for the API, 120 seconds for the worker. It validates the API response is `{"status":"ok"}` and the worker responds with "Worker is running". This is enough to prevent spin-down on the GitHub Actions free tier at no cost.

`Evidence: .github/workflows/keep-alive.yml`

---

## Infrastructure & Cost

---

**Q: How much does this cost to run?**

Currently zero. Render free tier for API and worker, Cloudflare Pages for frontend, Neon free tier for Postgres, GitHub Actions free tier for CI and keep-alive. The only production limitation is Render's spin-down behaviour on free tier. Moving the worker to Fly.io (always-on VMs with 1GB RAM, free tier) would cost nothing and solve the cold-start problem.

`Evidence: PERFORMANCE.md — platform alternatives table`

---

**Q: Why a browser singleton? What is the failure risk?**

Launching Chromium takes 1–3 seconds. A singleton means that cost is paid once at worker startup, not per job. All jobs open a new `page` on the existing browser instance and close it when done.

The failure risk: if `chromium.launch()` rejects, the module-level `browserPromise` variable holds a permanently rejected promise. Any subsequent `getBrowser()` call would re-await that rejected promise and fail immediately without retrying the launch. The fix is a `.catch()` handler that resets `browserPromise` to `null` on rejection, so the next job attempt retries the launch instead of hard-failing.

`Evidence: worker/src/browser.js:14–15 — browserPromise.catch(() => { browserPromise = null; })`

---

**Q: What is cursor-based pagination and why did you use it?**

Cursor pagination uses a column value from the last row of the current page as the start point for the next query. The history endpoint uses `created_at` as the cursor: the next page fetches rows where `created_at < :cursor ORDER BY created_at DESC LIMIT n`. Offset pagination — `LIMIT 20 OFFSET 40` — requires Postgres to scan and discard all preceding rows, which gets slower as the table grows. Cursor pagination is always a fast index scan because there is an index on `created_at DESC` in the schema.

`Evidence: api/src/routes/history.js, infra/init.sql — idx_jobs_created_at ON jobs(created_at DESC)`

---

**Q: Why Express 5 over Fastify?**

Short answer: the API is simple and the bottleneck is the Playwright crawl, not the HTTP layer.

Express has a larger ecosystem and is more familiar to interviewers reading the code. Fastify is genuinely faster with lower overhead — that is why I used it in Hearloop, where the API ran on a constrained t3.micro. Here, every request either returns a cached result in milliseconds or immediately queues a job and returns a job ID. HTTP throughput is not the constraint. Switching frameworks would have added churn for no measurable benefit.

`Evidence: api/package.json → "express": "^5.2.1"`

---

*Last updated: reflects pg-boss migration, multi-tenancy schema, and all concrete config values from source.*


# ClusterOps — Complete Interview Q&A

> Ground truth: every answer is backed by actual file paths and config values from the repo.
> Format: **Short answer** first, then reasoning, then `Evidence:` at the end.

---

## TABLE OF CONTENTS

1. [Architecture & System Design](#1-architecture--system-design)
2. [Kafka & Event Bus](#2-kafka--event-bus)
3. [Caching — Redis](#3-caching--redis)
4. [Real-Time — SSE](#4-real-time--sse)
5. [PostgreSQL & Data Layer](#5-postgresql--data-layer)
6. [API Design](#6-api-design)
7. [Observability](#7-observability)
8. [Assistant Engine](#8-assistant-engine)
9. [Simulator & Fault Injection](#9-simulator--fault-injection)
10. [Frontend](#10-frontend)
11. [Go Language & Patterns](#11-go-language--patterns)
12. [Data Models & Domain Design](#12-data-models--domain-design)
13. [Testing](#13-testing)
14. [Deployment & Infrastructure](#14-deployment--infrastructure)
15. [Gaps & Honest Limits](#15-gaps--honest-limits)

---

## 1. ARCHITECTURE & SYSTEM DESIGN


**Q: Walk me through the architecture of this system end to end.**

**Short answer:** Three independent Go binaries communicate through Kafka and Redis, with one read-only API server in front.

- **Simulator** generates synthetic GPU cluster activity (node events, job events, GPU telemetry, alerts) every 5–90 seconds and publishes JSON messages to four Kafka topics.
- **Ingestion service** consumes those topics, writes canonical state to PostgreSQL, and writes/invalidates Redis cache.
- **API server** is read-only — reads Redis first, falls back to Postgres on a miss, pushes live updates to browser clients over SSE.
- **Frontend** is React/TypeScript connecting to that single API server.

The key rule: only the simulator writes to Kafka, only ingestion writes to Postgres. That separation makes the read path lockless and cache invalidation explicit.

Evidence: `backend/cmd/` has three separate `main.go` files; `internal/ingestion/ingestion.go` package doc: "the only writer to the database"

---

**Q: Why three separate binaries instead of one monolith?**

**Short answer:** Each binary has a different reason to exist, a different scaling axis, and a different failure blast radius.

- The simulator is a dev/demo tool — you'd never run it alongside a real API in production. Keeping it separate means you can kill it without touching the API.
- The ingestion service is the only thing that writes to Postgres. If it crashes, the API keeps serving cached reads. If they were one process, a write-path bug could take down reads too.
- The API server scales by HTTP traffic. The ingestion service scales by Kafka partition count. Different knobs.

Trade-off I accepted: more operational overhead — three processes to start, three health checks to monitor. For a demo that's fine; in production you'd want proper orchestration (Kubernetes).

Evidence: `docker-compose.yml` — three separate service definitions: `api`, `ingestion`, `simulator`

---

**Q: How does data flow from the simulator to the browser?**

1. Simulator calls `producer.PublishNodeEvent()` / `PublishJobEvent()` / `PublishGPUMetric()` / `PublishAlertFired()` — JSON on four Kafka topics: `cluster.nodes`, `cluster.jobs`, `cluster.gpus`, `cluster.alerts`.
2. Ingestion service's four goroutines (one per topic) consume messages, upsert to Postgres, invalidate and warm Redis.
3. API server's `broadcastLoop` goroutine polls Postgres every 2 seconds, refreshes Redis, calls `broker.BroadcastEvent()` with the latest snapshot.
4. Browser receives SSE events named `cluster_summary`, `nodes`, `alerts` — no polling needed.

Evidence: `internal/ingestion/ingestion.go` handlers; `internal/api/handlers.go` `broadcastClusterSnapshot()`; `internal/api/sse.go`

---

**Q: Why is the ingestion service the only writer to the database?**

**Short answer:** Centralizing all writes in one place makes cache invalidation deterministic and the API server safe to scale horizontally.

If the API server also wrote to Postgres, you'd need to invalidate the cache from two places — now two code paths can put stale data in Redis. By making ingestion the single writer, every mutation goes through one path: write to Postgres → invalidate Redis → warm Redis. The API server never needs to think about cache consistency. You can run 10 API replicas behind a load balancer and none of them will conflict, because they're all read-only.

Evidence: `internal/ingestion/ingestion.go` — "It is the only writer to the database — the API server is read-only."

---

**Q: What is the health score and how is it calculated?**

**Short answer:** A 0–100 score computed on every `ClusterSummary` call with penalty deductions.

```
score = 100
score -= (unavailable_nodes / total_nodes) * 40   // up to -40
score -= (degraded_nodes / total_nodes) * 20       // up to -20
score -= gpu_waste_percent * 0.2                   // up to -20
score -= failed_jobs_penalty (2 pts each, max -10)
score = max(score, 0)
```

The weights reflect operator priorities: a node going fully offline is worse than degradation, which is worse than GPU inefficiency.

Evidence: `internal/store/summary.go` `ClusterSummary()`


---

## 2. KAFKA & EVENT BUS

---

**Q: Why Kafka? Why not write directly from the simulator to Postgres?**

**Verdict:** Kafka because it decouples producers from consumers and makes the pipeline survivable.

- Why it fits here: if the ingestion service is down, Kafka buffers the messages. With direct DB writes, a slow DB stalls the simulator. With Kafka, the simulator keeps publishing and ingestion catches up when it recovers.
- What a direct write is genuinely better at: simplicity. Fewer moving parts, no Kafka to operate, one less network hop.
- In this codebase: four topics — `cluster.nodes`, `cluster.jobs`, `cluster.gpus`, `cluster.alerts`. One `kafka.Writer` per topic in `internal/kafka/producer.go`. One `kafka.Reader` per topic in the consumer.
- Trade-off I accepted: Kafka is operationally heavy. For a demo you're running Zookeeper + Kafka as two extra Docker containers to buffer messages between two processes on the same machine. A Go channel or Redis Stream would have been simpler. The value shows at scale, not in a 5-node demo.

Evidence: `go.mod` — `github.com/segmentio/kafka-go v0.4.47`; `docker-compose.yml` — `zookeeper` + `kafka` services

---

**Q: Kafka vs RabbitMQ — which would you use here and why?**

**Verdict:** Kafka, and that's what's used.

- Why Kafka fits here: Kafka is a durable, replayable log. If the ingestion service crashes and restarts, it picks up from its last committed offset — no messages lost. RabbitMQ is a traditional message queue: once consumed and acked, a message is gone.
- What RabbitMQ is genuinely better at: complex routing (exchanges, routing keys, fan-out), message TTLs, dead-letter queues out of the box. For task queues where each message is a discrete unit of work, RabbitMQ is simpler.
- Trade-off I accepted: Kafka requires Zookeeper (in this stack, Confluent 7.6.1 still uses it). Newer Kafka versions (KRaft mode) remove that dependency, but this compose file uses the older setup.

Evidence: `docker-compose.yml` — `confluentinc/cp-kafka:7.6.1`, `confluentinc/cp-zookeeper:7.6.1`

---

**Q: How are Kafka topics structured? What's the partitioning strategy?**

Four topics, one per event type:
- `cluster.nodes` — node state changes, keyed by `node.ID`
- `cluster.jobs` — job state changes, keyed by `job.ID`
- `cluster.gpus` — GPU telemetry, keyed by `"nodeID:gpuIndex"` (ensures all metrics for a GPU go to the same partition, preserving order)
- `cluster.alerts` — alerts fired/resolved, keyed by `alert.ID`

The key-based partitioning means all events for the same entity arrive in order at the same partition. For GPU metrics this matters: you don't want metric N+1 processed before metric N for the same GPU.

The consumer uses a consumer group (`GroupID` in `ConsumerConfig`) so you can run multiple ingestion instances and Kafka will distribute partitions across them.

Evidence: `internal/kafka/producer.go` — `PublishGPUMetric()` key = `fmt.Sprintf("%s:%d", m.NodeID, m.GPUIndex)`; `internal/models/events.go` `KafkaTopics`

---

**Q: What happens if a Kafka message fails to process in the ingestion service?**

The consumer logs the error and continues — it does not retry or dead-letter the message. The comment in `consumer.go` says "log and skip — appropriate for a demo."

In production this is insufficient. You'd want:
1. A retry loop with backoff for transient errors (DB timeout, network blip).
2. A dead-letter topic for messages that fail after N retries.
3. An alert on dead-letter queue depth.

The current behavior means a DB error during ingestion silently drops an event. Redis will eventually expire the stale entry and the next successful ingestion will correct it — but there's a window of inconsistency.

Evidence: `internal/kafka/consumer.go` `consume()` — "log and skip (not retry) — appropriate for a demo"

---

**Q: Is Kafka message delivery at-least-once, at-most-once, or exactly-once here?**

At-least-once on the producer side: `RequiredAcks: kafka.RequireOne` means the broker acknowledges the message when the leader has written it, but before all replicas confirm. `Async: false` means the producer blocks until the ack is received, so the simulator won't lose messages unless the broker itself crashes after acking but before replicating.

On the consumer side, `kafka-go` auto-commits offsets after each successful `ReadMessage()`. If the ingestion service crashes mid-processing, the offset may already be committed, so the message won't be reprocessed — practically at-most-once on the consumer side for failed processing.

The upsert pattern (`ON CONFLICT DO UPDATE`) in Postgres means re-processing the same event is idempotent — the final state is correct even if a message is processed twice.

Evidence: `internal/kafka/producer.go` — `RequiredAcks: kafka.RequireOne`, `Async: false`; `internal/store/nodes.go` `UpsertNode()`


---

## 3. CACHING — REDIS

---

**Q: What is Redis and where did you use it?**

**In one line:** Redis is an in-memory key-value store used here as a read-through cache in front of Postgres.

- How it works: every API endpoint checks Redis first. On a hit, returns cached JSON without touching Postgres. On a miss, queries Postgres and writes the result to Redis with a TTL.
- In this codebase: `internal/cache/cache.go` wraps `go-redis/v9` with typed methods — `GetClusterSummary`, `GetNodeList`, `GetJob`, etc. TTLs are tuned to the dashboard's refresh feel: 2s for summary/alerts/GPU, 3–5s for nodes/jobs.
- When I'd reach for it: any hot read path where data changes on a known schedule and you can tolerate slight staleness.
- When not: when you need strong read-after-write consistency, or when your dataset doesn't fit in memory.

Evidence: `internal/cache/cache.go` TTL constants at the top of the file

---

**Q: What are the cache TTLs and how did you choose them?**

| Resource | TTL | Reason |
|---|---|---|
| Cluster summary | 2s | Dashboard feels real-time; ingestion refreshes this on every broadcast |
| Alerts (active) | 2s | Operators need to see new critical alerts fast |
| GPU summary | 2s | GPU metrics arrive every 5s; 2s keeps the chart smooth |
| Node list | 3s | Nodes change state less frequently than GPU readings |
| Individual node | 3s | Same reasoning as node list |
| Job list | 3s | Jobs submit every 20–90s; 3s staleness is imperceptible |
| Individual job | 5s | Detail views tolerate slightly more staleness |

General rule: TTL ≤ half the minimum interval at which the underlying data changes. GPU metrics arrive every 5s, so 2s TTL means at most one stale snapshot shown.

Evidence: `internal/cache/cache.go` lines 18–24 — `TTLClusterSummary` through `TTLGPUSummary`

---

**Q: How do you handle cache invalidation?**

Three strategies, chosen per resource:

1. **Invalidate-on-write** — when ingestion processes a node event, `cache.InvalidateNode(id)` deletes `node:<id>`, `nodes:list`, and `cluster:summary` in one `DEL` call, then immediately re-warms with the new value. Most aggressive — ensures the next API read gets fresh data.

2. **TTL expiry** — the primary safety net. Even if invalidation is missed (e.g. Redis is briefly down), stale data expires within 2–5 seconds automatically.

3. **Pattern flush** — for job list keys, which are parameterized by filter hash (`status|user_id`), the cache uses `SCAN` + `DEL` to flush all matching keys. This avoids maintaining an index of every active filter key. Uses `SCAN` cursor loop (not `KEYS`) to avoid blocking Redis on large keyspaces.

Evidence: `internal/cache/cache.go` — `InvalidateNode()`, `InvalidateJob()`, `flushByPattern()`

---

**Q: Redis vs Memcached — which would you use and why?**

**Verdict:** Redis, and that's what's used.

- Why it fits here: Redis supports TTL-per-key, pub/sub, and richer data types natively. Pub/sub or Redis Streams would be a natural upgrade path if the SSE broadcast loop needed to be distributed across API replicas.
- What Memcached is genuinely better at: raw throughput for simple get/set at extreme scale, multi-threaded architecture. If this were a CDN edge cache doing tens of millions of simple lookups per second, Memcached would be fair.
- Trade-off I accepted: Redis is single-threaded per core. At demo scale this is irrelevant.

Evidence: `go.mod` — `github.com/redis/go-redis/v9 v9.5.1`; `docker-compose.yml` — `redis:7-alpine`

---

**Q: What happens to the API if Redis goes down?**

Graceful degradation. Cache errors on read are silently ignored — the handler falls through to Postgres and still returns data. Cache errors on write are also swallowed. The pattern in every handler is:

```go
if data, hit, _ := s.cache.GetX(r.Context()); hit {
    return // serve from cache
}
// cache miss or error — query Postgres directly
data, _ = s.db.QueryX(r.Context())
_ = s.cache.SetX(r.Context(), data) // best-effort warm
```

Redis being down degrades performance (every request hits Postgres) but does not cause errors. The `/health` endpoint reports Redis status separately so operators can see the degradation.

Evidence: `internal/api/handlers.go` — every handler; `internal/api/handlers.go` `handleHealth()`


---

## 4. REAL-TIME — SSE

---

**Q: What is SSE and why did you use it instead of WebSockets?**

**In one line:** Server-Sent Events is a one-way HTTP/1.1 push channel — the server streams named events to the browser over a persistent connection.

- How it works: the client does one `GET /api/v1/stream`. The response never closes. The server writes `event: <name>\ndata: <json>\n\n` frames as data is ready. The browser's native `EventSource` API parses them automatically and reconnects on disconnect.
- In this codebase: `SSEBroker` in `internal/api/sse.go` manages a `map[chan []byte]struct{}` of connected clients. Each client has a buffered channel (size 16). The `broadcastLoop` goroutine calls `broker.BroadcastEvent()` every 2 seconds.
- Why not WebSockets: the browser only receives data, never sends. WebSockets add bidirectional complexity for no benefit here. SSE works through HTTP proxies and load balancers without special upgrade handling.
- When I'd pick WebSockets: if the client needed to send data back in real time — a chat app, a collaborative editor, a live terminal session.

Evidence: `internal/api/sse.go`; route `GET /api/v1/stream` in `internal/api/server.go`

---

**Q: How do you handle slow SSE clients?**

The `broadcast()` method uses a `select` with a 100ms timeout per client:

```go
select {
case ch <- data:
case <-time.After(100 * time.Millisecond):
    b.unsubscribe(ch) // drop the slow client
}
```

If a client can't consume within 100ms, it gets dropped. The browser's `EventSource` reconnects automatically. This prevents one stalled connection from blocking the broadcast loop for everyone else.

There's also a 15-second heartbeat comment (`": heartbeat\n\n"`) sent to keep the connection alive through proxies that close idle HTTP connections.

Evidence: `internal/api/sse.go` `broadcast()` and `ServeHTTP()`

---

**Q: How do you track connected SSE client count?**

A Prometheus gauge `clusterops_sse_connected_clients` is incremented in `subscribe()` and decremented in `unsubscribe()`. You can read the current count from `/metrics` or in Grafana at any time. There's no hard connection limit in the current code.

Evidence: `internal/api/metrics.go` `sseClientsGauge`; `internal/api/sse.go` `subscribe()` / `unsubscribe()`

---

**Q: SSE vs polling vs WebSockets — trade-off summary?**

| | Polling | SSE | WebSockets |
|---|---|---|---|
| Direction | Client pulls | Server pushes | Bidirectional |
| Protocol | HTTP | HTTP | WS upgrade |
| Proxy support | Universal | Good | Needs upgrade support |
| Auto-reconnect | Client manages | Browser `EventSource` | Client manages |
| Complexity | Simplest | Low | Higher |
| Use case | Simple dashboards | Live read-only feeds | Realtime two-way |

This project has a read-only feed, so SSE is the right level. Polling would waste bandwidth hitting the API every 2s per client when most responses are identical. WebSockets would add complexity for no functional gain.

Evidence: `internal/api/sse.go`; `internal/api/handlers.go` `broadcastClusterSnapshot()`


---

## 5. POSTGRESQL & DATA LAYER

---

**Q: Why PostgreSQL? Why not InfluxDB or TimescaleDB for GPU metrics?**

**Verdict:** Postgres, because it covers all three data shapes in one database without adding another system to operate.

- Why it fits here: nodes and jobs have relational integrity (alerts FK to both). GPU metrics are append-only time-series. Postgres handles both. The `ClusterGPUSummary` query uses `DISTINCT ON` to get the latest reading per GPU efficiently — a query that's awkward in a pure time-series store.
- What TimescaleDB/InfluxDB would be genuinely better at: automatic time-based partitioning, continuous aggregates, first-class retention policies. At millions of GPU metric rows per day, the plain `gpu_metrics` table would need manual partitioning.
- Trade-off I accepted: the `gpu_metrics` table grows unboundedly without the prune job. The ingestion service runs `PruneOldMetrics()` every 30 minutes deleting rows older than 24 hours — a manual retention policy, not a DB feature.

Evidence: `go.mod` — `github.com/jackc/pgx/v5 v5.5.5`; `store/migrations/002_retention.sql`

---

**Q: Why pgx instead of database/sql or an ORM like GORM?**

**Verdict:** pgx because it's the highest-performance Postgres driver for Go and handles native Postgres types without custom scanners.

- Why it fits here: `gpu_utilization` and `gpu_memory_used_gb` are `DOUBLE PRECISION[]` columns. pgx scans these directly into `[]float64`. With `database/sql` or GORM, you'd need a custom type scanner or JSON serialization workaround.
- What GORM is genuinely better at: faster scaffolding, automatic migrations, less boilerplate for simple CRUD on plain relational tables.
- Trade-off I accepted: more hand-written SQL. Every query in `store/nodes.go`, `store/jobs.go` is explicit — more code, but easier to audit, impossible to accidentally N+1, and easy to add query hints or partial indexes.

Evidence: `go.mod`; `internal/store/nodes.go` — direct `pool.Query()` calls with `[]float64` array scanning

---

**Q: How are database migrations handled?**

Migrations are SQL files embedded directly into the binary using Go's `//go:embed` directive. On startup, `db.migrate()` reads the embedded `migrations/` directory, sorts files by name (`001` before `002`), and executes each file. Every statement uses `IF NOT EXISTS` or `CREATE OR REPLACE`, making it idempotent — re-running the same migration doesn't fail.

Downside: no version tracking table, no "down" migration. For a demo this is fine. In production you'd use `golang-migrate` which tracks applied migrations in a `schema_migrations` table.

Evidence: `internal/store/db.go` `migrate()` function with `//go:embed migrations/*.sql`

---

**Q: Walk me through the database schema design.**

Four tables with clear roles:

- **`nodes`** — `TEXT PRIMARY KEY` (ID from simulator, must be stable). Stores per-GPU arrays directly as `DOUBLE PRECISION[]` — one row per node, not one row per GPU. Indexed on `status` and `last_seen DESC`.
- **`jobs`** — `TEXT PRIMARY KEY`. Upserted on every state change. `failure_reason` is nullable TEXT so unfailed jobs don't carry a dummy value. Indexed on `status`, `created_at DESC`, `user_id`.
- **`gpu_metrics`** — `BIGSERIAL PRIMARY KEY` (DB-generated, append-only). References `nodes(id) ON DELETE CASCADE`. Composite index `(node_id, recorded_at DESC)` covers the main time-series query. Plain table, not partitioned — comment notes that production would partition by day.
- **`alerts`** — FKs to both `nodes(id) ON DELETE SET NULL` and `jobs(id) ON DELETE SET NULL`. If a node or job is deleted, the alert survives for audit purposes. `gen_random_uuid()` used for IDs.

Evidence: `internal/store/migrations/001_initial_schema.sql`

---

**Q: How do you prevent N+1 queries?**

Three places this was explicitly designed out:

1. Node and job list handlers fetch the full list in one `SELECT` — no per-row follow-up queries.
2. `GetNodeGPUTimeSeries()` fetches all GPUs for a node in one query (`WHERE node_id = $1 AND recorded_at BETWEEN $2 AND $3`) and groups by `gpu_index` in Go.
3. `ClusterGPUSummary()` uses a single `WITH latest AS (DISTINCT ON (node_id, gpu_index) ...)` CTE to aggregate the freshest reading per GPU in one round trip — no loop over GPUs.

Evidence: `internal/store/gpu_metrics.go` `GetNodeGPUTimeSeries()` and `ClusterGPUSummary()`

---

**Q: How does upsert work and why use it instead of insert + update?**

All node and job writes use `INSERT ... ON CONFLICT (id) DO UPDATE SET`. This is one atomic Postgres statement. The alternative — check if exists, then insert or update — requires two round trips and a race condition between the check and the write.

Because the simulator republishes all nodes on every GPU tick, `UpsertNode()` is called ~40 times every 5 seconds (5 nodes × 8 GPUs worth of republishes). An insert-only approach would fail on the second publish. An update-only approach would fail on the first.

Evidence: `internal/store/nodes.go` `UpsertNode()`; `internal/store/jobs.go` `UpsertJob()`

---

**Q: How is the GPU metrics retention handled?**

Two layers:

1. **Application-level prune:** the ingestion service ticks every 30 minutes and calls `db.PruneOldMetrics(ctx, 24*time.Hour)` which does `DELETE FROM gpu_metrics WHERE recorded_at < $1`. The deleted row count is logged.
2. **SQL function:** migration `002_retention.sql` creates a `prune_gpu_metrics()` PL/pgSQL function that can be called manually or wired to `pg_cron` in production.

The comment in `002_retention.sql` explicitly notes: "In production this would be a pg_cron job or TimescaleDB retention policy."

Evidence: `internal/ingestion/ingestion.go` `pruneMetrics()`; `internal/store/gpu_metrics.go` `PruneOldMetrics()`; `internal/store/migrations/002_retention.sql`


---

## 6. API DESIGN

---

**Q: Walk me through the API design.**

The API is versioned under `/api/v1`. chi router with globally applied middleware: `RequestID`, `RealIP`, `Logger`, `Recoverer`, gzip compression at level 5, Prometheus instrumentation, and CORS.

Resources follow a simple REST shape:
- `GET /api/v1/cluster/summary` — health rollup
- `GET /api/v1/nodes`, `GET /api/v1/nodes/{id}`, `GET /api/v1/nodes/{id}/gpu-series`
- `GET /api/v1/jobs`, `GET /api/v1/jobs/{id}`, `GET /api/v1/jobs/{id}/alerts`
- `GET /api/v1/metrics/gpu`, `GET /api/v1/metrics/capacity`
- `GET /api/v1/alerts`
- `POST /api/v1/assistant/analyze`
- `GET /api/v1/stream` — SSE

`/health` and `/metrics` are at the root (no version prefix) because they're infrastructure endpoints, not API endpoints.

Evidence: `internal/api/server.go` `routes()`

---

**Q: Why chi instead of Gin or the standard library?**

**Verdict:** chi because it's idiomatic Go, composes cleanly with `net/http` middleware, and doesn't require learning framework-specific types.

- Why it fits here: chi's middleware stack is just `func(http.Handler) http.Handler` — the same interface as standard library handlers. The Prometheus middleware, CORS handler, and `promhttp.Handler()` all plug in without adapters or type conversions.
- What Gin is genuinely better at: marginally faster routing at extreme RPS, a larger ecosystem of Gin-specific middleware, and a more familiar API for developers coming from Node.js/Express.
- Trade-off I accepted: chi has a smaller ecosystem than Gin. For a project with 12 routes, that doesn't matter.

Evidence: `go.mod` — `github.com/go-chi/chi/v5 v5.0.12`; `internal/api/server.go` `routes()`

---

**Q: How does the cache-aside pattern work in the handlers?**

Every handler follows the same three-step pattern:

```go
// 1. Check Redis
if data, hit, _ := s.cache.GetX(r.Context()); hit {
    recordCacheHit("x")
    writeJSON(w, 200, data)
    return
}
// 2. Miss — query Postgres
recordCacheMiss("x")
data, err := s.db.QueryX(r.Context())
// 3. Warm cache for next request
_ = s.cache.SetX(r.Context(), data)
writeJSON(w, 200, data)
```

Cache errors on read fall through silently to Postgres. Cache errors on write are swallowed. Redis being down degrades performance, not correctness.

Evidence: `internal/api/handlers.go` — every handler follows this pattern

---

**Q: How are errors handled in the API?**

All errors return JSON: `{"error": "message"}` with an appropriate HTTP status code. The `writeError()` helper handles this consistently. There's no stack trace or internal error detail in the response — just a human-readable message. Internal errors are logged with `zap` before the response is written.

The `Recoverer` middleware from chi catches panics in handlers and returns a 500 instead of crashing the server.

Evidence: `internal/api/handlers.go` `writeError()`; `internal/api/server.go` `r.Use(middleware.Recoverer)`

---

**Q: How does the job list filtering work?**

`GET /api/v1/jobs` accepts `?status=running&user_id=alice`. The handler builds a cache key from these query params (`statusFilter + "|" + userFilter`) and checks Redis first. On a miss, it builds a dynamic SQL query in `store/jobs.go` `ListJobs()` using a `where []string` slice and positional parameters (`$1`, `$2`, etc.) — no string interpolation, no SQL injection risk. Default limit is 200 rows.

Evidence: `internal/api/handlers.go` `handleListJobs()`; `internal/store/jobs.go` `ListJobs()`


---

## 7. OBSERVABILITY

---

**Q: What observability does this system have?**

Three pillars, all wired up:

1. **Metrics (Prometheus + Grafana):** The API exposes `clusterops_api_requests_total` (counter by method/path/status), `clusterops_api_request_duration_seconds` (histogram with default buckets), `clusterops_cache_hits_total`, `clusterops_cache_misses_total`, and `clusterops_sse_connected_clients`. Prometheus scrapes `/metrics`, Grafana visualizes it on port 3001.

2. **Traces (OpenTelemetry → Jaeger):** `internal/telemetry/otel.go` initializes an OTLP gRPC exporter pointing at the otel-collector on port 4317. Sampler is `AlwaysSample()` — 100% trace capture, fine for a demo. Jaeger UI is on port 16686.

3. **Structured logging (zap):** All three binaries use `go.uber.org/zap` with structured fields — no `fmt.Printf`. Log lines include request IDs, node IDs, error types.

Evidence: `internal/api/metrics.go`; `internal/telemetry/otel.go`; `go.mod` — `go.opentelemetry.io/otel v1.26.0`, `go.uber.org/zap v1.27.0`

---

**Q: What is OpenTelemetry and why use it instead of directly integrating Jaeger?**

**In one line:** OpenTelemetry is a vendor-neutral SDK — "instrument once, export anywhere."

- How it works: your code calls `otel.Tracer("name").Start(ctx, "span")`. The SDK batches spans and sends them to the OTel Collector over OTLP/gRPC. The collector routes them to Jaeger (or Datadog, Grafana Tempo, etc.) without changing application code.
- In this codebase: the collector listens on port 4317 (gRPC) and 4318 (HTTP). If I wanted to switch from Jaeger to Tempo, I'd change one line in the collector config, not in any application code.
- When not to bother: if you only ever use one observability vendor and are willing to vendor-lock, direct SDK integration is simpler.

Evidence: `internal/telemetry/otel.go`; `docker-compose.yml` — `otel-collector`, `jaeger` services

---

**Q: What's the difference between tracing and metrics?**

- **Metrics** answer "how is the system doing in aggregate?" — request rate, error rate, p99 latency, cache hit ratio. Cheap to store (just counters and histograms). Good for dashboards and alerts.
- **Traces** answer "what happened for this specific request?" — which services it touched, how long each span took, where the latency went. Expensive to store at 100% sampling — sampled in production.

In this project: Prometheus metrics tell you if cache hit rate dropped below 80% across all requests (aggregate signal). A Jaeger trace would show you that one specific `/api/v1/cluster/summary` request spent 45ms in Postgres because of a cache miss (per-request signal).

Evidence: `internal/api/metrics.go`; `internal/telemetry/otel.go`

---

**Q: Why use zap instead of the standard library's log package or slog?**

**Short answer:** zap because it's structured (key-value fields, not format strings), zero-allocation on the hot path, and already the Go ecosystem standard for production services.

- Structured logging means log lines are machine-parseable by tools like Loki, Datadog, or CloudWatch. `log.Printf("error processing node %s: %v", id, err)` is hard to query. `logger.Error("upsert node", zap.String("id", n.ID), zap.Error(err))` produces JSON with typed fields.
- Go 1.21+ ships `slog` which has the same structured approach. If starting today I might use `slog` to avoid the dependency — but `zap` was the established choice when this was written.

Evidence: `go.mod` — `go.uber.org/zap v1.27.0`; `internal/ingestion/ingestion.go` — every log call uses `zap.String()`, `zap.Error()` fields

---

**Q: How does the Prometheus middleware work?**

`prometheusMiddleware` wraps every handler. It uses chi's `WrapResponseWriter` to capture the response status code after the handler runs, then records two metrics:
- `httpRequestsTotal.WithLabelValues(method, path, status).Inc()`
- `httpRequestDuration.WithLabelValues(method, path).Observe(duration)`

This gives you per-endpoint request rate and latency histograms in Grafana. The `promauto` package auto-registers the metrics with Prometheus's default registry on startup — no manual `prometheus.Register()` call needed.

Evidence: `internal/api/middleware.go` `prometheusMiddleware()`; `internal/api/metrics.go`


---

## 8. ASSISTANT ENGINE

---

**Q: What is the assistant and how does it work?**

**Short answer:** A deterministic rule-based failure analysis engine, not an LLM.

`POST /api/v1/assistant/analyze` accepts a `job_id` or `node_id`. For a job, the handler fetches the job + related alerts, then calls `engine.AnalyzeJob()`. The engine routes on `job.Status` and `job.FailureReason` (OOM, hardware fault, timeout, preemption, user error, unknown) and returns a structured `Analysis` — headline, severity, root cause, 2–6 ordered debugging steps with runnable shell commands, prevention tips, and a confidence score 0–1.

For a node, it routes on `node.Status` (healthy, degraded, unavailable) and inspects live telemetry arrays — if `max(GPUTemperature) > 85°C` it classifies thermal throttle; if `any(GPUMemoryUsedGB) > 78 GB` it classifies memory pressure.

This is explicitly not RAG or agentic. The package comment says "deterministic LLM-free baseline."

Evidence: `internal/assistant/engine.go`; `internal/assistant/job_rules.go`; `internal/assistant/node_rules.go`

---

**Q: What's the difference between this and a real RAG system?**

Real RAG: retrieve relevant documents from a vector index → inject as context → LLM generates a free-form response. The intelligence comes from the LLM.

This engine: the rules ARE the intelligence. It pattern-matches on typed enum values and numeric thresholds, then returns pre-written text templates populated with live job/node data.

What they share is structural shape: given a target (job/node), retrieve relevant context (failure reason, telemetry), augment with live data (duration, temperature readings, GPU counts), produce structured output. The engine's package comment explicitly describes this as the upgrade path — keep the retrieve/augment steps, replace the template-based generate step with an LLM call.

Evidence: `internal/assistant/engine.go` — "The structure mirrors a RAG pipeline" comment in the package doc

---

**Q: Why build a rule-based engine instead of calling an LLM directly?**

Three concrete reasons:

1. **Reliability:** rules are deterministic. The OOM rule always returns severity=critical and exactly those 6 debugging steps. An LLM can hallucinate commands, produce inconsistent severity ratings, refuse, or time out.

2. **Testability:** `engine_test.go` has 10 table-driven test cases covering every failure path. Each asserts exact `RootCause`, `Severity`, minimum `DebuggingSteps` count, and minimum confidence. You cannot write that kind of assertion test for LLM output.

3. **The rules are the eval harness for the LLM:** when you add Ollama or any LLM, you run the same test cases against LLM output and use rule output as the expected baseline. Any case where the LLM produces worse results (wrong severity, fewer steps, lower confidence) is a regression. This is how production AI systems measure LLM quality — deterministic baseline first.

Evidence: `internal/assistant/engine_test.go` — "AI meta-learning note" comment at top of file

---

**Q: What failure scenarios does the assistant cover?**

For jobs (5 failure types + 3 states):
- **OOM** — CUDA out-of-memory. Severity: critical. Confidence: 0.95. 6 steps: confirm in logs, check nvidia-smi, reduce batch size, gradient checkpointing, mixed precision, ZeRO-3/FSDP.
- **Hardware fault** — ECC/NVLink error. Severity: critical. Confidence: 0.92. 6 steps: check ECC counts, dmesg Xid errors, GPU diagnostics, drain the node, reset and retest, resubmit.
- **Timeout** — exceeded max duration. Severity: warning. Confidence: 0.88. 6 steps: check throughput, NCCL hangs, GPU utilization, data loader, checkpoint frequency, increase timeout.
- **Preemption** — low-priority job killed. Severity: warning. Confidence: 0.97. 4 steps: verify checkpoint, resume, raise priority, request reserved pool.
- **User error** — code/config exception. Severity: warning. Confidence: 0.85. 4 steps: read traceback, check tensor shapes, validate config, run locally.
- **Unknown** — no failure signal. Severity: warning. Confidence: 0.40. 2 steps: check node events, check exit code.

For nodes (3 states): degraded (with thermal/memory classification), unavailable, healthy.

Evidence: `internal/assistant/job_rules.go`; `internal/assistant/node_rules.go`

---

**Q: What are the confidence scores and how are they set?**

Hardcoded per rule — not dynamically computed. They reflect how unambiguous the classification is:

| Scenario | Confidence | Rationale |
|---|---|---|
| Completed | 1.0 | Definitional — no ambiguity |
| Running | 0.99 | Job is running — certain |
| Preemption | 0.97 | Scheduler preemption is explicit |
| OOM | 0.95 | `FailureReasonOOM` is a clear enum value |
| Queued | 0.95 | Waiting state is unambiguous |
| Hardware fault | 0.92 | ECC errors are clear hardware signals |
| Node unavailable | 0.90 | Node unreachable = definitive |
| Node degraded | 0.82 | Could have multiple causes |
| Timeout | 0.88 | Clear but root cause of slowness varies |
| User error | 0.85 | Could be infra; rules favor user error attribution |
| Unknown failure | 0.40 | No signal — low confidence by design |

In a real LLM-backed system, confidence would come from log-probabilities or a calibration model.

Evidence: `internal/assistant/job_rules.go` — each rule function sets `a.Confidence` explicitly


---

## 9. SIMULATOR & FAULT INJECTION

---

**Q: What does the simulator do and why does it exist?**

**Short answer:** It generates a realistic, self-contained synthetic GPU cluster so the system can be demoed without real Kubernetes or GPU hardware.

Three concurrent loops:
- `gpuLoop` — emits GPU telemetry every 5 seconds (40 metrics per tick: 5 nodes × 8 GPUs each)
- `jobLoop` — submits a new training job every 20–90 seconds (random interval, uniform distribution)
- `faultLoop` — fires fault scenarios every 60 seconds

The fault probabilities are tuned to create an engaging demo: 5% chance per minute a healthy node degrades, 8% per running job per minute of OOM, 6% preemption for low-priority jobs. This keeps the dashboard showing realistic failure patterns without everything breaking at once.

Evidence: `internal/simulator/config.go` `DefaultConfig()`; `internal/simulator/simulator.go` `Run()`

---

**Q: How does fault injection work? Walk me through `faultTick()`.**

`faultTick()` runs once per minute and makes independent probability draws:

1. **Node state transitions:** for each node, `rand.Float64() < FaultNodeDegradeProb (0.05)` → degrade. If already degraded: `rand.Float64() < FaultNodeDownProb (0.10)` → mark unavailable AND kill all running jobs on that node with `FailureReasonHardwareFault`. If degraded: `rand.Float64() < FaultNodeRecoverProb (0.30)` → recover to healthy.

2. **Thermal alerts:** independently, `rand.Float64() < FaultThermalThrottle (0.04)` per healthy node → fire a GPU high temperature alert.

3. **Job faults (checked in order, `continue` on first match):**
   - OOM: 8% per running job
   - Preemption: 6% but only for jobs with `priority <= 3`
   - Hardware fault: 3% per running job
   - Timeout: deterministic — if `DurationSeconds() > JobDurationMax (8 min)`, time out
   - Natural completion: 35% chance once past `JobDurationMin (2 min)`

4. **Capacity waste alert:** if >30% of GPUs are allocated but below 10% utilization, fire a warning.

Evidence: `internal/simulator/faults.go` `faultTick()`; `internal/simulator/config.go` probability constants

---

**Q: How does job scheduling work in the simulator?**

The simulator maintains in-memory cluster state. When `runJobSubmit()` fires, it calls `submitJob()` which:
1. Picks a random model name from the configured list (`llama-3-70b`, `mistral-7b`, `gpt-neox-20b`, `falcon-40b`, `qwen-72b`, `deepseek-67b`)
2. Picks a random user from the 5 configured users
3. Assigns a random priority 1–10 (low-priority jobs are preemption candidates)
4. Finds a healthy node with available GPU capacity
5. If capacity available → status=`running`, assign node, record start time
6. If no capacity → status=`queued`

`retryQueuedJobs()` runs on each fault tick to promote queued jobs to running when freed capacity becomes available.

Evidence: `internal/simulator/jobs.go` (not shown but referenced by `simulator.go`); `internal/simulator/config.go` `ModelNames`, `Users`

---

**Q: How does the simulator maintain state without a database?**

It keeps an in-memory `clusterState` struct with two maps: `nodes map[string]*models.Node` and `jobs map[string]*models.Job`, protected by a `sync.RWMutex`. Reads use `RLock()`, writes use `Lock()`. This is a single-process in-memory state — if the simulator crashes, all state is lost. That's intentional: on restart, it re-publishes the initial node state, and the ingestion service upserts everything fresh.

Evidence: `internal/simulator/simulator.go` `publishAllNodes()` on startup; `internal/simulator/faults.go` `s.state.mu.Lock()` / `s.state.mu.RUnlock()`


---

## 10. FRONTEND

---

**Q: Walk me through the frontend stack.**

React 18 with TypeScript, built by Vite. Routing with React Router v6. Styling with Tailwind CSS + `tailwind-merge` + `clsx`. Charts with Recharts. Headless accessible components from Radix UI (Dialog, Select, Tabs, Tooltip, Separator). Icons from Lucide React. Date formatting with `date-fns`.

Five pages: Dashboard, Nodes, Jobs, Alerts, Assistant — all nested under a shared `Layout` component with a sidebar nav. Each page is a route defined in `App.tsx`.

Evidence: `frontend/package.json`; `frontend/src/App.tsx`

---

**Q: Why Vite instead of Create React App or Next.js?**

**Verdict:** Vite because it's the fastest dev server for a pure client-side SPA with no SSR needs.

- Why it fits here: this is a pure SPA — no server-side rendering, no static generation needed. The API is a separate Go binary. Vite's native ES module dev server starts in milliseconds, and its esbuild-based production build is significantly faster than webpack (CRA's underlying bundler) for TypeScript projects.
- What Next.js is genuinely better at: SSR/SSG for SEO, server components for data fetching, file-based routing, API routes co-located with the frontend.
- Trade-off I accepted: no SSR means a blank page on initial load (white flash before JS hydrates). For a monitoring dashboard behind authentication, that's fine. For a public marketing page, it wouldn't be.

Evidence: `frontend/package.json` — `"vite": "^5.2.11"`

---

**Q: Why Radix UI for components instead of Material UI or Chakra?**

**Short answer:** Accessibility out of the box, unstyled so Tailwind controls everything.

Radix provides behavior (keyboard navigation, ARIA attributes, focus management, screen reader announcements, escape key handling) without imposing any CSS. Every Dialog, Select, Tabs, and Tooltip in the dashboard gets correct a11y semantics for free. If I'd used MUI or Chakra, I'd fight their CSS specificity with Tailwind overrides. Radix has no styles to fight — it's "bring your own CSS."

Evidence: `frontend/package.json` — five `@radix-ui/*` packages

---

**Q: Why Recharts for the GPU time series charts?**

Recharts is built on SVG, composable as React components (`<LineChart>`, `<Line>`, `<XAxis>`), and integrates naturally with React state. When the SSE stream pushes new data, the component re-renders and Recharts updates the chart — no imperative chart.update() call needed, unlike D3 or Chart.js.

Trade-off: SVG-based charts get slow with very large datasets (thousands of points). For a 1-hour GPU time series at 5s intervals that's ~720 points — fine. For a 24-hour view, you'd want downsampling on the server side.

Evidence: `frontend/package.json` — `"recharts": "^2.12.5"`

---

**Q: Why `tailwind-merge` and `clsx` together?**

- `clsx` conditionally joins class strings: `clsx("base", isActive && "active", className)` — cleaner than template literals with ternaries.
- `tailwind-merge` resolves Tailwind class conflicts: if you pass both `p-2` and `p-4`, `tailwind-merge` keeps only `p-4`. Without it, both classes end up in the DOM and the winner is determined by CSS specificity — which is often wrong with Tailwind's utility-first approach.

The pattern `cn = (...inputs) => twMerge(clsx(inputs))` is the standard Tailwind + Radix combination, seen in shadcn/ui and similar component libraries.

Evidence: `frontend/package.json` — `"clsx": "^2.1.1"`, `"tailwind-merge": "^2.3.0"`


---

## 11. GO LANGUAGE & PATTERNS

---

**Q: Why Go for the backend?**

**Short answer:** Go's concurrency model (goroutines + channels), small binary size, and fast compile times make it a natural fit for an event-driven backend with multiple concurrent loops.

- The simulator runs three concurrent ticker loops. The ingestion service runs four concurrent consumer goroutines. The API server runs the SSE broadcast loop concurrently with the HTTP server. All of this is expressed as `go func()` calls — lightweight goroutines, not OS threads.
- Go compiles to a single static binary with no runtime dependencies. All three services build from the same `Dockerfile.backend` using a `SERVICE` build arg — the only difference is which `cmd/` directory is compiled.
- The strong type system caught domain bugs at compile time (e.g., `JobStatus` and `FailureReason` are typed strings — you can't pass one where the other is expected).

Evidence: `backend/go.mod` — `go 1.22`; `internal/simulator/simulator.go` — three concurrent goroutines

---

**Q: How does concurrency work in the ingestion service?**

The ingestion service starts one goroutine per Kafka topic via `consumer.Start(ctx)`. Each goroutine runs an infinite read loop calling `r.ReadMessage(ctx)`. When the context is cancelled (shutdown signal), `ReadMessage` returns an error, the goroutine detects `ctx.Err() != nil`, logs "consumer loop stopped", and returns.

No channels between goroutines are needed — each goroutine independently reads from its Kafka topic and calls its handler. The only shared state is the database pool and cache client, which are safe for concurrent use (pgxpool and go-redis are both goroutine-safe by design).

Evidence: `internal/kafka/consumer.go` `Start()` and `consume()`

---

**Q: How is graceful shutdown handled?**

The main function passes a `context.Context` derived from `os.Signal` (SIGTERM/SIGINT) to every service. When the signal fires:
- The context is cancelled.
- Simulator's `Run()` select loop detects `<-ctx.Done()` and returns.
- Ingestion's consumer goroutines detect context cancellation in `ReadMessage()` and return.
- API server's `Start()` selects on `<-ctx.Done()` and calls `httpSrv.Shutdown(ctx)` with a 15-second timeout to drain in-flight requests.

Evidence: `internal/api/server.go` `Start()` and `shutdown()`; `internal/simulator/simulator.go` `Run()`

---

**Q: What is `embed.FS` and why use it for migrations?**

`//go:embed migrations/*.sql` is a Go directive that bakes the SQL files into the compiled binary at build time. The resulting binary has no external file dependencies — you don't need to ship a `migrations/` directory alongside it, and you can't accidentally deploy the binary without its migrations.

`embed.FS` is the read-only file system interface that exposes the embedded files. The `migrate()` function calls `migrationsFS.ReadDir("migrations")` and `migrationsFS.ReadFile("migrations/001_initial_schema.sql")` exactly as if they were on disk.

Evidence: `internal/store/db.go` — `//go:embed migrations/*.sql` and `var migrationsFS embed.FS`

---

**Q: Why use `sync.RWMutex` in the simulator instead of channels?**

The simulator's cluster state is a simple map that's read frequently (GPU tick reads every node) and written rarely (fault tick modifies a few nodes). `RWMutex` is the right tool: multiple goroutines can hold `RLock()` concurrently; only one can hold `Lock()`. Using channels for this would require a dedicated goroutine to serialize access (actor pattern), which is more code for no correctness benefit here.

The alternative — one goroutine owning all state, communicated via channels — would be idiomatic Go for more complex state machines but adds indirection when a mutex is sufficient.

Evidence: `internal/simulator/faults.go` — `s.state.mu.RLock()` for reads, `s.state.mu.Lock()` for node state transitions

---

**Q: Why does the ingestion service use a goroutine for GPU summary refresh?**

```go
go func() {
    refreshCtx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
    defer cancel()
    if summary, err := svc.db.ClusterGPUSummary(refreshCtx); err == nil {
        _ = svc.cache.SetGPUSummary(refreshCtx, summary)
    }
}()
```

GPU metrics arrive every 5 seconds from 40 GPU/node combinations. Recomputing and caching the cluster GPU summary synchronously on every metric insert would block the consumer goroutine. The summary refresh is best-effort — if it fails or the goroutine is slow, the 2s TTL on the cache ensures it expires and gets recomputed on the next API request. Fire-and-forget with a timeout is appropriate here.

Evidence: `internal/ingestion/ingestion.go` `handleGPUMetric()`


---

## 12. DATA MODELS & DOMAIN DESIGN

---

**Q: Walk me through the domain models.**

Five core models in `internal/models/`:

- **`Node`** — a physical GPU machine. Carries per-GPU arrays (`GPUUtilization []float64`, `GPUTemperature []float64`, etc.) — one element per GPU on the node. Status enum: `healthy`, `degraded`, `unavailable`, `maintenance`. Methods: `GPUWastePercent()` (GPUs allocated but util < 10%), `AvgGPUUtilization()`.

- **`Job`** — a training job. Status lifecycle: `queued` → `running` → `completed`/`failed`/`preempted`. `FailureReason` is a typed string enum (`oom`, `hardware_fault`, `timeout`, `preemption`, `user_error`) that drives the assistant routing. `Priority` is an int 1–10 — low-priority jobs (≤3) are preemption candidates. Method: `DurationSeconds()`, `IsTerminal()`.

- **`Alert`** — a fired notification. FK to both `NodeID` and `JobID` (both nullable). `Resolved bool` + `ResolvedAt *time.Time` for lifecycle tracking. `AlertType` enum drives UI badge rendering.

- **`ClusterSummary`** — the dashboard rollup. Embeds `ClusterGPUSummary` as a nested struct. Computed on every call to `store.ClusterSummary()` and cached in Redis.

- **Event types** (`NodeEvent`, `JobEvent`, `GPUMetricEvent`, `AlertEvent`) — typed envelopes wrapping domain objects for Kafka transport.

Evidence: `internal/models/node.go`, `job.go`, `alert.go`, `events.go`

---

**Q: Why are GPU metrics stored as arrays on the Node vs. separate rows per GPU?**

Two competing approaches:

1. **Array on node row** (what's done here for live state): `gpu_utilization DOUBLE PRECISION[]` stores all 8 GPU readings in one column. One upsert per node tick, one row to read for the node detail page. Simple, fast for the current node count.

2. **Separate `gpu_metrics` table** (what's done here for time-series history): each reading gets its own row with `(node_id, gpu_index, recorded_at)`. Enables time-range queries and aggregates.

Both are used simultaneously, serving different purposes: the array on the node row gives the latest snapshot instantly (no join, no time-range filter). The `gpu_metrics` table enables the GPU time-series chart (last 1 hour of readings per GPU index).

Evidence: `internal/models/node.go` — `GPUUtilization []float64`; `internal/store/migrations/001_initial_schema.sql` — both `nodes.gpu_utilization[]` and the `gpu_metrics` table

---

**Q: Why are `StartTime` and `EndTime` pointers on the Job model?**

```go
StartTime *time.Time `json:"start_time,omitempty"`
EndTime   *time.Time `json:"end_time,omitempty"`
```

A queued job has never started — `StartTime` is genuinely null, not zero. A running job has no end time. Using `*time.Time` (pointer) means `nil` in Go maps to `NULL` in Postgres and is omitted from JSON (`omitempty`). Using `time.Time` (value) would require a sentinel value like `time.Time{}` (zero time) to represent "not set," which would appear as `"0001-01-01T00:00:00Z"` in JSON responses — meaningless and confusing to API consumers.

Evidence: `internal/models/job.go`; `internal/store/jobs.go` `scanJob()` — `&j.StartTime` scanned as nullable

---

**Q: How are alert types and severity levels structured?**

Both use typed string constants:

```go
type AlertSeverity string
const (
    AlertSeverityCritical AlertSeverity = "critical"
    AlertSeverityWarning  AlertSeverity = "warning"
    AlertSeverityInfo     AlertSeverity = "info"
)
```

This gives three benefits: the compiler catches invalid values (you can't pass a raw string `"CRITICAL"` where `AlertSeverity` is expected), JSON serializes to the human-readable string (no magic numbers), and Postgres stores the string directly — readable in the DB without a lookup table.

Eight alert types are defined: `node_unavailable`, `node_degraded`, `gpu_high_temperature`, `gpu_memory_full`, `job_failed`, `capacity_waste`, `job_timeout`, `cluster_degraded`.

Evidence: `internal/models/alert.go`


---

## 13. TESTING

---

**Q: What tests exist and what do they cover?**

One test file: `internal/assistant/engine_test.go`. It has two table-driven test functions:

- **`TestAnalyzeJob`** — 7 cases covering every job status/failure combination: OOM, hardware fault, timeout, preemption, user error, running, and completed. Each case asserts: exact `RootCause` string, exact `Severity`, minimum `DebuggingSteps` count, minimum `Confidence` score, and that `Headline`/`Summary` are non-empty.

- **`TestAnalyzeNode`** — 3 cases: degraded node with high temperature, unavailable node, and healthy node. Each asserts `Severity` and `RootCause`.

The test file has a detailed comment explaining its dual purpose: it's both a correctness test for the current rule engine AND an eval harness for a future LLM — run the same cases against LLM output, compare against rule output as baseline.

Evidence: `internal/assistant/engine_test.go`

---

**Q: Why are there no integration tests or API tests?**

Honest answer: this is a demo project. The assistant engine was the one component with complex branching logic (5 failure types × multiple sub-conditions for nodes) that genuinely needed a test harness to be confident in correctness. The rest — HTTP handlers, Kafka consumer routing, cache invalidation — are straightforward enough that the integration test is "run `make dev` and check the dashboard."

In a production system I'd add:
- HTTP integration tests for the API handlers using `httptest.NewRecorder()`
- A test Postgres instance for store-layer tests (using `testcontainers-go`)
- A test Kafka for ingestion pipeline tests
- End-to-end smoke tests against the full Docker Compose stack

Evidence: Only `engine_test.go` exists in the entire backend test surface

---

**Q: How would you run the existing tests?**

```bash
cd backend
go test ./internal/assistant/...
```

Or from the project root using the Makefile (if a test target exists). No external dependencies needed — the engine test uses only in-memory structs and `zap.NewNop()` for the logger.

Evidence: `internal/assistant/engine_test.go` `makeEngine()` — `assistant.NewEngine(zap.NewNop())`


---

## 14. DEPLOYMENT & INFRASTRUCTURE

---

**Q: How is the system deployed locally?**

Everything runs in Docker Compose. One command — `make dev` — starts 13 services:

| Category | Services |
|---|---|
| Infrastructure | `postgres`, `redis`, `zookeeper`, `kafka` |
| Observability | `prometheus`, `grafana`, `jaeger`, `otel-collector` |
| Application | `api`, `ingestion`, `simulator` |
| Frontend | `frontend` (Vite dev server) |

Health checks are configured on every service. The application services use `depends_on: condition: service_healthy` to ensure Postgres, Redis, and Kafka are ready before starting.

Evidence: `docker-compose.yml`

---

**Q: How are the three Go binaries built from the same Dockerfile?**

`Dockerfile.backend` uses a `SERVICE` build argument:

```dockerfile
ARG SERVICE
RUN go build -o /app ./cmd/${SERVICE}
```

In `docker-compose.yml`:
```yaml
api:
  build:
    args:
      SERVICE: server
ingestion:
  build:
    args:
      SERVICE: ingestion
simulator:
  build:
    args:
      SERVICE: simulator
```

One Dockerfile, three images built from the same Go module, each compiling a different `cmd/` entry point.

Evidence: `docker-compose.yml` — `api`, `ingestion`, `simulator` services with `args: SERVICE:`

---

**Q: Why are observability configs baked into Docker images instead of bind-mounted?**

The `docker-compose.yml` has a comment explaining this: "All bind mounts have been replaced with baked images to work around a Docker Desktop bug where colons in the host path break volume parsing."

On macOS, paths like `/Users/shubhkapadia/Desktop/Development/Web-Apps/ClusterOps` contain no colons, but Docker Desktop has a known issue parsing volume strings when the path is on a non-standard drive or has certain characters. Baking config files into the image (`COPY config.yaml /etc/otel/`) is more portable and eliminates the bind mount dependency.

Evidence: `docker-compose.yml` comment at the top; `otel-collector`, `prometheus`, `grafana` all use `build:` instead of `image:` + volume

---

**Q: What ports are exposed and for what?**

| Port | Service | Purpose |
|---|---|---|
| 3000 | Frontend | Vite dev server |
| 3001 | Grafana | Dashboards |
| 8080 | API | REST + SSE |
| 9090 | Prometheus | Metrics scrape/UI |
| 9093 | Kafka | External broker access |
| 16686 | Jaeger | Trace UI |
| 4317 | OTel Collector | OTLP gRPC |
| 4318 | OTel Collector | OTLP HTTP |
| 5432 | Postgres | DB (dev access) |
| 6379 | Redis | Cache (dev access) |

Evidence: `docker-compose.yml` — `ports:` on each service

---

**Q: Is there a CI/CD pipeline?**

Not in this repository. There are no `.github/workflows/` or CI config files. This is a local dev/demo project. In a production setup I'd add:
- GitHub Actions: `go test ./...`, `go vet`, `golangci-lint` on every push
- Docker image builds on merge to main
- Deployment to a Kubernetes cluster via Helm or Kustomize

Evidence: No CI config files found in the workspace file tree


---

## 15. GAPS & HONEST LIMITS

---

**Q: What would you do differently or improve if this went to production?**

Honest list, grounded in what the code actually has vs. what it's missing:

1. **Kafka error handling:** the current consumer logs and skips on error. Production needs retry with backoff and a dead-letter topic. `internal/kafka/consumer.go` — "log and skip — appropriate for a demo."

2. **No authentication or authorization:** the API has `AllowedOrigins: ["*"]` CORS and no auth middleware. Every endpoint is public. Production needs at minimum JWT validation or mTLS.

3. **SSE doesn't scale across replicas:** `SSEBroker` is an in-memory map. If you run two API instances, clients connected to replica A don't receive events broadcast by replica B. Fix: replace the in-memory broker with a Redis pub/sub subscriber so all replicas receive events.

4. **GPU metrics table will grow unboundedly without the prune job:** the 30-minute application-level prune is a single point of failure. Production needs `pg_cron` or TimescaleDB retention policies.

5. **100% OTel sampling:** `AlwaysSample()` in `telemetry/otel.go` is fine for demos, prohibitively expensive at production traffic. Switch to head-based probabilistic sampling (1–5%).

6. **No down migrations:** the idempotent migration system has no rollback. If migration 003 introduces a bad column, you'd need to write a manual fix. Use `golang-migrate` with `up`/`down` files.

7. **Health check doesn't check Kafka:** `handleHealth()` checks Postgres and Redis but not Kafka connectivity. A Kafka partition leader outage wouldn't surface in `/health`.

Evidence: `internal/kafka/consumer.go`; `internal/api/server.go` CORS config; `internal/api/sse.go`; `internal/telemetry/otel.go`; `internal/api/handlers.go` `handleHealth()`

---

**Q: What does this project NOT demonstrate that might be on your resume?**

Being honest about what isn't in the code:

- **No real LLM or AI inference:** the assistant is rule-based. There's no Ollama, OpenAI, or vector store call anywhere in the codebase. Don't claim RAG or "AI-powered" if asked to define those precisely.
- **No Kubernetes:** everything is Docker Compose. No Helm charts, no manifests, no pod scheduling concepts.
- **No authentication/authorization:** no JWT, no OAuth, no RBAC.
- **No CI/CD pipeline:** no GitHub Actions, no automated tests in a pipeline.
- **No database partitioning:** the `gpu_metrics` table comment says "partitioned by day in production" — but there's no actual partitioning here.
- **No gRPC:** all service communication is either Kafka (async) or HTTP REST. OTLP uses gRPC but that's the OpenTelemetry SDK, not service-to-service gRPC you wrote.
- **No distributed tracing instrumented in handlers:** OTel is initialized but individual handler spans aren't created — the tracer provider is set up but `tracer.Start()` isn't called per request.

---

**Q: What are the most interesting technical decisions you made and why?**

Three that show real thinking:

1. **Single-writer ingestion pattern** — making the ingestion service the only DB writer and keeping the API server read-only eliminates an entire class of cache consistency bugs. It's a constraint that makes the system easier to reason about. Evidence: `internal/ingestion/ingestion.go` package doc.

2. **Rule engine as LLM eval harness** — building the assistant as deterministic rules first, with the test suite explicitly designed to serve as a regression baseline when swapping in an LLM. This is how production AI systems are actually built — not "let's add an LLM and see what happens." Evidence: `internal/assistant/engine_test.go` comment.

3. **Embedding migrations in the binary** — using `//go:embed` means the binary is self-contained. Deploy one file, get schema migrations automatically on startup. No external migration tool, no deployment checklist item for running migrations separately. Evidence: `internal/store/db.go`.

---

*Generated from live codebase scan — all claims are backed by real file paths.*
*Last scanned: ClusterOps @ commit state as of session start.*


# Fake Review Detector — Interview Q&A

All answers grounded in real code values from the repository.
Every `Evidence:` line points to the actual file and config that proves the answer.

---

## SECTION 1 — PROJECT OVERVIEW

**Q1: Walk me through this project at a high level.**

Short answer: I built a system that detects fake Yelp reviews using six ML models, served through a REST API and browser UI.

- The pipeline starts in `data_prep.py` — one script cleans all 608k reviews and produces every artifact that the six model families need, so all comparisons are on identical data.
- Classical models (LR, RF) consume a TF-IDF sparse matrix. Deep models (LSTM, BiLSTM) consume padded integer sequences. Transformers (BERT, RoBERTa) consume raw cleaned text via their own tokenizers.
- `app.py` is a Flask REST API that lazy-loads models on first request and caches them. Logs every prediction to SQLite. Exposes `/predict/batch`, `/history`, and `/stats`.
- The browser UI is vanilla JavaScript and HTML — no framework, no build step.

Evidence: `data_prep.py`, `app.py`, `classical_models.py`, `deep_models.py`, `transformer_models.py`

---

**Q2: Why did you build six models instead of just picking the best one?**

Short answer: the goal was a benchmark, not a product decision. You cannot say BERT is worth the compute cost unless you have a fair comparison against simpler models on the same data.

- All six models train from the same `data_prep.py` artifacts, same 80/20 stratified split, same text cleaning. Accuracy differences reflect model capability, not data handling.
- A team shipping to production would use classical models for real-time requests (0.020ms latency) and reach for BERT/RoBERTa only when accuracy matters more than cost.
- Trade-off I accepted: six models means six training pipelines to maintain.

Evidence: `data_prep.py` — single split and cleaning function shared across all pipelines.

---

## SECTION 2 — DATA PIPELINE

**Q3: Why did you put all preprocessing in one script instead of letting each model handle its own data?**

Short answer: if each model cleans its own data you cannot trust the accuracy comparisons.

- If LR uses one tokenizer and BERT uses another, and their test sets differ by even one row, you are comparing data pipelines not models.
- `data_prep.py` runs once and produces `train.csv`, `test.csv`, `y_train.npy`, `y_test.npy`, the TF-IDF matrix, the Keras tokenizer, and the padded sequences. Every downstream script consumes these exact files.
- Trade-off I accepted: you must run `data_prep.py` before any model can train. Mandatory setup step, fair price for reproducibility.

Evidence: `data_prep.py` — `TEST_SIZE=0.20`, `RANDOM_STATE=42`, `stratify=df["binary_label"]` used once for the whole project.

---

**Q4: What is TF-IDF and why did you use it?**

In one line: TF-IDF turns text into numbers by scoring how distinctive a word is in a specific document relative to the whole corpus.

- Term Frequency counts how often a word appears in one review. Inverse Document Frequency down-weights words that appear in almost every review like "the" and "and". Multiplying them highlights distinctive words.
- In this codebase: `TfidfVectorizer(max_features=30_000, ngram_range=(1,2), sublinear_tf=True)`. The 30k vocab cap keeps the sparse matrix manageable. Bigrams capture two-word signals like "never again". `sublinear_tf=True` applies log scaling so a word appearing 100 times does not get 100x the weight of a word appearing once.
- When I would reach for it: fast interpretable text features with no GPU. When not: when word order or context matters — TF-IDF treats "not good" and "good not" identically.

Evidence: `data_prep.py` lines 81-84.

---

**Q5: Why 30,000 features for TF-IDF?**

Short answer: 30k captures most meaningful vocabulary without making the sparse matrix too large for RAM.

- The alternative: using all features. On 608k reviews the vocabulary could push into the hundreds of thousands, creating matrices too large for memory.
- 30k keeps the training matrix around 2-3 GB — manageable on a laptop.
- Trade-off I accepted: rare but informative words beyond rank 30k are dropped. Fake review language tends to use common superlatives so the cap unlikely hurts accuracy meaningfully.

Evidence: `data_prep.py` — `MAX_FEATURES = 30_000`.

---

**Q6: Why bigrams in TF-IDF?**

Short answer: fake reviews tend to use specific two-word phrases that unigrams miss entirely.

- "Never again", "absolutely amazing", "best ever", "highly recommend" are signals that only make sense as a pair. A unigram model sees "never" and "again" separately with no connection.
- Trade-off: bigrams roughly double the feature space. The 30k cap controls this — most slots end up being the most informative unigrams and bigrams combined.

Evidence: `data_prep.py` — `TFIDF_NGRAMS = (1, 2)`.

---

**Q7: Why 80/20 train-test split?**

Short answer: 80/20 is standard for datasets above 100k rows. At 608k reviews, 20% gives 121k test samples — statistically more than sufficient.

- Cross-validation would give more robust estimates but at 6x the training cost. Running 5-fold CV on 6 models including BERT is impractical on CPU.
- 70/30 would waste training data — no benefit when you already have 486k training rows.
- Stratified split preserves the 6.6:1 fake-to-real imbalance in both splits.

Evidence: `data_prep.py` — `TEST_SIZE=0.20`, `stratify=df["binary_label"]`.

---

## SECTION 3 — CLASSICAL MODELS

**Q8: Why Logistic Regression as a baseline?**

Short answer: it is fast, interpretable, and strong on TF-IDF features for text classification.

- LR on TF-IDF is a proven baseline for binary text classification. If your complex model cannot beat it, the complex model is not earning its cost.
- `class_weight="balanced"` handles the 6.6:1 imbalance automatically.
- Single-sample inference at 0.020ms — fastest of all six models, measured directly from the saved artifact.
- Trade-off I accepted: LR assumes features are linearly separable. Fine for a baseline role.

Evidence: `classical_models.py` — `LogisticRegression(C=1.0, max_iter=1000, solver="lbfgs", class_weight="balanced")`.

---

**Q9: Why cap Random Forest training at 50,000 rows?**

Short answer: Random Forest on a 30k-feature sparse matrix is extremely slow at full scale. Training on 50k rows takes minutes on a laptop. Training on 486k would take hours.

- The subsample is stratified — same class ratio as the full training set — so the model is not biased.
- Trade-off I accepted: RF accuracy is from a model trained on 50k rows not 486k. Documented and I would acknowledge it.

Evidence: `classical_models.py` — `RF_TRAIN_SAMPLE_SIZE=50000`, `maybe_sample_for_random_forest()` uses stratified split.

---

**Q10: Explain the Random Forest hyperparameters you chose.**

- `n_estimators=80`: 80 trees balance prediction stability against training time. More trees reduce variance with diminishing returns.
- `max_depth=45`: prevents trees from memorizing individual reviews. Unlimited depth on sparse TF-IDF leads to severe overfitting.
- `max_features="sqrt"`: each split considers only sqrt(30000) ≈ 173 features, forcing diversity between trees.
- `max_samples=0.5`: each tree trains on 50% of rows, reducing correlation between trees.
- `min_samples_split=10`, `min_samples_leaf=3`: prevent nodes that cover only a handful of reviews.
- `class_weight="balanced_subsample"`: recomputes class weights per bootstrap sample — better for imbalanced data than a single global weight.

Evidence: `classical_models.py` lines 141-153.

---

**Q11: Logistic Regression vs Random Forest — when would you use each?**

Verdict: LR for real-time single-prediction serving. RF when you need slightly better handling of non-linear feature interactions and can afford the latency.

- LR: 0.020ms single-sample latency. RF: 13.3ms. Both measured from saved artifacts.
- RF can capture non-linear feature combinations — a review with "good" and "service" might be fake in one context and real in another. LR treats these as independent.
- What RF is genuinely better at: high-cardinality features, non-linear boundaries, naturally handling feature interactions.

Evidence: latency measured live from `artifacts/logistic_regression.pkl` and `artifacts/random_forest.pkl`.

---

## SECTION 4 — DEEP LEARNING

**Q12: Walk me through the LSTM architecture.**

Architecture: `Embedding(30000, 128) → LSTM(128, return_sequences=True) → GlobalMaxPooling1D → Dropout(0.3) → Dense(1, sigmoid)`

- `Embedding(30000, 128)` maps each of 30k vocabulary tokens to a 128-dimensional learned vector.
- `LSTM(128, return_sequences=True)` outputs a hidden state at every time step, not just the last one.
- `GlobalMaxPooling1D` takes the max value across all 200 time steps per feature — captures the most discriminative signal anywhere in the review.
- `Dropout(0.3)` randomly zeros 30% of neurons during training to prevent overfitting.
- `EarlyStopping(patience=2)` and `ReduceLROnPlateau(factor=0.5, patience=1)` handle convergence automatically.

Evidence: `deep_models.py` — `build_lstm()`.

---

**Q13: Why GlobalMaxPooling1D instead of taking the last LSTM hidden state?**

Short answer: `GlobalMaxPooling1D` is more robust for reviews where the key fake signal can appear anywhere.

- The last hidden state only reflects what the LSTM was processing at the final token. A suspicious phrase in the first half of a review may have faded by the time the LSTM reaches the end.
- `GlobalMaxPooling1D` scans all 200 time steps and takes the max per feature — captures the strongest signal wherever it appears.
- What the last hidden state is genuinely better at: tasks where the final state meaningfully summarizes the whole sequence, like language modeling.

Evidence: `deep_models.py` — `GlobalMaxPooling1D(name="pool")` in both `build_lstm()` and `build_bilstm()`.

---

**Q14: What is a BiLSTM and why include it alongside a regular LSTM?**

In one line: a BiLSTM runs two LSTMs simultaneously — one left-to-right and one right-to-left — and concatenates their outputs at every time step.

- The forward LSTM sees "this food was amazing" and the backward LSTM sees "amazing was food this". Both streams are concatenated, doubling the hidden state size to 256.
- Why it matters: fake reviews often have suspicious phrasing at the start or end. A unidirectional LSTM may miss end-of-review signals. BiLSTM captures both.
- Trade-off I accepted: BiLSTM is roughly 2x the parameters and slower to train. Worth keeping both to compare.

Evidence: `deep_models.py` — `Bidirectional(LSTM(128, return_sequences=True))`.

---

**Q15: Why mask_zero=True on the Embedding layer?**

Short answer: reviews are padded to 200 tokens but most reviews are shorter. `mask_zero=True` tells the LSTM to ignore padding tokens instead of treating them as real input.

- Without it the LSTM processes 200 tokens for every review even if the actual review is 40 tokens. The 160 padding zeros add noise to the hidden state.
- With `mask_zero=True` TensorFlow propagates a mask and the LSTM skips padded positions.

Evidence: `deep_models.py` — `Embedding(MAX_FEATURES, EMBED_DIM, mask_zero=True)`.

---

**Q16: How did you handle class imbalance in the deep models?**

Short answer: computed class weights using sklearn and passed them to `model.fit()`.

- The dataset has a 6.6:1 imbalance — 87% real and 13% fake. Without handling, a model achieves 87% accuracy by always predicting "real", which is useless.
- `compute_class_weight(class_weight="balanced")` calculates weights inversely proportional to class frequency. The fake class gets weight ~6.6, real gets ~1.0.
- These are passed as `class_weight={0: 6.6, 1: 1.0}` to `model.fit()` so each fake review error contributes 6.6x more to the loss.

Evidence: `deep_models.py` — `get_class_weight()`, `sklearn.utils.class_weight.compute_class_weight`.

---

**Q17: Why EarlyStopping patience=2 and ReduceLROnPlateau?**

Short answer: fixed epochs on a large dataset risks overfitting or wasting time.

- `EarlyStopping(patience=2, restore_best_weights=True)`: if validation loss does not improve for 2 consecutive epochs, stop and restore the best weights.
- `ReduceLROnPlateau(factor=0.5, patience=1, min_lr=1e-6)`: halve the learning rate if validation loss plateaus for 1 epoch.
- Trade-off I accepted: patience=2 is aggressive and the model might stop before fully converging. On a dataset this large, 2 epochs of no improvement is a reasonable stop signal.

Evidence: `deep_models.py` — `get_callbacks()`.

---

## SECTION 5 — TRANSFORMER MODELS

**Q18: What is BERT and why fine-tune instead of training from scratch?**

In one line: BERT is a large language model pre-trained by Google on billions of words that already understands language — fine-tuning applies that understanding to your specific task.

- Training from scratch requires hundreds of millions of examples and weeks of GPU compute. Fine-tuning takes hours on a small dataset.
- BERT already knows "absolutely amazing" and "highly recommend" are positive phrases. Fine-tuning shifts its parameters to recognize that in the fake review context these phrases are often suspicious.
- In this codebase: `AutoModelForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2)` — adds a 2-class classification head on top of the pre-trained encoder.

Evidence: `transformer_models.py` — `MODEL_REGISTRY = {"bert": ("bert-base-uncased", "bert_model")}`.

---

**Q19: BERT vs RoBERTa — what is the difference?**

Verdict: RoBERTa is stronger for classification tasks. I included both for the benchmark.

- RoBERTa is BERT trained longer, on more data, without the Next Sentence Prediction objective, and with dynamic masking. These changes consistently improve downstream task performance.
- What BERT is genuinely better at: it has been around longer with more community tooling. For some tasks with very limited fine-tuning data it generalizes slightly better.
- In this codebase: both use identical fine-tuning code — same `MAX_SEQ_LEN=128`, same `LR=2e-5`, same `EPOCHS`. The only difference is the pretrained checkpoint name.

Evidence: `transformer_models.py` — `MODEL_REGISTRY`, same `fine_tune()` function for both.

---

**Q20: Why learning rate 2e-5 for fine-tuning?**

Short answer: 2e-5 is the standard starting point from the original BERT paper. Small enough to avoid destroying pre-trained weights.

- Higher LR like 1e-4: the optimizer overshoots and destroys the language representations BERT learned — called catastrophic forgetting.
- Lower LR like 1e-6: training is too slow to converge meaningfully in 1-3 epochs.
- The warmup scheduler starts near zero and linearly increases to 2e-5 over the first 10% of steps, then linearly decays.

Evidence: `transformer_models.py` — `LR = float(os.environ.get("TRANSFORMER_LR", "2e-5"))`, `get_linear_schedule_with_warmup(num_warmup_steps=int(0.1 * total_steps))`.

---

**Q21: What is gradient clipping and why use it?**

In one line: gradient clipping caps the maximum size of gradient updates so a single bad batch cannot destabilize the whole model.

- After computing gradients, if the global gradient norm exceeds 1.0, all gradients are scaled down so the norm equals exactly 1.0.
- BERT has 110 million parameters. One batch with an unusually high loss can cause gradient explosion that makes the model useless in one step. Clipping prevents this.
- When I would skip it: small stable models like LR or shallow networks where gradient explosion is rare.

Evidence: `transformer_models.py` — `torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)`.

---

**Q22: Why max_length=128 for transformers instead of 200 like LSTM?**

Short answer: transformer self-attention scales quadratically with sequence length. Doubling from 128 to 256 quadruples memory and compute.

- LSTM processes tokens sequentially — going from 200 to 128 is a linear cost reduction.
- BERT self-attention computes pairwise attention between every token: 128x128=16,384 values vs 200x200=40,000 — 2.5x more memory per sample.
- Most Yelp reviews fit within 128 tokens. `truncation=True` drops the tail of longer reviews, acceptable since fake signals are usually concentrated early.

Evidence: `transformer_models.py` — `MAX_SEQ_LEN = int(os.environ.get("TRANSFORMER_MAX_SEQ_LEN", "128"))`.

---

**Q23: Why limit transformer training to 10,000 rows on CPU?**

Short answer: fine-tuning BERT on 486k rows at batch size 8 on CPU would take days. 10k is the practical ceiling for a laptop demo.

- At batch size 8 and ~3 seconds per batch on CPU: 10k rows = 1,250 batches = ~62 minutes per epoch. Acceptable.
- At 486k rows: ~60,750 batches = ~50 hours per epoch. Completely impractical.
- The limit automatically sets to 0 (use all data) when CUDA is detected, so the same codebase scales to GPU without any code change.
- Trade-off I accepted: transformer accuracy numbers are from a model trained on 10k rows not 486k. Documented and I would acknowledge it.

Evidence: `transformer_models.py` — `DEFAULT_TRAIN_LIMIT = "0" if DEVICE == "cuda" else "10000"`.

---

**Q24: What is AdamW and why use it over regular Adam?**

In one line: AdamW is Adam with decoupled weight decay — it regularizes model weights without interfering with the adaptive learning rate.

- Regular Adam applies weight decay through the gradient, which interacts badly with adaptive per-parameter learning rates.
- AdamW applies weight decay directly to the weights, separately from the gradient update. This is the standard choice for transformer fine-tuning.
- Trade-off vs SGD: Adam variants converge faster but use more memory — stores first and second moment estimates for every parameter. For 110M BERT parameters, that is significant.

Evidence: `transformer_models.py` — `from torch.optim import AdamW`, `optimizer = AdamW(model.parameters(), lr=LR, eps=1e-8)`.

---

## SECTION 6 — FLASK API AND SERVING

**Q25: Why Flask instead of FastAPI or Django?**

Verdict: Flask for simplicity. This is a model serving app with 5 routes.

- Django brings an ORM, admin panel, form handling, and an auth system. None of that is needed here.
- FastAPI is the right choice if I needed async I/O — if transformer inference was non-blocking. Flask is synchronous so a BERT request blocks the server thread for ~2 seconds.
- What FastAPI is genuinely better at: async handlers, automatic OpenAPI docs, type validation via Pydantic. For a growing real API, FastAPI is the better call.
- Trade-off I accepted: Flask is synchronous. Under concurrent load, transformer requests queue.

Evidence: `app.py` — `from flask import Flask`, `requirements.txt` — `flask>=3.0.0`.

---

**Q26: Why lazy-load models instead of loading everything at startup?**

Short answer: BERT and RoBERTa are ~440 MB each. Loading all 6 at startup consumes ~1-2 GB of RAM and crashes a free-tier server before serving a single request.

- `_models_cache` dict in `app.py` holds each model once loaded. First request for a model triggers loading (2-3 seconds for transformers). All subsequent requests are instant from cache.
- Classical models load in milliseconds and are cached the same way.
- Trade-off I accepted: the first request for any model is slower. For a demo or low-traffic tool this is invisible. For high-traffic production you would preload the most common model at startup.

Evidence: `app.py` — `_models_cache = {}`, `get_model()` — checks cache before loading.

---

**Q27: How does the batch endpoint work and why cap it at 100?**

Short answer: `/predict/batch` accepts a list of review texts, loops through them calling `run_prediction()` for each, and returns all results in one response.

- Currently processes reviews sequentially not in a true vectorized batch. For classical models this does not matter (0.020ms each). For transformers it would be worth vectorizing.
- The 100-review cap prevents a single request from tying up the server for minutes with transformer predictions and avoids memory spikes from very large input lists.
- Trade-off I accepted: sequential processing is simpler. A production system would implement true vectorized batching.

Evidence: `app.py` — `/predict/batch`, `if len(texts) > 100: return 400`.

---

**Q28: How does prediction logging work and why SQLite locally?**

Short answer: every `/predict` and `/predict/batch` call writes a row to a `predictions` table. SQLite locally because it is built into Python and requires zero infrastructure.

- Schema: `id, text, model, label, confidence, latency_ms, top_words (JSON), created_at`.
- In production, set `DATABASE_URL` env var to a PostgreSQL connection string and the same `db.py` code switches automatically.
- DB errors are non-fatal — wrapped in try/except so a DB failure never breaks a prediction.
- `/history?limit=20` returns recent predictions. `/stats` returns total count, per-model breakdown, and fake percentage.

Evidence: `db.py` — `_is_postgres()`, `init_db()`, `log_prediction()`. `app.py` — try/except around `log_prediction()`.

---

## SECTION 7 — SHAP EXPLAINABILITY

**Q29: What is SHAP and how did you use it?**

In one line: SHAP assigns each input feature a score representing how much it pushed the model's prediction toward one class or the other.

- SHAP is rooted in game theory. It computes the average marginal contribution of each feature across all possible subsets — asking "how much does removing this word change the prediction?"
- In this codebase: `shap.LinearExplainer` for Logistic Regression — fast because it uses the model's linear coefficients directly. Falls back to coefficient multiplication if SHAP fails.
- Only words actually present in the review are considered: `nonzero_idx = vec.nonzero()[1]`.
- Top 5 words by absolute SHAP value are returned as `top_words` in the API response.

Evidence: `explainer.py` — `explain_classical()`, `shap.LinearExplainer(model, vec, feature_perturbation="interventional")`.

---

**Q30: Why is SHAP only on classical models and not LSTM or BERT?**

Short answer: SHAP for deep models requires DeepSHAP or KernelSHAP, both orders of magnitude slower on CPU.

- `LinearExplainer` runs in under 1ms — uses the weight vector directly, no sampling needed.
- `KernelSHAP` for RF requires hundreds of model evaluations per explanation — impractical per live request on a 30k-feature vector.
- `DeepExplainer` for LSTM/BERT requires a background dataset and multiple forward passes per input — acceptable offline, not in a live API.
- Trade-off I accepted: `top_words` is null for LSTM, BiLSTM, BERT, and RoBERTa. Documented in `explainer.py`.

Evidence: `explainer.py` docstring — "Only works for logistic_regression and random_forest".

---

## SECTION 8 — LANGCHAIN INTEGRATION

**Q31: What is LangChain and why did you add it?**

In one line: LangChain is a framework for building AI applications where an agent calls multiple tools in sequence to complete a task.

- In this codebase: the detector is wrapped as a `Tool` with a name, description, and a `func` that takes review text and returns a plain-English verdict. Any LangChain agent can call `tool.run("review text")` without knowing about Flask, TF-IDF, or model loading.
- Why I added it: as a Tool the detector is composable. An agent could retrieve reviews from a database, call this tool on each, and generate a moderation report — all in one pipeline.

Evidence: `langchain_tool.py` — `build_fake_review_tool()`, `Tool(name="FakeReviewDetector", func=_run)`.

---

**Q32: Is this project agentic?**

Short answer: no. The LangChain Tool wrapper makes the detector composable inside an agent, but the project itself does not contain an agent with a reasoning loop.

- A true agentic system has a model that decides which tool to call, calls it, observes the result, and decides what to do next — a loop with state and decision-making.
- In this codebase there is no `initialize_agent()`, no `AgentExecutor`, no multi-step loop. The docstring shows how you would wire it into an agent but that code is not in this project.
- How I would describe it honestly: "I wrapped the detector as a LangChain Tool so it is ready to be used inside an agent pipeline. The tool itself is a single callable."

Evidence: `langchain_tool.py` — no `AgentExecutor`, no multi-step reasoning loop anywhere in the codebase.

---

## SECTION 9 — INT8 QUANTIZATION

**Q33: What is INT8 quantization and why did you add it?**

In one line: quantization converts model weights from 32-bit floating point to 8-bit integers, reducing model size by ~75% and speeding up CPU inference by 2-4x.

- How it works: instead of storing each weight as a 32-bit float, it maps the weight range to a 256-value integer scale with a stored scaling factor. Matrix multiplications run faster on integer hardware units available in all modern CPUs.
- In this codebase: `torch.quantization.quantize_dynamic(model, {torch.nn.Linear}, dtype=torch.qint8)` — only the Linear layers inside the transformer are quantized. Embeddings are left as float because quantizing them provides minimal benefit.
- Why this matters: a 440 MB BERT model becomes ~110 MB. On a free-tier server with 512 MB RAM, this is the difference between fitting in memory and crashing.
- Trade-off I accepted: tiny accuracy loss (typically <0.5%). Dynamic quantization does not require a calibration dataset — it quantizes activations at inference time which is slightly less efficient than static quantization but much simpler to set up.

Evidence: `quantize_transformers.py` — `torch.quantization.quantize_dynamic(model, {torch.nn.Linear}, dtype=torch.qint8)`.

---

**Q34: Dynamic quantization vs static quantization — what is the difference?**

Verdict: dynamic quantization for this project because it requires no calibration data and no extra training step.

- Dynamic quantization: weights are quantized ahead of time. Activations are quantized at inference time per batch. Simpler, works on any model immediately after training.
- Static quantization: both weights and activations are quantized using statistics collected from a representative calibration dataset run before deployment. Faster at inference but requires that calibration step.
- Post-training quantization-aware training (QAT): the model is fine-tuned with fake quantization in the forward pass so the model learns to compensate for quantization error. Best accuracy, highest effort.
- For this project: dynamic quantization is the right balance — no calibration dataset needed, immediate size and speed benefit, negligible accuracy cost.

Evidence: `quantize_transformers.py` — `torch.quantization.quantize_dynamic`.

---

## SECTION 10 — SYSTEM DESIGN AND ARCHITECTURE

**Q35: If you had to deploy this to production for 10,000 requests per day, what would you change?**

Short answer: four changes — async API, vectorized batch inference, model preloading, and a proper job queue.

1. Swap Flask for FastAPI with async handlers so transformer requests do not block the server thread.
2. Implement true vectorized batching for transformer models — group incoming requests into mini-batches and run one forward pass per batch instead of one per request.
3. Preload the most commonly requested model at startup rather than on first request.
4. Move transformer inference to a background worker (BullMQ or Celery) and return a job ID immediately, polling for the result — transformers are too slow for synchronous HTTP at scale.
5. Replace SQLite with PostgreSQL and add connection pooling.

Evidence: current `app.py` is synchronous Flask — the architectural gaps are real.

---

**Q36: How would you add monitoring to this system?**

Short answer: three layers — inference latency, prediction distribution drift, and error rates.

- Inference latency is already logged per prediction to the `predictions` table (`latency_ms` column). Aggregating this gives percentile latency over time.
- Prediction distribution drift: if the ratio of fake predictions starts rising unexpectedly, that signals either a change in the incoming review population or model degradation. The `/stats` endpoint already returns `fake_pct`.
- Error rates: wrap each model call in a counter that increments on exception. Expose via a `/metrics` endpoint in Prometheus format.
- What I have not built: a Prometheus exporter or Grafana dashboard. I would acknowledge this gap.

Evidence: `db.py` — `get_stats()` returns `fake_pct`, `per_model`, `total`. `app.py` — `latency_ms` logged on every prediction.

---

**Q37: How does the text cleaning work and why is it the same across all models?**

Short answer: lowercase, strip all non-alphabetic characters, collapse whitespace. Applied in `data_prep.py` for training and in `app.py` for inference — same function, same output.

- "AMAZING food!!!" becomes "amazing food" — same token for both train and test regardless of capitalization or punctuation.
- If `data_prep.py` cleaned differently than `app.py`, the model would see different inputs at training versus inference time. This is called a training-serving skew and is a common source of production bugs.
- The `clean_text()` function


# Brand Guardian AI — Interview Q&A

> Grounded in real source code. Every answer cites the actual file that proves it.

---

## SECTION 1 — PROJECT OVERVIEW

### Q: Walk me through what this project does.

**Short answer:** It's an internal compliance tool that takes a YouTube ad URL and tells you whether it violates YouTube's ad policies or FTC influencer guidelines — with exact citations to the rule that was broken.

- A reviewer submits a URL to `POST /audit`.
- A three-node LangGraph pipeline runs: `indexer` fetches metadata from YouTube Data API v3, `enrich` tries to pull captions via three progressively heavier methods, `auditor` does RAG against indexed compliance PDFs then calls GPT-4o to flag violations.
- The result (PASS/FAIL + severity-graded violations) is saved to Postgres and returned immediately.
- A human reviewer can optionally override the AI's decision, which sets the `final_status` separately from the `ai_status`.

Evidence: `backend/src/graph/workflow.py`, `backend/src/api/server.py`

---

## SECTION 2 — LANGGRAPH / AGENTIC PIPELINE

### Q: What is LangGraph and why did you use it?

**In one line:** LangGraph is a graph execution framework built on LangChain that lets you define multi-step LLM workflows as a directed state machine.

- How it works: You define nodes (Python functions), add directed edges between them, and a shared `TypedDict` state flows through each node. Each node reads from state, does work, and returns a dict that merges back in.
- In this codebase: `workflow.py` defines three nodes — `indexer → enrich → auditor` — each in its own file (`nodes.py`). The compiled graph is called with `compliance_graph.ainvoke(initial_inputs)` inside the `/audit` endpoint.
- When I'd reach for it: any multi-step LLM workflow where you need clear node separation, shared state, and async execution. When not: a single LLM call doesn't need a state machine.

Evidence: `backend/src/graph/workflow.py`, `backend/src/api/server.py`

---

### Q: Is this actually agentic? What makes it a pipeline vs an agent?

Honest answer: this is a **linear pipeline**, not a true agent. The graph has three nodes with hardcoded edges: indexer → enrich → auditor → END. There are no conditional branches, no routing decisions, no tool calls the LLM makes itself, and no retry loops. It's agentic in the sense that it uses an LLM to reason over retrieved context, but the flow is deterministic and sequential.

If you said "agentic workflow" on your resume, clarify it as: "a multi-step LLM pipeline orchestrated with LangGraph."

Evidence: `backend/src/graph/workflow.py` — only `add_edge` calls, no `add_conditional_edges`

---

### Q: Walk me through each node.

**`index_video_node`:** Calls `YouTubeTranscriptService.extract_data(video_url)` which uses YouTube Data API v3 to pull title, description, tags, and any captions available through the API. Sets `ingestion_source = "metadata"`. If it fails, it returns early with `final_status = "FAIL"` so downstream nodes can skip gracefully.

**`enrich_content_node`:** Tries three progressively heavier caption sources: (1) YouTube's `timedtext` endpoint (direct, no auth, supports `en`/`en-US`/`en-GB`), (2) `yt-dlp` subtitle extraction, (3) Azure Video Indexer for full speech transcription + OCR on-screen text. Updates `transcript` and `ocr_text` in state. If all three fail it falls back to the metadata already in state.

**`audit_content_node`:** Concatenates transcript + OCR text, calls `search_policy_chunks()` (RAG, top-k = 8 by default), formats them with CHUNK_ID + SOURCE labels, constructs a system prompt embedding those rules, sends to GPT-4o at `temperature=0.0`, parses the JSON response, and calls `_attach_citations()` to enrich each violation with the source PDF name and excerpt.

Evidence: `backend/src/graph/nodes.py`

---

### Q: What is the VideoAuditState and why use TypedDict?

**In one line:** It's the shared data contract that all three nodes read from and write to as the graph executes.

- `VideoAuditState` is a `TypedDict` with fields like `video_url`, `transcript`, `ocr_text`, `compliance_results`, `final_status`, `errors`. Two fields — `compliance_results` and `errors` — use `Annotated[List, operator.add]` which tells LangGraph to *append* rather than replace when multiple nodes write to them.
- TypedDict over a dataclass: zero overhead, type-safe, and LangGraph's `StateGraph` constructor takes it directly.

Evidence: `backend/src/graph/state.py`

---

## SECTION 3 — RAG (RETRIEVAL AUGMENTED GENERATION)

### Q: What is RAG and where did you use it?

**In one line:** RAG means you retrieve relevant chunks from a knowledge base at query time and inject them into the LLM prompt, so the model reasons against real documents instead of its training data.

- How it works: At index time, PDFs are split into chunks (1000 chars, 200 overlap), each chunk gets a UUID, embedded with `text-embedding-3-small`, and uploaded to Azure AI Search. At query time, `search_policy_chunks(query_text, k=8)` embeds the query and does cosine similarity search to return the 8 most relevant chunks. Those chunks — with CHUNK_ID and SOURCE labels — are injected directly into the GPT-4o system prompt.
- In this codebase: the query text is `transcript + OCR text` concatenated. The model is explicitly told to set `chunk_id` in each violation to the CHUNK_ID it relied on. After the response, `_attach_citations()` resolves each `chunk_id` back to the full source and excerpt.
- When not RAG: if the model just gets a static policy text pasted in the prompt every time, that's prompt injection, not RAG.

Evidence: `backend/src/services/policy_store.py`, `backend/src/services/policy_indexing.py`, `backend/src/graph/nodes.py`

---

### Q: Why Azure AI Search for the vector store, not Pinecone or ChromaDB?

**Verdict:** Azure AI Search because the whole stack is Azure and it avoids an extra service + API key to manage.

- Why it fits here: the project already uses Azure OpenAI, Azure Container Apps, and Azure Monitor. Using Azure AI Search keeps IAM, networking, and billing in one place.
- What Pinecone is genuinely better at: dedicated vector search with more index tuning options (HNSW params, namespaces, metadata filtering). If you needed sub-10ms retrieval at massive scale, Pinecone wins.
- ChromaDB is better for: local development / prototyping with zero infra. No cloud dependency.
- Trade-off I accepted: Azure AI Search's free tier has limited index capacity. The `similarity_search` call is a round-trip HTTP request per audit, no connection pooling.

Evidence: `backend/src/services/policy_store.py` — `AzureSearch(...)` from `langchain_community.vectorstores`

---

### Q: What is RAG_TOP_K and what value did you use?

`RAG_TOP_K` is the number of policy chunks retrieved per audit. It defaults to `8` (set via `int(os.getenv("RAG_TOP_K", "8"))`). You can override it per environment. 8 is a reasonable balance — enough context for the model to catch multi-rule violations without blowing the context window.

Evidence: `backend/src/services/policy_store.py` — `rag_top_k()` function

---

### Q: How are citations attached to violations?

The model is instructed in the system prompt to set `chunk_id` in each violation JSON to the `CHUNK_ID` it cited. After parsing the response, `_attach_citations()` builds a lookup dict (`chunk_map`) from the retrieved chunks, then for each violation, resolves `chunk_id → source filename + first 500 chars of content`. The `setdefault` calls mean the model's own excerpt wins if it provided one. If a `chunk_id` is missing or not in the map, the row is returned as-is without crashing.

Evidence: `backend/src/graph/nodes.py` — `_attach_citations()` function; `tests/test_citations.py` validates both the happy path and the missing-chunk-id graceful fallback

---

### Q: What embedding model did you use and why?

`text-embedding-3-small` from Azure OpenAI. It's the default in `policy_store.py` (`azure_deployment=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-3-small")`). It's OpenAI's cost-efficient embedding model, accurate enough for compliance text retrieval, and runs in the same Azure resource as GPT-4o — no extra service to manage.

Evidence: `backend/src/services/policy_store.py`

---

### Q: What chunk size and overlap did you use for indexing?

Chunk size: **1000 characters**, overlap: **200 characters**, using LangChain's `RecursiveCharacterTextSplitter`. The overlap ensures that a rule spanning a paragraph boundary isn't split mid-sentence and lost to retrieval.

Evidence: `backend/src/services/policy_indexing.py`

---

## SECTION 4 — HYBRID INGESTION

### Q: What is the hybrid ingestion service and why three methods?

**Short answer:** Getting accurate captions out of YouTube is unreliable. No single method works for all videos, so I implemented a fallback chain.

- Method 1 — `timedtext` endpoint: Direct call to `youtube.com/api/timedtext?v=VIDEO_ID&lang=en`. No auth, fast, works for videos with official captions. First tried for `en`, `en-US`, `en-GB` in order.
- Method 2 — `yt-dlp`: A well-maintained open source library that can extract auto-generated subtitles. Slower, downloads caption track URL from video info, fetches the raw track. Catches videos where the timedtext endpoint is blocked or returns nothing.
- Method 3 — Azure Video Indexer: The heavy fallback. Uploads the video URL to Azure VI, polls until `state == "Processed"` (up to 30 polls × 5s), then pulls both speech transcript AND `ocr` (on-screen text). This is the only source of OCR data.
- If all fail: the pipeline continues with just the metadata from the indexer node — it degrades gracefully rather than crashing.

Evidence: `backend/src/services/ingestion.py` — `HybridIngestionService.enrich()`

---

### Q: Why did you keep all three instead of just using Azure Video Indexer?

Cost and latency. Azure Video Indexer uploads and processes the full video — that's minutes of wait time and non-trivial cost per audit. The `timedtext` endpoint is free and instantaneous. yt-dlp is free and takes a few seconds. The expensive path only runs when both cheaper paths return nothing. You also need `AZURE_VI_ACCOUNT_ID` and `AZURE_VI_LOCATION` to be configured; the code checks for those before attempting it.

Evidence: `backend/src/services/ingestion.py` — `if all([VideoIndexerService().account_id, ...])`

---

### Q: What is the `ingestion_source` field for?

It records which method actually provided the content: `"metadata"`, `"captions"`, `"captions_ytdlp"`, or `"video_indexer"`. This is stored on the `Audit` DB row and returned in the API response. A reviewer looking at a FAIL result can see whether the audit was based on full captions or just metadata — which matters for confidence in the finding.

Evidence: `backend/src/db/models.py` (`ingestion_source` column on `Audit`), `backend/src/api/server.py`

---

## SECTION 5 — FASTAPI & SERVER DESIGN

### Q: Why FastAPI over Flask or Django?

**Verdict:** FastAPI, because this is a pure API with async I/O and I need automatic OpenAPI docs.

- Why it fits here: the `/audit` endpoint calls `compliance_graph.ainvoke()` which is async — FastAPI handles that natively. Flask is WSGI-only, Django is overkill for a JSON API.
- What Django is genuinely better at: built-in admin, ORM, session management — a full web app. Not needed here.
- Trade-off I accepted: FastAPI has no built-in background task queue. If audit volume got high I'd need to add a queue (Celery, ARQ). Right now it runs synchronously per request.

Evidence: `backend/src/api/server.py` — `FastAPI()`, `async def audit_video(...)`

---

### Q: How does the lifespan work?

FastAPI's `lifespan` context manager runs code at server startup (before the first request) and shutdown. In this project it bootstraps a default `Team` record in the DB when `AUTH_DISABLED=true`. This ensures the dev path has a team to attach users to without manual setup. In production (`AUTH_DISABLED=false`) this block doesn't run.

Evidence: `backend/src/api/server.py` — `@asynccontextmanager async def lifespan(app)`

---

### Q: What CORS setup did you use?

Origins are read from `ALLOWED_ORIGINS` env var as a comma-separated list (`_parse_allowed_origins()`), falling back to `http://localhost:8000`. The README explicitly warns against wildcard origins in production. `allow_credentials=True` is set, which is needed if the frontend sends cookies or auth headers.

Evidence: `backend/src/api/server.py`

---

## SECTION 6 — AUTHENTICATION & AUTHORIZATION

### Q: Explain the auth system.

**Short answer:** Dual-path auth — Microsoft Entra ID (JWT Bearer) for human users, SHA-256 hashed API keys for programmatic access — with three RBAC roles.

- **Entra ID path:** `GET /auth/me` and `POST /audit` check for a Bearer token. `decode_entra_token()` uses `PyJWKClient` to fetch Microsoft's public signing keys from the JWKS endpoint, validates the RS256 JWT (checking `exp`, `iss`, `aud`, `sub`), extracts the `oid` claim as the stable user ID, and maps `roles` claims to one of `admin`, `reviewer`, `read_only`.
- **API key path:** If `X-API-Key` header is present, `authenticate_api_key()` SHA-256 hashes the raw key, looks up the hash in `team_api_keys`, and synthesizes a `User` record scoped to that team.
- **Roles:** `admin` can reindex policies and manage API keys. `reviewer` can submit audits and override AI decisions. `read_only` can only list audit history — `require_audit_submitter` blocks them with 403.

Evidence: `backend/src/auth/dependencies.py`, `backend/src/auth/entra.py`, `backend/src/auth/api_keys.py`

---

### Q: Why PyJWT over python-jose or authlib?

`PyJWT` is the most widely maintained pure-Python JWT library. `python-jose` has had CVEs and slow maintenance. `authlib` is heavier and aimed at OAuth server implementation. For this use case — only token validation, not issuance — `PyJWT[crypto]` with its `PyJWKClient` is the minimal, correct choice.

Evidence: `pyproject.toml` — `"pyjwt[crypto]>=2.10.0"`

---

### Q: How does the JWKS client cache work?

The module-level `_jwks_client` is reused for 1 hour (`_JWKS_TTL_SECONDS = 3600`). `_get_jwks_client()` checks `time.time() - _jwks_client_created_at > 3600` and recreates the client if stale. This avoids a JWKS HTTP call on every request while not caching keys forever (Microsoft rotates keys periodically).

Evidence: `backend/src/auth/entra.py`

---

### Q: Why SHA-256 for API key hashing, not bcrypt?

API keys are long random secrets (32 bytes from `secrets.token_urlsafe`), so brute-force is impractical. bcrypt is designed for low-entropy passwords. SHA-256 is fast enough for a 256-bit random key lookup and doesn't add bcrypt's CPU cost per request. The `bg_` prefix allows fast rejection of non-API-key strings before hashing.

Evidence: `backend/src/auth/api_keys.py` — `hash_api_key()`, `raw_key = f"bg_{secrets.token_urlsafe(32)}"`

---

### Q: What is `AUTH_DISABLED` and why does it exist?

It's a dev escape hatch (`AUTH_DISABLED=true` in `.env`) that bypasses all token validation and returns a hardcoded admin `UserContext` via `_dev_user_context()`. Without it, local development requires a real Entra ID tenant, which is friction. The README explicitly says never set this in production. The code checks it with `os.getenv("AUTH_DISABLED", "false").lower() in ("1", "true", "yes")` to prevent accidental activation.

Evidence: `backend/src/auth/dependencies.py`, `backend/src/auth/entra.py`

---

## SECTION 7 — DATABASE & ORM

### Q: Why SQLAlchemy + PostgreSQL? Why not a NoSQL store?

**Verdict:** SQLAlchemy + PostgreSQL because the data has a clear relational shape and I needed audit history queries scoped by team.

- The schema has explicit FK relationships: `Team → User → Audit → AuditViolation`, `Audit → ReviewDecision`, `Audit → PolicyVersion`. These are naturally relational.
- Team-scoped queries (`list_audits_for_team`) benefit from indexed FK columns and the composite index `ix_audits_team_created` on `(team_id, created_at)`.
- `raw_response` is stored as JSONB — so the structured fields are normalized and queryable, but the full LLM response is also preserved for debugging.
- Alembic handles schema migrations with two versions: `001_initial_schema.py` (all core tables) and `002_team_api_keys.py` (adds `team_api_keys`). That's a real incremental migration history.

Evidence: `backend/src/db/models.py`, `alembic/versions/`

---

### Q: What is the `ai_status` vs `final_status` distinction?

`ai_status` is what the LLM returned (PASS/FAIL). `final_status` is the effective status after a human reviewer potentially overrides it. When no review exists, `final_status == ai_status`. When a reviewer calls `POST /reviews/{audit_id}` with `approved` or `rejected`, the `final_status` is updated. This separation is the core of the human-in-the-loop design — you can always see what the AI said versus what a human decided.

Evidence: `backend/src/db/models.py` — `Audit` model

---

### Q: Why store `raw_response` as JSONB?

Compliance is an audit trail domain. If the LLM output format changes, or if a team disputes a finding, you want the original response to be reconstructable. JSONB lets you store the full unmodified response without a schema migration every time the `compliance_results` format evolves, while still being queryable in PostgreSQL if needed.

Evidence: `backend/src/db/models.py` — `raw_response: Mapped[dict | None] = mapped_column(JSONB, nullable=True)`

---

### Q: Why is `policy_version_id` on the Audit row?

So you can always know exactly which version of the compliance documents was in the vector store when this audit ran. If you re-index with updated PDFs, old audits still reference the previous policy version. This is important for compliance traceability: "this ad was audited against policy v20250601-143022."

Evidence: `backend/src/db/models.py`, `backend/src/api/server.py` — `policy_version = get_current_policy_version(db)`

---

## SECTION 8 — RATE LIMITING

### Q: How does the rate limiter work?

**In one line:** In-memory sliding window per IP address, 30 requests per minute, applies only to `POST /audit`.

- It's a `BaseHTTPMiddleware` subclass. Each IP gets a `deque[float]` of request timestamps. On each request, stale entries (older than 60s) are popped from the left. If `len(bucket) >= 30`, it returns 429.
- Only `POST /audit` is rate-limited — all other routes pass through immediately.
- The limit is configurable via `RATE_LIMIT_PER_MINUTE` env var.

Evidence: `backend/src/middleware/rate_limit.py`

---

### Q: Redis is in your dependencies but you don't use it. Why?

`redis>=7.1.0` is installed but the rate limiter uses an in-memory `defaultdict(deque)`. The comment in the code says "Simple in memory rate limiter for pilot deployments." This is a deliberate ceiling for a single-instance deployment — the kind you get on Azure Container Apps' free tier with one replica.

The known ceiling: if you scale to multiple replicas, each instance has its own counter and the limit effectively multiplies. The upgrade path is to swap the deque for a Redis sorted set (ZRANGEBYSCORE + ZADD + EXPIRE) — Redis is already in the dependency so that migration is a one-file change.

Evidence: `backend/src/middleware/rate_limit.py` — docstring "Simple in memory rate limiter for pilot deployments", `pyproject.toml` — `"redis>=7.1.0"`

---

## SECTION 9 — OBSERVABILITY

### Q: How did you instrument this for observability?

Azure Monitor OpenTelemetry. `setup_telemetry()` in `telemetry.py` is called at server startup. It wires `azure-monitor-opentelemetry` into the FastAPI app via the `opentelemetry-instrumentation-fastapi` package. Traces flow into Azure Application Insights automatically (request spans, dependency spans for outbound HTTP calls to Azure OpenAI and Azure Search). LangSmith is also configured for optional LLM-level tracing (`LANGCHAIN_TRACING_V2=true`).

Evidence: `backend/src/api/telemetry.py`, `backend/src/api/server.py` — `setup_telemetry()`, `pyproject.toml` — `azure-monitor-opentelemetry`, `opentelemetry-instrumentation-fastapi`

---

## SECTION 10 — CI/CD & DEPLOYMENT

### Q: How does deployment work?

GitHub Actions pipeline in `.github/workflows/deploy.yml` triggers on every push to `main`. It builds a Docker image, pushes it to Azure Container Registry, and updates the Azure Container Apps revision. Container Apps is serverless — it scales to zero when there's no traffic, so there's no cost on idle. The `Dockerfile` packages the full Python app with `uvicorn` as the ASGI server.

Evidence: `.github/workflows/deploy.yml`, `Dockerfile`

---

### Q: Why Azure Container Apps over a VM or Kubernetes?

**Verdict:** Container Apps because it removes infra management at this scale.

- For a pilot internal tool, I don't need cluster management, node pools, or manual scaling rules. Container Apps handles that with a managed Kubernetes layer.
- Scale-to-zero means the free tier essentially runs for free when reviewers aren't active.
- What Kubernetes is genuinely better at: fine-grained scheduling, multi-service mesh, stateful workloads. Overkill here.
- Trade-off: Container Apps' concurrency model is simpler — can't tune pod scheduling, no sidecar containers without a workaround.

Evidence: `README.md` architecture table, `.github/workflows/deploy.yml`

---

## SECTION 11 — LLM DESIGN CHOICES

### Q: Why GPT-4o at temperature 0.0?

Temperature 0.0 makes the model deterministic — it always picks the highest probability token. For compliance auditing, you don't want creative variation. Two audits of the same video should return the same findings. The alternative — a higher temperature — might randomly include or exclude a violation between runs, which is unacceptable for a legal/compliance use case.

Evidence: `backend/src/graph/nodes.py` — `AzureChatOpenAI(..., temperature=0.0)`

---

### Q: Why structure the prompt to return JSON instead of free text?

The response is parsed with `json.loads()` and each violation is mapped into a typed `ComplianceIssue` object. Free text would require regex parsing to extract severity, category, and chunk_id — fragile and hard to version. The prompt includes a guard for markdown fences (`if "```" in content`) because GPT-4o sometimes wraps JSON in code blocks even when told not to.

Evidence: `backend/src/graph/nodes.py` — system prompt and `re.search(r"```(?:json)?\s*(.*?)```", content, re.DOTALL)`

---

### Q: Why did you use `SystemMessage + HumanMessage` instead of a single message?

The system prompt contains the retrieved policy rules and the auditor persona — things that should be treated as ground truth. The human message contains the video content to analyze. This split is both idiomatic for chat models and functionally important: system messages get higher attention weight and are less likely to be ignored when the model has to balance a long context.

Evidence: `backend/src/graph/nodes.py` — `llm.invoke([SystemMessage(...), HumanMessage(...)])`

---

## SECTION 12 — TESTING

### Q: What did you test?

Three test files, no framework beyond pytest:

- `tests/test_auth.py` — confirms `/health` is public (no auth), that the debug env routes were removed, that no token returns 401, and that a read-only user gets 403 on `POST /audit`.
- `tests/test_citations.py` — unit tests for `_attach_citations()`: happy path (chunk_id resolves to source + excerpt) and graceful handling of a missing chunk_id (row passes through unchanged).
- `tests/test_ingestion_hybrid.py` — tests the hybrid ingestion service: captions path sets `ingestion_source = "captions"`, and the metadata-only fallback path when captions return nothing.

Evidence: `tests/` directory

---

## SECTION 13 — TRADE-OFFS YOU ACCEPTED

### Q: What would you change if this went to production at scale?

1. **Rate limiter:** swap in-memory deque for Redis sorted set. Redis is already installed, it's a one-file change. Current limiter is per-replica, not per-cluster.
2. **Sync audit endpoint:** `/audit` blocks until the full LangGraph pipeline completes (several seconds). At scale, move to async job queue (Celery, ARQ) — submit returns a job ID, poll or webhook for result.
3. **API key auth defaults to `reviewer` role:** every API key gets `reviewer` — no finer-grained key-level permissions. For multi-tenant SaaS this needs per-key role scoping.
4. **No connection pooling on vector store:** `get_vector_store()` creates a new `AzureSearch` object on every audit. Under load this means repeated HTTP connection setup. Add a module-level singleton.
5. **Azure Video Indexer polls with `time.sleep(5)` 30 times:** that's a 150s max wait on the same thread. Move to proper async polling or a background task.

---

## SECTION 14 — GAPS (What the repo does NOT demonstrate)

| Claim | What's actually here |
|---|---|
| "Used Redis" | Redis is installed but not used — rate limiter is in-memory |
| "Built a queue / async job system" | No queue — synchronous request/response only |
| "Multi-tenant SaaS" | Team isolation exists but it's a single-tenant internal tool |
| "Fine-tuned a model" | No fine-tuning — prompt engineering only |
| "Real-time streaming" | No SSE or WebSocket — batch JSON response |
| "Docker Compose" | No docker-compose.yml — single container only |

Be precise about these if asked. Don't overclaim.

---

## QUICK CHEAT SHEET — Key Numbers

| Value | Source |
|---|---|
| RAG_TOP_K default | 8 (`policy_store.py`) |
| Chunk size / overlap | 1000 / 200 chars (`policy_indexing.py`) |
| LLM model | GPT-4o at temperature 0.0 (`nodes.py`) |
| Embedding model | text-embedding-3-small (`policy_store.py`) |
| Rate limit | 30 POST /audit per IP per minute (`rate_limit.py`) |
| JWKS cache TTL | 1 hour / 3600s (`entra.py`) |
| API key prefix | `bg_` + 32-byte urlsafe token (`api_keys.py`) |
| API key hashing | SHA-256 (`api_keys.py`) |
| Ingestion fallback chain | timedtext → yt-dlp → Azure Video Indexer (`ingestion.py`) |
| DB | PostgreSQL via SQLAlchemy 2.0 + Alembic (`pyproject.toml`) |
| Deployment | Azure Container Apps via GitHub Actions (`deploy.yml`) |
| Python version | 3.12+ (`pyproject.toml`) |


# Distributed Caching — Interview Q&A

> Grounded entirely in real code. Every answer cites the file and concrete value that proves it.
> Format: **Type A** = X vs Y trade-off | **Type B** = What is X | **Type C** = Why did you use X

---

## Table of Contents

1. [System Architecture](#1-system-architecture)
2. [Consistent Hashing](#2-consistent-hashing)
3. [Eviction Policies](#3-eviction-policies)
4. [Cache Invalidation Strategies](#4-cache-invalidation-strategies)
5. [Raft Consensus](#5-raft-consensus)
6. [gRPC Transport](#6-grpc-transport)
7. [In-Memory Cache Implementation](#7-in-memory-cache-implementation)
8. [Database Layer](#8-database-layer)
9. [API Design](#9-api-design)
10. [Concurrency & Thread Safety](#10-concurrency--thread-safety)
11. [Observability](#11-observability)
12. [Docker & Deployment](#12-docker--deployment)
13. [Testing Strategy](#13-testing-strategy)
14. [Language & Ecosystem Choices](#14-language--ecosystem-choices)
15. [Trade-off Summaries](#15-trade-off-summaries)

---

## 1. System Architecture


### Q1. Walk me through the overall architecture of this system.

**Short answer:** Five services wire together — a reverse proxy, an API layer, three cache nodes, PostgreSQL, and a Prometheus/Grafana monitoring stack.

- External clients hit the reverse proxy on port 8080. It forwards to the API on port 8081.
- The API layer owns the cache-aside read/write logic and connects to all three cache nodes via a consistent hashing ring.
- Each cache node runs an in-memory cache, a Raft state machine for leader election, and a gRPC server for cache operations.
- PostgreSQL (port 5433 externally) is the source of truth for product data.
- Prometheus scrapes metrics from all five services every 5 seconds. Grafana visualises them on port 3000.

Evidence: `docker-compose.yml` — service topology, ports, and health checks.

---

### Q2. Why did you separate the proxy and the API into two different services?

**Short answer:** Separation of concerns — the proxy handles cross-cutting HTTP concerns, the API handles business logic.

- The proxy (`cmd/proxy`) handles things like routing and can later add rate limiting or TLS termination without touching the API code.
- The API (`cmd/api`) is purely focused on the cache-aside pattern, DB queries, and invalidation logic.
- In Docker Compose the proxy depends on the API being healthy before it starts, giving a clean startup order.
- Trade-off I accepted: extra network hop. For a learning sandbox that's fine; in production you'd measure whether that hop hurts P99 latency.

Evidence: `docker-compose.yml` proxy service; `cmd/proxy/main.go`.

---

### Q3. How does a GET /products/{id} request flow end-to-end?

**Short answer:** Proxy → API → cache check → DB fallback → cache populate → response.

- Request arrives at proxy (:8080), forwarded to API (:8081).
- `handler.go GetProduct` calls `CacheAside.GetProduct`.
- Cache is checked first (`cache.Get`). On a HIT, return immediately with `X-Cache: HIT`.
- On a MISS, `db.GetProduct` runs a parameterised SELECT against PostgreSQL.
- The DB result is serialised as JSON and written to the cache with a 5-minute TTL.
- Response returns with `X-Cache: MISS`.

Evidence: `internal/api/middleware.go` — `GetProduct` method; `defaultProductTTL = 5 * time.Minute`.


---

## 2. Consistent Hashing

### Q4. What is consistent hashing and where did you use it?

**In one line:** A way to distribute keys across nodes so that adding or removing a node only remaps a fraction of the keys, not all of them.

- How it works: you place nodes on a circular uint32 ring using virtual tokens. To find which node owns a key, hash the key and walk clockwise to the first token.
- In this codebase: `internal/cluster/ring.go`. Each physical node gets 150 virtual tokens placed at deterministic positions using FNV-1a hashes of `"nodeID-0"` through `"nodeID-149"`. `ring.Get(key)` does a binary search over the sorted token list — O(log n).
- When I'd reach for it: any time you need to distribute keys across a fleet and can't afford full re-hashing when the fleet size changes (e.g. cache clusters, database sharding).
- When not: if the key space is tiny and you never add/remove nodes, a simple modulo is simpler.

Evidence: `internal/cluster/ring.go` — `defaultVirtualNodes = 150`, `hashKey` using `fnv.New32a()`.

---

### Q5. Why 150 virtual nodes per physical node?

**Short answer:** 150 gives even distribution across 3 nodes without wasting memory.

- With only 3 physical nodes and no virtual nodes, one unlucky hash collision could make one node handle 80% of keys.
- 150 virtual tokens per node = 450 total tokens on the ring, which is enough to even out the distribution.
- The cluster test `TestRing_MultipleNodes_DistributesKeys` verifies each node gets between 50–150 keys out of 300 — roughly ±50% variance is the sanity check.
- Trade-off: more virtual nodes = more memory for the token map and a longer sorted slice to binary search. 150 is the conventional sweet spot (Cassandra uses 256).

Evidence: `internal/cluster/ring.go` — `const defaultVirtualNodes = 150`; `internal/cluster/cluster_test.go` — `TestRing_MultipleNodes_DistributesKeys`.

---

### Q6. What hash function did you use for the ring and why?

**Short answer:** FNV-1a (32-bit) — fast, deterministic, and spreads keys well across a uint32 space.

- FNV-1a is just XOR-then-multiply in a tight loop. No allocations, no crypto overhead.
- It's deterministic: same input always produces the same token position, which is essential for routing — every API node must agree on which cache node owns a key.
- I didn't need cryptographic security here. SHA-256 would be overkill and slower.
- Trade-off: FNV-1a has known weaknesses against adversarial inputs (hash flooding). For a private Docker network that's irrelevant; for a public-facing key-value store you'd use SipHash.

Evidence: `internal/cluster/ring.go` — `hashKey` function using `hash/fnv` from stdlib.

---

### Q7. What happens when a cache node goes down?

**Short answer:** Keys owned by that node return cache misses and fall through to PostgreSQL. No rerouting.

- The coordinator's `Route(key)` checks `NodeHealth.IsAvailable()`. If the responsible node is unavailable, it returns `available=false` with no error.
- The API treats that as a cache miss and queries the DB directly.
- Keys are NOT rerouted to another node because that node doesn't have the data — you'd just get a miss either way. The ADR documents this explicitly.
- When the node recovers, the health probe marks it available again and cache population resumes on the next read.
- Trade-off: no high availability for cached data. Full Raft write replication would fix that at the cost of write latency.

Evidence: `internal/cluster/coordinator.go` — `Route` method; `docs/adr/0001-raft-for-leader-election-only.md`.


---

## 3. Eviction Policies

### Q8. What eviction policies did you implement and how do they work?

**Short answer:** Four — LRU, LFU, TTL-only, and Random. All implement the same `EvictionPolicy` interface.

- **LRU (Least Recently Used):** evicts the entry that hasn't been accessed the longest. Internally a doubly linked list: `OnAccess` moves the key to the front; `Evict` pops from the back.
- **LFU (Least Frequently Used):** evicts the entry with the lowest access count. On a tie, evicts the one with the older `accessedAt` timestamp.
- **TTL-only:** ignores recency or frequency; always evicts the entry closest to expiry. `OnAccess` is a no-op.
- **Random:** picks a key uniformly at random from the live set. No access tracking needed.

All four are pluggable via the `shared.EvictionPolicy` interface. The `cache.InMemoryCache` doesn't know which policy it has — it just calls `policy.OnAccess`, `policy.OnInsert`, `policy.OnEvict`, `policy.Evict`.

Evidence: `internal/shared/eviction.go` — interface; `internal/eviction/` — four implementations.

---

### Q9. LRU vs LFU — when would you pick one over the other?

**Verdict:** LRU for most web workloads; LFU when the hot key set is stable over time.

- LRU fits here: a product catalog has temporal locality — a product that just got featured will get a burst of reads. LRU keeps it warm during the burst.
- LFU is genuinely better at: filtering out one-hit wonders that would otherwise push useful items out.
- In this codebase: LRU is the default in `docker-compose.yml` (`EVICTION_POLICY: lru`) and is what all cache nodes and the API's local cache use. The benchmark at `cmd/benchmark` runs all four against a Zipf distribution (exponent=1.0, 10,000 ops, keyspace=500, capacity=100) so you can compare empirically.
- Trade-off I accepted: LFU has a cold-start penalty — a new product starts at frequency 1 and can get evicted even if it's about to become popular.

Evidence: `docker-compose.yml` — `EVICTION_POLICY: lru`; `internal/benchmark/eviction.go` — `DefaultEvictionConfig`.

---

### Q10. What is lazy expiry and why did you use it?

**Short answer:** Instead of a background goroutine scanning all entries for expired ones, we check TTL only when a key is actually accessed.

- On `cache.Get`, if the entry's `ExpiresAt` is in the past, we delete it and return a miss — no background work.
- This is the same approach Redis uses. It avoids a continuous O(n) scan and the goroutine complexity that comes with it.
- Trade-off: stale entries occupy memory until they're next accessed. `Len()` may overcount because it includes expired-but-not-yet-cleaned entries. `LiveLen()` does a full scan under a read lock and gives the accurate count — it's O(n) and documented as such.

Evidence: `internal/cache/cache.go` — `Get` method comment "Lazy expiry means we only check TTL when a key is actually accessed, rather than running a background goroutine scanning all entries. This is the same approach Redis uses."

---

### Q11. How does the cache stay under its capacity limit?

**Short answer:** Before inserting a new key, if `len(entries) >= capacity`, we call `policy.Evict()` to remove one entry first.

- The check is: `if len(c.entries) >= c.capacity` — note it only fires on new keys, not upserts.
- The evicted key is deleted from the map and `OnEvict` is called to clean up the policy's internal tracking.
- Capacity is validated at config load time: must be between 1 and 1,000,000.
- Cache nodes in Docker Compose run with `CACHE_CAPACITY: 10000`; the API's local cache uses `CACHE_CAPACITY: 5000`.

Evidence: `internal/cache/cache.go` — `Set` method; `internal/shared/config.go` — capacity validation; `docker-compose.yml`.


---

## 4. Cache Invalidation Strategies

### Q12. What cache invalidation strategies did you implement?

**Short answer:** Three — TTL (passive expiry), write-through (synchronous update), and write-behind (async deletion).

All three implement `shared.InvalidationStrategy`. The active strategy is injected at startup via `INVALIDATION_STRATEGY` env var. The API's Docker Compose config uses `write-through` as the default.

- **TTL:** `OnWrite` is a complete no-op. The cache entry expires naturally after 5 minutes. Simplest; readers may see stale data.
- **Write-through:** `OnWrite` synchronously calls `cache.Set` with the new value before returning. Both DB and cache are updated in the same request. TTL is reset to 5 minutes.
- **Write-behind:** `OnWrite` returns immediately, then a background goroutine deletes the cache key after a 100ms delay. The delete must complete within 5 seconds (`writeBehindDeadline`). We delete rather than set because a concurrent read may have already re-populated the cache with fresh data by the time the goroutine runs.

Evidence: `internal/invalidation/ttl.go`, `writethrough.go`, `writebehind.go`; `docker-compose.yml` — `INVALIDATION_STRATEGY: write-through`.

---

### Q13. Write-through vs write-behind — when would you pick each?

**Verdict:** Write-through when consistency matters most; write-behind when write latency matters most.

- Write-through fits this project: it's a product catalog where a price update should be visible immediately. The extra cache.Set call is negligible for a catalog workload.
- Write-behind is genuinely better at: high-throughput write scenarios (e.g. counters, view counts) where you want sub-millisecond write acknowledgement and can tolerate 5 seconds of staleness.
- In this codebase: write-through is the default in docker-compose. The benchmark at `internal/benchmark/invalidation.go` runs all three against 5,000 ops (80% reads, 20% writes) so you can see the latency difference empirically.
- Trade-off I accepted with write-behind: if the process crashes after the DB write but before the goroutine deletes the cache, the cache serves stale data until TTL expires.

Evidence: `internal/invalidation/writebehind.go` — `writeBehindDeadline = 5*time.Second`, `writeBehindDelay = 100*time.Millisecond`.

---

### Q14. What happens if the cache update fails after the DB write?

**Short answer:** The DB write has already committed — we treat the cache error as non-fatal and let the next read re-populate from DB.

- In write-through, if `cache.Set` returns an error, the strategy wraps it with `fmt.Errorf` and returns it, but `CacheAside.UpdateProduct` explicitly ignores the strategy error: `_ = ca.strategy.OnWrite(...)`.
- In write-behind, if the async `cache.Delete` fails, it logs the error and notes "will expire via TTL". No panic, no retry storm.
- This is intentional: the DB is the source of truth. A failed cache write just means the next GET will be a cache miss and hit the DB, which is correct behaviour.

Evidence: `internal/api/middleware.go` — `UpdateProduct` comment "Per requirement 6.2"; `internal/invalidation/writebehind.go` — async error handling.

---

### Q15. Why does write-behind DELETE the entry instead of SET the new value?

**Short answer:** By the time the goroutine runs (100ms+ later), a concurrent read may have already re-populated the cache with fresh data. Setting would overwrite a potentially newer value.

- The goroutine fires 100ms after the write. In that window, another GET for the same key could have hit the DB and written the latest value to the cache.
- If the goroutine then SET the old value, it would silently corrupt the cache.
- Deleting forces the next read to fetch from the DB, which is always correct.
- Trade-off: one extra cache miss on the next read, but correctness is preserved.

Evidence: `internal/invalidation/writebehind.go` — comment "We DELETE rather than SET because by the time the goroutine runs, a new read may have already re-populated the cache with fresh data from DB."


---

## 5. Raft Consensus

### Q16. What is Raft and why did you use it here?

**In one line:** A consensus algorithm that elects one node as leader so the cluster has a single coordinator for routing decisions.

- How it works: nodes start as followers. When a follower's election timer fires and no heartbeat has arrived, it becomes a candidate, increments its term, votes for itself, and sends `RequestVote` RPCs to peers. If it gets a majority, it becomes leader and starts sending `AppendEntries` heartbeats every 50ms to prevent re-elections.
- In this codebase: `internal/raft/` — the full state machine. The elected leader calls `coordinator.SetLeader(true)`, which enables routing in `Coordinator.Route`.
- When I'd reach for it: any time you need a cluster-wide agreement on "who's in charge" without a central single point of failure.

Evidence: `internal/raft/timer.go` — `electionTimeoutMin/Max = 150–300ms`, `heartbeatInterval = 50ms`.

---

### Q17. Why randomise the election timeout?

**Short answer:** If all three nodes had the same timeout, they'd all start elections simultaneously, vote for themselves, and nobody would win (split vote). Randomisation staggers them.

- Timeout is uniformly distributed in [150ms, 300ms]. Each node draws a new random value each time the timer resets.
- The probability that two nodes fire in exactly the same 1ms window is very low, so typically one node becomes a candidate first, sends `RequestVote`, and wins before others even time out.
- Split votes can still happen in rare races. The recovery is automatic: every node resets its timer after a failed election, draws a new random value, and the next round converges.

Evidence: `internal/raft/timer.go` — `randomElectionTimeout()` using `rand.Int63n`.

---

### Q18. Raft for leader election only vs full Raft with log replication — why did you choose the simpler path?

**Verdict:** Leader election only. The deciding factor is that cache data doesn't need to survive node failure — it just needs a miss to fall through to PostgreSQL.

- Why it fits here: this is a caching layer, not the source of truth. If a node dies, the worst case is a cache miss, which is an acceptable degradation.
- What full replication is genuinely better at: every key is available on any surviving node — no misses on node failure, lower latency for geo-distributed reads.
- In this codebase: `AppendEntriesRequest` has no `Entries` field (ADR 0001 explicitly notes this), and `RequestVoteRequest` has no `LastLogIndex`/`LastLogTerm`.
- Trade-off I accepted: cache data is not durable. Node restart = cold cache on that node until reads repopulate it.

Evidence: `docs/adr/0001-raft-for-leader-election-only.md`; `internal/raft/rpc.go` — comment on missing log fields.

---

### Q19. How does Raft persistent state survive a crash?

**Short answer:** `currentTerm` and `votedFor` are written to a JSON file on disk after every change. A restarted node loads this file before re-joining.

- Without persistence, a node could vote twice in the same term after a restart — breaking the election safety property.
- The write uses an atomic rename: write to `raft-nodeX.json.tmp`, then `os.Rename` to the real path. Rename is atomic on most Linux filesystems, so a crash mid-write leaves the old state intact.
- State dir is `/tmp/raft` in Docker Compose (ephemeral — intentional for a sandbox).

Evidence: `internal/raft/state.go` — `saveState()` and `loadState()`.


---

## 6. gRPC Transport

### Q20. Why gRPC instead of REST for inter-node communication?

**Verdict:** gRPC. The deciding factor is strongly-typed, binary-framed communication with built-in streaming support — perfect for a high-frequency internal API.

- Why it fits here: cache nodes exchange frequent RPCs (heartbeats every 50ms, cache get/set operations). gRPC's binary protobuf encoding is more compact than JSON and avoids per-request serialisation overhead.
- What REST is genuinely better at: browser compatibility, human-readable payloads, simpler debugging with curl.
- In this codebase: `internal/cluster/transport.go` — `grpcTransport` implements `raft.Transport`. Cache nodes listen on gRPC ports (9001–9003). `google.golang.org/grpc v1.63.2` is in `go.mod`.
- Trade-off I accepted: proto-gen is a required build step (`make proto-gen`) — the transport stubs won't compile to production code without it.

Evidence: `go.mod` — `google.golang.org/grpc v1.63.2`; `internal/cluster/transport.go`; `docker-compose.yml` — ports 9001–9003.

---

### Q21. What are protobuf files and why does this project have a make proto-gen step?

**In one line:** Protocol Buffers are a language-neutral schema that defines the shape of gRPC messages; proto-gen compiles them into Go structs and client/server interfaces.

- You write `.proto` files (e.g. `proto/cache/v1/cache.proto`), run `protoc`, and get generated Go code that both the client and server import.
- This project's transport currently uses placeholder structs in `internal/raft/rpc.go`. The `proto-gen` Makefile target compiles the real `.proto` files into `internal/proto/cache/v1`, `raft/v1`, and `api/v1`.
- When complete, `transport.go` would instantiate `raftv1.NewRaftServiceClient(conn)` and call the generated methods.
- Trade-off: the generated code is checked in or regenerated at build time — you have a hard dependency on `protoc` and the Go plugins.

Evidence: `Makefile` — `proto-gen` target; `internal/cluster/transport.go` — comment showing intended generated client usage.


---

## 7. In-Memory Cache Implementation

### Q22. What data structure backs the in-memory cache?

**Short answer:** A plain Go `map[string]*CacheEntry` — the eviction policy provides its own internal structure on top.

- The map gives O(1) average Get, Set, and Delete. Each value is a pointer to a `CacheEntry` struct containing the value bytes, expiry time, creation time, last-access time, and access count.
- Capacity is not a property of the map itself — the map grows up to `capacity` keys, after which the eviction policy removes one before each new insert.
- The eviction policy (e.g. LRU's doubly linked list) is a separate in-memory structure that mirrors the keys in the map. The cache notifies it via `OnInsert`, `OnAccess`, `OnEvict`.

Evidence: `internal/cache/cache.go` — `entries map[string]*CacheEntry`; `internal/cache/entry.go`.

---

### Q23. How do you handle TTL — absolute vs relative?

**Short answer:** Absolute. We store `ExpiresAt time.Time` computed at insert time (`now.Add(ttl)`), not a remaining-duration counter.

- On every `Get`, we compare `time.Now()` against `entry.ExpiresAt`. No arithmetic needed at read time.
- TTL=0 is treated as immediately expired: `ExpiresAt = now`, so `IsExpired` returns true on the very next read.
- Negative TTL returns an error. TTL > 86400 seconds (24h) returns an error. These are validated in `Set`.
- TTL=zero-value `time.Time` would mean "never expires", but the code always sets a non-zero `ExpiresAt`.

Evidence: `internal/cache/entry.go` — `IsExpired`; `internal/cache/cache.go` — TTL validation in `Set`.

---

### Q24. What does the X-Cache header do and why is it there?

**In one line:** It tells the caller whether the response was served from cache (HIT) or from the database (MISS) — standard convention used by Nginx, Varnish, and CDNs.

- Set on every GET /products/{id} response in `handler.go`.
- If the header fails to be set (the `w.Header().Get` check fails), the handler returns HTTP 500 rather than silently serving data without the header — this is per a requirement.
- In this codebase: `const xCacheHeader = "X-Cache"` in `middleware.go`.
- Useful for: debugging cache behaviour, load testing (verify hit rate without a metrics dashboard), SLA validation.

Evidence: `internal/api/middleware.go` — `xCacheHeader` constant; `internal/api/handler.go` — `GetProduct` header check.


---

## 8. Database Layer

### Q25. Why pgx instead of database/sql?

**Verdict:** pgx. The deciding factor is native PostgreSQL wire protocol support — no abstraction layer, better performance, and typed scanning.

- `database/sql` is a generic driver interface; it works but adds a layer of indirection and doesn't support PostgreSQL-specific types well.
- pgx talks the Postgres wire protocol directly. `pgxpool.Pool` manages a connection pool so we never open a new TCP connection per request.
- `pgx.ErrNoRows` maps cleanly to our `db.ErrNotFound` sentinel — the API layer checks `errors.Is(err, db.ErrNotFound)` and returns 404.
- Version `pgx/v5 v5.5.5` is pinned in `go.mod`.

Evidence: `go.mod` — `github.com/jackc/pgx/v5 v5.5.5`; `internal/db/postgres.go` — `pgxpool.New`, `pgx.ErrNoRows`.

---

### Q26. How does database migration work?

**Short answer:** The `db.New` function runs inline SQL on startup using `CREATE TABLE IF NOT EXISTS` and `INSERT ... ON CONFLICT DO NOTHING` — idempotent, no separate migration tool needed.

- On every service start, `migrate()` runs: creates the `products` table if it doesn't exist, creates an index on `category`, and seeds 10 sample products.
- `ON CONFLICT (id) DO NOTHING` makes the seed idempotent — safe to run repeatedly without duplicating data.
- Trade-off: no version-tracked migrations. If the schema changes, you'd need to add an `ALTER TABLE` and it can't be rolled back cleanly. For a sandbox that's acceptable; in production I'd use golang-migrate or Flyway.

Evidence: `internal/db/postgres.go` — `migrate()` method.

---

### Q27. How does the partial update (PUT /products/{id}) work at the SQL level?

**Short answer:** The UPDATE query is built dynamically — only non-nil pointer fields become SET clauses.

- `ProductUpdateRequest` uses `*string` and `*float64` pointers. Nil means "don't change". This is PATCH semantics delivered over a PUT verb.
- The `UpdateProduct` DB method loops over the request struct, appends `"field = $N"` for each non-nil field, and builds the final query with `fmt.Sprintf`. The `updated_at = NOW()` clause is always included.
- `RETURNING` gives back the full updated row in one round trip.

Evidence: `internal/db/postgres.go` — `UpdateProduct` with dynamic SET clauses; `internal/api/model.go` — `ProductUpdateRequest` pointer fields.


---

## 9. API Design

### Q28. Why does cache key use a "product:" prefix?

**Short answer:** Namespace isolation — prevents accidental key collisions if other types of data are ever cached.

- `const cacheKeyPrefix = "product:"` in `middleware.go`. All product keys are `"product:prod-001"`, `"product:prod-002"`, etc.
- If you later cached user sessions or search results, they'd use `"session:"` or `"search:"` prefixes and never collide with product entries.
- This is the same convention Redis namespacing uses.

Evidence: `internal/api/middleware.go` — `cacheKeyPrefix = "product:"`.

---

### Q29. How does pagination work on GET /products?

**Short answer:** Offset pagination — `LIMIT $1 OFFSET $2` in SQL, driven by `page` and `pageSize` query parameters.

- Default: page=1, pageSize=20. Max pageSize: 100 (capped in the handler before the DB call).
- The DB runs two queries: one `SELECT COUNT(*)` for the total, one `SELECT ... LIMIT/OFFSET` for the page.
- Response includes `products`, `page`, `page_size`, and `total_count`.
- Trade-off: offset pagination can drift if rows are inserted between pages. For a product catalog with infrequent writes, this is fine. Keyset pagination (cursor-based) would be more correct for high-write tables.

Evidence: `internal/api/handler.go` — `ListProducts`; `internal/db/postgres.go` — `ListProducts` SQL.

---

### Q30. How does the /cache/debug/{key} endpoint work?

**Short answer:** It shows the full routing decision for any key — which node owns it per consistent hashing, and whether it's currently in the API's local cache.

- Returns: `owner_node`, `owner_addr`, `in_cache`, `cache_status` (HIT/MISS), `is_coordinator`.
- Useful for diagnosing unexpected misses: if `owner_node` keeps changing, the ring is being rebuilt. If `in_cache` is always false, the TTL may be too short.
- The `ring.Get(key)` call is the same lookup the routing path uses — so debug output reflects actual routing.

Evidence: `internal/api/debug.go` — `CacheDebug` handler; `CacheDebugResponse` struct.


---

## 10. Concurrency & Thread Safety

### Q31. How is the cache thread-safe?

**Short answer:** A `sync.RWMutex` — many goroutines can read in parallel; writes get exclusive access.

- `cache.Get` acquires a read lock for the map lookup. If the entry is expired, it upgrades to a write lock to delete it. It re-checks expiry after acquiring the write lock (double-checked locking pattern) because another goroutine may have already deleted it.
- `cache.Set` and `cache.Delete` always acquire the full write lock.
- `CacheNodeMetrics` uses `atomic.Int64` counters — increment without acquiring any lock, safe for concurrent gRPC handlers.

Evidence: `internal/cache/cache.go` — `mu sync.RWMutex`, re-check after lock upgrade; `internal/cluster/cacheserver.go` — `atomic.Int64`.

---

### Q32. How does the Raft node protect its state?

**Short answer:** A single `sync.Mutex` protects all Raft state fields. The election loop and RPC handlers always lock before reading or writing state.

- `n.mu.Lock()` is taken at the top of `HandleRequestVote`, `HandleAppendEntries`, `startElection`, `sendHeartbeats`, and `becomeFollower/Candidate/Leader`.
- `isLeader` in the `Coordinator` uses `atomic.Bool` — no lock needed for reads in the hot path.

Evidence: `internal/raft/state.go` — `mu sync.Mutex`; `internal/cluster/coordinator.go` — `isLeader atomic.Bool`.

---

### Q33. What is the race detector and did you run it?

**Short answer:** Go's built-in data race detector — `go test -race` instruments every memory access and reports concurrent reads/writes without synchronisation.

- The CI pipeline runs `go test -race ./...` on every push to main (`.github/workflows/ci.yml`).
- The cache concurrency test `TestCache_ConcurrentAccess_NoRace` spins up 50 goroutines doing concurrent Get/Set/Delete and is specifically designed to trigger races if the locking is wrong.
- The Makefile has a `race` target: `go test -race ./...`.

Evidence: `.github/workflows/ci.yml` — `go test -race ./...`; `internal/cache/cache_test.go` — `TestCache_ConcurrentAccess_NoRace`; `Makefile` — `race` target.


---

## 11. Observability

### Q34. How is the system monitored?

**Short answer:** Prometheus scrapes metrics from all five services every 5 seconds. Grafana visualises them. `prometheus/client_golang v1.19.0` is the Go client.

- Each cache node exposes `/metrics` on its HTTP metrics port (9101, 9102, 9103).
- The API exposes `/metrics` on port 8081. The proxy exposes it on port 8080.
- Prometheus config is embedded directly in `docker-compose.yml` as a Docker config object — no separate `prometheus.yml` file to manage.
- Scrape interval: 5s (both `scrape_interval` and `evaluation_interval`).
- Metrics tracked per node: `cache_hits`, `cache_misses`, `cache_evictions`, `cache_entries`, plus the `eviction_policy` label so all four policies can be compared on the same Grafana dashboard.

Evidence: `docker-compose.yml` — prometheus service config; `go.mod` — `prometheus/client_golang v1.19.0`.

---

### Q35. How does health checking work across services?

**Short answer:** Each service exposes a `/health` HTTP endpoint. Docker Compose polls it every 5 seconds with a 2-second timeout and 5–10 retries before considering a service healthy.

- The `api` service waits for all three cache nodes AND postgres to pass health checks before starting — `depends_on` with `condition: service_healthy`.
- The proxy waits for the API. Startup order is fully deterministic.
- Cache node health: `{"healthy":true,"node_id":"node1","is_coordinator":false}`.
- The `NodeHealth` probe timeout is 500ms (`healthProbeTimeout` constant).

Evidence: `docker-compose.yml` — healthcheck config; `internal/cluster/node.go` — `healthProbeTimeout = 500ms`; `cmd/cachenode/main.go` — `/health` handler.

---

### Q36. What is the /cluster/status endpoint?

**Short answer:** A single call that aggregates health from all cache nodes and returns which one is the current Raft coordinator.

- The API's `DebugHandler.ClusterStatus` iterates over all registered node IDs from the ring, calls each node's `/health` endpoint (with a 500ms per-node timeout), parses the response, and combines everything into one `ClusterStatusResponse`.
- Returns: list of `NodeStatus` (healthy, is_coordinator, hit/miss/eviction counts, entry count) and the current `coordinator` node ID.

Evidence: `internal/api/debug.go` — `ClusterStatus` and `fetchNodeHealth`.


---

## 12. Docker & Deployment

### Q37. How does the multi-stage Dockerfile work?

**Short answer:** Two stages — a `golang:1.22-alpine` builder compiles all four binaries, then a minimal `alpine:3.19` image copies only the compiled binaries.

- Build stage caches the `go mod download` layer separately from the source copy, so dependency downloads only happen when `go.mod` or `go.sum` changes.
- `CGO_ENABLED=0 GOOS=linux` produces fully static binaries that run in Alpine without a C runtime.
- Final image: Alpine + wget (for health check probes) + four binaries (`cachenode`, `api`, `proxy`, `benchmark`). No Go toolchain in production.
- All four services use the same Docker image — the `command` field in `docker-compose.yml` selects which binary to run.

Evidence: `Dockerfile` — build and final stages; `docker-compose.yml` — `command:` overrides.

---

### Q38. How is configuration injected at runtime?

**Short answer:** Environment variables only — no config files, no command-line flags for most settings.

- `shared.Load()` reads from `os.Getenv` with sensible defaults. Validated at load time (eviction policy must be one of four values, capacity must be in [1, 1,000,000]).
- Docker Compose injects per-service config via the `environment:` block.
- Cache node-specific settings (node ID, peers, ports) are passed as command-line flags to `cachenode` because they vary per-instance and can't be expressed as environment variables without extra naming complexity.
- `DB_DSN` is required — the API fails fast with a fatal log if it's missing.

Evidence: `internal/shared/config.go` — `Load()`; `docker-compose.yml` — `environment:` blocks; `cmd/cachenode/main.go` — `flag.Parse()`.

---

### Q39. Why does PostgreSQL use port 5433 externally instead of 5432?

**Short answer:** To avoid a port conflict if the developer already has a local PostgreSQL instance running on 5432.

- Inside the Docker network, services connect to `postgres:5432` (the standard port).
- From the host machine, you connect on 5433 to avoid clashing with a local Postgres.
- DB_DSN in Docker Compose uses the internal address: `postgres://dcg:dcg_secret@postgres:5432/products`.

Evidence: `docker-compose.yml` — postgres service `ports: "5433:5432"`.


---

## 13. Testing Strategy

### Q40. What tests exist and what do they cover?

**Short answer:** Four test suites covering the cache, cluster/ring/coordinator, eviction policies, and invalidation strategies.

- `internal/cache/cache_test.go`: TTL expiry, zero TTL, negative TTL, max TTL, upserts, capacity enforcement, delete, and a concurrent-access test with 50 goroutines.
- `internal/cluster/cluster_test.go`: ring determinism, empty ring, single-node ring, minimal remapping on node removal, key distribution across 3 nodes, coordinator unavailable-node handling, no-leader error, healthy routing.
- `internal/eviction/eviction_test.go`: all four policies — evict order, access-moves-to-front (LRU), tie-breaking (LFU), TTL ordering (TTL-only), random stays in key set, empty evict returns false.
- `internal/eviction/compliance_test.go`: compile-time interface assertions that all four policy types implement `shared.EvictionPolicy`.
- `internal/invalidation/invalidation_test.go`: (file exists — strategy behaviour tests).

CI runs `go test -race ./...` on every push.

Evidence: `internal/cache/cache_test.go`, `internal/cluster/cluster_test.go`, `internal/eviction/eviction_test.go`, `internal/eviction/compliance_test.go`; `.github/workflows/ci.yml`.

---

### Q41. What is the compile-time interface assertion pattern?

**Short answer:** `var _ shared.EvictionPolicy = (*LRU)(nil)` — assigning a nil pointer of each type to the interface causes a compile error if the type doesn't satisfy the interface.

- This catches missing methods at compile time, not at runtime.
- The blank identifier `_` discards the value — it exists only for the compiler's type check.
- This is idiomatic Go; you'll find it in the standard library and many popular packages.

Evidence: `internal/eviction/compliance_test.go` — all four policy assertions.

---

### Q42. What is the benchmark and how does it work?

**Short answer:** A standalone binary (`cmd/benchmark`) that runs the same synthetic workload against all four eviction policies and all three invalidation strategies, then prints a formatted comparison table.

- Eviction benchmark config: capacity=100, 10,000 ops, 80% reads, keyspace=500 (5× capacity to force evictions), Zipf exponent=1.0 (realistic skew).
- The Zipf distribution mimics real traffic: a small number of "hot" keys get accessed frequently, most keys are rarely touched.
- Workload is pre-generated once with a fixed random seed (42) so all four policies see the exact same sequence of operations — fair comparison.
- Latency stats: mean and P99 in milliseconds, computed using an insertion sort (sufficient for benchmark sizes).
- Invalidation benchmark: 5,000 ops, 20% writes, keyspace=200.

Evidence: `internal/benchmark/eviction.go` — `DefaultEvictionConfig()`, `generateWorkload` with seed 42; `internal/benchmark/invalidation.go` — `DefaultInvalidationConfig()`.


---

## 14. Language & Ecosystem Choices

### Q43. Why Go for this project?

**Short answer:** Go's goroutines, channels, and built-in race detector make it a natural fit for concurrent distributed systems work.

- The Raft election loop runs as a goroutine. Heartbeats are sent to all peers in parallel goroutines. The write-behind strategy fires a goroutine per update. All of this is expressed cleanly in Go without callback hell.
- The `sync.RWMutex` pattern for the cache and `atomic.Int64` for metrics are stdlib — no extra dependencies.
- Static binary compilation (`CGO_ENABLED=0`) produces a Docker image with no runtime dependencies.
- Trade-off: Go's garbage collector can cause latency spikes under heavy allocation (e.g. many cache misses creating lots of `[]byte` values). For a learning project the GC pause is negligible.

Evidence: `Dockerfile` — `CGO_ENABLED=0`; `go.mod` — `go 1.22`.

---

### Q44. Why Go 1.22 specifically?

**Short answer:** Go 1.22 introduced native HTTP pattern matching with path parameters (`{id}` in route patterns), which the API uses directly.

- `mux.HandleFunc("GET /products/{id}", h.GetProduct)` and `r.PathValue("id")` are 1.22 features. Before 1.22 you needed a third-party router (gorilla/mux, chi, etc.) for path parameters.
- This means zero routing dependencies — just stdlib `net/http`.

Evidence: `go.mod` — `go 1.22`; `internal/api/server.go` — route patterns; `internal/api/handler.go` — `r.PathValue("id")`.

---

### Q45. What third-party dependencies does this project use and why?

**Short answer:** Three — pgx for Postgres, prometheus client for metrics, gRPC for inter-node communication. No web framework, no ORM, no dependency injection.

- `github.com/jackc/pgx/v5 v5.5.5`: native Postgres driver with connection pooling. stdlib `database/sql` would work but pgx is faster and has better Postgres type support.
- `github.com/prometheus/client_golang v1.19.0`: the official Go Prometheus client. Registering counters and gauges is a few lines of code; building it from scratch would be many.
- `google.golang.org/grpc v1.63.2`: gRPC for cache node and Raft RPCs. The alternative (HTTP/JSON) would be slower and lose the type safety of protobuf.
- Everything else (HTTP server, JSON encoding, sync primitives, testing) is stdlib.

Evidence: `go.mod` — direct dependencies.


---

## 15. Trade-off Summaries

### Q46. What are the biggest trade-offs in this system?

Here's a concise reference for any "what would you change in production?" question:

| Decision | What it buys | What it costs | Upgrade path |
|---|---|---|---|
| Raft for election only | Simple implementation | Cache miss on node failure | Add write replication |
| Lazy TTL expiry | No background goroutine | Stale entries linger in memory | Add a periodic sweep goroutine |
| No read replication | Simple routing, no sync overhead | All reads for a key hit one node | Replicate reads to replicas |
| Offset pagination | Simple SQL | Page drift on concurrent writes | Switch to keyset/cursor pagination |
| Inline schema migration | No migration tool dependency | No rollback, schema drift risk | Adopt golang-migrate |
| Insecure gRPC | Simpler local setup | Not suitable for production | Add TLS credentials |
| In-memory state dir (`/tmp/raft`) | Simple Docker setup | Raft state lost on container restart | Mount a persistent volume |
| Write-behind deletes (not sets) | Correctness under concurrent reads | Extra cache miss on next read | Accept the trade-off |
| FNV-1a for ring hashing | Fast, deterministic | Vulnerable to adversarial inputs | Switch to SipHash for public APIs |

---

### Q47. If you were taking this to production, what would you change first?

**Short answer:** Three things in priority order.

1. **TLS on gRPC connections.** Right now `grpc.WithTransportCredentials(insecure.NewCredentials())` is used. In production, any node on the internal network could intercept cache data.
2. **Persistent Raft state directory.** `/tmp/raft` is ephemeral. A container restart wipes the node's vote history — it could vote twice in the same term. Mount a volume.
3. **Cache read replicas or write replication.** A single cache node going down causes misses for all its keys. For a high-traffic catalog, those misses hit the DB hard. Either replicate writes across nodes or add a replica that can serve reads.

Evidence: `internal/cluster/transport.go` — `insecure.NewCredentials()`; `docker-compose.yml` — `--state-dir=/tmp/raft`; ADR 0001.

---

### Q48. How would you scale this beyond 3 nodes?

**Short answer:** Add the new node to the ring via `ring.Add`, update peer lists for Raft, and let consistent hashing redistribute only the affected key arcs.

- Adding a 4th node remaps approximately 1/4 of keys (the arc from the new node's tokens to the next node clockwise). All other keys stay put.
- The Raft cluster needs an odd number of nodes (3, 5, 7) to avoid split-brain. Going from 3 to 5 is the natural next step.
- Current limitation: the ring is built at startup from config. A production system would need a gossip protocol or a service registry (Consul, etcd) to discover new nodes dynamically.

Evidence: `internal/cluster/ring.go` — `Add/Remove` methods; `cmd/cachenode/main.go` — peer list parsed from flags at startup.

---

*Evidence for all answers is in the codebase at:*
`/Users/shubhkapadia/Desktop/Development/Web-Apps/DistributedCaching`
