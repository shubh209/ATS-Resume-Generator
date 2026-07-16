# GPT Builder paste bundle

Everything in this folder goes into **ChatGPT → Configure → Instructions**.

## Paste order

1. **`system-prompt.md`** — full file (includes skills list at bottom)
2. Replace placeholder **Work Experience** with contents of `work-experience.md`
3. Replace placeholder **Projects** with all 6 files from `projects/` concatenated (alphabetical order is fine)
4. Replace placeholder **LaTeX Template** with `../templates/main.tex`

## Optional (keep locally for tailoring; do not need to paste into GPT)

- `per-project-keywords.md` — project order and keyword scores per role

## Project files

| File | Resume name |
|------|-------------|
| `projects/hearloop.md` | Hearloop |
| `projects/seo-audit-engine.md` | SEO Audit Engine |
| `projects/crypto-market-simulator.md` | Crypto Market Simulator |
| `projects/distributed-caching.md` | Distributed Caching System |
| `projects/fake-review-detector.md` | Fake Review Detector |
| `projects/youtube-ads-compliance-pipeline.md` | Video Compliance Pipeline |

After editing any file here, re-paste into GPT Builder manually.

**JD tailoring:** governed by `governance/OUTPUT_CONTRACT.md` (not base variants in `per-project-keywords.md` alone — those are defaults; JD ranking may override).
