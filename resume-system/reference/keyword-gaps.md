# Recurring unverified JD terminology

Authorized tracking for resume tailoring. This ledger is not a candidate-fact source or evidence of a skill. Frequency counts distinct supplied JDs, not repeated mentions within one JD or repeated tailoring runs. Historical frequency has not been reconstructed.

| Literal term / genuine equivalents | Distinct JD identifiers | Count | Required/core/preferred | Evidence status | Verification or learning next step | Last notice |
|---|---|---|---|---|---|---|
| OAuth 2.0 / OpenID Connect / SAML (SSO/auth frameworks) | Dexcom SDE1 (JR120540) | 1 | Core (CAMS is an auth/authz team) | Unverified — have RBAC + session auth (eInfochips), not OAuth/OIDC/SAML | Build a small OAuth2/OIDC login flow in a project, or add SSO to an existing one, then record in a project master | 2026-09-19 |
| Angular | Dexcom SDE1 (JR120540) | 1 | Core (listed language/framework) | Unverified — React is the verified frontend framework (transferable, not Angular) | Build a small Angular app if targeting Angular shops; otherwise rely on React as the comparable-framework match | 2026-09-19 |
| Kotlin | Dexcom SDE1 (JR120540) | 1 | Core (listed language) | Unverified — no Kotlin in masters | Learn-on-the-job for 0-2yr role; no action unless pursuing Kotlin/JVM roles | 2026-09-19 |
| Java | Dexcom SDE1 (JR120540); Pure SWE (NYC); UBS AO SWE (344835BR) | 3 | Core (listed language) | Unverified — no Java in masters (Go/Node/TS/Python verified) | RECURRING (3 JDs): a small Java/Spring service is the single highest-value gap to close for JVM-stack roles | 2026-09-19 |
| Kubernetes | Dexcom SDE1 (JR120540) | 1 | Preferred (exposure) | Unverified — Docker verified, Kubernetes not | Deploy a containerized project to a K8s cluster (even local kind/minikube) and record anchors in a master | 2026-09-19 |
| Helm | Dexcom SDE1 (JR120540) | 1 | Preferred (exposure) | Unverified — no Helm in masters | Pairs with Kubernetes step above; no standalone action | 2026-09-19 |
| NoSQL (Cassandra / MongoDB / DynamoDB) | Dexcom SDE1 (JR120540) | 1 | Core (RDBMS or NoSQL acceptable) | Unverified — PostgreSQL/Redis verified; no document/wide-column NoSQL. RDBMS alternative is satisfied | Optional: add a MongoDB or DynamoDB slice to a project if targeting NoSQL-heavy roles | 2026-09-19 |
| React Native | Pure SWE (NYC) | 1 | Core (listed relevant tech; product has mobile) | Unverified — React (web) verified, not React Native (mobile) | Build a small React Native app if targeting mobile/cross-platform roles; otherwise React is the adjacent match | 2026-09-19 |
| .NET Framework / C# | UBS AO SWE (344835BR); UHS Associate SWE (368933) | 2 | UBS core (full-stack Java, .NET-adjacent); UHS preferred | Unverified — no .NET or C# in masters | RECURRING (2 JDs): Microsoft-stack roles; a small .NET/C# service would convert it. Lower priority than Java | 2026-09-19 |
| SQL Server (T-SQL, stored procedures) | UHS Associate SWE (368933) | 1 | Core (SQL Server views/tables/stored procedures) | Unverified for SQL Server specifically — PostgreSQL/transactions/stored-proc concepts are transferable, not SQL Server itself | Transferable from PostgreSQL; note the engine difference if asked. Optional: a small SQL Server project | 2026-09-19 |
| Visual Studio | UHS Associate SWE (368933) | 1 | Preferred | Unverified — VS Code/other IDEs used, not Visual Studio | Trivial tooling gap; no action needed | 2026-09-19 |
| Spring (Boot / JPA / Framework) | UBS AO SWE (344835BR) | 1 | Core (Java/Spring stack) | Unverified — no Spring in masters | Pairs with the Java gap; a Spring Boot service closes both | 2026-09-19 |

**Recurrence notices:**
- **Java** — unverified Core requirement in **3 distinct JDs** (Dexcom, Pure, UBS). Single highest-value gap to close for JVM-stack roles; a small Java/Spring service converts it, and also covers the Spring gap.
- **.NET Framework / C#** — unverified in **2 distinct JDs** (UBS .NET-adjacent, UHS preferred). Second Microsoft-stack signal; lower priority than Java.
- (NoSQL/MongoDB would also recur if the CareTria JD, where MongoDB appeared, is later logged; it was not logged, so its count stays at 1 per the no-invented-history rule.)

Counts begin from the first logged entry forward; earlier unlogged JDs were not reconstructed.
