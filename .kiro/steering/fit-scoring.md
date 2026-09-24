# Fit-scoring workflow for resume tailoring

When the user asks to tailor a resume and score it (or says "score", "fit", "loop to 85"), run this alongside the resume-tailor skill. This governs the score only; all resume-tailor and FACT_RULES rules still apply in full.

## What the score measures

Honest coverage of the JD's stated requirements and responsibilities by the tailored resume, where "covered" means backed by a verified master (locked bullet, `work-experience.md`, or a current selectable `projects/*.md`). Not keyword-stuffing. Not hypothetical-if-the-candidate-learned-it.

## Components and weights

- **Must-have requirements coverage — 45%.** Required qualifications / core skills. Band each DIRECT (verified, same tech or responsibility) = full, TRANSFERABLE (same underlying skill, different tool/context) = partial, GAP = zero.
- **Responsibilities match — 30%.** The JD's listed duties. Credit when verified evidence shows that *kind of work* even if the JD's wording differs. Meaning-match beats word-match. This is where JD wording may be mirrored in the flexible part of a bullet.
- **Preferred / nice-to-have coverage — 15%.** Same DIRECT/TRANSFERABLE/GAP banding, lower stakes.
- **Seniority & eligibility fit — 10%.** Years/level, degree, and hard gates (location, enrollment, work authorization). A failed hard gate caps this component at zero and must be flagged, since it can make true odds near zero regardless of the rest.

## Honesty caps (override the math)

- Score reflects only what verified masters support. No credit for reworded-to-imply or claimed-but-unheld skills.
- The score cannot be raised by any move that breaks a locked bullet, invents a metric, or claims an unheld skill.
- If honest tailoring cannot clear 85%, report the ceiling score once, give a one-line reason it cannot go higher, and stop. Do not loop toward 85 by cheating.

## Protected vs flexible when tailoring to raise the score

- **Protected, never cut or weakened to hit a number:** the business / "why it mattered" reason in each bullet, locked wording, metrics, employment facts. Cutting the business reason first is a known past failure mode; do not repeat it.
- **Flexible:** lane choice, project selection/order, bullet order, skills ordering and evidence-backed relabeling, header title, and mirroring JD wording in the non-locked part of a bullet.
- When a bullet must shrink, cut lower-value technical detail first, per FACT_RULES `Bullet compression`.

## Output contract

- Per iteration: return only `Fit: N%`. No report, no justification (per output-preferences), except the one-line ceiling reason when a JD cannot clear 85%.
- Full `resume.tex` only on the converged/final version (cleared 85%, or hit its honest ceiling and the user accepts it).
- After a final, if the user asks for changes, return only the changed LaTeX section.

## Honesty about the score itself

The score is a calibrated estimate from a language model, not a deterministic measurement. Keep the rubric and banding fixed so scores are comparable run-to-run, but treat small differences (e.g. 78 vs 82) as noise and large ones (88 vs 65) as signal. 85 is a go/no-go threshold, not a precise target.
