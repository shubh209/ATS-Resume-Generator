# Golden JD — AI Defense Engineer (WilmerHale, real posting)

**Use for regression:** An AI *security / defense* engineering role at a law firm (secure AI capabilities: threat modeling, guardrails, adversarial red-teaming, detections, AI incident response). Its regression value is the **adjacent-specialty gap** case: the content is AI/ML (routes to the AI lane) but the role's actual discipline is security engineering, which the candidate does not have. The system must route AI lane, surface the candidate's genuine but shallow security-adjacent evidence (app-level auth/access-control, guardrail-style evaluation) WITHOUT inflating it into security-engineering experience, and report a low, honest fit with the one-line ceiling reason. Tests resistance to turning standard secure-coding hygiene into claimed AI-defense / red-teaming / incident-response experience.
**Source:** Real WilmerHale "AI Defense Engineer" posting, Washington DC, hybrid. Captured October 2026.
**Note on seniority:** Early-career-ish (1+ year), but the gate is *specialty*, not seniority: it requires security engineering / appsec / MLOps-security experience specifically.

---

## AI Defense Engineer — WilmerHale

### Role overview

A technical contributor who helps secure AI capabilities in a global law firm. Implements practical defenses, guardrails, policy enforcement, monitoring/detections, adversarial testing, and secure operating practices for AI-enabled systems. Supports a buy-before-build strategy: evaluating, configuring, and operating commercial AI security solutions against legal-sector requirements (matter confidentiality, ethical walls, data residency, client audit).

### What you will be doing (abridged)

- **Threat modeling & risk assessment** for AI/ML systems; identify prompt injection, data leakage, jailbreaks, unsafe autonomy, vendor-AI misuse.
- **AI defense engineering**: input/output filters, policy enforcement, content-safety checks, rate limiting, abuse detection; monitor AI attack patterns via logs/telemetry/model signals; secure integration of enterprise AI (Copilot and other LLM platforms).
- **Adversarial testing & red teaming**: run prompt libraries, fuzzing harnesses, automated AI-attack tools; simulate attacker behaviors against AI endpoints/agents; track vulnerabilities and re-test.
- **Tooling & automation**: integrate AI security into SIEM, SOAR, EDR, WAF, API gateways, identity platforms.
- **Incident response & forensics for AI systems**: AI abuse, data exfiltration via AI, compromised API keys, poisoned training data; reconstruct attack paths; improve playbooks/runbooks.

### What you will bring

- Foundational ML/AI pipeline knowledge (data, training, evaluation, deployment, monitoring).
- Understanding of enterprise AI (SaaS/PaaS) deployment/governance, data handling, isolation.
- Hands-on with a major cloud (AWS/Azure/GCP); containers, Kubernetes, secrets management, CI/CD.
- Foundational security: authN/authZ, network security, data protection, logging/telemetry, secure SWE, vulnerability management.
- Familiarity with an AI framework (LangChain, Semantic Kernel, LlamaIndex), agentic/orchestration, a plus.
- 1+ years in security engineering, application security, ML/MLOps engineering, or related.

### Candidate-fit notes for regression testing

- **Expected lane:** AI Engineer by content (AI/ML systems), but this is the **adjacent-specialty-gap** edge case: the role's real discipline is security engineering, not AI engineering. The AI lane is the only one that maps the candidate's ML/LLM evidence; there is no security lane. Route AI, caveat heavily.
- **Genuine but shallow matches (do not overstate):** ML/AI pipeline knowledge is real (Video Compliance, Hearloop, Fake Review full ML lifecycle). App-level security hygiene is real and verified: Video Compliance (Microsoft Entra ID / JWT, SHA-256 API-key hashing, CORS allowlist, Postgres-backed rate limiting — from its master Auth & Security line), Hearloop (HMAC webhook signatures, SSRF protection, partner-scoped multi-tenant isolation), eInfochips (RBAC, input validation, transactions, CloudWatch audit logging). Evaluation/guardrail framing (golden-dataset eval) maps loosely to "guardrails." Observability (Prometheus/Grafana/OTel/Jaeger, Azure Monitor) maps to "telemetry/detections" at a basic level.
- **The decisive gap (point of this fixture):** NO security-engineering experience. The candidate has not done threat modeling, adversarial testing / red teaming, prompt-injection/jailbreak testing, AI abuse detection, SIEM/SOAR/EDR/WAF integration, or AI incident response / forensics. These are the core of the job. App-level auth/access-control hygiene is NOT the same as AI-defense security engineering and must not be presented as such.
- **Real gaps to handle honestly (do NOT claim):** AI red teaming / adversarial testing, prompt-injection/jailbreak defense, threat modeling, SIEM/SOAR/EDR/WAF, AI incident response/forensics, poisoned-training-data defense, Kubernetes, secrets-management platforms, security-engineering tenure, legal-sector security requirements (ethical walls, matter confidentiality).
- **Title handling:** header uses the exact JD title "AI Defense Engineer" per the title rule, BUT flag prominently that this title claims a security-defense identity the candidate does not hold; recommend the user consider overriding to "AI Engineer." Work-history stays plain Software Engineer / Software Engineer Intern.
- **Tailoring behavior to test:** route AI lane, surface the real auth/access-control + ML-pipeline + observability evidence, map it to the role's "guardrails / telemetry / secure integration" language where honest, and REPORT a low fit (well below 85) with the one-line reason "security-engineering specialty role; candidate has app-level security hygiene and ML-pipeline knowledge but no AI-defense / red-teaming / incident-response experience." Do not loop toward 85; do not inflate hygiene into security engineering.
- **Application-fit assessment:** Low / wrong-specialty. The candidate can honestly speak to secure-coding basics and ML pipelines, but the security-engineering core (threat modeling, red teaming, detections, IR) is absent. The correct output tells the user this is likely the wrong role to spend an application on, rather than overselling adjacent evidence.

