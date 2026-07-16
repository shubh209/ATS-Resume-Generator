# Shubh Kapadia — Networking Profile (master truth)

> Source of truth: `gpt/work-experience.md` and `gpt/projects/*.md`.  
> Do not use metrics from older `prompts/networking.md` drafts (e.g. 80+ ads/hr, 91.3% F1).

## Identity (connection notes)

- **Name:** Shubh Kapadia
- **Education:** MS CS, Arizona State University, May 2026
- **Visa:** OPT available Jun 29, 2026; will need H1-B sponsorship (omit from 300-char LinkedIn connection notes unless user overrides)
- **Lanes:** Full Stack, Backend, AI Engineer (pick project by recipient role + company)

## Experience (one-liners for Line 1)

- **eInfochips SWE Intern (2023):** Paired with senior engineer; 5+ REST APIs for accounting payment tracking; OAuth/JWT/RBAC
- **ASU Academic Records (2026):** Course transfer research; collaboration, feedback, process improvement; 150+ records/day

## Projects — pick ONE for Line 2 (defensible metrics only)

| Project | Use when | One-line result (MEASURED unless noted) |
|---------|----------|----------------------------------------|
| **Hearloop** | Voice, SaaS, AWS, full stack, feedback | 200 concurrent users, 149ms p95 load test (k6); AWS cost $35→$9.60 |
| **Video Compliance** | AI, RAG, LangGraph, Azure, compliance | 37 policy chunks indexed; LangGraph + RAG on Azure; prototype (not live customers) |
| **SEO Audit Engine** | Node, async jobs, Redis, web crawling | Warm audits ~5s (from ~24s); API accepts jobs in <400ms |
| **Fake Review Detector** | ML, NLP, PyTorch | 608k reviews; 6 models; LR inference 0.020ms avg |
| **Crypto Market Simulator** | Mobile, React Native, Cloudflare | 176k+ D1 rows; 100+ assets; educational simulator |
| **Distributed Caching** | Go, backend, systems, LLM infra | 10,600 reads/sec; 93.9% compute reduction in RAG sim at 1M req/day |

## Never claim in connection notes

- Live paying customers or production rollout for Hearloop / Video Compliance prototypes
- Metrics not in project MD
- Kubernetes/Kafka unless in that project's MD

## Project ranking for recipient

Use same logic as `governance/OUTPUT_CONTRACT.md` when JD is pasted (referral intent). Otherwise match recipient role + company + their experience blurb to the closest project row above.
