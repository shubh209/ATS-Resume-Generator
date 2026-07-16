# 3-Week Interview Technical Preparation Roadmap

**Goal:** In 3 weeks, be able to explain each major project in 30 seconds, 2 minutes, and 5 minutes, then answer technical follow-ups without blanking.

**Daily time commitment:** 90 minutes per day  
**Total time:** 31.5 hours over 21 days  
**Main focus:** Project clarity, technical depth, spoken delivery, and pressure practice

---

## Daily structure: 90 minutes

Use this structure every day.

### 1. Understand: 20 minutes
Read your project notes or ask an AI agent to explain one area:
- Architecture
- End-to-end workflow
- Tech stack
- Tradeoffs
- Failure modes
- Metrics
- What you personally built

### 2. Build your spoken version: 25 minutes
Turn the understanding into interview-ready bullets.

Do not write polished paragraphs first. Use cue bullets:
- Project
- Problem
- Flow
- Tradeoff
- Result
- Company tie-in

### 3. Speak out loud: 25 minutes
Record yourself answering 3 to 5 questions.

After recording:
- Listen once.
- Fix only the confusing parts.
- Do not restart ten times trying to make it perfect.

### 4. Follow-up drill: 20 minutes
Practice follow-up questions:
- Why this technology?
- What broke?
- How would you scale it?
- What would you improve?
- What was your role?
- What tradeoff did you make?

---

# Week 1: Fix project clarity

**Goal:** Stop blanking on basic questions like "What does this project do?" and "Walk me through it."

---

## Day 1: Hearloop product story

### Focus
Understand what Hearloop does in plain English.

### You should be able to answer
- What is Hearloop?
- Who is it for?
- What problem does it solve?
- What happens when a user records feedback?
- Why is this an AI project, not just a CRUD app?

### Agent prompt

```text
I built Hearloop. Help me understand and explain this project for interviews.
Focus only on the product story: what it does, who uses it, the problem, the user journey, and why it matters.
Do not give me a long essay. Give me a 30-second version, a 2-minute version, and 10 likely interviewer follow-up questions.
Use simple spoken English.
```

### Output to create
- Hearloop 30-second explanation
- Hearloop 2-minute walkthrough

### Practice question
> Walk me through Hearloop.

---

## Day 2: Hearloop architecture

### Focus
Understand the technical flow from voice recording to dashboard result.

### Know this flow
- Widget or hosted page captures voice.
- Audio uploads to S3.
- API finalizes the session.
- BullMQ runs async jobs.
- Groq Whisper transcribes.
- AWS Bedrock classifies.
- PostgreSQL stores results.
- Dashboard shows insights.

### Agent prompt

```text
Explain Hearloop's architecture like I am preparing for a technical interview.
Cover the end-to-end flow from voice recording to dashboard result.
Explain each service, database, queue, and AI model.
Then give me a clean spoken walkthrough with no jargon overload.
Finally, ask me 10 technical follow-up questions.
```

### Practice question
> Walk me through Hearloop's architecture.

---

## Day 3: Hearloop tradeoffs and metrics

### Focus
Understand why you made technical decisions.

### Know these cold
- Why async processing?
- Why BullMQ?
- Why Groq Whisper?
- Why AWS Bedrock Nova Lite with fallback?
- Why signed S3 upload?
- Why PostgreSQL and Redis?
- What did you measure?

### Important numbers
- p95 latency: 149 ms at 200 concurrent users.
- Bedrock classification cost: around $0.00003 per session.
- Manual deploy time improved from around 15 minutes to around 60 seconds.
- AWS cost reduced from $35 to $9.60.

### Practice questions
- Why did you choose this architecture?
- What was the hardest technical part?
- How did you control AI cost?
- How did you test reliability?

---

## Day 4: YouTube Compliance Pipeline product story

### Focus
Be able to explain the project you struggled with in the interview.

### Simple explanation to master
> Paste a YouTube ad link, the system pulls metadata and captions, retrieves relevant YouTube and FTC policy chunks, asks GPT-4o to audit against those chunks, then returns a cited PASS or FAIL report with human review.

### Agent prompt

```text
Help me deeply understand my YouTube Ads Compliance Pipeline for interviews.
Start with the product story in plain English.
Then explain why this is useful for marketing or compliance teams.
Give me a 30-second version, 2-minute version, and 5-minute version.
Avoid buzzwords unless you explain them simply.
```

### Practice question
> Walk me through your YouTube policy project.

---

## Day 5: YouTube Compliance Pipeline architecture

### Focus
Understand the system flow.

### Know this flow
- User submits YouTube URL.
- FastAPI receives request.
- YouTube Data API pulls metadata.
- Captions are pulled through timedtext or yt-dlp.
- Azure AI Search retrieves policy chunks.
- GPT-4o audits with temperature 0.
- PostgreSQL stores audit result.
- Human reviewer can override.

### Agent prompt

```text
Explain the architecture of my YouTube Ads Compliance Pipeline.
Cover FastAPI, LangGraph, YouTube Data API, captions, Azure AI Search, GPT-4o, PostgreSQL, human review, and deployment.
Then generate a simple diagram in text and a spoken interview walkthrough.
```

