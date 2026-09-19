# Cover-letter examples

> These fictional cases test selection and judgment. Acceptable letters must contain exactly two paragraphs and no more than 200 words. Rejected samples intentionally demonstrate failures.

## CL-01: Backend job processing and reliability

### Input

- Company: QueueWorks, fictional
- Role: Backend Software Engineer
- JD: Node.js APIs, background browser jobs, PostgreSQL, operational reliability, and customer-visible failure handling

### Expected decision

Build one argument around reliable asynchronous work. Connect the SEO audit prototype's job isolation to Digital Aid Seattle's reconciliation and observability work.

### Allowed evidence

- Express accepts audit work while Redis-backed BullMQ workers run Playwright outside the request path.
- Digital Aid Seattle uses Node.js, PostgreSQL, webhooks, mismatch review, and Azure Monitor in production workflows.

### Acceptable letter

```text
QueueWorks is hiring a backend engineer to keep long-running customer jobs reliable without tying up request handling. I worked through that same design problem in an SEO audit prototype: an Express API accepted work while Redis-backed BullMQ workers ran Playwright crawls outside the request path, so one slow site could not block the rest of a batch.

At Digital Aid Seattle, I also built Node.js and PostgreSQL payment reconciliation with webhook-driven updates, human review for mismatches, and Azure Monitor tracing across production workflows. That combination taught me to treat job execution, data correctness, and failure visibility as parts of the same backend system. Those are the practical services I want to keep building. I would welcome a conversation about how that experience could support QueueWorks as it makes background processing more dependable for customers.
```

Words: 134/200. Paragraphs: 2.

### Reject

Do not add unrelated AI projects, every backend technology, or an audit benchmark that needs project context.

### Acceptance

- One central reliability argument.
- One project and one work experience reinforce each other.
- The closing points back to QueueWorks' stated responsibility.

## CL-02: broad Full Stack ownership

### Input

- Company: MemberFlow, fictional
- JD: React member portal, TypeScript APIs, PostgreSQL, payment status, and production support

### Expected decision

Use Digital Aid Seattle as one end-to-end evidence unit. The argument is shared data and workflow ownership across the UI, API, database, and production operations.

### Allowed evidence

React, TypeScript, Node.js, PostgreSQL, shared interfaces, member status, payment reconciliation, and production observability from Digital Aid Seattle.

### Reject

Do not split the letter into a frontend paragraph, backend paragraph, and project list. Do not add the 400-member metric unless the sentence explains why that scale matters.

### Acceptance

- The user workflow connects frontend and backend evidence.
- No technology inventory.
- Exactly two paragraphs and no more than 200 words.

## CL-03: vague AI language with concrete evaluation work

### Input

- Company: PolicyLens, fictional
- JD: Repeatedly says `AI-first`; concrete work is retrieval, evaluation datasets, cited findings, and deployment checks.

### Expected decision

Ignore marketing adjectives. Build the argument around grounded compliance findings and measurable evaluation.

### Allowed evidence

The YouTube Ads Compliance Pipeline uses LangGraph, RAG, Azure AI Search, cited policy sources, a golden evaluation dataset, and recorded holdout results. Preserve prototype framing.

### Reject

Do not claim broad AI expertise, production customers, or passion for `transforming the AI landscape`.

### Acceptance

- Evaluation and traceability carry the letter.
- Prototype status remains clear.
- Company claims come from the fictional JD.

## CL-04: mixed role

### Input

- Company: SupportStack, fictional
- JD: Mostly React and TypeScript product work, with Node APIs and one AI summarization feature.

### Expected decision

Classify the role as mixed with Full Stack primary. Use an end-to-end product workflow as the main argument and mention AI only if it supports the same user problem.

### Allowed evidence

Digital Aid Seattle full-stack work plus, at most, one adjacent AI pipeline decision.

### Reject

Do not devote equal space to Full Stack, Backend, and AI lanes. Do not mention three projects.

### Acceptance

- One dominant lane and argument.
- Secondary evidence strengthens rather than changes the argument.
- The reader can state the candidate's fit in one sentence.

## CL-05: ordinary company

### Input

- Company: FleetCore, fictional
- JD: Internal maintenance scheduling and data-quality workflows

### Expected decision

