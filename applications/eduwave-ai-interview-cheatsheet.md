# Eduwave AI — Interview Cheatsheet (30-min call)

**Role:** AI Engineering Summer Intern / Software Full-Stack Engineer · stipend + equity, founding team, remote
**Interviewer:** Kanksha Dixit — **Founding Product Designer** (Figma, student/parent dashboards, design system, user research)
**Call type:** 30-min intro / fit call with a *non-technical* (design/product) interviewer.

> **READ THIS FIRST — how to play this room.** Kanksha is a designer, not an engineer. She is *not* going to whiteboard you. She wants to know: Can you turn her Figma designs into a working product? Do you communicate clearly with non-engineers? Are you self-driven enough for a founding team? Do you care about education + AI? **Lead with collaboration, communication, and "I ship designs into real features." Keep tech in plain English. Only go deep technical if she asks.**

---



## 0. The 30-second pitch (memorize, say it warm)

"I'm a full-stack engineer who likes building AI products end to end, not just the model. I've built and deployed apps where the whole flow matters: a clean React dashboard on the front, Node or Python APIs in the middle, and real LLM and RAG pipelines underneath. My favorite work is taking a rough idea or a design and turning it into something a real user can actually click through. The reason Eduwave caught me is it's that exact mix: real AI, real product, and it's pointed at education, which actually matters."

---



## 1. Responsibility → Proof map (the core of this sheet)


| JD responsibility                                        | Your strongest proof                                                                                                                                                      | One-line you can say                                                                                                                                                                                             |
| -------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Front-end: HTML/CSS/JS, React**                        | **Hearloop** (Next.js 15 / React 19 dashboard), **ClusterOps** (React 18 live dashboard), **SEO Audit Engine** (JS UI)                                                    | "I built the Hearloop partner dashboard in React and Next.js, and a live React monitoring dashboard for ClusterOps with real-time updates."                                                                      |
| **Back-end: Node / Go / Python, REST APIs**              | **Hearloop** (Node + Fastify), **SEO Engine** (Node + Express), **YouTube Compliance** (Python + FastAPI), **ClusterOps** (Go), **eInfochips** (Node + Express REST APIs) | "I'm comfortable in all three: Node for Hearloop and the SEO engine, Python and FastAPI for the compliance pipeline, Go for ClusterOps."                                                                         |
| **Databases (PostgreSQL/MongoDB)**                       | **PostgreSQL** everywhere (Hearloop/Neon, SEO/Neon, YouTube/Azure PG, eInfochips). **MongoDB = gap (be honest, see §5)**                                                  | "I've used PostgreSQL across every project. I haven't shipped MongoDB but the document model is straightforward to pick up."                                                                                     |
| **AI model integration (OpenAI/Gemini/LLaMA)**           | **YouTube Compliance** (Azure OpenAI GPT-4o), **Hearloop** (AWS Bedrock Nova Lite + Haiku fallback, Groq Whisper), **Fake Review** (fine-tuned BERT/RoBERTa)              | "I integrate models as swappable components: GPT-4o in the compliance tool, Bedrock in Hearloop, and I fine-tuned BERT and RoBERTa for the review detector."                                                     |
| **RAG (Retrieval-Augmented Generation)**                 | **YouTube Compliance Pipeline — your headline RAG project** (Azure AI Search vector index, 37 policy chunks, top-k=8 retrieval, GPT-4o, cited findings)                   | "I built a real RAG pipeline: official policy PDFs chunked into a vector index, top-8 retrieval per request, then GPT-4o generates a cited pass/fail. Findings point back to the actual rule, not model memory." |
| **AI Agents / Agentic frameworks**                       | **YouTube Compliance** (LangGraph 3-node workflow: index → enrich → audit, LangChain)                                                                                     | "I orchestrated a multi-step LangGraph workflow where each node has one job and the run fails cleanly if a step breaks. That's the agent backbone I'd extend for tutoring flows."                                |
| **Git collaboration practices**                          | **eInfochips** (daily pairing + code reviews with a senior engineer), CI gates on every project (52 Jest tests SEO, pytest gate YouTube, validate gate Hearloop)          | "At eInfochips I worked in daily code reviews with a senior engineer, and on my own projects I gate every merge on CI so nothing broken ships."                                                                  |
| **Self-driven + communication + problem-solving**        | All 6 projects built **solo, end to end**; **ASU** (proactively proposed automation, took feedback well)                                                                  | "I built six projects solo from idea to deploy, so I'm used to driving without someone handing me tasks."                                                                                                        |
| **Technical feasibility of UI/UX designs** *(her world)* | **Hearloop dashboard**, **ClusterOps dashboard**, **SEO report UI** — all built from concept to working UI                                                                | "I like the feasibility conversation early. I've built dashboards from scratch, so I can tell you fast what's cheap, what's expensive, and what to fake first."                                                  |
| **Bonus: EdTech / AI-powered tools**                     | **EdTech = gap (honest).** All projects are AI-powered tools though                                                                                                       | "I haven't worked in EdTech yet, but every project I build is an AI-powered tool, and learning is the use case I'm most excited to build for."                                                                   |


