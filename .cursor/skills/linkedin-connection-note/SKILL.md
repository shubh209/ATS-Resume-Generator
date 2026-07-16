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

1. Read `prompts/linkedin-connection-note.md` (full rules)
2. Read `networking/candidate-profile.md` (metrics and project picks)
3. If referral intent or JD pasted, read relevant `gpt/projects/*.md` for accurate metrics
4. Apply `reference/humanizer.md` to the final 3 lines

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
| 2 | One project + one metric from master context, mapped to their work or JD |
| 3 | Ask per intent (see prompt file) |

## Defaults

- **network** → Line 3: `Would love to connect.`
- **ask** → Line 3: 15 minutes on calendar to review application for [Company]
- **referral** → Line 3: applied to [role] — open to referral if fit
- **No OPT/H1-B** in the 300-char note
- **No demo/portfolio links** in the note (character budget)

## Output

Use the format in `prompts/linkedin-connection-note.md`:

- Metadata (intent, project, metric label)
- `--- COPY BELOW ---` block with exactly 3 lines
- `Characters: N/300` — must be ≤300; rewrite until compliant

## Do not

- Use stale metrics from old networking drafts (80+ ads/hr, 91.3% F1, etc.)
- Claim production customers for prototype projects
- Add a fourth line or "Hi [Name]," greeting
- Output two asks in Line 3