Open on the operational workflow. Do not invent emotional attachment to fleet maintenance or praise the company as visionary.

### Allowed evidence

Transfer-credit data validation, payment reconciliation, or another verified workflow where data accuracy affects human review.

### Rejected generic opening

```text
I am thrilled to apply to FleetCore, an innovative industry leader whose mission deeply resonates with me. Your commitment to excellence, collaboration, and customer success makes this an exciting opportunity to contribute my diverse technical background.
```

This could be sent to almost any company and invents motivation.

### Acceptance

- Specific to the work even when the company is not personally inspiring.
- Confidence comes from evidence.
- No unsupported praise.

## CL-06: thin company context

### Input

- Company: Acme, fictional
- JD: Identifies a Backend Engineer role and responsibilities but gives no product, customers, or mission.

### Expected decision

Focus on the stated backend work. Do not fabricate a company problem, customer group, growth stage, or culture.

### Allowed evidence

Whichever verified backend experience best matches the responsibilities.

### Reject

Do not claim that Acme is changing an industry or solving a meaningful customer problem the JD never states.

### Acceptance

- Role-specific rather than falsely company-specific.
- The opening still identifies concrete work.
- No automatic browsing.

## CL-07: missing technology

### Input

- Company: SystemsLab, fictional
- JD: Rust preferred; distributed systems and service reliability are core responsibilities.

### Expected decision

Do not claim Rust. Build the letter around verified distributed-systems decisions in Go and acknowledge language transfer only if needed.

### Allowed evidence

Go, gRPC, Raft-based coordination, caching, durable PostgreSQL fallback, and observability from the distributed-caching prototype.

### Reject

Do not say `experienced in Rust`, add Rust to a technology list, or spend half the letter apologizing for the gap.

### Acceptance

- Evidence matches the underlying work.
- The missing tool remains missing.
- The central argument is contribution, not deficiency.

## CL-08: context-poor metric

### Input

- Company: ComputeGrid, fictional
- JD: Infrastructure observability and failure diagnosis

### Expected decision

Describe the ClusterOps prototype's telemetry, alerting, and structured failure-analysis capability. Omit service counts and estimated timing unless the sentence makes their value legible.

### Allowed evidence

Only facts and estimates permitted by the ClusterOps master, with prototype and estimate framing preserved.

### Reject

Do not present `11 services`, a telemetry count, or an estimated diagnostic time as impressive by itself.

### Acceptance

- Capability before number.
- No production-scale implication.
- The evidence supports the JD's observable problem.

## CL-09: early-career boundaries

### Input

- Company: ScaleBase, fictional
- JD: Uses senior-sounding ownership language but accepts early-career applicants.

### Expected decision

Use confident individual-contributor evidence without claiming leadership, mentorship, broad architecture ownership, or production scale beyond the facts.

### Allowed evidence

Shubh's verified implementation decisions, collaboration, deployed Digital Aid Seattle work, and clearly labeled prototypes.

### Reject

Do not convert `paired with a senior engineer` into leadership or claim that Shubh led teams.

### Acceptance

- Confidence and maturity boundaries coexist.
- Personal contribution is clear.
- No inflated title or ownership.

## CL-10: resume-summary failure

### Input

- Company: BuildCloud, fictional
- JD: Broad Backend role with APIs, queues, databases, cloud, and AI-adjacent work

### Expected decision

Choose the most important responsibility and one coherent work/project pair.

### Allowed evidence

Any verified pair that supports one argument.

### Rejected resume summary

```text
I have experience with React, TypeScript, Node.js, Express, PostgreSQL, AWS, Azure, Redis, BullMQ, Playwright, Docker, Go, gRPC, Raft, LangGraph, RAG, and PyTorch. At eInfochips I built APIs, at Digital Aid Seattle I built membership workflows, and at ASU I worked with Python and SQL.

I also built Hearloop, an SEO Audit Engine, a compliance pipeline, a distributed cache, ClusterOps, and a fake-review detector. This diverse background makes me a strong fit for BuildCloud, and I look forward to discussing the opportunity.
```

The letter lists evidence instead of making an argument and gives no reason those facts matter to BuildCloud.

### Acceptance

- One central argument.
- At most one work experience and one project by default.
- Tools appear only where they explain a decision.
