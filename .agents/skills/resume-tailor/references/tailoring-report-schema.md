# Tailoring report schema

> Use this schema only when the user explicitly requests a tailoring report. Never append it to a default tailoring response.

Use these headings in this order.

## Target

- Company:
- Role:
- Source JD:
- Date:

## Lane

- Selected lane:
- Routing rule:
- Source template:

## Three JD priorities

1.
2.
3.

## Experience order

For every experience role, list bullet IDs or the first eight words of each locked bullet in final order.

## Project selection

| Rank | Project | Score | Match band | Bullet count | Source |
|---|---|---:|---|---:|---|

## Skills changes

- Category order:
- Item reordering:
- Removed items:

## Gaps

| JD requirement | Available evidence | Band | Resume handling |
|---|---|---|---|

Use these definitions:

- DIRECT (90–100): the verified technology or responsibility is the same as the JD requirement.
- TRANSFERABLE (75–89): the verified underlying skill applies in a different context.
- ADJACENT (60–74): related evidence that does not satisfy the exact requirement.
- GAP (below 60): no verified supporting evidence.

## Fact check

| Claim | Source | Label | Status |
|---|---|---|---|

Use MEASURED or ESTIMATE for metrics and OK or REJECT for status. An external evidence pointer recorded in the current master is acceptable, but the report must not imply that the tailoring run independently reverified it. REJECT claims must not appear in `resume.tex`.

## Validation

- Preflight:
- Locked bullet integrity:
- eInfochips bullet count:
- Project count and distribution:
- Master files unchanged:
- LaTeX compilation:
- Page count:
- Overall result:

Never report compilation or page count as passing when no LaTeX engine ran.
