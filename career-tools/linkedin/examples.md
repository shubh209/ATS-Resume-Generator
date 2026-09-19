# LinkedIn connection-note examples

> These fictional cases test decisions, not exact wording. A generated note may differ and still pass if it satisfies the decision and acceptance criteria.

## LI-01: detailed recruiter

### Input

- Name: Maya Patel
- Job title: Senior Technical Recruiter
- Company: AtlasPay
- About: Recruits backend engineers for API, risk, and payments-platform teams.
- Experience: Three years hiring engineers for platform teams.

### Chosen angle

Ask what distinguishes early-career backend candidates for the teams she actually recruits.

### Evidence allowed

Shubh has verified Node.js, PostgreSQL, payment-workflow, and API experience. The note does not need a record-count metric.

### Reject

```text
Impressed by your journey at AtlasPay.
I built APIs that handled 10,000+ records. Would love to connect.
```

This uses generic praise, drops an unexplained number, and asks only for acceptance.

### Acceptable direction

```text
You recruit API and payments engineers at AtlasPay.
I've built Node/Postgres payment workflows. For early-career backend hires, what usually separates a strong profile from an average one?
```

Characters: 188/300. Questions: 1.

### Acceptance

- Uses her stated recruiting scope.
- Gives one credible reason for the question.
- Invites a short reply.
- Avoids a direct application review or referral ask.

## LI-02: sparse recruiter

### Input

- Name: Chris Lee
- Job title: Technical Recruiter
- Company: Northstar
- About: unavailable
- Experience: Recruits backend and frontend software engineers.

### Chosen angle

Use the only meaningful scope detail and ask which kind of early-career ownership the company currently needs.

### Evidence allowed

MS CS at ASU plus verified Full Stack and Backend experience. No project or metric is necessary.

### Reject

Do not invent a team, open role, or hiring priority that the profile does not state.

### Acceptable direction

```text
You recruit backend and frontend engineers at Northstar.
I'm finishing my MS at ASU with experience on both sides. Are early-career roles there leaning toward backend ownership or full-stack breadth?
```

Characters: 199/300. Questions: 1.

### Acceptance

- Stays within the limited profile evidence.
- Makes the question easy to answer.
- Does not pretend Northstar has a specific opening.

## LI-03: close engineer overlap

### Input

- Name: Daniel Kim
- Job title: Senior Platform Engineer
- Company: CrawlWorks
- About: Builds reliable crawling infrastructure.
- Experience: Mentions Redis queues and browser-worker isolation.

### Chosen angle

Connect his browser-worker work to Shubh's verified async audit workflow, then ask about one engineering tradeoff.

### Evidence allowed

The SEO audit prototype keeps Playwright crawls off the request path with Redis-backed background work.

### Reject

Do not lead with the project name, warm-audit timing, or a stack list. They consume space without improving the question.

### Acceptable direction

```text
You've worked on Redis queues and browser workers at CrawlWorks.
I built a similar async audit flow to keep browser jobs off the request path. Which tradeoff mattered most as the workload grew?
```

Characters: 193/300. Questions: 1.

### Acceptance

- The overlap is meaningful and verified.
- The capability is understandable without knowing the project.
- The question draws on Daniel's experience.

## LI-04: adjacent engineer overlap

### Input

- Name: Priya Shah
- Job title: Senior ML Platform Engineer
- Company: ModelDock
- About: Owns training infrastructure reliability.
- Experience: Moved from application engineering into ML platform and observability work.

### Chosen angle

Lead with the career transition. Describe Shubh's cluster-observability work as adjacent rather than equivalent production experience.

### Evidence allowed

ClusterOps is a prototype for simulated GPU telemetry, failure analysis, and observability. Its estimates are not needed.

### Reject

Do not claim Shubh has operated production ML infrastructure. Do not use an estimated telemetry count or service count as proof of scale.

### Acceptance

- Uses `adjacent` or avoids an equivalence claim entirely.
- Focuses on Priya's transition or judgment.
- Contains one answerable question.

## LI-05: career transition without a project

### Input

- Name: Luis Romero
- Job title: Staff Platform Engineer
- Company: Acme
- About: unavailable
- Experience: Frontend Engineer, then Backend Engineer, then Platform Engineer.

### Chosen angle

The transition itself is enough. Do not force a project into the note.

### Evidence allowed

Shubh is finishing an MS in CS and moving toward backend-heavy work.

### Reject

Do not invent details about Luis's platform team or ask a broad question such as `Any advice?`

### Acceptable direction

```text
Your path from frontend to backend and then platform work stood out.
I'm making a similar shift while finishing my MS at ASU. What helped you build credibility for that first platform role?
```

Characters: 189/300. Questions: 1.

### Acceptance

- The recipient's path carries the note.
- No project or metric is forced in.
- The question is specific enough for a short reply.

## LI-06: founder with adjacent product work

### Input

- Name: Erin Brooks
- Job title: Founder
- Company: MedVoice
- About: Builds voice workflows for pharmacy operations.
- Experience: Product and operations background; no public engineering-role details.

### Chosen angle

Use adjacent voice and AI pipeline building blocks, acknowledge the different use case, and ask about the engineering problem behind the product.

### Evidence allowed

Hearloop is a multi-tenant voice-feedback prototype with an async transcription and classification pipeline.

### Reject

Do not say Shubh solved the same pharmacy-automation problem. Do not ask for a call or roles before earning a reply.

### Acceptable direction

```text
You're building voice workflows for pharmacy operations at MedVoice.
I've built adjacent voice and AI pipelines for a different use case. Which engineering problem has been harder than it first looked?
```

Characters: 201/300. Questions: 1.

### Acceptance

- States the overlap honestly.
- Avoids flattery and a meeting request.
- Gives Erin a concrete, low-pressure way to reply.

## LI-07: context-poor metric

### Input

- Name: Jordan Wells
- Job title: Infrastructure Recruiter
- Company: ComputeGrid
- About: Hires engineers for compute infrastructure.
- Experience: No technical benchmark or team-scale detail.

### Chosen angle

If candidate evidence is useful, describe the observable capability of tracing simulated cluster failures. Omit ClusterOps estimates and service counts.

### Evidence allowed

ClusterOps models telemetry, alerting, and structured failure analysis in a prototype.

### Reject

```text
I built ClusterOps, an 11-service AI platform stack.
Would love to connect.
```

The recipient cannot judge whether 11 services is good, and the note provides no reason to reply.

### Acceptance

- No service count, telemetry count, or unsupported throughput claim.
- The note connects to Jordan's recruiting scope or asks a specific hiring question.
- The capability is described before any project name.

## LI-08: unsafe personalization

### Input

- Name: Sam Chen
- Job title: Senior Software Engineer
- Company: Acme
- About: unavailable
- Experience: Only the current title and company are visible.

### Chosen angle

No safe personalized angle exists.

### Evidence allowed

None until the user supplies one more profile detail, visible technical focus, post, team, or career-history item.

### Reject

Do not generate a generic note about being impressed by Acme or insert a random Shubh project.

### Required clarification

```text
Sam's profile only gives me a title and company, so I can't create an honest reply-worthy hook yet. Can you share one Experience bullet, About detail, recent post, or visible technical focus?
```

### Acceptance

- Asks one focused question.
- Explains why the detail is needed.
- Does not draft around the missing information.
