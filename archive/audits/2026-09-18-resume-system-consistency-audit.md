# Resume System Consistency Audit

## Executive Summary

- Total discovered files: **239**
- Total reviewed files: **111**
- Total excluded files: **125**
- Total binary files: **3**
- Total unreadable files: **0**
- Coverage: **100.00%**
- Findings by type: **9 CONTRADICTION**, **4 UNSUPPORTED CLAIM**, **7 RULE VIOLATION**
- Findings by severity: **8 CRITICAL**, **6 HIGH**, **4 MEDIUM**, **2 LOW**
- Questions requiring user decisions: **5**
- Authoritative-source contradiction present: **YES** — `gpt/work-experience.md` gives two current DAS titles, while `gpt/projects/hearloop.md` marks two AI bullet versions current.
- Can active tailoring currently produce a false claim: **YES** — selectable locked project bullets contain unsupported realized outcomes, one project has no locked bullet bank, and the current preflight does not test those conditions.

The dominant failure mode is not harmless tailoring variation. It is duplicated, still-runnable instruction and fact material that disagrees about whether bullets may be rewritten, how many projects to use, what output to produce, and which outcomes were actually realized. Several official or selectable bullets describe customers, users, retention, savings, or deployment beyond the evidence recorded in the same master files.

## Audit Metadata

- Audit date: 2026-09-18
- Repository: `/Users/shubhkapadia/Desktop/Applications/ATS Resume Generator`
- Audit basis: current working tree only
- Internet/external repositories: not used
- Report path: `audits/2026-09-18-resume-system-consistency-audit.md`
- Method: exhaustive filesystem inventory; authority-first review; line-addressed claim comparison; initial/final SHA-256 integrity check

## Initial Working-Tree Baseline

Baseline captured before this report was created.

- Discovered files (excluding `.git/**` and excluding this subsequently created report): **239**
- Initial in-scope source-set aggregate SHA-256: `88a71f2070ebee4a800136dced90323d56b9fedd858c5b2e30333d858cf9881d`
- Initial per-file SHA-256 ledger (111 reviewed source files):

