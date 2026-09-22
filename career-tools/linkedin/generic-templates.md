# Generic LinkedIn Connection Notes (zero-edit)

Send-as-is cold connection notes. No placeholders to fill. Pick the cell at the intersection of **company size** (row) and **recipient type** (column), copy, send.

## What these are and are not

- Built entirely on constants: who Shubh is (early-career SWE, MS in CS), and why he's reaching out (building his network + genuine interest in the kind of work, no job-ask).
- **No ask.** They do not request openings, referrals, or "keep me in mind." Research (incl. Reddit job-search threads) is clear that an opening-hunt ask in a cold note reads as needy and outsources the career-page check to the recipient.
- **No detail about the recipient**, so they cannot earn many replies. A generic note's realistic ceiling is "gets accepted, stays quiet." The only lever that converts a cold note to a reply is one specific line about the person, which by definition cannot be pre-written. For a company Shubh actually wants to work at, write a tailored note using the `linkedin-connection-note` skill instead.
- Tone tracks company size: formal (large) → warm (mid) → casual (startup).
- All notes verified <= 300 characters with a tool.

## Matrix

| Company size | Recruiter | Hiring Manager | Senior / Staff Engineer | Founder / CTO |
|---|---|---|---|---|
| **Large / MMC** | Hi, I'm an early-career software engineer with a master's in computer science. I'm building out my network with people in the industry and connecting with recruiters whose work touches the kind of engineering teams I'd like to be part of. Glad to connect. | Hi, I'm an early-career software engineer with a master's in computer science, building my network in the industry. I'm drawn to the kind of engineering work your teams do and wanted to connect. Glad to be in touch. | Hi, I'm an early-career software engineer with a master's in computer science, building my network with engineers in the field. I like learning from people doing the kind of work I want to grow into, and wanted to connect. Glad to be in touch. | Hi, I'm an early-career software engineer with a master's in computer science, building my network in the industry. I'm genuinely interested in the kind of product you're building and wanted to connect. Glad to be in touch. |
| **Mid-size** | Hi, I'm a recent CS master's grad early in my software engineering career, building my professional network. I like connecting with recruiters working in the space I'm growing into. Glad to connect. | Hi, I'm a recent CS master's grad early in my software engineering career and growing my network. The kind of work your teams take on is exactly what I'm interested in, so I wanted to connect. Glad to be in touch. | Hi, I'm a recent CS master's grad early in my software engineering career, growing my network. I enjoy connecting with engineers whose work I can learn from as I develop. Glad to be in touch. | Hi, I'm a recent CS master's grad early in my software engineering career, growing my network. The kind of company you're building is the sort I'd love to be around, so I wanted to connect. Glad to be in touch. |
| **Startup** | Hey, I'm a recent CS master's grad early in my software engineering career and building my network. Always up for connecting with recruiters in the space I want to work in. Glad to connect. | Hey, I'm a recent CS master's grad early in my career, building my network. Small teams where engineers own a lot is where I want to be, so I figured I'd connect. Glad to be in touch. | Hey, I'm a recent CS master's grad early in my career, building my network. Always keen to connect with engineers doing work I want to learn from. Glad to be in touch. | Hey, I'm a recent CS master's grad early in my career, building my network. I want to be building at the early stage, close to the product and the users, so I wanted to connect. Glad to be in touch. |

## Reference (codes + verified char counts)

| Code | Cell | Chars |
|---|---|---:|
| REC-LG | Recruiter / Large | 255 |
| REC-MID | Recruiter / Mid | 198 |
| REC-STARTUP | Recruiter / Startup | 189 |
| HM-LG | Hiring Manager / Large | 215 |
| HM-MID | Hiring Manager / Mid | 213 |
| HM-STARTUP | Hiring Manager / Startup | 183 |
| ENG-LG | Engineer / Large | 243 |
| ENG-MID | Engineer / Mid | 191 |
| ENG-STARTUP | Engineer / Startup | 167 |
| FDR-LG | Founder-CTO / Large | 223 |
| FDR-MID | Founder-CTO / Mid | 210 |
| FDR-STARTUP | Founder-CTO / Startup | 198 |

## Revision log

Use codes (e.g. HM-STARTUP) to reference a cell when testing and revising. When a cell underperforms in real use, note it here and rework that cell only.

- 2026-09-19: Initial set of 12. HM-STARTUP and FDR-STARTUP reworded to drop cliché "kind of work I'm drawn to" phrasing in favor of concrete ownership / early-stage-building reasons.

---

# Tier 2 — 10-second personalize (for targeted companies)

Use these for people at companies Shubh actually wants to work at. They are NOT zero-edit: each has ONE slot you fill from something visible on the profile in about 10 seconds (their team, product, a recent post, or their stack). The slot goes first, so the note opens with them, which is the single lever that turns a cold connect into a reply. Still no job-ask.

**Rules for the fill:**
- Fill the slot with something you can actually see at a glance and could talk about for two sentences if they reply. If you can't, use the Tier 1 generic note instead. A named thing you can't discuss is worse than no detail.
- Keep the whole note <= 300 chars. Fills are short; if a fill runs long, trim the middle, not the opener or the close.
- Never turn "I saw your team works on X" into a claim you have X experience.

| Recipient | Skeleton (fill the [slot]) | Filled example |
|---|---|---|
| **Recruiter** | Hi [Name], I saw you recruit for [team/role area]. I'm an early-career software engineer with an MS in CS, focused on that kind of work, and wanted to be connected as I job-search seriously. No ask, just glad to be in your network. | Hi Priya, I saw you recruit for backend and platform teams. I'm an early-career software engineer with an MS in CS, focused on that kind of work, and wanted to be connected as I job-search seriously. No ask, just glad to be in your network. |
| **Hiring Manager** | Hi [Name], I saw your team works on [product/area]. I'm an early-career software engineer with an MS in CS and that's the kind of problem I want to work on. Wanted to connect, no ask attached. | Hi Dan, I saw your team works on the payments platform. I'm an early-career software engineer with an MS in CS and that's the kind of problem I want to work on. Wanted to connect, no ask attached. |
| **Senior / Staff Engineer** | Hi [Name], your work on [specific thing: a project, post, or area] caught my interest. I'm an early-career engineer with an MS in CS working on similar things, and I'd value connecting to learn from how you approach it. | Hi Sara, your post on cutting eval flakiness caught my interest. I'm an early-career engineer with an MS in CS working on similar things, and I'd value connecting to learn from how you approach it. |
| **Founder / CTO** | Hi [Name], I've been following what you're building at [product/company thing]. I'm an early-career engineer with an MS in CS, drawn to that problem, and wanted to connect and follow along as you grow it. | Hi Alex, I've been following what you're building with the ambient-scribe product. I'm an early-career engineer with an MS in CS, drawn to that problem, and wanted to connect and follow along as you grow it. |

Filled examples verified 196-240 chars. Base skeletons 192-231 chars before the fill, so a fill of roughly 40-70 chars keeps it under 300.

**When to go past Tier 2:** for a top-priority target (a company you're actively applying to, or a warm/alumni connection), skip templates entirely and write a fully tailored note with the `linkedin-connection-note` skill. Tier 2 is the fast-but-real middle; a bespoke note is still the strongest.
