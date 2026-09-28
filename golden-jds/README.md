# Golden JDs — organized by lane

Regression-test job descriptions, split into the three roles Shubh applies to. A golden JD lives in the subfolder for the lane it routes to, so the corpus mirrors the resume-tailor lanes.

```
golden-jds/
  full-stack/    Full Stack lane
  backend/       Backend lane
  ai-engineer/   AI Engineer lane
```

## Which lane does a golden JD go in?

Classify by the lane the JD routes to under the resume-tailor routing table (`.agents/skills/resume-tailor/SKILL.md`), not by its title alone. Use the first rule that matches.

1. **AI Engineer** — the title or the *required* work centers on ML, LLMs, GenAI, RAG, agents, model evaluation, prompt orchestration, or MLOps as the engineering itself. If AI is only the *method* (e.g. "use AI coding tools") or only a *preferred* nice-to-have layered on a conventional stack, it is NOT AI Engineer.
2. **Full Stack** — the title says Full Stack, OR the required qualifications include both a frontend framework (React/Next.js/Angular/Vue) and backend/API development, OR it is a general SWE posting spanning frontend and backend with no dominant specialty.
3. **Backend** — the title or required work centers on APIs, services, databases, platforms, distributed systems, infrastructure, data engineering/pipelines, or backend development, without a dominant frontend or AI-modeling requirement.

### Tie-breakers
- "AI-native" or "uses AI coding tools" company, but the built product is a conventional web/backend app → route by the stack (Full Stack or Backend), not AI Engineer. AI evidence is surfaced within that lane.
- Data engineering / data platform (ETL, pipelines, warehousing, streaming) → Backend.
- Systems / infrastructure / observability / inference-serving → Backend.
- A senior/specialist or multi-lane posting still routes to one lane; record the routing rule and note the fit level (strong vs moderate/stretch) in the JD's own fit-notes.

## Current contents

### full-stack/
- `full-stack-software-engineer.md`
- `full-stack-product-growth-cloudflare.md`
- `software-engineer-intuit-entry-level.md` — multi-lane general SWE; routes Full Stack by default.

### backend/
- `backend-software-engineer.md`
- `backend-software-engineer-mastercard.md`
- `backend-software-engineer-cloud-sonos.md` — strong-fit fixture.
- `backend-software-engineer-billing-cursor.md` — moderate/stretch (billing/ledger specialist).
- `backend-software-engineer-data-platform-abnormal.md` — moderate/stretch (data platform).
- `backend-software-engineer-inference-infra-cerebras.md` — moderate/stretch (inference infra, K8s gap).
- `backend-software-engineer-commerce-apple.md` — moderate/stretch (Java, high-QPS transactional).
- `systems-engineer-postgresql-cloudflare.md` — systems/Postgres, Backend lane.

### ai-engineer/
- `ai-software-engineer.md`
- `ai-software-engineer-commure.md`
- `ai-engineer-sierra.md`
- `ai-engineer-morgan-stanley.md`
- `ai-engineer-nuclear-company.md`

## Adding a new golden JD
1. Route it with the rules above.
2. Name it `<lane>-<role>-<company>.md` and place it in the matching subfolder.
3. Include the JD content plus a "Candidate-fit notes for regression testing" section that records the expected lane, the routing rule, strongest matches, honest gaps, and overall fit (strong vs moderate/stretch).
