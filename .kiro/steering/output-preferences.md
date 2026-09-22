# Output preferences for career deliverables

The user does not read decision reports or process metadata. Return only the deliverable.

## Resume tailoring
- Return only the complete `resume.tex` LaTeX code.
- Do NOT print the tailoring report, priorities list, project-selection table, skills-change list, gaps table, fact-check table, or validation section.
- Still run the full resume-tailor workflow internally (preflight, lane routing, locked-bullet integrity, fact checks, verified counts). Just do not print the report.

## Application answers, LinkedIn connection notes, cover letters
- Return only the final paste-ready copy, plus its verified count (`Words: N/limit` or `Characters: N/limit`).
- Do NOT print the recipient-type/angle/evidence/omitted metadata block, evidence-ranking notes, or draft alternatives.
- Still apply the channel playbook and communication standard internally, and still verify counts with a tool before returning.

## Fixes
- When the user asks to fix something, return only the updated section (the changed bullet, the changed skills line, the changed answer, or the changed note), not the whole document again.

## Flags
- Keep any honest gap or risk warning to one or two short lines, only when it is genuinely material. Do not expand it into a full warnings section.

## What is unchanged
- Truth, fact-sourcing, locked-bullet, and length rules still apply in full. This preference changes what is printed, never what is checked.
