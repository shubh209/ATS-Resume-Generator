# Amazon Behavioral Interview Stories — Version 1.0

Prepared for external review. Each answer is organized using Situation, Task, Action, and Result.

---

# Amazon Behavioral Stories Version 1 — NON-LIVE LEGACY BANK

> Use the individual files in `Amazon-LP/stories/` and `STORY-QUESTION-MAP.md`. This consolidated bank is retained as history and must not override current story facts. The discarded Rainbow account below remains only to document what must not be used.

# ASU Academic Transfer Credit Workplace Story
## Best question types

- Tell me about a time you went beyond the immediate issue to find a larger pattern.
- Tell me about a time you used data to influence a decision.
- Tell me about a time you improved a process outside your authority.
- Tell me about a time you balanced automation with accuracy.
- Tell me about a time you proposed and evaluated a small experiment.

## Leadership Principles

- Primary: Dive Deep
- Secondary: Ownership; Are Right, A Lot; Bias for Action

## Spoken answer: Version 1.0

### Situation

At ASU Academic Transfer Credit Solutions, our team reviewed course-transfer requests from domestic and international universities. Our own course catalog stored rules showing which outside courses matched ASU courses and the years each rule was valid.

Over time, some courses had accumulated more than 20 separate validity rules. That meant an evaluator might have to check more than 20 timelines before deciding which rule applied to one request.

### Task

My daily responsibility was to maintain transfer-rule pipelines, review course requests, and send unresolved pipeline issues to my manager through Salesforce. For this problem, the goal was to understand why the same duplicate-rule issue kept returning and find a safe way to reduce the manual review without changing a course rule when the data was unclear.

### Action

While reviewing our Salesforce tickets, I saw that many were about this same problem. Instead of treating each ticket as a separate issue, I showed the pattern to my manager and asked for approval to investigate it further.

Once my manager approved the investigation, I wrote a simple SQL query to pull two years of Salesforce tickets related to duplicate rules. I exported the results into a spreadsheet and compared the resolution of each ticket with the rules in our catalog. I then grouped the cases by institution and country to see where the problem happened most often. That is how I found that more than 80% of the tickets returned by my filter involved international institutions.

That pattern suggested to me that this was an issue in the pipeline logic, not a series of unrelated review mistakes. I did not want to overstep and force a conclusion, so I took the Salesforce data, catalog comparisons, and spreadsheet findings to my manager. I walked him through how I reached the conclusion, and he confirmed that the pipeline behavior was the part we needed to investigate.

Based on that data, I proposed a simple decision rule. If the incoming course information matched an existing rule and the difference in validity was less than two years, the system would extend the existing rule instead of creating a duplicate. If the gap was more than two years, or any of the course information was different, it would still go to a person for review. Since we were working with student academic records, accuracy was more important than automating every case.

I was an intern, so I could not change the API myself. My manager helped me turn the analysis into a written report and spreadsheet charts that stakeholders could understand without going through every ticket. In that report, I proposed testing the change only for high-volume countries such as India, Pakistan, and Saudi Arabia because those cases were already creating a large amount of review work. This gave us a way to test the idea without changing the whole pipeline.

The department head liked the proposal and presented it in a cross-department meeting. The technical team then gave us a separate environment for the prototype. For the next two months, I selected cases for the pilot, compared the old and new behavior, tracked how many tickets evaluators completed, collected their feedback, and queried Salesforce for the same duplicate-rule issue.

### Result

At the end of the pilot, the average manual review time had gone from seven minutes to four minutes per ticket. We also saw about a 30% reduction in Salesforce tickets raised for this specific problem. I reported those findings to my manager, and the organization later added the new rule-validity logic to the main system.


---

# ASU Team Capacity: EARN, OWN, DR, EBE
## Best question types

- Tell me about a time you helped a teammate who was falling behind.
- Tell me about a time your team had an uneven workload.
- Tell me about a time you took responsibility beyond your assigned work.
- Tell me about a time you improved how a team worked together.
- Tell me about a time you protected a team commitment.

## Leadership Principles

- Primary: Earn Trust
- Secondary: Ownership, Deliver Results, Strive to Be Earth's Best Employer

## Spoken answer: Version 1.0

### Situation

During my four-month Semantic Web Mining project at ASU, I worked in a team of six to build a fake-review detection system. We divided the work from reserach to data preparation and pre-processing to machine-learning models training to evaluation and fianlly deployment.

One teammate owned one of the model training and its evaluation, but he was also managing deadlines from other courses. We had not missed the final course deadline, but some of our weekly checkpoints were starting to slip. Because his model had to be combined with the rest of our work, those delays eventually hold up the whole team progress.

### Task

I needed to complete my own assigned work while helping the team to get back on schedule.

### Action

