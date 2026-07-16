# Golden JDs — Regression Test Inputs

Use these saved job descriptions to verify tailoring behavior after prompt or governance changes.

## How to test

1. Paste `gpt/system-prompt.md` + master context into GPT Builder (or use Cursor with `@governance/OUTPUT_CONTRACT.md`).
2. Paste one golden JD below.
3. Add: `Tailor per governance/OUTPUT_CONTRACT.md`
4. Verify output against `governance/DEFINITION_OF_DONE.md`.

## Expected lane per file

| File | Expected proposed lane | Notes |
|------|------------------------|-------|
| `full-stack-software-engineer.md` | Full Stack | React/Node/SQL/AWS |
| `backend-software-engineer.md` | Backend | Go/gRPC optional boost for Distributed Caching |
| `ai-software-engineer.md` | AI Engineer | LangGraph/RAG/LLM; ASU 3rd bullet candidate |

## Pass criteria (quick)

- [ ] Project Selection + Fact Check tables present
- [ ] No Validation Summary unless requested
- [ ] LaTeX sections only
- [ ] Lane and projects plausible for JD
- [ ] No REJECT facts in LaTeX
- [ ] Compiles to 1 page in Overleaf

Log failures in `governance/feedback-log.md`.
