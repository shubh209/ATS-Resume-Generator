# Fact Rules — Master Context Is Source of Truth

> GPT reads `resume-system/facts/` in this repo, not dev project repos. If master MD is stale, the resume will be wrong.

---

## Hierarchy

1. **Locked resume bullets** in `resume-system/facts/projects/*.md` and `resume-system/facts/work-experience.md` — facts and wording are fixed during live tailoring; wording changes only in explicitly authorized master maintenance
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
| Select and reorder locked bullets verbatim | Change locked wording, stack, scale, or outcome facts during live tailoring |
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

## JD keyword honesty

| Situation | Action |
|-----------|--------|
| JD requires keyword you have in master MD | Include in bullets or skills |
| JD requires keyword you lack | Do **not** put in project bullets; do not stuff skills |
| JD uses synonym you have | Mirror JD wording (e.g. RESTful API ↔ REST API) |

---

## Fact Check statuses

| Status | Meaning |
|--------|---------|
| **OK** | Sourced; include in LaTeX |
| **REJECT** | Omit from LaTeX; note in table |

---

## Sync rule

When a dev repo project changes, update `resume-system/facts/projects/<name>.md` **before** tailoring for a JD that needs that project.