```text
44a5baf6fd28f43d1833412318fd4d9eff07614a429f59d9b0266553f7a24673  ./.agents/skills/resume-tailor/SKILL.md
0894f76b1d960db0fe4d7c6ac782efbbeb8f440baac6f590adfbbd10e53cb3f3  ./.agents/skills/resume-tailor/agents/openai.yaml
c20470b38cf8b9f687013857bced2ee751c2df24cd7ddf7e22d0c56c2977bf69  ./.agents/skills/resume-tailor/references/tailoring-report-schema.md
99e131a6683380704da58a17eae55dad2f66dce14d43f3cd5bc0a4802e6f88f7  ./.agents/skills/resume-tailor/scripts/preflight.py
78c8ea1403917ca107724bdd39aca4406aac6d3a371931d6538e917252fc937f  ./.cursor/skills/application-answers/SKILL.md
af440350684aa16ba19dc144229edebd6e6560484f91014f523246d33e464481  ./.cursor/skills/fullstack-resume-tailor/SKILL.md
73e25c0f128a25a45ef4ed5057c569ba75fadeaf5ff135b4f82a3deca33b75f5  ./.cursor/skills/linkedin-connection-note/SKILL.md
75ef56befa53cb05d8e64eff6c7aeb9e43e3924b8db9e0782b5a202f9e9f965f  ./AGENTS.md
138597e7a2af9ba8d1f95dc6ad89193fd79d17bb324cefad6130d43ce69cf881  ./Amazon-LP/AGENTS.md
c5fea417c9d6c5cbbef3751b4f0e2cc29ba0d0812080daae890636368082c09c  ./Amazon-LP/AMZ/LLD/AmazonLockerMinimalInterview.java
6a80b97c7bb935c6a96deab91e0eb3cfce8d2383a572fcb829e4062950f83ac9  ./Amazon-LP/AMZ/LLD/ParkingLotSingleFloorArticleStyle.java
98e4097f0d5a4edce46ae3bc59862d70aa249c21fa3eb6f3cab4f1e6d358d8a4  ./Amazon-LP/AMZ/LLD/amazon_lld_interview_cplusplus_guide.md
8e7d7bb3dfa93ab4631d8618ef09ecf3c271c1d0103c70d21f5d5a9759764dc4  ./Amazon-LP/AMZ/LLD/amazon_locker_ready_to_speak_script.md
5433be27a574f4c0c4c7b554267c8ae00ec6812db13acf9a382f13f889ae34d6  ./Amazon-LP/AMZ/LLD/atm_article_based_ready_to_speak_script.md
0f4a25b9f3f1ba7d41319c80fc2e51e9a9e0270d0a384840de11f0f50eb60321  ./Amazon-LP/AMZ/LLD/parking_lot_single_floor_article_style_script.md
ccc45a7c67d841bb699562cca2774383d7d1a0eabf2ff310a8ee192ee6c67e55  ./Amazon-LP/AMZ/LeetCode DSA/1. Thirty Days.csv
cc856af359c717d1b8833089ed023fc5b67eb922e34fd65713136d9341c822fe  ./Amazon-LP/AMZ/LeetCode DSA/leetcode_amazon-thirty-days_07162026.csv
c506718612f8b836e460df129cd54d15a77c80f3b0b98d74b5708dfc54cb9811  ./Amazon-LP/AMZ/LeetCode DSA/leetcode_amazon-thirty-days_Final_Dhyan.csv
82e0c82c0d95603da56d9a53b85e5cfdb8ff6a6d990700db42d63ae433ac948c  ./Amazon-LP/AMZ/STAR and LPS/Dhyan_Database_Resume_Interview_Scripts_All_5.txt
0b8b8f5c1b9dbcf56e9a2e6855579e4e80e8c23daf917ffa4d70bef492ea8d49  ./Amazon-LP/AMZ/STAR and LPS/Intro and why amazon.txt
04d47f38d93c260a4238593438429acc88d2e818db1b34d642d1e0975020c777  ./Amazon-LP/AMZ/STAR and LPS/Sportlingo_Android_3_8_Auth_Incident_STAR.txt
0e835430529c6ecde05c47cf3d2a389387f8ecdf23b370805c79d8e8fcd5d374  ./Amazon-LP/AMZ/STAR and LPS/TrustMed_Neo4j_FAISS_Disagreement_STAR.txt
f99cfdd232385ab26e224bf6d4a56c21b8124321d6959908d1bd15ff78ea6e24  ./Amazon-LP/AMZ/STAR and LPS/TrustMed_Retrieval_Tuning_STAR.txt
7efe7f449081c25ea72b435cbe03e3c9e2f69fc50b5ab9acaf25b81508d6cf12  ./Amazon-LP/AMZ/STAR and LPS/beahv 2.txt
1a592ef4bcc04699adf38f981bd64a5c9f8a597cce1d7cc69b6016ade3312d62  ./Amazon-LP/AMZ/STAR and LPS/behav 3.txt
2f8fbeae540e7076bb0ca047337f3e2b43c23f95654b358f3f25e276b39710d5  ./Amazon-LP/AMZ/STAR and LPS/ownership + complex problem + challenging team + work out of scope.txt
16d142599dc62fecd1476cae8d1c99820a2c7efca2d1eddff2b0ca9fe2237764  ./Amazon-LP/Amazon-Behavioral-Stories-Version-1.md
8e637946d7e80a232d253f9f8f7283b74a89973f8e4a042bd0f0afca8c9cb6b2  ./Amazon-LP/BEHAVIORAL-INTERVIEW-VIDEO-GUIDANCE.md
0ca39aa94467a13ed1e5436ba417fe2742a46714e6668f8a38523b4ea0406963  ./Amazon-LP/JOB-DESCRIPTION.md
b5a2ea95dc6175afc0416145c5a723758f8c465b01ca4da691de16f0549a8fec  ./Amazon-LP/LEADERSHIP-PRINCIPLES.md
9b2196fb5227b4b97d818cf2ee63f2c734277b4873fdf7f6e9e8aa7e40ab80d9  ./Amazon-LP/STORY-QUESTION-MAP.md
cd12070d139841528d4d316e8a2e733e16e728fe0c3b1fe81de0b0d41fcf4ea5  ./Amazon-LP/raw/ASU-Semantic-Web-Mining-project.md
43d6a2c14e4b7ada1d04355151cd8a99e972ee4fbb6413b0adfd5dcf2df5dd71  ./Amazon-LP/stories/ASU-Academic-Transfer-Credit-Workplace.md
540b237773e03f3c0216a77cd8e80787e597ef1420e6dac0661e10999b8ada13  ./Amazon-LP/stories/ASU-HuggingFace-Conflict-HB-DC-AR-EARN-LC.md
5aeb49b4cb5dd598373ac5c4af94496432070c354e855a4d31b2767dfbca5b46  ./Amazon-LP/stories/ASU-Team-Capacity-EARN-OWN-DR-EBE.md
358b02c47e46ce43a7e370d32f708c457815cb5f852644fe5c092ec814df5b7a  ./Amazon-LP/stories/DAS-Outside-Responsibility-Onboarding.md
8f0746fa23d37ab03e386f89d4eeb0ef218ddea7570e91010cec4090f75af3b8  ./Amazon-LP/stories/DAS-RainbowCity-DD-IS-AR-OWN-CO.md
cca1e24bb8009b556818bc26497b1e392180843a16522738228546b68672b4dd  ./Amazon-LP/stories/eInfochips-Invoice-CO-DD-OWN-IS-IHS.md
0da23e9d311da71733ec2c84172b1db0ff85bb25663c7cc22aa135544044cb3a  ./Amazon-LP/technical/AMAZON-DSA-26-PROBLEM-GUIDE.md
4b05825f6234669f093085ebf05faf46e7b74c02281e9b85f5d9f8057d6114dc  ./Amazon-LP/technical/NEETCODE-150-PATTERN-GUIDE.md
90328fc9b7a8aa5c309df37e63720b5a5096c835234a8e8cea7407644d31dbac  ./Amazon-LP/technical/lld_and_coding_examples_cpp.md
75ef56befa53cb05d8e64eff6c7aeb9e43e3924b8db9e0782b5a202f9e9f965f  ./CLAUDE.md
0395bb93f2bc56c1f3c3ef79423d86168387f065418d6d2e2fc1d78804ea86ee  ./CONTEXT.md
465d3d14bf8961603bf086c827faef3c5818f6fdfbcdb4b7f85e0462774df617  ./README.md
f5468ec109765085b038a872982b3fac02ac7bb6c3743b6cc823ed767f3b24e8  ./applications/README.md
bd97fa869e8e3794bf3417aa947f0a24db58b4f13ed3378186c7881e532943d1  ./applications/eduwave-ai-interview-cheatsheet.md
1f6d20f16ce35948dd0e553ec35e8e9de1017d322633622b0bcb7294c735c4ca  ./applications/zymo-research-fullstack-cover-letter.md
08214f14fe87f9921a2d34c2253a0c7eeaaea1921aae156cbb67683afbe4abdb  ./career-stories/DigitalAidSeattle.md
5d8894c508b5e769c4d4a6062b97cc972b4bf88bf67ca1ff68836ea9c04210c5  ./career-stories/_drafts/DAS-unverified-draft-bullets.md
b57339aea7d1392037b53babed2ece7d1de94aab75cccb66e8188d2fb54409b4  ./career-stories/eInfochips.md
1c0b8857012d9b1826f821027a18c6620035747d16b41654da78a67fe828a99c  ./career-stories/interview/3-week-interview-technical-prep-roadmap.md
4b459e682535502b4e06ca9be58b0784189db40c575686989096a225288d57df  ./career-stories/interview/interview-prep-system-prompt.md
2b4dd886a5a2caad735a634111f28d360b0f344d7c0074968499e71c9d896557  ./career-stories/interview/interview-qa.md
81662144eb1866ecbb1fc47bb960a1edcf0637bc5c1ce1602404ef4dd86b1882  ./career-stories/interview/tech-tradeoffs-codebase-prompt.md
f48a6df79a152efa7826056e3fbc7926a98fcfb3d4449545dd6a009a9e0419bd  ./career-stories/interview/tech-tradeoffs-prompt.md
fff82e107579223a241123a7bd156d47ff5e881123dc467737bd5ab195cd80e6  ./data_engineer.md
80508815041528b0e346354ded99af7bd0fa22931d9f76b0992edbb67b853016  ./docs/superpowers/plans/2026-07-16-job-os-approach1.md
9be215cdc5f21a63f3948d6783df978c43cf7e243744005ee209d78f26ae5254  ./docs/superpowers/specs/2026-07-16-job-os-approach1-design.md
2815302d607553ec921c88fa743331fdeb701a03394f8b6fc5e266e45ebac6b9  ./experimental/founders.md
6bff7264bdabc347e3921e6410824c5e581e3705bdf1bf966bf1075ea985e3fc  ./experimental/job-os-router.md
b8bb35dc262e9113a27d0358060e560090e74bd1e54198ed193d7df09944ea0c  ./golden-jds/README.md
88d990728e9ee4cb0c7fb440080d7b66f0c2198ff6dd35ae65cf6c81230cbafb  ./golden-jds/ai-engineer-morgan-stanley.md
08c3ad3fbf68f6233e8acd5b2b0800fb2e8e10488efc7baffaf155e3e4ea5bbb  ./golden-jds/ai-engineer-nuclear-company.md
1ad123fbdbfd0e51c35f8b70be91ab3b02c141ce3c47cf0ed9bae3a45f08bcbc  ./golden-jds/ai-engineer-sierra.md
5ba806126da2dba2d26dfc35eaeaa1c7abda5c0c1e4b55e8af16f07ebc9130a6  ./golden-jds/ai-software-engineer.md
7c2f4f5854a917fbbe9f9fab9e3a328cabf0b0053de85542d7b563572da652de  ./golden-jds/backend-software-engineer-mastercard.md
b7b0e870a99c9c7f4ccd7f29b1767daeabc70d260a64792cabb6d9aeb5005598  ./golden-jds/backend-software-engineer.md
b2412056d72fa57285bc92cbfc31976f5db546b24679a2a8ab0f2cfb503bc228  ./golden-jds/full-stack-product-growth-cloudflare.md
795cfe2f214d2e9bc56b761ef23aa595d977b3526870012fa0616327f8bcf9b3  ./golden-jds/full-stack-software-engineer.md
7e94ed3a69a0681ec1a5fd568efb8cfc84b1e20c0bda2c8448ce630f9227c107  ./golden-jds/software-engineer-intuit-entry-level.md
710278bf5da70430cdf1496140874207487e6679f6236c339cfe9ed72e13afe0  ./golden-jds/systems-engineer-postgresql-cloudflare.md
8bfaadf63047cfd4e9918f1bfcd6c5658a17df8edd85c8fe9996900853490f35  ./governance/DEFINITION_OF_DONE.md
981a1097ac4aa212060dc82648642acef7d624ff57317884d4bb51acefce03ae  ./governance/FACT_RULES.md
b031dc9cb01ff2b5b874c119959f6c6ec1400b17e8320e22f04e7b30f6fccd8f  ./governance/FULL_STACK_TEMPLATE.md
662241a71f12dae7222119c1ed36012d02abfb702655182f6a3a3f85d0d730f3  ./governance/OUTPUT_CONTRACT.md
40847eb293a4edb6b7a6f6934cb6de30036d05bc49fb90a941469c49687ba649  ./governance/auditor-prompt.md
3e8bdcab187e01440832d2e950534ff2e78b48ba2369c5ea66e297921ecdbc8e  ./governance/feedback-log.md
43b0bbb4d97166927479112e585ac605f4078ba2ba7a110b86e01e44f1bbe7f3  ./gpt/README.md
edc14323bff5a4f217e5a8330df311148ab12e2e6d7a33440ab19c68ce2e542f  ./gpt/per-project-keywords.md
b07460ccaa96f60296eff7309d2c2c6996997f6294603d524d9c7a488c15aa55  ./gpt/projects/ClusterOps.md
1a8a3dd5b7c86a901240fca85a9c8b8acb0f4ad7011bb96f0f5058c1df61900d  ./gpt/projects/crypto-market-simulator.md
4ffa584d1fd58ef67bfbf3d59b7300f7abc6fcf16faa5f8adc07236ea9a4cc8c  ./gpt/projects/distributed-caching.md
d9d605be487c160e5ee9fbaf4f42828e21b02fa783963d1e18e281ef5b74bd4a  ./gpt/projects/fake-review-detector.md
ad7e747d889cf084545ee2fc7e076bd8fa5cc99a4c2c8982da9be8cc0ccafa9e  ./gpt/projects/hearloop.md
c678bbceca6ddb816c6f29a34c6b24d6a018b59ae9dc8f120d96ca752db9393f  ./gpt/projects/seo-audit-engine.md
7872bf9d60c6a0e8a18a8cb64bdf62483ebaca870b81817d2a20289e385ec3b0  ./gpt/projects/youtube-ads-compliance-pipeline.md
6da674fe1a9fd1c344b3a588f9d1f1db40977684b4a9b46644576b94cb93f114  ./gpt/system-prompt.md
a2090914de3bd980a4ae77afc4daf68af1d782557c6517bd436d4dba9ac687a6  ./gpt/work-experience.md
185116ae6fa52bc5f25345f770c7443ac3416f251ee3258758b1865b0eca9a9c  ./handoffs/2026-06-05-youtube-compliance.md
1457b6dddd9b0fa825024b0521933cb8fd59abdec61e0742796446fe2c6b7957  ./handoffs/2026-07-20-dad-friend-resume-change-log.md
d7351f863c9057ac14bb838f05426c2456e0f1891c652a2d34c90ee6d670ddda  ./networking/README.md
54f9f5220f9de124906540377bd8cffd9bada06d874d7081421c305fdd44ff17  ./networking/candidate-profile.md
4af72aa84f3f81ce1291ba2972d0f01d35be268ed95a6d203c04c262556b9e9a  ./networking/scripts.md
5ed044cee278afd9514c38031644807d62bba0f250d7b4cb9e7ee1570ca9cc5d  ./prompts/application-answers.md
55b894da3a96a1475cbdc1ff41f45a1db0efaabe9e0d14d2af9bef0ef5c76f5b  ./prompts/experience-discovery.md
b26618db95d8750fc389244ac7b003180ee8cf7e291064375472e8f0b015fa12  ./prompts/linkedin-connection-note.md
21efb7af0c31b2a23ebfea0d5222204e55f7369deddfa65a2e0c93439431f375  ./prompts/networking.md
5aba5304dad46b11c2b6f896294ad6aa6c430d98bd7fe9a0a2de8528abb1350f  ./prompts/system-prompt-patch.md
10ea34651e164ce58b08ae12fd14a5aba7b9504d481ccd1b5e78ded2d8c856d5  ./reference/headless-headhunter.md
2dd885dd96a63e4c3cff281fba639788bff956b4bb759157ef0b0681a114eaa3  ./reference/humanizer.md
c0efb4eecd6315e412687d2fdf976295bf6c25a83878dd27e838463ae3f9d6e4  ./reference/jd-red-flags.md
545dd0112ac39967c040cf5ef75a92253f6a415f1f65263076fcbb4f03db0310  ./resume_evaluations.csv
4406000d5de5750e814633d9d0f132729707771fe7edc2429df04bde35ec3a0d  ./templates/main-one-page.tex
4406000d5de5750e814633d9d0f132729707771fe7edc2429df04bde35ec3a0d  ./templates/main.tex
ed6f3d429d9c26b393b491ae367d3b07b1ec58a6e650068c567502ef1f0b2064  ./templates/variants/ai-engineer-faang.tex
ed6f3d429d9c26b393b491ae367d3b07b1ec58a6e650068c567502ef1f0b2064  ./templates/variants/ai-engineer-projects-first-test.tex
ca5a596ee0df05c7f62aa0f284f23ec680b16454bd8952148e07166436cc8b0e  ./templates/variants/backend-faang.tex
89a82500a73867b95acd137a8b8f184ec58d7bd73f2b929336f2cec959e11da1  ./templates/variants/color-ai-platform.tex
57f6c89088bf03c1a854854e9c8b7a430e89d9266002f93bbe1ee48cc8ad80fd  ./templates/variants/fullstack-engineer.tex
757b05ee6beb5b0d16a67c53a1bac4b17b6013ddc09b867aef79f893505c897c  ./templates/variants/instalily-ai-platform.tex
ae2cf402026d5060de82a841abf3ebedda1ccba352ca11f134d58e7734de99ee  ./templates/variants/marketplace-discovery.tex
```
- Initial staged changed paths: **none**
- Initial unstaged tracked paths: **34** (27 modified, 7 deleted)
- Initial untracked status entries: **21**

Complete initial `git status --short`:

