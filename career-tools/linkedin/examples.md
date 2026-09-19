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

## LI-09: engineer overlap — regression case from a real session

> Unlike LI-01 through LI-08, this case records what the agent actually shipped in a live session and the corrections the user made. Its purpose is to make three recurring failure modes deterministic to catch, not to test a new angle.

### Input

- Name: Saketh Babu Palla
- Job title: Senior Software Engineer
- Company: SLB
- About: 10+ years on distributed, production-critical systems; leads architecture and mentoring.
- Experience: At SLB, led end-to-end data workflows integrating ML and computer-vision models into production robotic-inspection pipelines; partnered with data scientists to productionize models; built state-managed frontend components; mentored an intern.

### Chosen angle

Lead with the observation that the hard part of his work is wiring a model into a live inspection pipeline, not the model itself. Connect Shubh's adjacent async ML pipeline with human review, then ask one question about where productionization friction shows up.

### Evidence allowed

Adjacent only: Shubh's own async ML pipeline with a human-review path (side project). No metrics. No project name. MS CS stated in past tense.

### Failure 1 — timeline contradicted stored facts

First draft said `about to finish my MS CS`. The candidate profile records `MS CS, ASU, May 2026` and the resume says `Graduated 2026`; the session date is September 2026, so the MS is already finished. The agent initially implied the fact file was stale.

Recommended fix: the fact was correct; the draft was wrong. MS graduation is past tense (`after my MS CS`). Do not blame the fact file for a drafting error. Confirm claim maturity and timeline against `resume-system/facts/` before drafting.

### Failure 2 — generic praise opener

Second draft opened with `your work ... caught my eye`. This is the same failure as LI-01's `Impressed by your journey`: a reusable praise opener with no observation, portable to anyone with a similar profile. It trips reject-pass criteria 5 (name-swappable) and 7 (generic praise / AI-sounding filler).

Root cause the user identified: the agent read the standards but never ran the final rejection pass on its own draft before returning it. Reading the rules is not the same as scoring the draft against them.

Recommended fix: open with a specific observation about the recipient's work, never a praise opener. `your work caught my eye` is a rejected opener, alongside `impressed by your journey`.

### Failure 3 — fabricated character count

The agent reported exact counts (`299/300`) it never computed, twice. A user-verified count showed one draft was actually 314 characters, over the limit.

Root cause: the agent estimated the count and asserted a precise number instead of counting. A model cannot reliably eyeball character counts.

Recommended fix: count the exact copy block with a tool (`printf '%s' "<copy>" | wc -m`) before returning any length-capped note. Never assert a character count that was not computed.

### Failure 4 — junior diagnosing a senior's work

An earlier "acceptable" draft opened `the hard part of your SLB work sounds less like the CV model and more like wiring it into a live inspection pipeline`. That is a confident diagnosis of a 10-year senior engineer's job that only a production-ML peer could credibly make. From an early-career candidate it reads as presumptuous, and the recipient can tell the insight is borrowed.

Root cause: the note asserted shared senior-level insight Shubh does not have, instead of asking the senior engineer to supply it. Shubh is an early-career candidate; he cannot credibly interpret what an experienced engineer's hardest problem is from an About or Experience section.

Recommended fix — stance rule: when the recipient is clearly more senior, the note stays at the level of what the profile literally states and asks the recipient to explain their experience. It must not tell the recipient what their work is like, what the hard part is, or what tradeoff mattered. Position Shubh honestly as early-career so the question reads as sincere curiosity, not a peer challenge.

### Acceptable direction

```text
Hi Saketh, I saw you productionize CV models into robotic inspection pipelines with data scientists at SLB. I'm early in my career and have only built small ML pipelines with human review after my MS CS. When a model moves from the data science side into a live pipeline, what tends to break first?
```

Characters: 298/300 (verified with `wc -m`). Questions: 1.

### Acceptance

- Opener restates only what the profile literally says he does; no diagnosis of his work.
- Positions Shubh honestly as early-career and the overlap as small/adjacent.
- MS CS is past tense and consistent with the fact files.
- The one question asks the senior engineer to explain his own experience, answerable in a sentence.
- Character count is computed with a tool before returning, and is at or under 300.

## LI-10: batch of five SLB recipients — voice, recited facts, and reply-rate research

