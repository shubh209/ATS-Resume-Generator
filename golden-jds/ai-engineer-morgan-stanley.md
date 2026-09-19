# Golden JD — AI Engineer (Morgan Stanley, real posting)

**Use for regression:** AI Engineer lane, agentic orchestration + LLM + RAG emphasis.
**Source:** Real posting (Morgan Stanley, Technology division). Captured Aug 2026.
**Note on seniority:** This posting is titled Software Engineering III / Director level and asks for
"mastery" of agent frameworks and "expert-level Python (mandatory)." It skews more senior than the
synthetic `ai-software-engineer.md` golden. Use it to test how tailoring behaves against a
higher-bar, agentic-heavy AI JD — and to check honest gap handling (e.g. Kubernetes, CrewAI/AutoGen,
Pinecone/Weaviate, fine-tuning are named but not all in the candidate's master facts).

---

## Software Engineering III — Advanced Analytics, ML & GenAI Platform (Morgan Stanley)

### About the role

In the Technology division, this team builds autonomous systems that reason, use tools, and complete
multi-step tasks using LLMs and reasoning models, plus calibration scoring and guardrails for agent
accuracy. The role is part of the cloud adoption and engineering roadmap and expects scalable, agile,
robust architecture. Works with global teams (India and US), with limited or no supervision, and
shares knowledge across the team.

**Work authorization:** Must be legally authorized to work in the US and not require sponsorship now
or in the future. (Flag for the candidate: this is a hard sponsorship exclusion.)

### What you'll do

- Hands-on engineer building and deploying AI agents at scale to accelerate technology and business roadmaps.
- Evaluate state-of-the-art GenAI technologies and prototype solutions to improve the architecture and platform.
- Design, implement, and operationalize distributed, scalable, reliable data flows that ingest, process, store, and access data at scale (batch and real-time) used by AI agents.

### Required qualifications

- 2+ years building **GenAI** solutions and supporting components: design, architecture, development, and operationalization of **agent orchestrations at scale**.
- **Agent orchestration frameworks:** LangChain, LangGraph, CrewAI, Microsoft AutoGen — building multi-agent workflows.
- **LLM implementation:** LLM APIs (OpenAI, Anthropic, AWS Bedrock), prompt engineering (Chain-of-Thought), and fine-tuning for agentic behaviors.
- **Memory & context management:** vector databases (Pinecone, Weaviate) and Retrieval-Augmented Generation (RAG) pipelines.
- **Tool-calling & APIs:** integrating external APIs as agent tools, function calling, and error handling for malformed model outputs.
- **Languages & backend:** expert-level **Python** (mandatory), often paired with **FastAPI**, **Node.js**, or **Go**. Familiarity with **Docker** and **Kubernetes** for containerized deployment.
- Ability to work in a fast-paced, dynamic environment.
- Good written and verbal communication skills.

### Candidate-fit notes (for regression testing, not part of the JD)

- Strongest project match: Video Compliance Pipeline (LangGraph agentic orchestration, RAG, Azure AI Search vector store, GPT-4o, evaluation/guardrails, Chain-of-Thought, structured/tool output, error handling on malformed model output).
- Real gaps to handle honestly (do not invent): CrewAI, AutoGen, Pinecone, Weaviate (candidate uses LangGraph + Azure AI Search, not these specific tools); fine-tuning (candidate fine-tuned BERT/RoBERTa in Fake Review Detector — an open-source-model fine-tune, adjacent but not agentic-LLM fine-tuning); Kubernetes (ClusterOps is Kubernetes-adjacent/Docker Compose, not real K8s per its Never Claim).
- Sponsorship exclusion is a hard filter per the candidate profile (OPT/H1-B). Flag before spending an application slot (see `resume-system/reference/jd-red-flags.md`).