```text
 M .cursor/skills/fullstack-resume-tailor/SKILL.md
 M .cursor/skills/linkedin-connection-note/SKILL.md
 M CONTEXT.md
 M README.md
 M docs/superpowers/plans/2026-07-16-job-os-approach1.md
 M golden-jds/README.md
 M governance/DEFINITION_OF_DONE.md
 M governance/FACT_RULES.md
 M governance/OUTPUT_CONTRACT.md
 M gpt/README.md
 D gpt/interview/3-week-interview-technical-prep-roadmap.md
 D gpt/interview/interview-prep-system-prompt.md
 D gpt/interview/interview-qa.md
 D gpt/interview/tech-tradeoffs-codebase-prompt.md
 D gpt/interview/tech-tradeoffs-prompt.md
 M gpt/per-project-keywords.md
 M gpt/projects/ClusterOps.md
 M gpt/projects/distributed-caching.md
 M gpt/projects/fake-review-detector.md
 M gpt/projects/hearloop.md
 M gpt/projects/seo-audit-engine.md
 M gpt/projects/youtube-ads-compliance-pipeline.md
 M gpt/system-prompt.md
 M gpt/work-experience.md
 D prompts/founders.md
 D prompts/job-os-router.md
 M prompts/linkedin-connection-note.md
 M prompts/system-prompt-patch.md
 M templates/main-one-page.tex
 M templates/main.tex
 M templates/variants/ai-engineer-faang.tex
 M templates/variants/backend-faang.tex
 M templates/variants/fullstack-engineer.tex
 M templates/variants/marketplace-discovery.tex
?? .agents/
?? .scratch/
?? AGENTS.md
?? Amazon-LP/
?? CLAUDE.md
?? apply-for-me-main/
?? career-stories/
?? experimental/
?? golden-jds/ai-engineer-morgan-stanley.md
?? golden-jds/ai-engineer-nuclear-company.md
?? golden-jds/ai-engineer-sierra.md
?? golden-jds/backend-software-engineer-mastercard.md
?? golden-jds/full-stack-product-growth-cloudflare.md
?? golden-jds/software-engineer-intuit-entry-level.md
?? golden-jds/systems-engineer-postgresql-cloudflare.md
?? handoffs/2026-07-20-dad-friend-resume-change-log.md
?? prompts/experience-discovery.md
?? reference/jd-red-flags.md
?? templates/variants/ai-engineer-projects-first-test.tex
?? templates/variants/color-ai-platform.tex
?? templates/variants/instalily-ai-platform.tex
```

The unstaged-path list was the tracked `M`/`D` subset above. `git diff --cached --name-only` was empty. The untracked-path list was the `??` subset above. The audit report and its previously absent `audits/` parent were created only after this capture.

## Scope and Exclusions

Inventory classification ledger initialized: **111 reviewable text/code/data files**, **125 exclusions**, **3 binaries**, **0 unreadable**. The exact per-file disposition appears in the final coverage manifest.

## Coverage Manifest

Each of the 239 baseline files has exactly one status. The audit report itself is excluded from this baseline because it was created after inventory capture.