> Second regression case from a real session. Records failures the user caught across a five-recipient batch, plus corrections backed by outreach research. Purpose: make the observation side of a note deterministic, not just the claims about Shubh.

### Input

Five SLB-connected recipients supplied at once:

- Altay Sansal — Principal AI Engineer, decade-plus, seismic/energy ML, open-source MDIO project (senior).
- Aishwarya Vidiyala — Full Stack SWE and CS grad student; productionized an ML model for log anomaly detection (near-peer).
- Ross Winningham — Talent Acquisition Lead, Technology (recruiter).
- Elise Reynolds — Engineering Recruiter, Data Center; recruits mechanical and electrical engineers (field mismatch).
- Priscila Campos — HR Manager, Kansas and Brazil; no stated tech-recruiting scope (sparse, non-technical).

### Failure 5 — referencing profile facts Shubh cannot speak to

First drafts name-dropped specifics lifted straight from the profiles: Altay's "open-source MDIO project," "seismic foundation models," and Aishwarya's "ONNX Runtime" and "Sentence Transformers." Shubh has never used these and could not hold a two-sentence conversation about them. The user flagged that this does not sound like him and only appeared because the terms were in the About section.

Root cause: the agent stacked profile jargon to look researched, instead of saying only what Shubh could genuinely say and defend. A named project, paper, or tool Shubh has not used is not personalization; it collapses the moment the recipient replies.

Recommended fix — voice rule: reference the recipient's work only at a level Shubh actually understands (for example "machine learning for energy and seismic data" instead of a named model or repo). If Shubh could not discuss a detail unprompted, cut it. This is the "would Shubh struggle to defend this sentence?" check applied to the observation, not just the claims about himself.

### Failure 6 — reciting a fact the recipient already knows

The Priscila draft opened `I saw your HR work at SLB across the Kansas and Brazil offices`. That recites her own job history back to her and adds nothing; she knows where she has worked better than Shubh does.

Root cause: a copied profile fact used as filler personalization. It could be dropped without weakening the note, which means it should be.

Recommended fix: do not open by stating a profile fact the recipient obviously knows unless it directly sets up the observation or question. Contrast: Ross's "you lead technical recruiting at SLB" and Elise's "you recruit ... mechanical and electrical" earn their place because each sets up a question that only makes sense given that scope. Priscila's location recitation set up nothing, so it was cut and the note led with the ask.

### Research check (outreach studies, several Reddit-sourced)

Confirmed the session's earlier fixes and added one new lever. Paraphrased for compliance:

- A note barely changes acceptance rate but roughly doubles reply rate once accepted, so the note exists to earn the conversation, not the accept. The playbook's reply-first goal is correct.
- Template-style praise openers ("came across your profile and was impressed") measurably lower responses, confirming the LI-01 and LI-09 praise-opener rejects.
- Reddit-sourced advice favors casual, specific, low-pressure notes that barely feel like job seeking, over polished pitches. Lead with the recipient, keep it short, use a low-friction ask.
- Shared background (alumni tie, same grad-student status, mutual group) is a strong, underused accept lever. Use it when real; never invent it.

Sources: recruiterflow.com, expandi.io, hyperclapper.com, salesrobot.co, linkedhelper.com (Reddit-thread analysis), and a Reddit post summarized by economictimes.indiatimes.com.

### Acceptable direction

```text
Hi Altay, I saw you've spent years working on machine learning for energy and seismic data at SLB. I'm an early-career engineer who just finished my MS and I'm trying to grow into applied ML. If you had any advice for someone at that starting point, I'd really value it.
```

```text
Hi Priscila, I'm an early-career software engineer hoping to join SLB after finishing my MS in CS. Since you're in HR there, I wanted to ask if you know who handles recruiting for early-career software roles?
```

Altay 270/300, Priscila 208/300 (both verified with a tool). Questions: 1 each.

### Acceptance

- References the recipient's area only at a level Shubh can discuss and defend; no borrowed project names, papers, or tools.
- No recited profile fact that fails to set up the observation or question.
- Casual and low-pressure; the ask is a small question, not a pitch, referral, or meeting request on first contact.
- Shared background used only when genuine (Aishwarya: both recent CS grads); never invented.
- Weak-fit contacts (Elise field mismatch, Priscila no tech scope) handled honestly rather than with manufactured fit.
- Character count computed with a tool before returning, at or under 300.
