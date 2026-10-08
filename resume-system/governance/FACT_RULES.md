# Fact Rules — Master Context Is Source of Truth

> GPT reads `resume-system/facts/` in this repo, not dev project repos. If master MD is stale, the resume will be wrong.

---

## Hierarchy

1. **Baseline resume bullets** (including banks headed “Locked Resume Bullets”) in `resume-system/facts/projects/*.md` and `resume-system/facts/work-experience.md` — facts are fixed; application-copy wording may change under the JD terminology rules below. Master wording changes only during explicitly authorized master maintenance
2. **Raw context / Verified Metrics / Metrics Ledger** in project MD, `resume-system/facts/work-experience.md`, and role master-story files in `career-stories/*.md` (e.g. `eInfochips.md`) — same authority as project MD
3. **Never Claim** sections in project MD, `work-experience.md`, or `career-stories/*.md` (when present)
4. **`resume-system/facts/per-project-keywords.md`** — role coverage reference only; does not authorize new facts

Draft/unverified files carry **no authority** regardless of location — e.g. `career-stories/_drafts/*.md`. Nothing may be sourced from a `_drafts/` file without first being fact-checked and promoted into a locked file above.

---

## Metrics (`\metric{}`)

| Label | Rule |
|-------|------|
| **MEASURED** | From project MD with `[MEASURED]` or defensible raw context |
| **ESTIMATE** | From project MD with `[ESTIMATE]` or honest projection |

Both may appear in `\metric{}` when the current master records the measurement or estimate and identifies its evidence source. The evidence may live in the originating project repository; the Fact Check table must label the metric and must not claim it was independently reverified during tailoring.

**Do not** invent metrics to match the JD.

---

## Bullet facts vs wording

| Allowed | Not allowed |
|---------|-------------|
| Select and reorder baseline bullets; adapt application-copy wording under JD terminology rules | Change stack, scale, contribution, or outcome facts during live tailoring |
| Emphasize JD-relevant tech you actually used | Add tech you only plan to use |
| Drop irrelevant accomplishments | Invent accomplishments |

---

## Bullet compression

Every resume bullet must retain four parts: **what was done, how it was done, where or in what context, and why it mattered**. The final reason may be a verified business outcome, a measured system outcome, or an honestly framed intended purpose for a side project.

When the user asks to tailor, shorten, tighten, or fix line wrapping, cut in this order:

1. Repeated ideas and filler
2. Secondary implementation details
3. Lower-priority technologies or vendor names that the target JD does not reward
4. Extra examples and modifiers

Preserve the reason. Do not solve a length problem by deleting or weakening the bullet's business reason. Rewrite the reason more concisely when needed, and remove a lower-value technical detail first.

A shortened bullet is complete only when its ending still answers **why the work mattered** in plain language. A technical capability by itself is incomplete. For side projects without real users, state the intended purpose with language such as `designed to` rather than implying adoption or realized customer impact.

---

## Bullet rewriting

Applies to explicit bullet edits and evidence-backed rewording of baseline bullets in a tailored application copy. Live tailoring leaves the source masters unchanged.

**Preserve, without exception:**

- Every metric, number, and `\metric{}` value, unchanged.
- Every employment fact: company, dates, location, status, stack actually used, and contribution level. Resume titles may use only the approved functional variants recorded in `work-experience.md`; retain original titles in the factual record and forms requesting official employment titles.
- The business / "why it mattered" clause. This is the most-reverted mistake in this repo's history: a reworded bullet that keeps the jargon and drops the reason is a regression, not an edit. If the original ends on a real outcome or intended purpose, the rewrite ends on that same meaning.

**Voice and quality bar:**

- The bullet must read as **one smooth sentence**, not fragments glued together. If it sounds like clauses were concatenated, it fails.
- Match the register of the surrounding bullets — same seniority, same level of plainness. A rewritten bullet should not stand out in tone.
- No soft, vague, or childish phrasing. Banned patterns include "could never corrupt," "so nothing ever breaks," "making everything better," and similar hand-wavy outcomes. State the mechanism and the real consequence instead (e.g. "every update either fully applied or rolled back, keeping reconciliation numbers trustworthy").
- Lead with the technical build, carry the reason to the end. Do not front-load the outcome and strand the mechanics.
- Meaning over wording: preserve what the bullet actually says. Reword to improve clarity and flow, not to insert JD keywords that change or inflate the claim.

**Done test:** the rewrite preserves every fact and the business reason, reads as one natural sentence, and matches the tone of its neighbors. If any of those fail, it is not finished.

---

## Prototype intended-purpose framing

Experience bullets and project bullets carry different truth-framing, and the distinction is a rule, not a judgment call:

- **Experience bullets** (DAS, ASU, eInfochips) close on a **real business or system outcome** that actually happened for real users or stakeholders.
- **Project bullets** (portfolio prototypes with no real users) close on **intended purpose** using language such as `designed to` or `built to`. They must not imply adoption, customers, or realized impact that did not occur.

Never write "helped users do X," "so customers could Y," or any user-facing outcome for a prototype project. The candidate has no users for these projects; do not invent one. State what the system was built to do, not what users did with it.

---

## Technology claims

### Project bullets — hard rule

A technology may appear in a **project bullet** only if it appears in that project’s master MD (tech stack, locked bullets, or impact).

`[PLANNED]` in keyword docs does **not** qualify for bullets.

### Skills section — evidence rule

A technology may appear in **Skills** only when current `resume-system/facts/work-experience.md` or a current selectable `resume-system/facts/projects/*.md` master documents that it was actually used. A template, legacy prompt, keyword list, planned item, or adjacent technology never authorizes a skill claim by itself.