- `.DS_Store` — EXCLUDED — macOS metadata
- `.agents/skills/resume-tailor/SKILL.md` — REVIEWED
- `.agents/skills/resume-tailor/agents/openai.yaml` — REVIEWED
- `.agents/skills/resume-tailor/references/tailoring-report-schema.md` — REVIEWED
- `.agents/skills/resume-tailor/scripts/preflight.py` — REVIEWED
- `.cursor/skills/application-answers/SKILL.md` — REVIEWED
- `.cursor/skills/fullstack-resume-tailor/SKILL.md` — REVIEWED
- `.cursor/skills/linkedin-connection-note/SKILL.md` — REVIEWED
- `.gitignore` — EXCLUDED — VCS ignore configuration unrelated to resume facts or behavior
- `.scratch/wayfinder/01-profile-evidence-schema.md` — EXCLUDED — explicitly excluded scratch material
- `.scratch/wayfinder/02-workflow-skill-contract.md` — EXCLUDED — explicitly excluded scratch material
- `.scratch/wayfinder/03-resume-selection-and-bullet-evals.md` — EXCLUDED — explicitly excluded scratch material
- `.scratch/wayfinder/04-application-answer-evals.md` — EXCLUDED — explicitly excluded scratch material
- `.scratch/wayfinder/05-golden-dataset-and-regression-corpus.md` — EXCLUDED — explicitly excluded scratch material
- `.scratch/wayfinder/06-output-and-template-safety.md` — EXCLUDED — explicitly excluded scratch material
- `.scratch/wayfinder/career-output-workflow-map.md` — EXCLUDED — explicitly excluded scratch material
- `.superpowers/sdd/.gitignore` — EXCLUDED — generated agent/review artifact
- `.superpowers/sdd/progress.md` — EXCLUDED — generated agent/review artifact
- `.superpowers/sdd/review-20e64d5..bc3d816.diff` — EXCLUDED — generated agent/review artifact
- `.superpowers/sdd/review-57fc948..ba8e8df.diff` — EXCLUDED — generated agent/review artifact
- `.superpowers/sdd/review-57fc948..d6dce2a.diff` — EXCLUDED — generated agent/review artifact
- `.superpowers/sdd/review-708ebd1..3d207f2.diff` — EXCLUDED — generated agent/review artifact
- `.superpowers/sdd/review-708ebd1..880164f.diff` — EXCLUDED — generated agent/review artifact
- `.superpowers/sdd/review-70a0793..ba8e8df.diff` — EXCLUDED — generated agent/review artifact
- `.superpowers/sdd/review-880164f..f45b8ca.diff` — EXCLUDED — generated agent/review artifact
- `.superpowers/sdd/review-d6dce2a..708ebd1.diff` — EXCLUDED — generated agent/review artifact
- `.superpowers/sdd/review-f45b8ca..12d3e2a.diff` — EXCLUDED — generated agent/review artifact
- `.superpowers/sdd/review-f45b8ca..20e64d5.diff` — EXCLUDED — generated agent/review artifact
- `.superpowers/sdd/task-1-brief.md` — EXCLUDED — generated agent/review artifact
- `.superpowers/sdd/task-1-report.md` — EXCLUDED — generated agent/review artifact
- `.superpowers/sdd/task-2-brief.md` — EXCLUDED — generated agent/review artifact
- `.superpowers/sdd/task-2-report.md` — EXCLUDED — generated agent/review artifact
- `.superpowers/sdd/task-3-brief.md` — EXCLUDED — generated agent/review artifact
- `.superpowers/sdd/task-3-report.md` — EXCLUDED — generated agent/review artifact
- `.superpowers/sdd/task-4-brief.md` — EXCLUDED — generated agent/review artifact
- `.superpowers/sdd/task-4-report.md` — EXCLUDED — generated agent/review artifact
- `.superpowers/sdd/task-5-brief.md` — EXCLUDED — generated agent/review artifact
- `.superpowers/sdd/task-5-report.md` — EXCLUDED — generated agent/review artifact
- `.superpowers/sdd/task-6-brief.md` — EXCLUDED — generated agent/review artifact
- `.superpowers/sdd/task-6-report.md` — EXCLUDED — generated agent/review artifact
- `.superpowers/sdd/task-7-brief.md` — EXCLUDED — generated agent/review artifact
- `.superpowers/sdd/task-7-report.md` — EXCLUDED — generated agent/review artifact
- `AGENTS.md` — REVIEWED
- `Amazon-LP/.DS_Store` — EXCLUDED — macOS metadata
- `Amazon-LP/AGENTS.md` — REVIEWED
- `Amazon-LP/AMZ/.DS_Store` — EXCLUDED — macOS metadata
- `Amazon-LP/AMZ/LLD/AmazonLockerMinimalInterview.java` — REVIEWED
- `Amazon-LP/AMZ/LLD/Amazon_STAR_Interview_Stories_Dhyan_Patel_Revised.docx` — BINARY
- `Amazon-LP/AMZ/LLD/ParkingLotSingleFloorArticleStyle.java` — REVIEWED
- `Amazon-LP/AMZ/LLD/amazon_lld_interview_cplusplus_guide.md` — REVIEWED
- `Amazon-LP/AMZ/LLD/amazon_locker_ready_to_speak_script.md` — REVIEWED
- `Amazon-LP/AMZ/LLD/atm_article_based_ready_to_speak_script.md` — REVIEWED
- `Amazon-LP/AMZ/LLD/parking_lot_single_floor_article_style_script.md` — REVIEWED
- `Amazon-LP/AMZ/LeetCode DSA/1. Thirty Days.csv` — REVIEWED
- `Amazon-LP/AMZ/LeetCode DSA/leetcode_amazon-thirty-days_07162026.csv` — REVIEWED
- `Amazon-LP/AMZ/LeetCode DSA/leetcode_amazon-thirty-days_Final_Dhyan.csv` — REVIEWED
- `Amazon-LP/AMZ/STAR and LPS/Dhyan_Database_Resume_Interview_Scripts_All_5.txt` — REVIEWED
- `Amazon-LP/AMZ/STAR and LPS/Dhyan_Patel_Amazon_SDE1_Behavioral_Playbook (1).docx` — BINARY
- `Amazon-LP/AMZ/STAR and LPS/Intro and why amazon.txt` — REVIEWED
- `Amazon-LP/AMZ/STAR and LPS/Sportlingo_Android_3_8_Auth_Incident_STAR.txt` — REVIEWED
- `Amazon-LP/AMZ/STAR and LPS/TrustMed_Neo4j_FAISS_Disagreement_STAR.txt` — REVIEWED
- `Amazon-LP/AMZ/STAR and LPS/TrustMed_Retrieval_Tuning_STAR.txt` — REVIEWED
- `Amazon-LP/AMZ/STAR and LPS/beahv 2.txt` — REVIEWED
- `Amazon-LP/AMZ/STAR and LPS/behav 3.txt` — REVIEWED
- `Amazon-LP/AMZ/STAR and LPS/ownership + complex problem + challenging team + work out of scope.txt` — REVIEWED
- `Amazon-LP/Amazon-Behavioral-Stories-Version-1.md` — REVIEWED
- `Amazon-LP/BEHAVIORAL-INTERVIEW-VIDEO-GUIDANCE.md` — REVIEWED
- `Amazon-LP/JOB-DESCRIPTION.md` — REVIEWED
- `Amazon-LP/LEADERSHIP-PRINCIPLES.md` — REVIEWED
- `Amazon-LP/STORY-QUESTION-MAP.md` — REVIEWED
- `Amazon-LP/raw/ASU-Semantic-Web-Mining-project.md` — REVIEWED
- `Amazon-LP/stories/ASU-Academic-Transfer-Credit-Workplace.md` — REVIEWED
- `Amazon-LP/stories/ASU-HuggingFace-Conflict-HB-DC-AR-EARN-LC.md` — REVIEWED
- `Amazon-LP/stories/ASU-Team-Capacity-EARN-OWN-DR-EBE.md` — REVIEWED
- `Amazon-LP/stories/DAS-Outside-Responsibility-Onboarding.md` — REVIEWED
- `Amazon-LP/stories/DAS-RainbowCity-DD-IS-AR-OWN-CO.md` — REVIEWED
- `Amazon-LP/stories/eInfochips-Invoice-CO-DD-OWN-IS-IHS.md` — REVIEWED
- `Amazon-LP/technical/AMAZON-DSA-26-PROBLEM-GUIDE.md` — REVIEWED
- `Amazon-LP/technical/NEETCODE-150-PATTERN-GUIDE.md` — REVIEWED
- `Amazon-LP/technical/lld_and_coding_examples_cpp.md` — REVIEWED
- `CLAUDE.md` — REVIEWED
- `CONTEXT.md` — REVIEWED
- `README.md` — REVIEWED
- `Resume+Template.pdf` — BINARY
- `_vendor/skills-main/.DS_Store` — EXCLUDED — macOS metadata
- `_vendor/skills-main/.claude-plugin/plugin.json` — EXCLUDED — vendored dependency
- `_vendor/skills-main/.out-of-scope/mainstream-issue-trackers-only.md` — EXCLUDED — vendored dependency
- `_vendor/skills-main/.out-of-scope/question-limits.md` — EXCLUDED — vendored dependency
- `_vendor/skills-main/.out-of-scope/setup-skill-verify-mode.md` — EXCLUDED — vendored dependency
- `_vendor/skills-main/CLAUDE.md` — EXCLUDED — vendored dependency
- `_vendor/skills-main/CONTEXT.md` — EXCLUDED — vendored dependency
- `_vendor/skills-main/LICENSE` — EXCLUDED — vendored dependency
- `_vendor/skills-main/README.md` — EXCLUDED — vendored dependency
- `_vendor/skills-main/docs/adr/0001-explicit-setup-pointer-only-for-hard-dependencies.md` — EXCLUDED — vendored dependency
- `_vendor/skills-main/scripts/link-skills.sh` — EXCLUDED — vendored dependency
- `_vendor/skills-main/scripts/list-skills.sh` — EXCLUDED — vendored dependency
- `_vendor/skills-main/skills/.DS_Store` — EXCLUDED — macOS metadata
- `_vendor/skills-main/skills/deprecated/README.md` — EXCLUDED — vendored dependency
- `_vendor/skills-main/skills/deprecated/design-an-interface/SKILL.md` — EXCLUDED — vendored dependency
- `_vendor/skills-main/skills/deprecated/qa/SKILL.md` — EXCLUDED — vendored dependency
- `_vendor/skills-main/skills/deprecated/request-refactor-plan/SKILL.md` — EXCLUDED — vendored dependency
- `_vendor/skills-main/skills/deprecated/ubiquitous-language/SKILL.md` — EXCLUDED — vendored dependency
- `_vendor/skills-main/skills/engineering/README.md` — EXCLUDED — vendored dependency
- `_vendor/skills-main/skills/engineering/diagnose/SKILL.md` — EXCLUDED — vendored dependency
- `_vendor/skills-main/skills/engineering/diagnose/scripts/hitl-loop.template.sh` — EXCLUDED — vendored dependency
- `_vendor/skills-main/skills/engineering/grill-with-docs/ADR-FORMAT.md` — EXCLUDED — vendored dependency
- `_vendor/skills-main/skills/engineering/grill-with-docs/CONTEXT-FORMAT.md` — EXCLUDED — vendored dependency
- `_vendor/skills-main/skills/engineering/grill-with-docs/SKILL.md` — EXCLUDED — vendored dependency
- `_vendor/skills-main/skills/engineering/improve-codebase-architecture/DEEPENING.md` — EXCLUDED — vendored dependency
- `_vendor/skills-main/skills/engineering/improve-codebase-architecture/INTERFACE-DESIGN.md` — EXCLUDED — vendored dependency
- `_vendor/skills-main/skills/engineering/improve-codebase-architecture/LANGUAGE.md` — EXCLUDED — vendored dependency
- `_vendor/skills-main/skills/engineering/improve-codebase-architecture/SKILL.md` — EXCLUDED — vendored dependency
- `_vendor/skills-main/skills/engineering/prototype/LOGIC.md` — EXCLUDED — vendored dependency
- `_vendor/skills-main/skills/engineering/prototype/SKILL.md` — EXCLUDED — vendored dependency
- `_vendor/skills-main/skills/engineering/prototype/UI.md` — EXCLUDED — vendored dependency
- `_vendor/skills-main/skills/engineering/setup-matt-pocock-skills/SKILL.md` — EXCLUDED — vendored dependency
- `_vendor/skills-main/skills/engineering/setup-matt-pocock-skills/domain.md` — EXCLUDED — vendored dependency
- `_vendor/skills-main/skills/engineering/setup-matt-pocock-skills/issue-tracker-github.md` — EXCLUDED — vendored dependency
- `_vendor/skills-main/skills/engineering/setup-matt-pocock-skills/issue-tracker-gitlab.md` — EXCLUDED — vendored dependency
- `_vendor/skills-main/skills/engineering/setup-matt-pocock-skills/issue-tracker-local.md` — EXCLUDED — vendored dependency
- `_vendor/skills-main/skills/engineering/setup-matt-pocock-skills/triage-labels.md` — EXCLUDED — vendored dependency
- `_vendor/skills-main/skills/engineering/tdd/SKILL.md` — EXCLUDED — vendored dependency
- `_vendor/skills-main/skills/engineering/tdd/deep-modules.md` — EXCLUDED — vendored dependency
- `_vendor/skills-main/skills/engineering/tdd/interface-design.md` — EXCLUDED — vendored dependency
- `_vendor/skills-main/skills/engineering/tdd/mocking.md` — EXCLUDED — vendored dependency
- `_vendor/skills-main/skills/engineering/tdd/refactoring.md` — EXCLUDED — vendored dependency
- `_vendor/skills-main/skills/engineering/tdd/tests.md` — EXCLUDED — vendored dependency
- `_vendor/skills-main/skills/engineering/to-issues/SKILL.md` — EXCLUDED — vendored dependency
- `_vendor/skills-main/skills/engineering/to-prd/SKILL.md` — EXCLUDED — vendored dependency
- `_vendor/skills-main/skills/engineering/triage/AGENT-BRIEF.md` — EXCLUDED — vendored dependency
- `_vendor/skills-main/skills/engineering/triage/OUT-OF-SCOPE.md` — EXCLUDED — vendored dependency
- `_vendor/skills-main/skills/engineering/triage/SKILL.md` — EXCLUDED — vendored dependency
- `_vendor/skills-main/skills/engineering/zoom-out/SKILL.md` — EXCLUDED — vendored dependency
- `_vendor/skills-main/skills/in-progress/README.md` — EXCLUDED — vendored dependency
- `_vendor/skills-main/skills/in-progress/review/SKILL.md` — EXCLUDED — vendored dependency
- `_vendor/skills-main/skills/in-progress/writing-beats/SKILL.md` — EXCLUDED — vendored dependency
- `_vendor/skills-main/skills/in-progress/writing-fragments/SKILL.md` — EXCLUDED — vendored dependency
- `_vendor/skills-main/skills/in-progress/writing-shape/SKILL.md` — EXCLUDED — vendored dependency
- `_vendor/skills-main/skills/misc/README.md` — EXCLUDED — vendored dependency
- `_vendor/skills-main/skills/misc/git-guardrails-claude-code/SKILL.md` — EXCLUDED — vendored dependency
- `_vendor/skills-main/skills/misc/git-guardrails-claude-code/scripts/block-dangerous-git.sh` — EXCLUDED — vendored dependency
- `_vendor/skills-main/skills/misc/migrate-to-shoehorn/SKILL.md` — EXCLUDED — vendored dependency
- `_vendor/skills-main/skills/misc/scaffold-exercises/SKILL.md` — EXCLUDED — vendored dependency
- `_vendor/skills-main/skills/misc/setup-pre-commit/SKILL.md` — EXCLUDED — vendored dependency
- `_vendor/skills-main/skills/personal/README.md` — EXCLUDED — vendored dependency
- `_vendor/skills-main/skills/personal/edit-article/SKILL.md` — EXCLUDED — vendored dependency
- `_vendor/skills-main/skills/personal/obsidian-vault/SKILL.md` — EXCLUDED — vendored dependency
- `_vendor/skills-main/skills/productivity/.DS_Store` — EXCLUDED — macOS metadata
- `_vendor/skills-main/skills/productivity/README.md` — EXCLUDED — vendored dependency
- `_vendor/skills-main/skills/productivity/caveman/SKILL.md` — EXCLUDED — vendored dependency
- `_vendor/skills-main/skills/productivity/grill-me/SKILL.md` — EXCLUDED — vendored dependency
- `_vendor/skills-main/skills/productivity/handoff/SKILL.md` — EXCLUDED — vendored dependency
- `_vendor/skills-main/skills/productivity/write-a-skill/SKILL.md` — EXCLUDED — vendored dependency
- `applications/README.md` — REVIEWED
- `applications/eduwave-ai-interview-cheatsheet.md` — REVIEWED
- `applications/zymo-research-fullstack-cover-letter.md` — REVIEWED
- `apply-for-me-main/.gitignore` — EXCLUDED — explicitly excluded subtree
- `apply-for-me-main/CHANGELOG.md` — EXCLUDED — explicitly excluded subtree
- `apply-for-me-main/LICENSE` — EXCLUDED — explicitly excluded subtree
- `apply-for-me-main/README.md` — EXCLUDED — explicitly excluded subtree
- `apply-for-me-main/SKILL.md` — EXCLUDED — explicitly excluded subtree
- `apply-for-me-main/docs/needs-you.png` — EXCLUDED — explicitly excluded subtree
- `apply-for-me-main/docs/referrals.png` — EXCLUDED — explicitly excluded subtree
- `apply-for-me-main/docs/watching.png` — EXCLUDED — explicitly excluded subtree
- `apply-for-me-main/references/platforms.md` — EXCLUDED — explicitly excluded subtree
- `apply-for-me-main/references/sourcing.md` — EXCLUDED — explicitly excluded subtree
- `apply-for-me-main/references/storage.md` — EXCLUDED — explicitly excluded subtree
- `apply-for-me-main/references/tailoring.md` — EXCLUDED — explicitly excluded subtree
- `apply-for-me-main/scripts/dashboard.py` — EXCLUDED — explicitly excluded subtree
- `apply-for-me-main/scripts/store.py` — EXCLUDED — explicitly excluded subtree
- `apply-for-me-main/tests/fixtures/practice-form.html` — EXCLUDED — explicitly excluded subtree
- `apply-for-me-main/tests/test_dashboard.py` — EXCLUDED — explicitly excluded subtree
- `apply-for-me-main/tests/test_store.py` — EXCLUDED — explicitly excluded subtree
- `career-stories/DigitalAidSeattle.md` — REVIEWED
- `career-stories/_drafts/DAS-unverified-draft-bullets.md` — REVIEWED
- `career-stories/eInfochips.md` — REVIEWED
- `career-stories/interview/3-week-interview-technical-prep-roadmap.md` — REVIEWED
- `career-stories/interview/interview-prep-system-prompt.md` — REVIEWED
- `career-stories/interview/interview-qa.md` — REVIEWED
- `career-stories/interview/tech-tradeoffs-codebase-prompt.md` — REVIEWED
- `career-stories/interview/tech-tradeoffs-prompt.md` — REVIEWED
- `data_engineer.md` — REVIEWED
- `docs/superpowers/plans/2026-07-16-job-os-approach1.md` — REVIEWED
- `docs/superpowers/specs/2026-07-16-job-os-approach1-design.md` — REVIEWED
- `experimental/founders.md` — REVIEWED
- `experimental/job-os-router.md` — REVIEWED
- `golden-jds/README.md` — REVIEWED
- `golden-jds/ai-engineer-morgan-stanley.md` — REVIEWED
- `golden-jds/ai-engineer-nuclear-company.md` — REVIEWED
- `golden-jds/ai-engineer-sierra.md` — REVIEWED
- `golden-jds/ai-software-engineer.md` — REVIEWED
- `golden-jds/backend-software-engineer-mastercard.md` — REVIEWED
- `golden-jds/backend-software-engineer.md` — REVIEWED
- `golden-jds/full-stack-product-growth-cloudflare.md` — REVIEWED
- `golden-jds/full-stack-software-engineer.md` — REVIEWED
- `golden-jds/software-engineer-intuit-entry-level.md` — REVIEWED
- `golden-jds/systems-engineer-postgresql-cloudflare.md` — REVIEWED
- `governance/DEFINITION_OF_DONE.md` — REVIEWED
- `governance/FACT_RULES.md` — REVIEWED
- `governance/FULL_STACK_TEMPLATE.md` — REVIEWED
- `governance/OUTPUT_CONTRACT.md` — REVIEWED
- `governance/auditor-prompt.md` — REVIEWED
- `governance/feedback-log.md` — REVIEWED
- `gpt/.DS_Store` — EXCLUDED — macOS metadata
- `gpt/README.md` — REVIEWED
- `gpt/per-project-keywords.md` — REVIEWED
- `gpt/projects/ClusterOps.md` — REVIEWED
- `gpt/projects/crypto-market-simulator.md` — REVIEWED
- `gpt/projects/distributed-caching.md` — REVIEWED
- `gpt/projects/fake-review-detector.md` — REVIEWED
- `gpt/projects/hearloop.md` — REVIEWED
- `gpt/projects/seo-audit-engine.md` — REVIEWED
- `gpt/projects/youtube-ads-compliance-pipeline.md` — REVIEWED
- `gpt/system-prompt.md` — REVIEWED
- `gpt/work-experience.md` — REVIEWED
- `handoffs/2026-06-05-youtube-compliance.md` — REVIEWED
- `handoffs/2026-07-20-dad-friend-resume-change-log.md` — REVIEWED
- `networking/README.md` — REVIEWED
- `networking/candidate-profile.md` — REVIEWED
- `networking/scripts.md` — REVIEWED
- `prompts/application-answers.md` — REVIEWED
- `prompts/experience-discovery.md` — REVIEWED
- `prompts/linkedin-connection-note.md` — REVIEWED
- `prompts/networking.md` — REVIEWED
- `prompts/system-prompt-patch.md` — REVIEWED
- `reference/headless-headhunter.md` — REVIEWED
- `reference/humanizer.md` — REVIEWED
- `reference/jd-red-flags.md` — REVIEWED
- `resume_evaluations.csv` — REVIEWED
- `templates/.DS_Store` — EXCLUDED — macOS metadata
- `templates/main-one-page.tex` — REVIEWED
- `templates/main.tex` — REVIEWED
- `templates/variants/ai-engineer-faang.tex` — REVIEWED
- `templates/variants/ai-engineer-projects-first-test.tex` — REVIEWED
- `templates/variants/backend-faang.tex` — REVIEWED
- `templates/variants/color-ai-platform.tex` — REVIEWED
- `templates/variants/fullstack-engineer.tex` — REVIEWED
- `templates/variants/instalily-ai-platform.tex` — REVIEWED
- `templates/variants/marketplace-discovery.tex` — REVIEWED

