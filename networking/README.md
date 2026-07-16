# Networking

Outreach copy for LinkedIn, email, and follow-ups.

## LinkedIn connection note (primary)

| File | Purpose |
|------|---------|
| [`prompts/linkedin-connection-note.md`](../prompts/linkedin-connection-note.md) | Full rules: 300 chars, 3 lines, `network` / `ask` / `referral` |
| [`candidate-profile.md`](candidate-profile.md) | Metrics and project picks (synced from `gpt/`) |
| [`.cursor/skills/linkedin-connection-note/SKILL.md`](../.cursor/skills/linkedin-connection-note/SKILL.md) | Cursor skill — invoke when drafting a connection note |

**Input template:**

```
Name:
Company:
Role:
Their experience:
Intent: network | ask | referral
Reason:
Job title:          (optional; required for referral if no JD)
JD:                 (optional; paste for referral)
Ask detail:         (optional)
```

## Broader library

| File | Purpose |
|------|---------|
| [`prompts/networking.md`](../prompts/networking.md) | 20-script GPT system prompt (DM, email, follow-up) |
| [`scripts.md`](scripts.md) | Script reference templates |

## Truth sources

Never invent metrics. Use `gpt/projects/*.md` and `governance/FACT_RULES.md`.