Example: Docker in master MD does **not** authorize Kubernetes on the resume unless Kubernetes is in master MD.

When in doubt: **omit**.

---

## Never Claim (global)

Never claim on any resume unless added to master MD with evidence:

- Production customer rollout for prototype projects
- Latency, accuracy, or success rates not in master MD
- Team size, revenue impact, or user counts not in master MD
- "Led" or "mentored" when role was junior / individual contributor

Per-project Never Claim lists (add to project MDs over time) override general rules.

### YouTube Compliance (from handoff)

Do not claim: production customer rollout; React/TypeScript frontend; measured latency/accuracy; ~30 sec review time; ~95% metadata success; 80 videos tested.

---

## Prototype framing

These are **working prototypes / portfolio** unless master MD says otherwise:

- YouTube Ads Compliance Pipeline
- Hearloop (demo scale; no live partner count at scale)

Fact Check: mark **Prototype: YES**. Bullets may describe capability without implying live customer deployment.

---

## Metric legibility

Before any metric goes into a bullet, it must pass a legibility test: **a recruiter with zero context must immediately understand why the number matters, without needing domain knowledge to judge whether it's good.**

| Passes legibility | Fails legibility — flag for approval first |
|---|---|
| "10,000+ payment records" | "72 tests passing" (recruiter has no baseline for what's a lot) |
| "$2,000 annual budget" *with the tradeoff stated in the same sentence* | "$2,000 annual budget" alone, with no stated tradeoff (reads as trivia) |
| "200 concurrent users, 0% errors" | "AWS cost $35 → $9.60" when the "before" number was self-inflicted overengineering, not a real constraint |
| Any before/after where both numbers are independently meaningful | A count of design artifacts (entities, tables, iterations) offered as if it were scale or impact |

**If a metric fails this test:** do not include it by default. Surface it to the user for explicit approval before use, with the specific reason it fails. Do not silently drop it either — flag it.

---

## Metric discovery and honest estimation

When a real accomplishment has no obvious number, find or estimate one **honestly** before defaulting to no metric at all:

| Technique | Example |
|---|---|
| Quantify the input when the output is unmeasured | Can't cite users? Cite "processed 500K+ records" or "trained on 1M+ data points" instead |
| Conservative estimate, labeled `[ESTIMATE]` | If unsure whether it was 40% or 60%, use the lower, defensible number |
| Range instead of a false-precise figure | "8–12" instead of inventing a single number |
| Scale/volume as a substitute for outcome | Team size, record count, request volume — when the business outcome itself isn't measured |

**Every estimate must be interview-defensible.** If asked "how did you arrive at that number," there must be a real answer, not "I made it up to sound better." An estimate that can't survive that question is treated as an invented metric and is not allowed, per the "Do not invent metrics" rule above.

---

## Design vs. build verbs

Design work and implementation work are different accomplishments and use different verbs. Do not blend them.

| Status | Allowed verbs | Forbidden verbs |
|---|---|---|
| **Designed only** — architecture, data model, plan exists; no code confirmed running | Designed, Architected, Modeled, Planned | Built, Implemented, Deployed, Shipped, Running in production |
| **Built** — real code exists, confirmed by the user pointing to something concrete (a repo, a file, a running endpoint) | Built, Implemented, Shipped | Deployed, Running in production (unless deployment is separately confirmed) |
| **Deployed** — confirmed live in a real environment | Deployed, Running in production | — |

**Escalating a claim from "designed" to "built" requires a concrete anchor**: a named repo, a specific file/function, or an observable running behavior, not a restated or broader version of the same claim. If the user's answer to "what's the evidence" is just a firmer assertion of the same claim, treat the status as unchanged and ask again.

---

## JD terminology and visibility

Prioritize required qualifications and core responsibilities, followed by useful preferred terms. There is no keyword quota. Use the JD's exact terminology when verified evidence supports its meaning and it reads naturally in context.

For each important term, distinguish **supported and visible**, **supported but omitted**, and **unverified**. Search visibility and qualification evidence are separate: verified tools may appear in Skills, while claimed responsibilities require contextual bullet evidence.

Allowed application-copy edits include equivalent names, abbreviations, and descriptions of the same work (Postgres → PostgreSQL; REST API → RESTful API; spreadsheet validation → validation during data ingestion). Keep every edit traceable to a baseline bullet and verified context. A broader term requires evidence for its entire meaning: building API endpoints alone does not establish system architecture; using Docker does not establish Kubernetes; using LangGraph alone does not establish memory or recovery from failure.

Preserve what/how/where/why, all numbers, the actual contribution and seniority, and prototype framing. End on the same specific business or system reason, or the same intended purpose for a prototype. Cut secondary implementation details before weakening that reason. Equivalent wording does not authorize new tools, scale, ownership, expertise, or outcomes.

Approved functional titles are resume descriptions of verified duties, not claims that the employer formally assigned that title. Preserve internship and volunteer status. Choose among the role's recorded variants; AI Engineer applications do not authorize relabeling non-AI employment as AI Engineer.

Unverified terms remain gaps. Investigating source code is a separate, user-authorized evidence-maintenance task: inspect named project repositories, record concrete implementation anchors and limitations in the relevant master, then tailor from that updated master. Plans, dependencies, generated claims, and framework capabilities alone do not prove implementation.

---

## Fact Check statuses

| Status | Meaning |
|--------|---------|
| **OK** | Sourced; include in LaTeX |
| **REJECT** | Omit from LaTeX; note in table |

---

## Sync rule

When a dev repo project changes, update `resume-system/facts/projects/<name>.md` **before** tailoring for a JD that needs that project.
