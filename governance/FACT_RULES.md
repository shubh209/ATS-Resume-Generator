# Fact Rules — Master Context Is Source of Truth

> GPT reads `gpt/` in this repo, not dev project repos. If master MD is stale, the resume will be wrong.

---

## Hierarchy

1. **Locked resume bullets** in `gpt/projects/*.md` — facts are fixed; wording may change per JD
2. **Raw context / Verified Metrics** in project MD and `gpt/work-experience.md`
3. **Never Claim** sections in project MD (when present)
4. **`gpt/per-project-keywords.md`** — role coverage reference only; does not authorize new facts

---

## Metrics (`\metric{}`)

| Label | Rule |
|-------|------|
| **MEASURED** | From project MD with `[MEASURED]` or defensible raw context |
| **ESTIMATE** | From project MD with `[ESTIMATE]` or honest projection |

Both may appear in `\metric{}` **if sourced in master MD**. Fact Check table must label each.

**Do not** invent metrics to match the JD.

---

## Bullet facts vs wording

| Allowed | Not allowed |
|---------|-------------|
| Reword bullets to mirror JD language | Change stack, scale, or outcome facts |
| Emphasize JD-relevant tech you actually used | Add tech you only plan to use |
| Drop irrelevant accomplishments | Invent accomplishments |

---

## Technology claims

### Project bullets — hard rule

A technology may appear in a **project bullet** only if it appears in that project’s master MD (tech stack, locked bullets, or impact).

`[PLANNED]` in keyword docs does **not** qualify for bullets.

### Skills section — adjacent rule

A technology **not** in master context may appear in **Skills** only when:
- It is explicitly in the **master skills list** in `gpt/system-prompt.md`, **or**
- It is **directly adjacent** to proven tech (same ecosystem) and honestly listed in a project MD

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

When a dev repo project changes, update `gpt/projects/<name>.md` **before** tailoring for a JD that needs that project.
