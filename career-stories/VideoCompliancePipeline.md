# Video Compliance Pipeline — Engineering Story Bank

Personal reference, not a script. Purpose: recall real, defensible engineering episodes from this project before an interview or when answering application questions, without inventing anything. Every episode is grounded in a commit, code comment, or file. Items marked **[UNVERIFIED — confirm]** were not independently corroborated and must be confirmed before stating as fact.

Source note: this project had no raw chat-transcript store. Episodes below are grounded in git commits, code comments, and one in-session reversal recorded in commit bodies. Mined from the project's own build history and cross-checked against `resume-system/facts/projects/youtube-ads-compliance-pipeline.md`.

## Never-claim guardrails (carry into any answer)
- The v2 evaluation rounds were run and prompt fixes applied **manually**, not by an autonomous self-improving loop. Do not describe a "champion loop" as an autonomous system.
- Do not claim accuracy above the recorded 88.2% on unseen holdout cases. The 93.3% improvement-set number is measured on tuning cases and must not be presented as generalization.
- This is a working prototype for demos and interviews, not a live customer rollout.

---

## Evals

### The false-positive problem and the two-round fix (strongest eval story)
- **What happened:** The champion baseline caught violations but over-flagged compliant ads. Baseline was 76.9% accuracy (80/104) with a 68.8% false-positive rate; it recognized only ~31% of compliant ads.
- **Method:** Ran the 104-case golden dataset v2, measured per-category accuracy, FP, and FN; root-caused the over-flagging to the GPT-4o reasoning prompt penalizing hedged/qualified language. Round 1: added an explicit "DO NOT FLAG" section of 10 compliant patterns to the reasoning prompt. Round 2: added an ad-level disclosure rule that scans all claims for a material-connection phrase before flagging.
- **Outcome:** Round 1 took the improvement set to 93.3% (from 72.5%) and FP to 9.1% (from 73.7%); holdout reached 88.2% with 0% false positives, though FN rose to 12% on 3 cases. Round 2 brought the disclosure category to 93.3% (14/15), 0% FP, with no holdout regression.
- **Evidence:** commits 9c777e3 (baseline), 1a3f046 (round 1), fb4e983 (round 2).
- **Confidence:** VERIFIED. Manual rounds — not autonomous.

---

## Debugging episodes

### Eval cases hung because SIGALRM couldn't interrupt blocking LLM I/O
- **What happened:** Eval cases hung indefinitely (30+ min each).
- **Method:** First mitigation added a 90s SIGALRM per case; later found SIGALRM does not fire on blocking network calls, so it never interrupted the LLM I/O. Replaced it with a ThreadPoolExecutor timeout.
- **Outcome:** After the thread-based timeout, no case could hang beyond the limit; 5 cases completed in <90s total instead of hanging.
- **Evidence:** commit f8f7730; commit 1a3f046 body ("replace broken SIGALRM with ThreadPoolExecutor").
- **Confidence:** VERIFIED.

### Azure Whisper transcription timed out, breaking the E2E path
- **What happened:** Azure Whisper timed out, breaking end-to-end runs.
- **Method:** Switched transcription to Groq Whisper (whisper-large-v3-turbo) when GROQ_API_KEY is set, Azure as fallback; verified with an E2E run.
- **Outcome:** ~2s transcription vs timeout; E2E test 2.9s, sample ad returned PASS and saved.
- **Evidence:** commit 44c07de.
- **Confidence:** VERIFIED.

### Langfuse CallbackHandler v4 blocked startup when its host was unreachable
- **What happened:** Pipeline startup blocked on Langfuse init when the host couldn't be resolved.
- **Method:** Disabled Langfuse to unblock; later root-caused to host resolution and re-enabled by setting LANGFUSE_HOST from config before init.
- **Outcome:** Re-enabled with tracing confirmed; E2E 2.7s with no blocking.
- **Evidence:** commit 44c07de; commit 09c780f.
- **Confidence:** VERIFIED.

### Phi-4-mini broke after the Azure AI Foundry endpoint domain changed
- **What happened:** Phi-4-mini calls failed after the endpoint domain changed.
- **Method:** Migrated PHI4_ENDPOINT from .services.ai.azure.com to .cognitiveservices.azure.com.
- **Outcome:** Fixed as part of the same E2E-verified change.
- **Evidence:** commit 44c07de body.
- **Confidence:** VERIFIED.

### Reindexing risked mixing embedding spaces
- **What happened:** Changing the embedding endpoint risked an embedding-space mismatch on reindex.
- **Method:** Adopted wipe-and-replace on reindex (delete all docs before adding new); recorded versioned namespacing as future scope (FS-6).
- **Outcome:** Wipe-and-replace in place; versioned namespacing deferred.
- **Evidence:** commit 31dffc8; src/services/policy_indexing.py:125.
- **Confidence:** VERIFIED.

### URL-path indexer ran redundantly on the upload path
- **What happened:** index_video_node ran even when the worker had already provided a transcript on the upload path.
- **Method:** Skipped index_video_node when the transcript is pre-provided.
- **Outcome:** Redundant indexing removed for the upload path.
- **Evidence:** commit 8760798.
- **Confidence:** VERIFIED.

### Blob downloads failed on public URL
- **What happened:** Blob downloads failed when using a public URL; switched to downloading via connection string.
- **Evidence:** commit 3a29b8e.
- **Confidence:** [UNVERIFIED — confirm]. Kept at user request; confirm the details before stating in an interview.

---

## Tradeoffs & reversals

### Family-framing disclosure attempt, reverted
- **What happened:** Tried to catch a family-vlog undisclosed-sponsorship case by adding family/group endorsement framing to the disclosure rule.
- **Method:** Added the framing, measured category impact; it regressed the disclosure category and still missed the target case, so it was reverted.
- **Outcome:** Regressed the category to 80%; reverted and left for a future round. Good "knew when to roll back" story.
- **Evidence:** commit fb4e983 body.
- **Confidence:** VERIFIED.

### Two-model split for cost
- **What happened:** Chose Phi-4-mini for claim extraction/synthesis and GPT-4o only for reasoning, to reduce cost.
- **Evidence:** commit 24ec8af.
- **Confidence:** VERIFIED.

### Firecrawl /extract over /scrape
- **What happened:** Chose structured /extract (per-rule JSON) over /scrape despite ~30 credits/URL vs 1, because per-rule chunks enable filtered search. Documented upgrade path (batch_scrape + LLM extraction) if credit cost becomes prohibitive.
- **Outcome:** 35 URLs x 30 = 1,050 credits per reindex, accepted.
- **Evidence:** src/services/policy_fetcher.py:50-53.
- **Confidence:** VERIFIED.

### Text-based reports instead of true PDF
- **What happened:** Generated text-based reports to avoid adding a PDF-rendering dependency. Documented ceiling (no styling) and upgrade path (reportlab/weasyprint).
- **Evidence:** src/services/report_generator.py:91-94.
- **Confidence:** VERIFIED.

### O(n^2) claim grouping to batch GPT-4o calls
- **What happened:** Grouped claims sharing policy chunks into fewer GPT-4o calls with an O(n^2) overlap check. Documented ceiling (>50 claims per video) and upgrade path (hash-based grouping or single call under a threshold).
- **Evidence:** src/services/compliance_auditor.py:285-288.
- **Confidence:** VERIFIED.

---

## Gaps (no defensible evidence in this project)
- **agent_error:** No captured episode of an AI coding agent producing wrong code that was caught/corrected. No chat-transcript store exists.
- **collaboration:** Solo build; no recorded disagreement or review back-and-forth.