---



## 2. Your two star projects (know these cold)



### YouTube Ads Compliance Pipeline — *the RAG + Agents proof*

- **What:** Paste a YouTube ad link, get a cited PASS/FAIL compliance report.
- **Why it matters for Eduwave:** This is real **RAG + agentic orchestration + LLM integration** — exactly their stack (RAG, AI Agents, GPT).
- **Stack:** Python, FastAPI, **LangGraph + LangChain**, **Azure OpenAI GPT-4o**, **Azure AI Search (vector RAG)**, embeddings (text-embedding-3-small), PostgreSQL, Docker, CI/CD.
- **The RAG flow (say it simply):** policy PDFs → chunked into 37 pieces → vector index → retrieve top 8 relevant chunks per audit → GPT-4o reasons over them at temperature 0 → returns structured findings **with citations** to the real rule.
- **The agent flow:** LangGraph workflow with 3 nodes — index metadata → enrich (captions, fallback) → audit (RAG + LLM). Each step isolated, fails cleanly.
- **Honest scope:** working **prototype** for demos, not a live customer rollout. UI is vanilla JS (not React). Say that plainly if asked.
- **Eduwave bridge:** "The same pattern fits tutoring: chunk the curriculum, retrieve the relevant concept for a student's question, and have the model answer grounded in *their* material instead of guessing."



### Hearloop — *the full-stack + shipped-it-solo proof*

- **What:** Voice-feedback platform; customers speak, businesses get analyzed feedback on a dashboard.
- **Why it matters:** Full **React/Next front end + Node back end + LLM pipeline**, actually **deployed**, built **solo**. Shows you ship.
- **Stack:** TypeScript, **Next.js 15 / React 19**, Node + Fastify, PostgreSQL (Neon), Redis, BullMQ async pipeline, **AWS Bedrock (Nova Lite + Haiku fallback)**, Groq Whisper, AWS, Docker, GitHub Actions.
- **Numbers (real, [MEASURED]):** p95 **149 ms** at 200 concurrent users; AWS cost **−72.6%** ($35→$9.60/mo); deploy **15 min → 60 s**; classification ~**$0.00003/session**.
- **Honest nuance:** the business-context personalization is **prompt injection, not RAG** — don't call it RAG. Built solo with AI-assisted dev tools.
- **Eduwave bridge:** "Hearloop is the closest to what you're doing: a clean dashboard for a non-technical user sitting on top of an LLM pipeline, deployed and cost-controlled."

---



## 3. Behavioral answers she's likely to ask (designer/product lens)

Each is read-aloud ready. Pick the bullets, don't recite robotically.

**"Tell me about yourself."**

- I'm a full-stack engineer who builds AI products end to end, front end through the model.
- Most recently I built Hearloop, a deployed voice-feedback app with a React dashboard on an LLM pipeline.
- I also built a RAG and LangGraph compliance tool, so retrieval and agents aren't new to me.
- What pulls me to Eduwave is the mix of real AI, real product, and education actually mattering.