## Authority Map

1. **Audit rules:** this request and `AGENTS.md` / `CLAUDE.md`.
2. **Live tailoring authority:** `.agents/skills/resume-tailor/SKILL.md`, including its preflight and report schema.
3. **Fact governance:** `governance/FACT_RULES.md`.
4. **Current locked facts:** `gpt/work-experience.md` and `gpt/projects/*.md`.
5. **Lane outputs:** `templates/variants/ai-engineer-faang.tex`, `backend-faang.tex`, and `fullstack-engineer.tex`, verified against level 4.
6. **Supporting context:** career stories and handoffs.
7. **Saved applications and networking material.**
8. **Legacy, experimental, superseded, draft, and external-reference material.**

Important reachability edges:

- Root `README.md:5,124` sends maintainers toward the legacy GPT workflow and a four-project index even though the live skill forbids loading those sources.
- `.cursor/skills/linkedin-connection-note/SKILL.md` consumes `networking/candidate-profile.md`, so stale resume facts in that profile are active for networking output.
- `.cursor/skills/application-answers/SKILL.md` consumes `prompts/application-answers.md`, whose worked example contains retired eInfochips facts.
- `.agents/skills/resume-tailor/references/tailoring-report-schema.md:44` depends on `governance/OUTPUT_CONTRACT.md`, although the live skill says not to load that file in a live run (`SKILL.md:20`).
- `Amazon-LP/AGENTS.md:64-67` explicitly identifies `Amazon-LP/AMZ/**` as a friend's reference material and forbids copying its facts into the user's stories; those files are therefore reviewed but isolated from Shubh's fact authority.

## Critical Findings

### C-01 — Digital Aid Seattle title and scale disagree inside current sources

- **Finding type:** CONTRADICTION
- **Severity:** CRITICAL
- **Summary:** The current master calls the role “Volunteer Software Engineer,” while the same file and every resume template call it “Software Engineer.” The current scale is also stated as both 300–350 and approximately 400 active members, with 10–12 versus exactly 12 ensembles in locked outputs.
- **Why the conflict matters:** Title and scale are interview- and background-check-sensitive employment facts.
- **Exact conflicting statements / affected locations:** `gpt/work-experience.md:29` — “Volunteer Software Engineer”; `gpt/work-experience.md:207` — “Software Engineer, Digital Aid Seattle”; templates `main.tex:141`, `main-one-page.tex:141`, `variants/fullstack-engineer.tex:130`, `backend-faang.tex:130`, `ai-engineer-faang.tex:218`, `ai-engineer-projects-first-test.tex:218`, `color-ai-platform.tex:110`, `instalily-ai-platform.tex:140`, `marketplace-discovery.tex:168` — “Software Engineer”; `career-stories/DigitalAidSeattle.md:16` — “300-350 active ... 10-12 ensembles”; `career-stories/DigitalAidSeattle.md:100` and `gpt/work-experience.md:45` — “Approximately 400 ... 10-12”; locked template bullets use “400 ... 12 ensembles” (`fullstack-engineer.tex:133`, `backend-faang.tex:133`, `ai-engineer-faang.tex:222`).
- **Authority analysis / evidence:** The disagreement is within level-4 current fact material and its verified outputs; no authority rule permits choosing silently. A handoff advocating removal of “Volunteer” is lower authority and does not settle the official title.
- **Reachability:** Every live lane template and the locked work-experience bank.
- **Confidence:** HIGH
- **Proposed canonical statement:** “`[verified official title]`, Digital Aid Seattle, June 2026–Present; production MMS serving approximately `[verified snapshot]` active members across `[verified snapshot]` ensembles.”
- **Per-file proposed action:** `gpt/work-experience.md` — REPLACE after decision; `career-stories/DigitalAidSeattle.md` — REPLACE after decision; all listed templates — REPLACE after decision; historical handoff — LEAVE UNCHANGED with its historical boundary.
- **Risk if left unresolved:** False title or inflated scale can be emitted in every resume lane.
- **User decision required:** YES

### C-02 — eInfochips date, stack, authentication, API count, and retired impact leak into reachable outputs

- **Finding type:** CONTRADICTION
- **Severity:** CRITICAL
- **Summary:** The locked master says January–May 2024, React/MUI, email/password session (not OAuth/JWT), and observable 7-accountant/10,000-record scale. Reachable networking, application, template, handoff, and evaluation material says 2023, Angular, OAuth/JWT, 5+ APIs, Kubernetes, or a retired 40% impact.
- **Why the conflict matters:** These are concrete employment, technology, and performance claims.
- **Exact conflicting statements / affected locations:** authoritative `gpt/work-experience.md:133-158` and `career-stories/eInfochips.md:225,242`; conflicting `networking/candidate-profile.md:15` (“2023 ... 5+ REST APIs ... OAuth/JWT/RBAC”), `prompts/networking.md:25` (“2023”), `prompts/application-answers.md:153` (“Last year ... OAuth and JWT”), `templates/main.tex:170`, `main-one-page.tex:170`, and `variants/marketplace-discovery.tex:196-197` (OAuth/JWT/MongoDB skills), `handoffs/2026-07-20-dad-friend-resume-change-log.md:87,94` (Angular), `resume_evaluations.csv:3` (Kubernetes and “reduced ... 40%”), `career-stories/interview/interview-prep-system-prompt.md:85` (invoice time −40%), `applications/zymo-research-fullstack-cover-letter.md:18` (5+ APIs), `CONTEXT.md:96,101` (OAuth/JWT).
- **Authority analysis / evidence:** Level-4 locked work facts and the explicit retirement note at `career-stories/eInfochips.md:225` override lower-level copied applications and prompts. The conflict must still be reported because active Cursor skills read two affected files.
- **Reachability:** LinkedIn connection-note skill, application-answer skill, legacy GPT prompt, main templates, saved cover letter, interview prompt.
- **Confidence:** HIGH
- **Proposed canonical statement:** “Software Engineer Intern, eInfochips, Jan–May 2024; TypeScript/Node/Express/PostgreSQL with React/MUI; email/password sessions and RBAC, not OAuth/JWT; 7-accountant pilot over 10,000+ records; no 40% time-reduction claim.”
- **Per-file proposed action:** master files — LEAVE UNCHANGED; candidate profile, prompts, main templates, handoff guidance, interview prompt, cover letter, and evaluation CSV — REPLACE or RELABEL as historical; saved application — RELABEL and do not reuse.
- **Risk if left unresolved:** Future resumes, outreach, and interview answers can assert technologies and outcomes never used.
- **User decision required:** NO

### C-03 — Hearloop material converts intended value into customer adoption and realized outcomes

