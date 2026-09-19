# LinkedIn Connection Note Generator

> **Scope:** LinkedIn connection request note only. 300 character **hard limit**. Exactly **3 lines**.  
> **Truth:** `career-tools/linkedin/candidate-profile.md` + `resume-system/facts/projects/*.md` + `resume-system/governance/FACT_RULES.md`  
> **Humanizer:** Apply `career-tools/reference/humanizer.md` before final output.

---

## ROLE

Generate one ready-to-paste LinkedIn connection note for **Shubh Kapadia**. Never generic. Every note ties Shubh's background to **this** person's role, company, and work.

---

## USER INPUT TEMPLATE

Collect what the user provides. **Refuse to generate** if missing: Name, Company, Role, Their experience (any length), Intent, Reason.

```
Name:
Company:
Role:
Their experience:
Intent: network | ask | referral
Reason:
Job title:          (optional; required for referral if no JD)
JD:                 (optional; paste for referral / role-specific ask)
Ask detail:         (optional; overrides default Line 3)
```

### Intent rules

| Intent | Line 3 default | Extra inputs |
|--------|----------------|--------------|
| **network** | Would love to connect. | Reason helps Line 1 hook |
| **ask** | Open to 15 minutes on your calendar to review my application for [Company]? | Optional job title sharpens ask |
| **referral** | Applied to [Job title] at [Company] — open to a referral if you think it's a fit? | **JD or job title required** — refuse if both missing |
| **founder-cold** | Open to a quick chat? / Open to hearing more about the [role] roles? | For founders/startups reached cold on LinkedIn or via a YC/direct message — see Cold Outreach section below |

If `Ask detail` is provided, use it as Line 3 (still ≤300 chars total).

### Recipient type: warm vs. cold

- **Warm** (recruiter, hiring manager, engineer at a company where a real project maps cleanly to their JD or team) → standard Line 2 rule applies: one project + one metric.
- **Cold** (founder, stranger, someone reached via a LinkedIn DM or YC "Work at a Startup" message with no JD in hand) → **Cold Outreach rules override Line 2.** See below. This is the default for `founder-cold` intent.

---

## STRUCTURE (MANDATORY)

**Exactly 3 lines. No greeting line** (no "Hi Name," — LinkedIn shows their name separately).

| Line | Content |
|------|---------|
| **1** | Who Shubh is — one sentence tying **MS CS ASU / SWE background** to **their role or team problem** at **Company**. Use Reason + Their experience when relevant. |
| **2** | Why Shubh is a strong fit — **one** project + **one** metric mapped to their work or JD. Never two projects. |
| **3** | The ask — per Intent table above. Small, specific, easy to say yes. |

### Length

- **Hard limit: 300 characters** including spaces and punctuation (count newlines as 1 char each if platform counts them; target ≤298 to be safe).
- If over limit: shorten in order **Line 2 metric → Line 1 → Line 3** until ≤300.
- **Never** output over-limit text as the final note.

### OPT / H1-B

**Do not** include OPT or H1-B in the 300-char note (default). User may say otherwise in `Ask detail`.

---

## PROJECT & METRIC SELECTION

1. Read `career-tools/linkedin/candidate-profile.md` for quick mapping.
2. Confirm metric in source `resume-system/facts/projects/<file>.md`.
3. **MEASURED** and **ESTIMATE** metrics allowed if labeled in project MD.
4. **Referral + JD pasted:** pick project using the evidence bands and JD priorities in `.agents/skills/resume-tailor/SKILL.md`.
5. **Recruiter vs engineer:** same 3-line structure; only Line 3 wording changes (referral vs calendar ask).

---

## COLD OUTREACH RULES (founders, strangers, no JD in hand)

**The problem this section fixes:** a bare benchmark dropped into a cold DM is unreadable to someone with zero context on the project. It requires them to already know what the project is to judge whether the number matters. This is a *different* flavor of the exact thing this skill exists to avoid — generic flattery ("impressed by your work...") and unexplained number-flexing both fail the same test: neither is genuine or direct, they're just two ways of not actually saying anything.

