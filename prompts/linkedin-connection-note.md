# LinkedIn Connection Note Generator

> **Scope:** LinkedIn connection request note only. 300 character **hard limit**. Exactly **3 lines**.  
> **Truth:** `networking/candidate-profile.md` + `gpt/projects/*.md` + `governance/FACT_RULES.md`  
> **Humanizer:** Apply `reference/humanizer.md` before final output.

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

If `Ask detail` is provided, use it as Line 3 (still ≤300 chars total).

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

1. Read `networking/candidate-profile.md` for quick mapping.
2. Confirm metric in source `gpt/projects/<file>.md`.
3. **MEASURED** and **ESTIMATE** metrics allowed if labeled in project MD.
4. **Referral + JD pasted:** pick project using JD keyword overlap (same spirit as `governance/OUTPUT_CONTRACT.md`).
5. **Recruiter vs engineer:** same 3-line structure; only Line 3 wording changes (referral vs calendar ask).

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

---

## EXAMPLES (structure only — personalize every time)

**Network / engineer**

```
MS CS grad (ASU) building voice + AI pipelines — your backend work on real-time systems at Acme maps to what I've been shipping.
Built Hearloop on AWS: 200 concurrent users at 149ms p95 in load tests.
Would love to connect.
```

**Ask / hiring manager**

```
MS CS grad (ASU) — I've been building LangGraph compliance pipelines on Azure, close to the trust-and-safety problems your team owns.
Indexed 37 policy chunks with RAG for ad screening prototypes.
Open to 15 minutes on your calendar to review my application for Acme?
```

**Referral / JD pasted**

```
MS CS grad (ASU) with Node async job systems — your platform team's scale challenges match the audit queue I built on Render.
Cut warm SEO audits from ~24s to ~5s with BullMQ + Playwright workers.
Applied to Backend Engineer at Acme — open to a referral if you think it's a fit?
```

---

## RELATED

- Full networking library (email, follow-up, alumni): `prompts/networking.md`
- Cursor skill: `.cursor/skills/linkedin-connection-note/SKILL.md`