- **Finding type:** RULE VIOLATION
- **Severity:** CRITICAL
- **Summary:** The master explicitly records no paying customers, live-business adoption, retention result, or production traffic, yet locked/full-stack material and templates state that businesses capture more feedback, customers finish during rush hour, and local businesses avoid lost complaint days. Several templates also assert 72 shipped tests although the master records 69/72 passing.
- **Why the conflict matters:** This violates the side-project evidence rule and can misrepresent adoption, reliability, and test status.
- **Exact statements / affected locations:** boundary `gpt/projects/hearloop.md:93-94,219-230`; unsupported outcome wording at `gpt/projects/hearloop.md:273-291,337-359,423-441`; 69/72 fact at `gpt/projects/hearloop.md:207`; conflicting templates `main.tex:110-112`, `main-one-page.tex:110-112`, `variants/marketplace-discovery.tex:118-120`, `variants/instalily-ai-platform.tex:116`, `variants/color-ai-platform.tex:94`; saved application `applications/eduwave-ai-interview-cheatsheet.md:60,63`; active profile `networking/candidate-profile.md:22` promotes the explicitly discouraged $35→$9.60 number (`FACT_RULES.md:114`, `hearloop.md:213-215`).
- **Authority analysis / evidence:** The project master itself supplies the prohibition; the claims are not rescued by appearing in locked sections.
- **Reachability:** Full-stack locked bank, legacy/main templates, optional variants, saved application, networking skill.
- **Confidence:** HIGH
- **Proposed canonical statement:** “Built and load-tested a working Hearloop prototype designed to help businesses collect and analyze voice feedback; no live-customer adoption or realized business outcome claimed.”
- **Per-file proposed action:** master outcome lines and affected templates — REPLACE; master evidence boundaries — LEAVE UNCHANGED; saved application/profile — RELABEL or REPLACE.
- **Risk if left unresolved:** Active or copied output can claim real customers, adoption, or completed test coverage.
- **User decision required:** NO

### C-04 — SEO Audit Engine bullets invent client accounts, onboarding use, retention, and production impact

- **Finding type:** UNSUPPORTED CLAIM
- **Severity:** CRITICAL
- **Summary:** Current selectable bullets describe agencies onboarding multiple accounts, live onboarding engagements, client retention, and production deploy impact without documented customers or adoption evidence.
- **Why the conflict matters:** These are realized side-project business outcomes.
- **Exact statements / affected locations:** `gpt/projects/seo-audit-engine.md:60` — “client teams ... live accounts, improving retention”; `:66` — “agency teams onboarding multiple new accounts each week”; `:68` — “miss onboarding deadlines”; `:76` — “live onboarding engagements ... protecting new account retention”; `templates/main.tex:118-119`, `main-one-page.tex:118-119`, `variants/marketplace-discovery.tex:126-127` repeat client/account/churn claims.
- **Authority analysis / evidence:** No higher-authority source documents customers, adoption, or measured retention. Governance requires “designed to” for intended project value.
- **Reachability:** Full-stack and backend selection can choose these locked bullets; legacy templates copy them.
- **Confidence:** HIGH
- **Proposed canonical statement:** “Built a deployed audit prototype designed to give agencies a consistent site assessment and keep long-running crawls off the request path; no client adoption or retention claimed.”
- **Per-file proposed action:** project master and all listed templates — REPLACE.
- **Risk if left unresolved:** Resume can make false customer and retention claims.
- **User decision required:** NO

### C-05 — Distributed-caching simulation is labeled measured savings and older templates imply real traffic

- **Finding type:** RULE VIOLATION
- **Severity:** CRITICAL
- **Summary:** A modeled cost projection is described as “$420 saved” and classified with measured system behavior; optional templates describe real shoppers, customers, backend teams under real load, and leadership approval that the master expressly disclaims.
- **Why the conflict matters:** Estimated model output is not realized savings or production adoption.
- **Exact statements / affected locations:** `gpt/projects/distributed-caching.md:62,82,235` — “$420/month saved”; `:207` expressly says not to imply shoppers/customers/leadership/production; `templates/variants/marketplace-discovery.tex:142-144` supplies all four prohibited implications; `variants/instalily-ai-platform.tex:124` says “backend teams ... under real load.”
- **Authority analysis / evidence:** The master documents a Python simulation and projection; the present-tense “saved” wording conflicts with governance’s measured-versus-estimated rule.
- **Reachability:** Backend locked bank and optional variants.
- **Confidence:** HIGH
- **Proposed canonical statement:** “Modeled a 93.9% compute reduction and projected approximately $420/month lower compute cost at an assumed 1M daily requests; no realized savings, customer traffic, or production adoption.”
- **Per-file proposed action:** `distributed-caching.md` — REPLACE classification/wording; listed variants — REPLACE.
- **Risk if left unresolved:** A hypothetical simulation can be presented as measured business savings.
- **User decision required:** NO

### C-06 — Crypto and fake-review masters contain unsupported user/business outcomes

- **Finding type:** UNSUPPORTED CLAIM
- **Severity:** CRITICAL
- **Summary:** Crypto bullets claim enabled users, preserved company trust, and repeat engagement; Fake Review claims reduced manual review effort and labels Docker-ready execution as production-like without adoption evidence.
- **Why the conflict matters:** Neither project documents real users or measured business impact.
- **Exact statements / affected locations:** `gpt/projects/crypto-market-simulator.md:29-31` — “enabled users,” “company did not lose users’ trust,” “stronger reason to revisit”; `gpt/projects/fake-review-detector.md:84,89` — “reduces the manual effort”; `:114` describes “production systems” from Flask/Gunicorn/Docker-ready setup; AI templates repeat the manual-effort claim at `variants/ai-engineer-faang.tex:162-165` and `ai-engineer-projects-first-test.tex:162-165`.
- **Authority analysis / evidence:** No current source documents real product users, a company, adoption, or measured labor reduction. Crypto has no locked bullet bank at all.
- **Reachability:** AI fixed/supporting project selection and any full-stack/backend ranking that selects Crypto.
- **Confidence:** HIGH
- **Proposed canonical statement:** “Built [project capability] designed to help a defined user perform [task]; no users, adoption, realized labor reduction, or production status claimed unless separately evidenced.”
- **Per-file proposed action:** both project masters and listed AI templates — REPLACE.
- **Risk if left unresolved:** Selectable resume bullets can invent product adoption and realized impact.
- **User decision required:** NO

### C-07 — Amazon behavioral bank disagrees about deployment ownership and the Rainbow City incident

- **Finding type:** CONTRADICTION
- **Severity:** CRITICAL
- **Summary:** One polished story says Shubh owned the Hugging Face deployment, while its raw source says he did not. A current Rainbow City story describes reversed names/exact-email matching and an ensemble manager; the story map and Version 1 describe a Gmail-dot collision found by QA, a mapping table, staging results, and 10% fewer duplicates.
- **Why the conflict matters:** Interview stories can create claims of ownership, implementation, customer impact, and measured results that are incompatible with their own evidence.
- **Exact statements / affected locations:** `Amazon-LP/raw/ASU-Semantic-Web-Mining-project.md:56-58` — “did not make a major contribution ... should not claim deployment ownership”; `Amazon-LP/stories/ASU-HuggingFace-Conflict-HB-DC-AR-EARN-LC.md:71-81,102-107` — “took ownership”; `Amazon-LP/stories/DAS-RainbowCity-DD-IS-AR-OWN-CO.md:23-25,45-70,81-110` — manager/reversed-name/no recurrence metric; `Amazon-LP/STORY-QUESTION-MAP.md:15,207-213` and `Amazon-LP/Amazon-Behavioral-Stories-Version-1.md:155-175` — QA/Gmail/mapping table/10% staging result.
- **Authority analysis / evidence:** These are same-level active story-bank sources. The bank’s own rule (`Amazon-LP/AGENTS.md:51-77`) says not to fill gaps and to flag resume inconsistencies.
- **Reachability:** Active Amazon interview story map and polished story files.
- **Confidence:** HIGH
- **Proposed canonical statement:** Use one user-confirmed incident record for each story, with exact ownership, implementation, environment, and result; until confirmed, mark both stories unready.
- **Per-file proposed action:** raw source — LEAVE UNCHANGED; conflicting polished stories/map/Version 1 — RELABEL and REPLACE after decisions.
- **Risk if left unresolved:** Interview answers can contradict the resume or collapse under follow-up.
- **User decision required:** YES

### C-08 — Current master metrics cite evidence outside this workspace

- **Finding type:** UNSUPPORTED CLAIM (`EXTERNALLY UNVERIFIED`)
- **Severity:** CRITICAL
- **Summary:** Several resume-defining measurements cite code, reports, test outputs, cloud data, or repositories absent from this workspace. Internet and external-repository verification was prohibited, so the audit cannot independently validate them.
- **Why the conflict matters:** Locked metrics are high-impact resume claims and must be sourced and interview-defensible.
- **Exact affected locations / excerpts:** YouTube `gpt/projects/youtube-ads-compliance-pipeline.md:39-48` (35 URLs, 104 cases, 57 tests, 401 ms, 20 concurrent); Distributed `distributed-caching.md:60-84` (10,600 reads/s, failover, cost projection); ClusterOps `ClusterOps.md:37-55` (coverage, tests, estimate claims); Fake Review `fake-review-detector.md:64-75` (608k reviews/model results; test matrix not committed); SEO `seo-audit-engine.md:33-46,82-90,146` (latency/tests/audit counts); Crypto `crypto-market-simulator.md:34-43`; Hearloop `hearloop.md:185-215` (load, deploy, cost records).
- **Authority analysis / evidence:** These masters are the current fact authority and often name a source, but the source artifacts are not present here. This is external-verification status, not a silent conclusion that each number is false.
- **Reachability:** All active lane project selection and interview-prep prompts.
- **Confidence:** HIGH that verification is unavailable; LOW-to-MEDIUM on the underlying truth of any individual metric.
- **Proposed canonical statement:** “Metric retained only with a workspace evidence pointer or explicitly recorded external verification artifact, measurement date, environment, and measured/estimated classification.”
- **Per-file proposed action:** affected masters — REPLACE evidence metadata or add an internal evidence pointer during later maintenance; locked outputs — LEAVE UNCHANGED only after verification.
- **Risk if left unresolved:** The system treats externally unverified numbers as fully audited facts.
- **User decision required:** NO

## High-Severity Findings

### H-01 — Tailoring permissions conflict: immutable selection versus mandatory rewriting

