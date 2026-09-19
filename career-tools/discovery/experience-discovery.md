# Experience Discovery

> **Scope:** Surface real, undocumented work — new project material, new work-experience facts, or
> gap-filling detail — before it's needed for a specific JD tailoring pass.
> **Truth:** Everything captured here becomes candidate master context, not resume content yet.
> **Governance:** `resume-system/governance/FACT_RULES.md` (metric legibility, design-vs-build verbs, estimation
> rules all apply to what gets captured here, same as anywhere else).

---

## ROLE

Run a structured interview to surface facts about a project or work-experience role that exist in
the user's head but are not yet written into `resume-system/facts/projects/*.md`, `resume-system/facts/work-experience.md`, or a
`career-stories/*.md` master file. This is **not** a tailoring pass — no resume bullets get written
in this mode. The output is updated/new master context, ready for a later tailoring pass to draw on.

**When to use this:**
- A JD keyword lands in the GAP band (per `.agents/skills/resume-tailor/SKILL.md`) and the user isn't
  sure whether it's a true gap or just undocumented
- The user mentions doing something new on a project/role that isn't reflected in its master file
- Before starting work on a brand new project or role that has no master file yet

**When NOT to use this:** Do not use this to retroactively justify a claim already made in a
locked bullet. If a fact-check dispute is already in progress on a *specific* claim, that's
governed by `resume-system/governance/FACT_RULES.md`'s design-vs-build and metric rules directly, not this mode.

---

## PROCESS

### Step 1 — Identify the target

Ask: which project or work-experience role is this about? If it doesn't have a master file yet
(`resume-system/facts/projects/<name>.md` or `career-stories/<name>.md`), say so — this session may produce one.

### Step 2 — Open-ended probe first

Start broad, not with a checklist: **"What have you actually built or done here that isn't written
down yet?"** Let the user talk before narrowing. Do not lead with a specific technology or metric —
that primes the answer instead of surfacing what's real.

### Step 3 — Branch based on the answer

| Signal in the answer | Follow-up direction |
|---|---|
| Concrete and specific ("I wrote the X handler," "I fixed a bug where Y") | Go deeper: what exactly changed, is it merged/shipped, what would the evidence be (repo, file, running behavior) |
| Vague or restated ("I did the backend," "I worked on the whole thing") | Push for specificity per `FACT_RULES.md`'s design-vs-build rule — a broader restatement of the same claim does not count as new evidence. Ask for one named file, endpoint, or observable behavior. |
| Design/planning language ("I proposed," "I designed," "we decided") | This is legitimate design-status material — capture it as such, verb-locked to "Designed/Architected/Planned," not escalated to "Built" without a separate concrete anchor |
| A number appears | Run it through the metric legibility check before treating it as usable (`resume-system/governance/FACT_RULES.md`) — if it fails, ask what it would take to make it legible (a comparison point, a before/after) rather than dropping it silently |
| Nothing concrete surfaces after two follow-ups on the same thread | Stop pushing on that thread. Note it as unconfirmed and move to the next area rather than manufacturing detail |

### Step 4 — Cover the standard categories once the open probe is exhausted

Only after Step 2–3 produce what they produce, check these areas explicitly so nothing is missed:

- **What was built** — the actual technical output, not the assigned task description
- **Stack actually touched** — by this person, not the team/repo in general
- **The problem and who it was for** — business or user context
- **Metrics** — MEASURED, ESTIMATE, or none (per `FACT_RULES.md` — do not force one)
- **Scale/volume signals** — as a substitute for outcome when outcome isn't measured
- **Soft-skill evidence** — kept as fallback material for JD-driven soft-skill-lead bullets (hybrid rule)
- **What's confirmed vs. what's still open/unconfirmed** — explicit, not implied

### Step 5 — Write to the right file, labeled correctly

- New project → new `resume-system/facts/projects/<name>.md`, following the structure of a current neighboring project master
- New/updated work-experience role → `resume-system/facts/work-experience.md`, following its existing Raw Context /
  Keyword Coverage / Locked Bullets structure
- Deep interview-prep story (architecture, bug stories, behavioral STAR material) → new or updated
  `career-stories/<name>.md`, following the structure of `career-stories/eInfochips.md`
- Anything not yet fact-checked or approved → `career-stories/_drafts/`, explicitly marked
  unverified per the Hierarchy rule in `resume-system/governance/FACT_RULES.md` — never written directly into a
  locked file

**Do not silently merge new material into a locked file.** Show what's proposed, get approval, then
write — same discipline as any other governance change in this project.

---

## OUTPUT FORMAT

```
Target: [project name / role name]
Existing master file: [path, or "none yet"]

New facts surfaced:
- [fact] — [confirmed / unconfirmed] — [source: user statement this session]

Metrics surfaced:
- [metric] — [MEASURED / ESTIMATE / flagged for legibility approval]

Still open / not resolved this session:
- [item]

Proposed write: [file path]
[Show the actual proposed content before writing]
```

Wait for explicit approval before writing to any file.
