# Golden JD — Machine Learning Engineer (XPO, real posting)

**Use for regression:** MLOps / ML-infrastructure engineering role at a large logistics company. This is the AI lane's hard, weak-fit edge case: the work is ML *infrastructure and operations* (data-prep/validation tooling, training/eval/deployment infra, CI/CD for models, drift detection, model serving), NOT the LLM/RAG/agent *application* work the AI lane normally leads with. Its regression value is testing that the system routes honestly, maps only transferable evidence, and reports the MLOps gaps instead of inflating the candidate into an experienced ML-infra engineer.
**Source:** Real XPO "Machine Learning Engineer - Hybrid" posting, Boston MA, Req 389274. Captured September 2026.
**Note on seniority:** Minimum is 1 year of software/ML engineering with hands-on data-pipeline/ML-infra/MLOps work; an M.S. and 3+ years ML-infra-at-scale are preferred. The candidate is early-career with no production MLOps role, so this sits at or slightly below the stated minimum on the MLOps-specific experience. Treat as a stretch application; do not manufacture MLOps seniority.

---

## Machine Learning Engineer — XPO

### Company overview

XPO is a top-ten global transportation and logistics provider with an integrated network of people, technology, and physical assets. The ML org builds infrastructure and tooling that moves applied/data-science models from experimentation into reliable production. Boston, MA; hybrid. Annual salary range $100,000–$120,000, incentive-eligible. Pre-employment drug test may apply.

### Job overview

A Machine Learning Engineer builds and maintains the data-preparation and validation tooling, ML training/evaluation/deployment infrastructure, CI/CD for models, and monitoring/drift/feedback-loop systems that let applied and data scientists productionize models reliably. The role partners closely with data science and data engineering teams. The emphasis is MLOps and ML platform work, not building LLM/agent product features.

### What you'll do

- Build and maintain data-preparation and validation tooling to ensure high-quality inputs for ML and optimization models.
- Design and implement ML infrastructure for model training, evaluation, and deployment.
- Build and maintain CI/CD pipelines for ML models, including automated testing and validation.
- Implement model monitoring, drift detection, and feedback loops to track production model performance.
- Partner with applied/data scientists to productionize models and streamline experimentation-to-deployment.
- Collaborate with data engineering teams on reliable, accessible data pipelines.
- Contribute to shared MLOps tooling and best practices across the AI/ML org.

### What you have

- Bachelor's in CS/Engineering or related, or equivalent experience.
- 1 year in software or ML engineering, including hands-on data pipelines, ML infrastructure, or MLOps tooling.
- Experience building data preparation, validation, or quality-checking tooling for ML pipelines.
- Proficiency in Python and SQL.
- Experience with cloud data/ML platforms (AWS, GCP, BigQuery).
- Strong collaboration with data science / applied science and data engineering teams.

### Preferred

- M.S. in CS or related.
- 3+ years building ML infrastructure for training, evaluation, and deployment at scale.
- CI/CD for ML models; model serving and inference infra (batch and real-time); model monitoring, drift detection, feedback-loop tooling; Docker/Kubernetes; data-pipeline reliability partnership.

### Candidate-fit notes for regression testing

- **Expected lane:** AI Engineer, as filed, but this is the lane's weakest-fit edge. The routing is defensible because the role is ML-centric and the AI lane carries the only ML/eval/data-pipeline evidence; however, the role is MLOps/ML-platform, not LLM/RAG/agent application work, so the usual AI-lane strength (Video Compliance orchestration) is only partially relevant. A reasonable alternate is Backend (the role is heavily infrastructure/pipeline/CI-CD). Record the lane and the tension.
- **Strongest honest matches (DIRECT):** Python and SQL (verified across projects, ASU, Fake Review). Data-preparation/validation tooling — ASU's Python/SQL automated data-validation pipeline that flags questionable records for human review is the single closest match to "data preparation, validation, or quality-checking tooling for ML pipelines." DAS's PostgreSQL ingestion/traceability pipeline on Azure is transferable data-pipeline evidence.
- **Evaluation evidence (TRANSFERABLE):** Video Compliance's 104-case golden evaluation dataset with holdout testing maps to "model training, evaluation" and automated validation — but it is LLM-output evaluation, not classical model training/serving infra. Frame as evaluation-harness discipline, not production ML-training-infra experience.
- **CI/CD (TRANSFERABLE, not model-specific):** GitHub Actions CI/CD with a pytest gate (Video Compliance), Docker/GitHub Actions deploys (Hearloop) map to "CI/CD pipelines" generally. The JD wants CI/CD *for ML models* specifically; the candidate has CI/CD for services, which is adjacent, not direct. Do not claim model-CI/CD experience.
- **ML/model evidence:** Fake Review Detector (fine-tuned transformers in PyTorch/Hugging Face on 608k reviews) is the only real "train a model" evidence. It covers model building; it does not cover production serving, drift detection, or feedback loops.
- **Observability (ADJACENT to model monitoring):** Prometheus/Grafana/OpenTelemetry (ClusterOps, Distributed Caching), Azure Monitor (DAS), CloudWatch (eInfochips) cover system/service monitoring. The JD asks for *model* monitoring and *drift detection*, which the candidate has NOT done. System observability is adjacent, not the same thing. Do not present service monitoring as model-drift experience.
- **Real gaps to handle honestly (do NOT claim):** model serving / inference infrastructure (batch or real-time); model monitoring, drift detection, feedback-loop tooling; CI/CD specifically for ML models; ML infrastructure at scale; BigQuery; Kubernetes (Docker is verified, K8s is not); GCP (AWS and Azure are verified, GCP is not); 3+ years ML-infra; partnering with data-science teams in a production MLOps setting.
- **Eligibility / logistics:** Hybrid in Boston, MA — a location gate. Flag if the candidate is not Boston-based or open to relocation. Possible pre-employment drug test.
- **Tailoring behavior to test:** Route to AI lane but lead with the data-validation/data-pipeline evidence (ASU, DAS) and the one real model-training project (Fake Review), use Video Compliance's eval harness as evaluation discipline rather than ML-training infra, and REPORT the MLOps-specific gaps (model serving, drift detection, model CI/CD, Kubernetes, GCP/BigQuery) rather than reframing adjacent service work as held MLOps experience. The correct output is honest and gap-flagged, not a confident MLOps resume.
- **Application-fit assessment:** Weak-to-moderate honest fit. Clears Python/SQL and data-validation/data-pipeline tooling on transferable evidence, and has one genuine model-training project. Genuine gaps across the core MLOps surface (serving/inference infra, drift detection, feedback loops, model-specific CI/CD, Kubernetes, GCP/BigQuery, ML-infra-at-scale) and a Boston location gate. The system should surface this as a stretch application and not disguise the MLOps experience the candidate does not have.

</content>
</file>