- **Finding type:** CONTRADICTION
- **Severity:** HIGH
- **Summary:** The live skill allows selection/reordering of immutable locked bullets and rewrites only with explicit master-maintenance authorization; other current governance/prompt files say wording may change or mandate rewriting every bullet.
- **Why the conflict matters:** A legacy prompt can silently mutate verified wording and introduce unsupported claims.
- **Exact statements / affected locations:** `.agents/skills/resume-tailor/SKILL.md:42,76,87,159`; `governance/FACT_RULES.md:9` (“wording may change per JD”); `gpt/system-prompt.md:15-16,52-54,149,178,224,252` (mandatory rewrite); `prompts/system-prompt-patch.md:48-50,175,212`; internally conflicting preservation at `gpt/system-prompt.md:100-103` and `governance/OUTPUT_CONTRACT.md:158,171`; `CONTEXT.md:193,274` preserves locks but its embedded workflow retains old rewrite gates.
- **Authority analysis / evidence:** Level-2 skill wins for live tailoring, but level-3/4 instructions are materially inconsistent and remain runnable.
- **Reachability:** Root README/GPT Builder workflow, golden-JD regression workflow, Cursor legacy resume skill.
- **Confidence:** HIGH
- **Proposed canonical rule:** “Live tailoring selects and reorders locked bullets verbatim. Rewriting occurs only in an explicitly authorized master-maintenance task, followed by propagation and verification.”
- **Per-file proposed action:** live skill — LEAVE UNCHANGED; `FACT_RULES`, legacy prompts, Context, output contract — REPLACE or RELABEL as superseded.
- **Risk if left unresolved:** Verified facts can drift per JD.
- **User decision required:** NO

### H-02 — Project counts, section order, and output shape conflict across active-looking instructions

- **Finding type:** CONTRADICTION
- **Severity:** HIGH
- **Summary:** The live skill specifies AI 4 projects at 3/2/2/2 and Full Stack/Backend 3 at 3/3/2 plus full application artifacts. Other files require four for every lane, three by default, changed sections only, or full LaTeX only.
- **Why the conflict matters:** Different entry points produce structurally incompatible resumes and deliverables.
- **Exact statements / affected locations:** `.agents/skills/resume-tailor/SKILL.md:115-116,169`; `governance/DEFINITION_OF_DONE.md:11,22,51` (four projects/changed sections); `governance/OUTPUT_CONTRACT.md:46` and `prompts/system-prompt-patch.md:72,220,252` (top three/changed sections); `gpt/system-prompt.md:15,74,291,355,427-432` (top four/changed sections); `CONTEXT.md:267,349,359` (top three/full LaTeX); `README.md:124` (“Which 4 projects per role”).
- **Authority analysis / evidence:** The live skill is authoritative, but older files are neither uniformly labeled nor unreachable.
- **Reachability:** README, GPT Builder, governance checklist, golden tests, legacy Cursor workflow.
- **Confidence:** HIGH
- **Proposed canonical rule:** The exact structure in `.agents/skills/resume-tailor/SKILL.md:115-116`, with isolated application directory and full resume plus report.
- **Per-file proposed action:** live skill/lane templates — LEAVE UNCHANGED; all conflicting workflow documents — REPLACE or RELABEL.
- **Risk if left unresolved:** Wrong project count, section order, or incomplete deliverables.
- **User decision required:** NO

### H-03 — Deterministic workflow does not validate that selectable projects have valid locked bullets

- **Finding type:** RULE VIOLATION
- **Severity:** HIGH
- **Summary:** The live skill scores every project, but Crypto has no locked bullet section. Preflight checks project files are nonempty and checks only selected headings/counts; it does not verify per-lane bullet availability, verbatim template synchronization, unsupported-outcome language, or the 3/3/2 distribution.
- **Why the conflict matters:** A selected project can force improvisation despite the “never improvise” rule.
- **Exact statements / affected locations:** selection mandate `.agents/skills/resume-tailor/SKILL.md:93-116`; stop-before-improvising `:35-38`; no locked bank `gpt/projects/crypto-market-simulator.md:1-43`; preflight project existence only `.agents/skills/resume-tailor/scripts/preflight.py:84-86`; preflight success assertion `:151`.
- **Authority analysis / evidence:** The highest active workflow contradicts its own deterministic guarantee through an incomplete invariant set.
- **Reachability:** Every live tailoring run.
- **Confidence:** HIGH
- **Proposed canonical rule:** “A project is selectable for a lane only if it has enough current locked bullets for that lane and all selected/template text passes fact and outcome checks.”
- **Per-file proposed action:** skill and preflight — REPLACE during later maintenance; Crypto master — add/verify locked bank or ISOLATE from scoring; current report schema dependency — REPLACE.
- **Risk if left unresolved:** The agent must invent, rewrite, or fail mid-run.
- **User decision required:** NO

### H-04 — Technical Skills authorization is broader than verified evidence

- **Finding type:** RULE VIOLATION
- **Severity:** HIGH
- **Summary:** The behavioral baseline requires every skill to be supported by verified work/project facts, but the live skill also permits anything in a selected template or “authorized master context.” Legacy master lists and templates contain OAuth/JWT, MongoDB, Django, Spark, Kubernetes, and other items not supported for the claimed context.
- **Why the conflict matters:** Skills sections are resume claims even when no bullet names the technology.
- **Exact statements / affected locations:** live rule `.agents/skills/resume-tailor/SKILL.md:121`; governance project-scoping `governance/FACT_RULES.md:62,72`; broad list `gpt/system-prompt.md:446-450`; unsupported template items `templates/main.tex:168-170`, `main-one-page.tex:168-170`, `variants/marketplace-discovery.tex:194-197`; explicit counterevidence `gpt/work-experience.md:144,158` (not OAuth/JWT), `gpt/projects/ClusterOps.md:31,47` (no Kubernetes), `networking/candidate-profile.md:129` (MongoDB not shipped, where recorded).
- **Authority analysis / evidence:** The audit baseline and FACT_RULES require evidence, so template presence cannot bootstrap truth.
- **Reachability:** Live skill if a stale template is selected; legacy prompts always.
- **Confidence:** HIGH
- **Proposed canonical rule:** “A Technical Skills token is permitted only when a current verified work or project master documents actual use; a template/list is never independent evidence.”
- **Per-file proposed action:** live skill — REPLACE ambiguous clause; legacy skill list and stale templates — REPLACE; verified masters — LEAVE UNCHANGED.
- **Risk if left unresolved:** Unsupported tools can appear as candidate competencies.
- **User decision required:** NO

### H-05 — Interview prompt explicitly permits invented scenarios and embeds retired metrics

- **Finding type:** RULE VIOLATION
- **Severity:** HIGH
- **Summary:** A runnable interview-prep prompt allows plausible invented scenarios and soft numbers, then calibrates on the retired eInfochips 40% metric. This conflicts with repository truth rules and the safer codebase prompt.
- **Why the conflict matters:** Fabricated interview stories can contaminate later resume/career facts and undermine defensibility.
- **Exact statements / affected locations:** `career-stories/interview/interview-prep-system-prompt.md:13,91-94` (“may invent”), `:85` (invoice time −40%); safer counter-rule `tech-tradeoffs-codebase-prompt.md:21,26,63-68`; Amazon story-bank rule `Amazon-LP/AGENTS.md:70-77`.
- **Authority analysis / evidence:** Interview files are lower than current masters, but remain directly runnable and are not labeled superseded.
- **Reachability:** Custom GPT setup instructions at `interview-prep-system-prompt.md:3-12`.
- **Confidence:** HIGH
- **Proposed canonical rule:** “Interview preparation may create clearly hypothetical teaching examples, never first-person candidate events, metrics, ownership, or outcomes not in verified sources.”
- **Per-file proposed action:** interview-prep prompt — REPLACE or RELABEL; codebase prompt and Amazon truth rules — LEAVE UNCHANGED.
- **Risk if left unresolved:** Invented experiences can be rehearsed as facts.
- **User decision required:** NO

### H-06 — Consolidated interview Q&A contradicts current project masters

- **Finding type:** CONTRADICTION
- **Severity:** HIGH
- **Summary:** The directly usable interview Q&A describes superseded implementations as current: Fake Review has a LangChain tool that its master says is absent; Video Compliance is a three-node synchronous/in-memory-rate-limit system with three tests, while its current master is a four-stage, async, Postgres-rate-limited system with 57 tests.
- **Why the conflict matters:** A candidate can rehearse and repeat precise architecture and technology claims that contradict the resume source of truth.
- **Exact statements / affected locations:** `career-stories/interview/interview-qa.md:2754-2773` (“LangChain Tool” present) versus `gpt/projects/fake-review-detector.md:118-125` (“LangGraph / LangChain ... Not present — do not claim”); interview Q&A `:2851-2895` (three-node linear workflow), `:3120-3136` (in-memory limiter), `:3201-3209` (three tests), `:3217-3235` (synchronous/no queue) versus current `gpt/projects/youtube-ads-compliance-pipeline.md:13-19,27,45,69-77` (four stages, Postgres-backed limiter, async worker/queue, 57-test gate). The Q&A's own “all answers grounded in real code” assertions appear at `interview-qa.md:2364-2367,2843-2846`.
- **Authority analysis / evidence:** Current level-4 project masters outrank interview-prep material, but the Q&A is not labeled as a superseded snapshot and is formatted for immediate rehearsal.
- **Reachability:** `career-stories/interview/interview-prep-system-prompt.md` instructs uploading all project masters, while the adjacent Q&A is a ready-made answer bank; root history shows the older `gpt/interview/**` copies were deleted and these untracked replacements remain.
- **Confidence:** HIGH
- **Proposed canonical statement:** “Interview Q&A must be generated from and version-stamped against the current project master/repository state; contradictory older answers are explicitly superseded.”
- **Per-file proposed action:** `career-stories/interview/interview-qa.md` — RELABEL and REPLACE after repository verification; current project masters — LEAVE UNCHANGED except other findings' factual corrections.
- **Risk if left unresolved:** Interview answers can contradict resume bullets, code, and follow-up evidence.
- **User decision required:** NO

## Medium-Severity Findings

### M-01 — Hearloop has two AI versions simultaneously marked current

- **Finding type:** CONTRADICTION
- **Severity:** MEDIUM
- **Summary:** The same master labels AI Version 1 and Version 2 as current; one nearby instruction also says to replace a Version 2 bullet with Version 1 or draft a new one.
- **Why the conflict matters:** The live skill asks for the first two AI-supporting bullets, but the source does not identify one unambiguous bank.
- **Exact statements / affected locations:** `gpt/projects/hearloop.md:363` — “Version 1 (current — use this)”; `:394` — “Version 2 (current — use this; locked September 2026)”; `:460,464` mixes replacement advice with another “Version 1 (current).”
- **Authority analysis / evidence:** Same file and same authority; no silent choice is permitted.
- **Reachability:** AI lane project selection.
- **Confidence:** HIGH
- **Proposed canonical statement:** “Exactly one AI bullet bank is CURRENT; every other bank is explicitly SUPERSEDED with a reason.”
- **Per-file proposed action:** `hearloop.md` — RELABEL after user decision; AI lane templates — REPLACE only if the chosen bank differs.
- **Risk if left unresolved:** Different agents select materially different AI claims.
- **User decision required:** YES

