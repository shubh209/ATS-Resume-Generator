# Definition of Done — Before You Paste Into Overleaf

> The resume is **not done** when GPT finishes. You are the gate.

Use this checklist after every JD tailor run. All boxes must pass.

---

## 1. Tables received

- [ ] **Project Selection table** present with lane, header title, 4 projects in order, bullet counts
- [ ] **Fact Check table** present for every `\metric{}` and strong factual claim
- [ ] **No Validation Summary** unless you asked for it
- [ ] LaTeX is **sections only** (not full template)

---

## 2. Role & projects (you confirm)

- [ ] **Lane** fits the JD (or you intentionally overrode GPT’s proposal)
- [ ] **Header title** is appropriate (JD match or lane default)
- [ ] **4 projects** make sense for this JD; order supports your story in the interview
- [ ] **Demo links** present on projects that have URLs in master MD
- [ ] Spot-check: **≥75% of JD keywords** appear in the **top half** of page 1 (bullets, not Skills)

---

## 3. Fact check (you defend in interview)

- [ ] Every `\metric{}` has a **Fact Check row** with source file
- [ ] You know whether each metric is **MEASURED** or **ESTIMATE** and can explain it
- [ ] **No REJECT rows** made it into LaTeX
- [ ] No technology in **project bullets** that isn’t in master context
- [ ] Prototype projects (Compliance, etc.) aren’t framed as live customer production

---

## 4. Bullet quality

- [ ] Each bullet has plain-English **Why** — a non-technical reader understands the outcome
- [ ] Internship bullets **lead with behavior**, not OAuth/Jest/tools
- [ ] No em dash or hyphen inside bullet text
- [ ] Max **2 lines** per bullet; no orphaned short second lines
- [ ] Facts match master MD — only **wording** changed for JD

---

## 5. Overleaf

- [ ] Pasted changed sections into `templates/main.tex`
- [ ] **Compiles without errors**
- [ ] **Exactly 1 page** — if over, apply trim ladder (experience → skills → projects) and re-check

---

## 6. Optional second pass

- [ ] Run `governance/auditor-prompt.md` in a **separate** GPT chat if high-stakes application
- [ ] Log failures in `governance/feedback-log.md` (create when first failure occurs)

---

## Grade reminder (Headless Headhunter)

Interview ratio target: **1:10** (A+) to **1:25** (B). Resume quality is validated by interviews, not keyword count.