Once my own assigned work was complete, I offered to help him. We split his remaining work into smaller parts, and I verified his output before we integrated it with the rest of the project. That helped us protect the immediate checkpoint, but the same situation happened a second time.

At that point, I did not think continuing to rescue individual tasks was a good solution. I proposed that we revisit the distribution of work across the entire team. Instead of assuming everyone had the same amount of time, I asked each person about their daily availability and commitments in other courses. I used that information to suggest a new division of the remaining work based on the time people could realistically give. The team agreed to use that plan for the rest of the project.

### Result

After we redistributed the work, we started meeting our weekly checkpoints and completed the project by the course deadline. The experience changed how I think about teamwork. Equal task distribution does not always create a fair or reliable plan because people may have different constraints. I still make sure my own commitments are under control before taking on extra work, but I also try to make it easy for teammates to ask for help early. If support is repeatedly needed, I look for a planning problem instead of treating every delay as an individual failure.


---

# ASU Hugging Face Conflict: HB, DC, AR, EARN, LC
## Best question types

- Tell me about a time you disagreed with your team.
- Tell me about a time the team rejected your recommendation.
- Tell me about a time you changed your position after hearing another perspective.
- Tell me about a time you committed to a decision you disagreed with.
- Tell me about a time you worked with technology outside your experience.

## Leadership Principles

- Primary: Have Backbone; Disagree and Commit
- Secondary: Are Right, A Lot; Earn Trust; Learn and Be Curious

## Spoken answer: Version 1.0

### Situation

During my four-month Semantic Web Mining project at ASU, our six-person team built a fake-review detection application. We had completed the main parts of the application, but we still had to choose where and how to deploy it.

The decision was not straightforward. A normal web deployment would give us separate control over the frontend and backend, while a machine-learning platform could keep our multi-gigabyte dataset and application in one place.

### Task

As a member of the team, I needed to help evaluate the deployment options and explain which one I believed fit the project. At the same time, this was a team decision, so I also needed to support the final choice even if the team selected a different option.

### Action

I recommended separating the frontend and backend. My proposal was to use Vercel for the frontend and Render for the backend because that was a familiar pattern from my full-stack experience, and I believed it would give us a faster interface and more control over backend startup behavior.

One teammate disagreed and recommended Hugging Face. He had deployed similar machine-learning projects there before. He showed us one of his previous projects and explained that Hugging Face would let us keep the multi-gigabyte dataset close to the application, work within an ML-focused environment, and use deployment analytics that were useful for our project.

We discussed the two options but did not prototype them. The team voted, and most of the team supported Hugging Face. I still believed my architecture had advantages, but I also recognized that my evidence came mostly from full-stack conventions while my teammate had direct experience with this type of ML deployment.

Once the decision was made, I committed to it. I adapted my BERT model and preprocessing output for the Hugging Face environment, helped test the deployed application, documented setup steps, and supported the final demo. During testing, I also investigated the logs and helped identify why cold starts took one to two minutes: after the free-tier environment went to sleep, startup attempted to load the full dataset into memory again. We could not remove the delay with the compute available to us, but it did not cause us to miss the deadline or affect the demo.

### Result

The application was deployed successfully. The main thing I learned was that a familiar industry pattern is not automatically the best option for every workload. I should still raise a concern when I see a tradeoff, but I also need to compare the relevance of the evidence behind each option. After a team decision, committing means helping make that decision work rather than waiting to prove that my original idea was better.


---

# DAS Rainbow City Identity Collision — DISCARDED VERSION

Status: **DISCARDED — DO NOT USE.** The prior QA/Gmail-dot/mapping-table/staging-metric account was rejected by the user on September 18, 2026.

Canonical story: `stories/DAS-RainbowCity-DD-IS-AR-OWN-CO.md`.

Canonical boundary: An ensemble manager discovered duplicate records caused by different emails and reversed name order. Shubh added order-independent name-token matching as a possible-match signal with human approval. No deployment result or recurrence metric is confirmed.


---

# DAS Outside Responsibility: Venture Solution Productization
## Best question types

- Tell me about a time you worked outside your assigned responsibilities.
- Tell me about a time you invented a simpler way of working.
- Tell me about a time you improved developer productivity.
- Tell me about a time you used AI to solve an engineering problem.
- Tell me about a time you influenced more experienced developers.
- Tell me about a time your idea became an organization-wide standard.

## Leadership Principles

- Primary: Invent and Simplify
- Secondary: Ownership; Think Big; Frugality; Earn Trust

## Spoken answer: Version 1.0

### Situation

At Digital Aid Seattle, we build custom software for nonprofits. Our engineering time and resources are limited, so the faster we can finish one project, the sooner we can help another organization.