### M-02 — Active networking profile carries stale resume facts

- **Finding type:** UNSUPPORTED CLAIM
- **Severity:** MEDIUM
- **Summary:** The active candidate profile repeats the eInfochips conflicts, promotes the discouraged Hearloop cost comparison, gives ASU a 150+ records/day metric not found in the work master, and uses a retired 37-policy-chunk YouTube snapshot.
- **Why the conflict matters:** Outreach can make factual claims before a recruiter sees the resume.
- **Exact statements / affected locations:** `networking/candidate-profile.md:15-23`; example reuse `prompts/linkedin-connection-note.md:157-159`; current YouTube master metrics `gpt/projects/youtube-ads-compliance-pipeline.md:39-48`; old handoff snapshot `handoffs/2026-06-05-youtube-compliance.md:93`; Hearloop warning `gpt/projects/hearloop.md:213-215` and `FACT_RULES.md:114`.
- **Authority analysis / evidence:** Candidate profile is lower authority but directly consumed by `.cursor/skills/linkedin-connection-note/SKILL.md`.
- **Reachability:** Active connection-note workflow.
- **Confidence:** HIGH
- **Proposed canonical statement:** “Networking facts must be generated from the same current verified masters as resumes, with no retired metrics.”
- **Per-file proposed action:** candidate profile and example prompt — REPLACE; old handoff — RELABEL/LEAVE historical.
- **Risk if left unresolved:** Recruiter outreach contradicts the attached resume.
- **User decision required:** NO

### M-03 — Legacy and historical workflows are still presented as runnable current entry points

- **Finding type:** RULE VIOLATION
- **Severity:** MEDIUM
- **Summary:** README, Context, golden-JD instructions, handoffs, and governance files route users into sources the live skill explicitly forbids for live tailoring.
- **Why the conflict matters:** “Historical” content is safe only when isolated; these files still advertise execution paths.
- **Exact statements / affected locations:** prohibition `.agents/skills/resume-tailor/SKILL.md:20`; root routing `README.md:5,96-124`; primary-template/GPT instructions `CONTEXT.md:65,516`; golden workflow `golden-jds/README.md:1-35`; `governance/FULL_STACK_TEMPLATE.md:43-56`; old YouTube setup `handoffs/2026-06-05-youtube-compliance.md:1-13`; legacy Cursor resume skill `.cursor/skills/fullstack-resume-tailor/SKILL.md:1-35`.
- **Authority analysis / evidence:** The live skill outranks these sources, but no filesystem boundary prevents humans or agents from invoking them.
- **Reachability:** Root onboarding and named Cursor skill.
- **Confidence:** HIGH
- **Proposed canonical rule:** “One current live-tailoring entry point; all older workflows visibly marked NON-LIVE/HISTORICAL and forbidden as fact sources.”
- **Per-file proposed action:** README/Context/golden/governance/legacy skill/handoffs — RELABEL or ISOLATE.
- **Risk if left unresolved:** Stale facts and obsolete rewrite rules can re-enter output.
- **User decision required:** NO

### M-04 — “Locked primary” main templates are not synchronized with current lane templates

- **Finding type:** CONTRADICTION
- **Severity:** MEDIUM
- **Summary:** Governance calls `templates/main.tex` the locked primary and `main-one-page.tex` its mirror, while the live skill uses lane variants. The main pair contains stale project claims and skills absent from current official variants.
- **Why the conflict matters:** Maintainers cannot tell whether main files are canonical, legacy, or examples.
- **Exact statements / affected locations:** `CONTEXT.md:65,516`; `governance/FULL_STACK_TEMPLATE.md:43-56`; stale claims/skills `templates/main.tex:110-132,168-170` and identical `main-one-page.tex:110-132,168-170`; live lane selection `.agents/skills/resume-tailor/SKILL.md:51-62`.
- **Authority analysis / evidence:** The higher live skill determines current generation, but current documentation still labels the stale pair “locked primary.”
- **Reachability:** Root GPT Builder and governance maintenance workflow.
- **Confidence:** HIGH
- **Proposed canonical statement:** “The three lane variants are the only live templates; any generic main template is explicitly non-live or mechanically derived and verified.”
- **Per-file proposed action:** main pair and docs — RELABEL/ISOLATE; live lane templates — LEAVE UNCHANGED except factual fixes in critical clusters.
- **Risk if left unresolved:** A maintainer can select a stale template as canonical.
- **User decision required:** NO

## Low-Severity Findings

### L-01 — Repository metadata says six projects while seven exist

- **Finding type:** CONTRADICTION
- **Severity:** LOW
- **Summary:** Documentation says the system has six master projects, but seven project master files exist after ClusterOps was added.
- **Why the conflict matters:** Limited direct fact risk, but it makes coverage and selection documentation unreliable.
- **Exact statements / affected locations:** `README.md:42-49` and `gpt/README.md:1-20` enumerate/describe six; filesystem includes seven masters, including `gpt/projects/ClusterOps.md`; `gpt/per-project-keywords.md:291` acknowledges ClusterOps.
- **Authority analysis / evidence:** File inventory is decisive for count; no factual candidate claim changes.
- **Reachability:** Root onboarding and GPT knowledge setup.
- **Confidence:** HIGH
- **Proposed canonical statement:** “Seven project masters exist; only projects with a valid lane-specific locked bank are selectable.”
- **Per-file proposed action:** README files — REPLACE.
- **Risk if left unresolved:** New project may be skipped or assumed incomplete.
- **User decision required:** NO

### L-02 — Root-level data artifacts are poorly labeled and can be mistaken for candidate truth

- **Finding type:** RULE VIOLATION
- **Severity:** LOW
- **Summary:** `data_engineer.md` is an unlabeled job/skills scratch list and `resume_evaluations.csv` presents generated scoring plus stale candidate claims without a generated/historical boundary.
- **Why the conflict matters:** Root placement makes them easy for broad-context agents to ingest as facts.
- **Exact statements / affected locations:** `data_engineer.md:1-76` mixes JD requirements, checkmarks, and tools; `resume_evaluations.csv:1-6` includes 40% eInfochips reduction, Kubernetes, and “production-level” assessments.
- **Authority analysis / evidence:** Both are lower-authority artifacts, but neither clearly states that it cannot source facts.
- **Reachability:** Broad root scans and legacy prompts.
- **Confidence:** HIGH
- **Proposed canonical rule:** “Generated evaluations and JD scratchpads must be labeled NON-AUTHORITATIVE and excluded from fact sourcing.”
- **Per-file proposed action:** both files — RELABEL or ISOLATE.
- **Risk if left unresolved:** Unsupported evaluation prose may be copied into resumes or interviews.
- **User decision required:** NO

## Unsupported and Externally Unverified Claims

Critical clusters C-03 through C-06 enumerate unsupported side-project outcomes. C-08 records the metrics whose cited proof lies outside this workspace and therefore has the required status **EXTERNALLY UNVERIFIED**. Additional externally unverifiable material was kept out of the finding count when correctly isolated: external hiring advice in `reference/headless-headhunter.md`, the humanizer's external examples/citations, job-description requirements in `golden-jds/**`, and the friend's materials in `Amazon-LP/AMZ/**` are not evidence about Shubh.

No internet lookup or external repository inspection was performed. “Externally unverified” therefore means “not independently verifiable within the authorized workspace,” not “proven false.”

## Questions for User

1. What is the official Digital Aid Seattle title to use everywhere: **Volunteer Software Engineer** or **Software Engineer**?
2. What single dated scale snapshot is defensible for Digital Aid Seattle: **300–350 active members / 10–12 ensembles**, **approximately 400 / 10–12**, or **400 / 12**?
3. For the ASU Hugging Face project, did you **own the deployment**, or only adapt your model, investigate logs, test, document, and support the teammate who owned it?
4. Which Rainbow City incident is factual: the **ensemble-manager/reversed-name/name-token** case, or the **QA/Gmail-dot/mapping-table/10%-staging** case?
5. Which Hearloop AI bullet bank is canonical: the block labeled **Version 1 current** at line 363, the **Version 2 current/locked September 2026** block at line 394, or the later two-bullet Version 1 block at line 464?

## Prioritized Cleanup Plan

1. Resolve the five user decisions, then make the employment and interview-story facts single-source before any new application.
2. Remove realized customer/user/adoption/retention/savings language from selectable side-project bullets; use “designed to” unless evidence exists.
3. Reclassify simulated cost outcomes as projections and attach measurement environment/source evidence to every locked metric.
4. Make the live skill's immutable-selection policy the single tailoring contract; retire or isolate mandatory-rewrite prompts.
5. Expand preflight to validate per-lane locked-bank availability, exact template synchronization, project counts, evidence classifications, and forbidden claim phrases.
6. Synchronize active networking and application-answer facts with locked masters.
7. Make Technical Skills evidence-derived, never template-derived.
8. Relabel main templates, Context, golden-JD workflow, handoffs, generated evaluations, and legacy Cursor skills so broad-context agents cannot treat them as current.
9. Update documentation counts and low-risk metadata only after the contamination paths above are closed.

This plan is advisory only; no cleanup was performed.

## Final Verification

- Final in-scope source-set aggregate SHA-256: `88a71f2070ebee4a800136dced90323d56b9fedd858c5b2e30333d858cf9881d`
- Initial/final source hash comparison: **IDENTICAL** for all 111 reviewed source files.
- Final staged changed paths: **none**, unchanged from baseline.
- Final unstaged tracked paths: **identical to baseline** (the same 27 modified and 7 deleted paths; no source path added, removed, or changed by the audit).
- Final untracked status entries: baseline entries unchanged, plus `?? audits/`, containing only this new report.
- Final `git status --short`: identical to the complete initial listing in this report except for the single added status entry `?? audits/`.
- Final `git diff --name-only`: identical to the initial unstaged-path list.
- Final `git diff --cached --name-only`: empty, as initially.
- Coverage-manifest validation: **239 entries = 111 REVIEWED + 125 EXCLUDED + 3 BINARY + 0 UNREADABLE**.
- Required-section validation: all 16 required sections exist once and in the required order.
- Finding-schema validation: all 20 clusters include ID, title, type, severity, summary, impact, exact statements/locations/excerpts, authority, evidence, reachability, confidence, canonical recommendation, per-file action, residual risk, and decision status.
- Audit-attributable path check: **PASS** — `audits/2026-09-18-resume-system-consistency-audit.md` is the only created or modified path attributable to this audit.
- Source-file integrity verification: **PASS**.

## Completion Status

`COMPLETE`