**"How do you work with designers / non-technical teammates?"** *(she cares most about this)*

- I like getting pulled into design early so I can flag what's cheap versus expensive before it's locked.
- At eInfochips I worked daily with a senior engineer and a non-technical accounting team, translating between what they wanted and what the code could do.
- When I build dashboards I start from the user's flow, not the database, so the UI drives the API and not the other way around.
- Close: "I see the feasibility check as a collaboration, not me saying no."

**"Tell me about a time you got tough feedback."** (STAR)

- At my eInfochips internship I was building REST APIs for the accounting team, in daily code review with a senior engineer.
- He flagged that my logic kept drifting from the original task scope.
- I stopped getting defensive, walked through my reasoning out loud, and started confirming scope up front.
- That one habit cut my rework on every later ticket and is how I shipped reliable payment APIs.

**"Why Eduwave / why education?"**

- I build AI tools, and education is the use case where good tooling changes someone's actual trajectory.
- A founding role where I shape product and engineering from day one is exactly the speed I like.
- I've shipped solo, so a fast-moving small team plays to how I already work.
- Close: "I'd rather own a real piece of a mission than be one cog on a huge team."

**"What are you looking for / why a stipend+equity startup?"**

- I'm optimizing for ownership and learning velocity right now, not a big salary.
- A founding team means I touch the whole stack and the product decisions, which is how I grow fastest.

---



## 4. Smart questions to ask HER (pick 2–3 — designer-flavored)

- "How does the design-to-engineering handoff work today — Figma to shipped feature?"
- "Where are you on the tutoring AI: prompt-based today, or already doing RAG over curriculum content?"
- "What's the riskiest part of the product right now — the AI quality, or the dashboards landing with students and parents?"
- "For a founding engineer, what does the first 90 days actually look like?"
- "How do you balance shipping fast against getting the learning experience right for kids?"

---



## 5. Honesty guardrails (do NOT overclaim — it backfires)


| Topic                         | The truth                                                             | How to say it                                                                                                                   |
| ----------------------------- | --------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| **MongoDB**                   | Never shipped it; PostgreSQL only                                     | "Deep on PostgreSQL, comfortable picking up MongoDB's document model."                                                          |
| **Gemini / LLaMA**            | Used GPT-4o (Azure) + Bedrock, not those two                          | "I treat the model as swappable — I've used GPT-4o and Bedrock, so adding Gemini or LLaMA is a provider change, not a rewrite." |
| **EdTech experience**         | None                                                                  | "No EdTech yet — it's the space I most want to build in."                                                                       |
| **Hearloop "RAG"**            | It's prompt injection, not RAG                                        | Call it "business context injected into the prompt," not RAG.                                                                   |
| **ClusterOps "AI"**           | Assistant is rule-based, LLM is a planned swap-in                     | "It's a rule-based engine architected as a clean LLM swap-in — I built the RAG-shaped scaffold, not live LLM calls."            |
| **Production scale**          | Most are prototypes; Hearloop deployed, eInfochips real internal tool | "Portfolio builds are deployed prototypes; my production team experience is the eInfochips internship."                         |
| **Fake Review = RAG/agents?** | No — it's fine-tuned ML models                                        | Don't tie it to RAG or agents; it's an ML/LLM fine-tuning project.                                                              |


---



## 6. Last-15-minutes checklist

- [x] Warm up the Hearloop demo URL (cold start) and the YouTube compliance demo so you can offer to show them.
- [x] Reread §2 (your two star projects) once out loud.
- [x] Have the 30-second pitch (§0) ready as your first answer.
- [x] Pick your top 2 questions for her (§4).
- [x] Mindset: she's a teammate evaluating *can we build together*, not an examiner. Be warm, concrete, and curious about the product.
- [x] One closing line ready: "I'm genuinely excited about this one — I'd love to build the tutoring experience with you."