**Rule:** for cold outreach, Line 2 is a **plain, self-contained capability statement** — what you can do, in one clause that needs no prior knowledge of any specific project. Do not use a bare metric in Line 2 for a cold recipient, even if a project maps loosely to their space.

### Also required: honesty about the actual overlap

Before writing Line 1, check how close the mapped project actually is to what the company does. If a project only shares a *surface-level* pattern (e.g. both involve "voice input" or both use an LLM pipeline) but solve a materially different problem (e.g. after-the-fact feedback analysis vs. real-time conversational automation with workflow writes), do not claim it is "exactly the kind of problem" they're solving. Say "similar building blocks" or "adjacent," not "the same problem" — a claim that oversells the overlap falls apart under one follow-up question.

### Cold structure

| Line | Content |
|------|---------|
| **1** | Who Shubh is — one plain-language capability statement (what you build), tied to the *general category* of problem the company works in. No numbers. |
| **2** | Direct statement of intent: you like shipping real systems, not prototypes, and want to hear more about the roles. No flattery, no metric. |
| **3** | Small, low-pressure ask — "Open to a quick chat?" or similar. |

### Voice for cold outreach

Be direct and transactional, not falsely warm. The user's own words: *"nothing smart to say... instead I wanna talk smart and be direct about what I want and what they get in return. Just a basic transaction."* Follow that literally:
- State what you can offer (real capability, plainly) and what you want (to learn about the roles) — that's the whole transaction, no more.
- Do not manufacture enthusiasm about the company beyond what's genuinely true and specific.
- If nothing specific and true can be said about the company, don't invent something — stay on the capability statement and the ask.

---

## VOICE & BANS

- Tone: direct peer grad, not salesy.
- **Banned openers:** I hope, Hope this finds you, I am reaching out, Passionate about, Excited to, I'd love to pick your brain.
- No em dashes. No hyphenated compounds inside sentences.
- No rule-of-three flattery. No corporate jargon.
- Run humanizer pass: sound like a person typed this on their phone.

---

## OUTPUT FORMAT

Always output in this order:

```
Intent: [network | ask | referral]
Project used: [name]
Metric: [short label] [MEASURED | ESTIMATE]
Recipient: [Name] — [Role] @ [Company]

--- COPY BELOW ---

Line 1 text
Line 2 text
Line 3 text

--- END ---
Characters: N/300
```

If `N > 300`, do not show the over-limit version — regenerate until compliant.

**Before finalizing any metric in Line 2:** run the metric legibility check from `resume-system/governance/FACT_RULES.md` — a recruiter/founder with zero context must understand why the number matters without needing domain knowledge to judge it. If it fails, drop the metric (warm recipient: use a plainer capability phrase instead; cold recipient: this should not have had a metric in Line 2 to begin with — see Cold Outreach rules).

---

## EXAMPLES (structure only — personalize every time)

**Network / engineer**

```
MS CS grad (ASU) building voice + AI pipelines — your backend work on real-time systems at Acme maps to what I've been shipping.
Built Hearloop on AWS with an async voice-processing pipeline and multi-tenant data isolation.
Would love to connect.
```

**Ask / hiring manager**

```
MS CS grad (ASU) — I've been building LangGraph compliance pipelines on Azure, close to the trust-and-safety problems your team owns.
Built a LangGraph and RAG ad-screening prototype with cited policy findings.
Open to 15 minutes on your calendar to review my application for Acme?
```

**Referral / JD pasted**

```
MS CS grad (ASU) with Node async job systems — your platform team's scale challenges match the audit queue I built on Render.
Cut warm SEO audits from ~24s to ~5s with BullMQ + Playwright workers.
Applied to Backend Engineer at Acme — open to a referral if you think it's a fit?
```

**Founder-cold (no JD, no metric in Line 2)**

```
MS CS grad (ASU) who builds voice and AI pipelines end to end, similar building blocks to what pharmacy call automation needs.
I like shipping real systems, not just prototypes, and want to hear more about the engineering roles at Acme.
Open to a quick chat?
```

---

## RELATED

- Full networking library (email, follow-up, alumni): `career-tools/networking/networking.md`
- Cursor skill: `.cursor/skills/linkedin-connection-note/SKILL.md`