Across our projects, teams needed many of the same basic capabilities, including sign-in, user profiles, admin pages, loading states, and common frontend and backend configuration. The final design was different for each nonprofit, but much of the work underneath could potentially be reused.

### Task

This was outside the project work assigned to me, but I wanted to find out whether we could reuse that work without forcing every nonprofit into the same design.

My task was to identify which components were common enough to keep, define a consistent way to evaluate them, and propose a system that other teams could maintain after I left.

### Action

I started by reviewing Jira tickets from active and completed projects to see which work teams were repeating. I then reviewed the documentation for each project and used AI to break each solution into smaller capabilities. When the documentation was not enough, I checked the code as well. Then I worked backward from the customized version to identify the smallest useful version of each component. I recorded the results in a document and grouped them into areas such as data, integrations, presentation, and monitoring.

I needed a clear rule because making everything reusable would create another problem. We would spend more time maintaining a shared library than we saved. My threshold was that a component had to appear in more than 80% of the projects and still be easy to customize. If it was too specific to one nonprofit, it stayed with that project.

I took the findings and analysis to the CTO and proposed storing the selected components as custom npm packages. The biggest concern from experienced developers was long-term maintenance. A shared package could break several projects when React or another dependency changed. There was also a risk that teams would be forced to use an abstraction that did not fit their project.

Based on that feedback, I expanded the proposal. I wrote a productization document that required each shared solution to have clear ownership, documentation, versioning, testing, security checks, monitoring, and an upgrade path. I also separated the common behavior from the part each nonprofit could configure.

To put the idea into practice, I researched how established component libraries were organized. I used an existing starter kit to create and configure a monorepo where we could maintain separate npm packages in one place.

### Result

The stakeholders approved the approach, added it to the organization's documentation, and created a checklist that teams had to follow before adding a shared component. QA was the first department to apply the same model by creating shared test documents for common components instead of rewriting the same tests for every project. After the repository was introduced, our projected MVP delivery window went from 12 weeks to 9 weeks. The framework also became the organization-wide benchmark for deciding when a custom solution was ready to be reused.


---

# eInfochips Invoice Reporting: CO, DD, OWN, IS, IHS
## Best question types

- Tell me about a time you solved a difficult customer problem.
- Tell me about a time you found that a system did not meet the user's actual need.
- Tell me about a time you made a design decision with long-term consequences.
- Tell me about a time you went deep to find the root cause of a problem.

## Leadership Principles

- Primary: Customer Obsession
- Secondary: Dive Deep, Ownership, Invent and Simplify, Insist on the Highest Standards

## Spoken answer: Version 1.0

### Situation

During my internship at eInfochips, I was working on an internal payment tracking system used by the accounting team. The system stored more than 10,000 payment records, and seven accountants were using the pilot.

An accountant found a problem while preparing a report for stakeholders. Suppose an invoice had a total of $100, but the payment was split into four transactions with different transaction IDs. Our system ingested all four transactions correctly. The problem was that the report also showed them as four separate payments. The accountant needed one invoice-level total because the stakeholders did not need the transaction-level breakdown.

### Task

My task was to find why the report did not match the accountant's needs and correct it without losing the individual transactions required for auditing. Because this involved financial records, the change also had to preserve the accuracy of the existing data.

### Action

I investigated the ingestion flow, database schema, and reporting query. I found that the source document had an invoice ID, but our original system did not store it and did not treat an invoice as its own entity. We had designed the system at transaction level, while the report needed invoice-level data.

I considered two options. The faster option was a SQL view that grouped transactions during every report query. It required less work, but the aggregation would be repeated, the logic would stay buried in SQL, and we would still have nowhere to store invoice-level fields such as status or due date. The second option was to add an invoice parent record and connect each transaction to it. That required a schema migration and more work upfront, but it matched the actual business model and gave us a better base for future reporting and payment features.

I recommended the parent-child model, and my supervisor approved it. I created the invoices table, added the invoice foreign key to transactions, wrote the ingestion and reporting logic, and backfilled the existing data. Because the old records did not contain invoice IDs, we grouped them using fields such as vendor name, date, payment method, and amount, then manually checked the matches against the original invoices.

Since this involved financial data, I did not move everyone to the new report immediately. I ran the old and new versions side by side and checked that every invoice total still matched the transactions under it. If the numbers did not match, the system flagged the invoice for review. We also tested cases such as partial payments, refunds, and duplicate transactions. Once the results stayed consistent, we moved the accounting team to the new report.

### Result

After the change, the report showed one $100 invoice instead of four separate payments. The accountant could still open that invoice and see all four transactions when they needed the details for an audit. The accountant who raised the issue tested the new report and confirmed that it matched how the team needed to present the data to stakeholders.

What I learned was that storing the correct data is only part of the problem. I also need to understand how the user expects to view and use that data before I decide how to structure the system.