### Practice questions
- Why LangGraph?
- Why RAG?
- How did you chunk policies?
- How did you reduce hallucinations?
- Why human review?

---

## Day 6: eInfochips work experience

### Focus
Make your internship sound clear, credible, and specific.

### Know this
- Internal REST APIs for the accounting team.
- Payment tracking system.
- Node.js, Express, TypeScript, PostgreSQL.
- JWT, OAuth 2.0, RBAC.
- Worked with a senior engineer.
- Code reviews and feedback.
- Accounting team used APIs to reduce manual spreadsheet handoffs.

### Practice questions
- Tell me about your internship.
- What did you build at eInfochips?
- Tell me about a time you received feedback.
- How did you work with non-engineering stakeholders?

---

## Day 7: Weekly mock day

### Focus
No new learning. Practice recall under pressure.

### Record answers to these 6 questions
1. Tell me about yourself.
2. Walk me through Hearloop.
3. Walk me through YouTube Compliance Pipeline.
4. What was your hardest technical challenge?
5. How do you handle hallucinations?
6. Tell me about your internship.

### After recording, write down only 3 fixes
- One content fix
- One structure fix
- One delivery fix

---

# Week 2: Build technical depth

**Goal:** Be ready for follow-up questions.

---

## Day 8: RAG deep dive

### Focus
Understand RAG clearly enough to explain it without buzzwords.

### You need simple answers for
- What is RAG?
- Why use RAG instead of model memory?
- How do embeddings work at a high level?
- What is chunking?
- What is retrieval top-k?
- How do citations reduce hallucination?

### Practice answer

```text
RAG means I retrieve trusted context first, then ask the model to answer using that context. 
In my YouTube project, I indexed YouTube and FTC policy chunks into Azure AI Search, retrieved the top 8 chunks per audit, and passed those into GPT-4o so the final PASS or FAIL decision was grounded in written policy.
```

---

## Day 9: Agentic workflows and LangGraph

### Focus
Understand what makes a workflow agentic and why LangGraph was useful.

### Know the difference
- LangChain gives components: prompts, tools, retrievers, parsers.
- LangGraph gives control flow: nodes, state, branching, retries.
- You used LangGraph because compliance audits have steps, not one giant prompt.

### Practice questions
- What is an agent?
- What makes your project agentic?
- Why LangGraph over LangChain?
- Where would you use agents in Eduwave AI?

---

## Day 10: AI quality and hallucination handling

### Focus
Build your standard answer for AI quality.

### Key points
- Ground with trusted context.
- Use structured output.
- Keep temperature low when consistency matters.
- Add validation.
- Add fallback.
- Add human review for sensitive decisions.
- Track examples that fail.

### Practice questions
- How do you know the AI answer is good?
- How do you handle hallucinations?
- How would you evaluate an AI tutor?
- How would you handle wrong student answers?

---

## Day 11: Databases and backend flow

### Focus
Explain data flow clearly.

### For each project, answer
- What gets stored?
- Why store it?
- What table or object is the source of truth?
- What is cached?
- What happens on failure?

### Projects to cover
- Hearloop: sessions, partners, transcripts, classifications, webhook attempts.
- YouTube Compliance Pipeline: audit records, violations, AI status, final status, review notes.
- SEO Audit Engine: jobs, status, reports, cache.
- eInfochips: payment records and authenticated access.

---

## Day 12: Queues and async processing

### Focus
Master async processing because it applies to Hearloop, SEO Audit Engine, and AI workflows.

### Core explanation

```text
I used queues when the user should not wait for a slow process. 
The API accepts the request quickly, stores the job, and a worker handles the expensive steps in the background.
```

### Practice questions
- Why not do everything in the API request?
- What happens if a job fails?
- How would you retry failed jobs?
- How would you show progress to the frontend?

---

## Day 13: Tradeoffs day

### Focus
Create 3 tradeoffs for every major project.

### Hearloop examples
- Nova Lite was cheaper, while Haiku fallback protected parsing reliability.
- S3 direct upload reduced API load, but added signed URL complexity.
- Async jobs improved user experience, but required queue monitoring.

### YouTube Compliance Pipeline examples
- Captions first was faster, but missed visual-only claims.
- Temperature 0 improved consistency, but reduced flexibility.
- Human review added friction, but improved trust.

### Output to create
A tradeoff sheet with:
- Project
- Decision
- Why I chose it
- Downside
- What I would improve next

---

## Day 14: Weekly mock day

### Focus
Run a 30-minute fake interview.

### Questions
1. Tell me about yourself.
2. Favorite project?
3. Deep dive into architecture.
4. Why this tech stack?
5. What failed or was hard?
6. How would you improve it?
7. Why this role?

### Afterward
Rewrite only the weakest 2 answers.

---

# Week 3: Pressure practice and company tailoring

**Goal:** Sound natural under interview pressure.

---

## Day 15: Build project one-pagers

### Focus
Create a one-pager for each major project.

