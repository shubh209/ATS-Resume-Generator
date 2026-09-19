---
name: linkedin-connection-note
description: >-
  Generate humanized LinkedIn connection notes for Shubh Kapadia under 300
  characters and exactly 3 lines. Use when the user wants a connection note,
  LinkedIn connect message, networking outreach, referral ask, or provides
  Name, Company, Role, experience, and intent network or ask.
---

# LinkedIn Connection Note

Generate a **3-line**, **≤300 character** LinkedIn connection request note for Shubh Kapadia.

## Before writing

1. Read `career-tools/linkedin/linkedin-connection-note.md` (full rules)
2. Read `career-tools/linkedin/candidate-profile.md` (metrics and project picks)
3. If referral intent or JD pasted, read relevant `resume-system/facts/projects/*.md` for accurate metrics
4. Apply `career-tools/reference/humanizer.md` to the final 3 lines

## Required user inputs

Refuse to generate until you have:

- Name, Company, Role, Their experience (blurb)
- **Intent:** `network` | `ask` | `referral`
- **Reason** (why reaching out)

For **referral:** also require **JD paste** or **Job title**.

Optional: `Ask detail` (overrides Line 3), `Job title` (sharpens ask).

## Structure (no greeting)

| Line | Content |
|------|---------|
| 1 | Who Shubh is — tie MS CS ASU / SWE background to their role at Company |
| 2 | **Warm recipient:** one project + one metric from master context, mapped to their work or JD. **Cold recipient (founder/stranger, no JD):** plain capability statement, no metric — see Cold Outreach rules in `career-tools/linkedin/linkedin-connection-note.md` |
| 3 | Ask per intent (see prompt file) |

## Defaults

- **network** → Line 3: `Would love to connect.`
- **ask** → Line 3: 15 minutes on calendar to review application for [Company]
- **referral** → Line 3: applied to [role] — open to referral if fit
- **founder-cold** → Line 3: `Open to a quick chat?` — for founders/startups reached cold (LinkedIn, YC message)
- **No OPT/H1-B** in the 300-char note
- **No demo/portfolio links** in the note (character budget)
- **No bare metric with no context in a cold note** — run the metric legibility check (`resume-system/governance/FACT_RULES.md`) before using any number in Line 2

## Output

Use the format in `career-tools/linkedin/linkedin-connection-note.md`:

- Metadata (intent, project, metric label)
- `--- COPY BELOW ---` block with exactly 3 lines
- `Characters: N/300` — must be ≤300; rewrite until compliant

## Do not

- Use stale metrics from old networking drafts (80+ ads/hr, 91.3% F1, etc.)
- Claim production customers for prototype projects
- Add a fourth line or "Hi [Name]," greeting
- Output two asks in Line 3
