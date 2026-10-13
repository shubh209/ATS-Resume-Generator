# Workspace Instructions

This repo produces career deliverables from locked-fact masters. Each task below has one authoritative skill that defines exactly which context files to read and what to output. Before acting on a request, match it to the table and read that skill's `SKILL.md` first. Read only the files that skill routes you to — do not scan the repo for context.

## Task router

| When the user asks for... | Read and follow |
|---|---|
| Tailor, match, optimize, or adapt a resume to a JD, or supplies a JD for resume work | `.agents/skills/resume-tailor/SKILL.md` |
| A cover letter, application letter, or short tailored letter | `.agents/skills/cover-letter/SKILL.md` |
| YC or Wellfound startup application introductions (including Wellfound's company-interest field), founder/teammate LinkedIn connection notes tied to a startup opening, or company LinkedIn job messages | `.agents/skills/startup-job-messages/SKILL.md` |
| A LinkedIn connection note or outreach note from a person's profile without startup job context | `.agents/skills/linkedin-connection-note/SKILL.md` |
| Application / supplemental questions (Greenhouse, Lever, Workday, portals, fit, motivation, behavioral) | `.agents/skills/application-answers/SKILL.md` |

Each skill is authoritative for its task. When a request spans two tasks (e.g. "tailor my resume and answer these questions"), run each matching skill in turn, not a blended improvisation.

## Shared rules (apply to every task)

- The skill's Route section is the complete context list. If the information you need is not reachable from that list, ask rather than scanning the repo.
- `resume-system/governance/FACT_RULES.md` governs all facts, metrics, bullet wording, bullet rewriting, and prototype framing. It outranks any skill on fact and truth questions.
- Treat older prompt copies, legacy resume skills, golden JDs, career stories, session history, and master-maintenance workflows as out of scope unless the user explicitly asks to update those sources.
- `.kiro/steering/output-preferences.md` and `.kiro/steering/fit-scoring.md` govern what is printed and how deliverables are scored. Honor them on every task.

## Standing defaults

Confirmed behavioral defaults. Apply them without re-asking unless the user overrides them for a specific request.

1. **Never save output** unless the user explicitly asks. Deliverables live in the chat, not on disk.
2. **The JD is the source of truth for company facts.** Do not browse the web to verify a company claim unless asked.
3. **Route the lane (Full Stack / Backend / AI) silently** from the JD when the user does not name one. Do not stop to confirm it.
4. **ESTIMATE-labeled metrics are usable** when their master authorizes them. Do not warn on each use.
5. **No stated length limit means choose the length** — shorter and tighter over hitting a ceiling.
6. **"Fix this" returns only the changed section**, not the whole document. Do not re-verify resume page fit for a snippet-level fix.
7. **`archive/` and `docs/superpowers/` are out of scope** — never read them for facts.
8. **Ask before writing to the keyword-gaps ledger** (`resume-system/reference/keyword-gaps.md`). Reading it is fine; present the proposed entry or recurrence notice and write only after the user approves. This overrides any silent-write authorization in the resume-tailor skill.
9. **Titles mirror the JD's title, not the duties.** Header = the exact JD role title verbatim (e.g. "Software Development Engineer 1"); fall back to the lane name only if the JD names no clean title. DAS/eInfochips employment titles mirror the JD title's family: Backend/Full Stack when the JD title uses it, else the SE/SDE form matching the JD's wording ("Software Engineer" and "Software Development Engineer" are the same; use the JD's word). Retain Intern/volunteer status.

## Pre-send checklist (run before returning ANY deliverable)

Re-read the relevant skill/rule files for the task before producing output — do not run from memory. Then check the deliverable against every item below before sending. These are the mistakes that recur; a visible check beats recall.

1. **Resume bullets follow What + How + Where + Why, in that order** — open on what was built and how (tech), give the context, and close on a plain, non-technical business/human reason. The Why is never dropped and never written as jargon. Leading with the Why is wrong; the Why closes the bullet.
2. **Application answers are ≤120 words** (unless a portal states a limit) and in the candidate's recorded voice from `candidate-voice.md` — short, plain, human. "No stated limit" does NOT mean write long.
3. **Header title = the exact JD role title, verbatim**; DAS/eInfochips employment titles mirror the JD title's family (Backend / Full Stack / SE = SDE), per Standing default 9.
4. **Project and experience counts match the lane:** AI = 4 projects at 3/2/2/1 and experience 3/2/2; Full Stack & Backend = 3 projects at 3/2/2.
5. **Every word/character count is verified with a tool**, never asserted from estimate.
6. **No task-specific style instruction crosses tasks.** A style request given for an application answer (or any one task) never changes resume bullet wording; resume bullets always follow item 1 regardless of other instructions in the same message.

## Layout

All skills live under `.agents/skills/`: `resume-tailor`, `cover-letter`, `linkedin-connection-note`, `application-answers`, `startup-job-messages`. New skills go in the same directory and get a row in the task router above.