### Projects
- Hearloop
- YouTube Compliance Pipeline
- eInfochips
- ASU job
- Distributed Caching System
- Fake Review Detector

### One-pager template

```text
Project:
One-line summary:
User problem:
My role:
Architecture:
AI part:
Backend part:
Frontend part:
Database:
Hardest problem:
Tradeoff:
Metric:
What I would improve:
Best interview questions for this project:
```

---

## Day 16: Fix bullet confusion

### Focus
Move from polished sentences to cue bullets.

You said reading full bullets makes you confused. That means you need cue bullets first, then spoken sentences.

### Example cue-bullet format

```text
Hook: YouTube project = cited AI compliance audit.

- Problem: manual ad review was slow and inconsistent.
- Flow: URL → metadata/captions → policy retrieval → GPT-4o audit.
- Trust: 37 chunks, top 8 retrieval, citations, temperature 0.
- Review: PostgreSQL history plus human override.

Close: Same pattern applies to Eduwave: trusted content in, grounded AI answer out.
```

### Practice
Convert 5 old answers into cue bullets.

---

## Day 17: Eduwave-specific preparation

### Focus
Prepare company-specific answers.

### Prepare answers for
- Why Eduwave AI?
- What AI feature would you build?
- How would you build a personalized tutor?
- How would you evaluate answer quality?
- How would you work with a product designer?
- How would you collaborate with teachers and parents?

### Strong product idea

```text
I would build personalized explanations that adapt to the student's current understanding level.
The system would retrieve the lesson context, identify the student's misconception, generate an explanation at the right difficulty level, and let the student or teacher give feedback when it misses.
```

---

## Day 18: Work experience and behavioral answers

### Focus
Prepare behavioral stories that connect to real work.

### Prepare these stories
- Tough feedback: eInfochips code review.
- Ambiguous task: ASU transfer edge cases.
- Cross functional: accounting team and engineering.
- Initiative: ASU web scraping idea.
- Ownership: authentication delivery at eInfochips.
- Failure: today's interview, if asked honestly later.

### Rule
Do not overdramatize. Keep it simple and mature.

---

## Day 19: Rapid-fire technical drills

### Focus
Answer fast without freezing.

Set a timer. Answer each in 60 seconds.

### Questions
- What is RAG?
- What is LangGraph?
- Why async queue?
- Why PostgreSQL?
- Why Redis?
- Why FastAPI?
- Why Node.js?
- How do you reduce hallucinations?
- How do you evaluate AI output?
- How do you scale Hearloop?
- How do you secure uploaded audio?
- How do you handle failed AI jobs?

### Rule
Do not pause and restart. Finish the answer even if it is messy.

---

## Day 20: Full mock interview

### Focus
Record a full 30-minute mock interview.

### Structure
- 5 minutes: intro and motivation.
- 10 minutes: favorite project deep dive.
- 10 minutes: AI technical follow-ups.
- 5 minutes: behavioral and questions for interviewer.

### Grade yourself on
- Did I explain what the project does?
- Did I explain my role?
- Did I explain the architecture?
- Did I answer why choices were made?
- Did I stay calm when I forgot something?

---

## Day 21: Final consolidation

### Focus
Create your final interview pack.

### Final interview pack
1. 30-second intro.
2. 2-minute Hearloop.
3. 2-minute YouTube Compliance Pipeline.
4. 1-minute eInfochips.
5. 1-minute ASU.
6. AI quality answer.
7. Hallucination answer.
8. LangGraph vs LangChain answer.
9. Favorite project answer.
10. Why this company answer.

### Final rule
Do not memorize paragraphs. Memorize flow.

---

# The main system to use

Stop preparing answers as polished bullets first.

Use this:

```text
Project = what it is.
Problem = why it matters.
Flow = how it works.
Tradeoff = why I chose it.
Result = what improved.
Company tie = why relevant.
```

## Example

```text
YouTube project.
Ad compliance audit.
Manual review slow.
URL to metadata and captions.
Policy chunks from Azure AI Search.
GPT-4o gives cited PASS or FAIL.
Human review protects edge cases.
Same pattern fits educational tutoring with trusted lesson content.
```

This is easier to speak than memorized sentences.

---

# What to do today: Day 0

Since the interview just happened, do not start with all projects.

Spend 90 minutes only on this:

1. Write what went wrong in 5 bullets.
2. Create the 30-second Hearloop explanation.
3. Create the 2-minute YouTube project walkthrough.
4. Record both twice.
5. Save the better version.

Then start Day 1 tomorrow.

---

# Weekly checkpoint questions

At the end of each week, answer these honestly:

1. Can I explain Hearloop without notes?
2. Can I explain the YouTube Compliance Pipeline without notes?
3. Can I answer "why this tech?" without guessing?
4. Can I recover if I forget a detail?
5. Did I practice out loud every day?
6. Did I record myself at least twice this week?
7. Which answer still sounds fake, confusing, or memorized?

---

# Final reminder

Reading does not count as practice.  
Thinking silently does not count as practice.  
Only spoken reps count.
