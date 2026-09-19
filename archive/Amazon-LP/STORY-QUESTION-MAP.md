# Amazon Behavioral Story Question Map

This map shows which behavioral questions each story can answer without changing its facts. A story can support several questions, but the opening and emphasis should change based on the question.

Use the best-fit questions first. Use backup questions only when the relevant facts are clear. Do not use a story for the avoid questions unless new facts are confirmed.

## Story preparation table

| Story | Main principles | Conflict or challenge | Decision | Main tradeoff | Result | Follow-up details |
|---|---|---|---|---|---|---|
| eInfochips Invoice Reporting | Customer Obsession, Dive Deep, Ownership, Highest Standards | The system stored transactions correctly but could not produce the invoice-level report accountants needed. | Treat the invoice as a separate business record instead of grouping payments only when a report ran. | Faster SQL fix versus a larger change that supported accurate future reporting. | The accountant received one invoice total while keeping the transaction details needed for audits. | Historical backfill, reconciliation, edge cases, ownership of the original design. |
| ASU Academic Transfer Credit | Dive Deep, Ownership, Are Right A Lot, Bias for Action | Repeated duplicate rules slowed evaluators, but the user did not own the system. | Use historical evidence to propose a limited rule and test it with selected countries. | Faster reviews versus the risk of changing a student's academic record incorrectly. | Review time fell from seven to four minutes, and related tickets fell about 30% during the test. | Meaning of the 80% figure, two-year threshold, pilot measurement, implementation ownership. |
| ASU Team Capacity | Earn Trust, Ownership, Deliver Results | A teammate's workload caused weekly checkpoints to slip. | Help with the immediate work, then redistribute the remaining work using everyone's real availability. | Supporting a teammate versus protecting personal commitments and avoiding repeated rescue work. | The team resumed meeting checkpoints and completed the project by the course deadline. | How the teammate responded, what work was shared, how availability was discussed. |
| ASU Hugging Face Disagreement | Have Backbone, Earn Trust, Learn and Be Curious | The user and a teammate preferred different deployment approaches. | Raise the preferred option, listen to more relevant evidence, accept the team vote, and support Hugging Face. | Familiar full-stack control versus an ML-focused platform with dataset and environment benefits. | The team deployed the application; the user integrated the Gradio frontend and owned the frontend–backend contract, not the full deployment. | Teammate's evidence, exact integration ownership, unresolved cold start, why the original idea was not proven better. |
| DAS Rainbow City Identity Collision | Dive Deep, Customer Obsession, Ownership, Invent and Simplify | An ensemble manager discovered that two records represented one member because the source records used different emails and reversed name order. | Add order-independent name-token matching as a possible-match signal and require human approval. | Better duplicate detection versus the risk of merging two different people. | The matching rule and human-review safeguard were added; deployment and recurrence metrics are unconfirmed. | Ensemble-manager discovery, different emails, reversed name order, and the human-approval boundary. |
| DAS Venture Solution Productization | Invent and Simplify, Ownership, Think Big, Earn Trust | Teams repeated common work, but a shared library could create maintenance problems or force bad abstractions. | Reuse only common and configurable capabilities, with ownership and quality rules for every package. | Faster future development versus long-term maintenance and reduced project flexibility. | The framework became an organizational standard; the MVP window was projected to move from 12 to 9 weeks. | AI usage, 80% threshold, developer concerns, monorepo choice, projected versus measured result. |

## Answer framework

### Situation

- Where was this?
- What was the problem?
- Why did it matter?

Keep this to one or two simple sentences. Someone without technical knowledge should understand it.

### Task

- What was your responsibility?
- What was at stake?

State the goal directly. For example: “I wanted to fix the reporting problem without losing the details needed for audits.”

### Action

- What did you do?
- What options did you consider?
- Why did you choose your path?
- How did you communicate or handle the people involved?

The action should explain judgment. Technical detail belongs here only when it explains a decision, risk, tradeoff, or way of working.

### Result

- What changed?
- What was the impact?
- What metric, time saving, quality improvement, risk reduction, or customer benefit can be defended?

### Lesson learned

- What did you learn?
- What would you do differently today?
- What did you change in later work because of this experience?

## Simple rule

For every story, ask: **What was the human or business problem behind the technical problem?**

Do not explain the whole project. Explain your judgment inside the project.

## Story 1 eInfochips Invoice Reporting

### Best-fit questions

- Tell me about a time you discovered that a system did not meet the customer's real need.
- Tell me about a time you solved a difficult customer problem.
- Tell me about a time you dug into a problem and found the root cause.
- Tell me about a time you chose long-term value over a faster solution.
- Tell me about a time you protected quality while changing sensitive data.
- Tell me about a time you realized that the original direction could cause future problems.

### Backup questions

- Tell me about a difficult decision where you had more than one reasonable option.
- Tell me about a time you simplified a complicated process for a customer.
- Tell me about a time you tested a change carefully before releasing it.

### Use only if confirmed

- Tell me about a mistake you made. This works only if you personally helped make the original transaction-level design decision and can clearly own that mistake.

### Avoid

- Tight deadline or calculated risk
- Disagreement with a teammate
- Tough feedback
- Missed commitment

### Memory path

Accountant's report did not work -> understand the real need -> find the missing invoice relationship -> compare two options -> choose the safer long-term model -> validate financial data -> accountant confirms the result.

## Story 2 ASU Academic Transfer Credit

### Best-fit questions

- Tell me about a time you noticed a larger pattern behind repeated problems.
- Tell me about a time you used data to find the root cause.
- Tell me about a time a metric or trend showed that something needed to change.
- Tell me about a time you took responsibility beyond your assigned work.
- Tell me about a time you influenced a decision without owning the system.
- Tell me about a time you balanced efficiency with accuracy.
- Tell me about a time you proposed a small test before making a larger change.
- Tell me about a time you saw a bigger opportunity in routine work.

### Backup questions

- Tell me about a time you acted even though you did not have every answer.
- Tell me about a time you improved a process for customers or coworkers.
- Tell me about a time you worked with another team to make a change.

### Avoid

- Personal failure or mistake
- Tight deadline
- Conflict with a teammate
- Missed commitment

### Memory path

Repeated tickets -> ask manager to investigate -> review two years of cases -> find international pattern -> propose a safe rule -> limited three-country test -> measure time and ticket reduction -> main system adopts the change.

## Story 3 ASU Team Capacity

### Best-fit questions

- Tell me about a time you saw a teammate struggling and helped them.
- Tell me about a time your team had an uneven workload.
- Tell me about a time you improved team productivity.
- Tell me about a time you protected a team commitment.
- Tell me about a time you found a team problem and helped fix it.
- Tell me about a time you took on work outside your responsibility.
- Tell me about a time you made it easier for someone to ask for help.

### Backup questions

- Tell me about a time a project was at risk of falling behind.
- Tell me about a time you improved how a team planned its work.
- Tell me about a time you earned trust with a teammate.

### Avoid

- Missed deadline, because the final course deadline was met
- Tough feedback
- Disagreement or conflict
- Individual failure
- Claiming that you completed the teammate's model alone

### Memory path

Weekly checkpoints slip -> finish my work -> help teammate twice -> notice repeated support is not enough -> discuss everyone's availability -> redistribute remaining work -> meet checkpoints and final deadline.

## Story 4 ASU Hugging Face Disagreement

### Best-fit questions

- Tell me about a time you disagreed with a teammate.
- Tell me about a time your team rejected your recommendation.
- Tell me about a time someone challenged you to think differently.
- Tell me about a time you changed your position after hearing better evidence.
- Tell me about a time you committed to a decision you disagreed with.
- Tell me about a time you worked with a technology outside your experience.
- Tell me about a time you learned that your familiar approach was not the best fit.

### Backup questions

- Tell me about a time you had to support a team decision you did not make.
- Tell me about a time you learned from someone with more relevant experience.
- Tell me about a time a solution had a limitation you could not fully remove.

### Avoid

- Claiming that you convinced the team to choose your idea
- Claiming that the cold start proved your original idea was better
- Personal failure or missed commitment
- Customer Obsession
- Tight deadline

### Memory path

Need deployment -> I recommend split services -> teammate recommends Hugging Face -> compare experience and evidence -> team votes -> commit to the choice -> adapt my work and help test -> learn to judge evidence by relevance.

## Story 5 DAS Rainbow City Identity Collision

### Best-fit questions

- Tell me about a time you found the root cause of a complex problem.
- Tell me about a time conflicting data led you to investigate further.
- Tell me about a difficult decision with several reasonable options.
- Tell me about a time you chose accuracy over full automation.
- Tell me about a time you protected a customer from a harmful mistake.
- Tell me about a time you improved data quality across multiple systems.
- Tell me about a time testing exposed a weakness and led to a better design.
- Tell me about a time you balanced customer experience with operational effort.

### Backup questions

- Tell me about a time you challenged an assumption in a system design.
- Tell me about a time user feedback exposed a serious data-quality issue.
- Tell me about a time you created a process for handling unclear cases.
- Tell me about a time you prevented the same problem from happening again.

### Avoid

- Tight deadline, because the project did not have one
- Production or recurrence impact, because neither deployment nor a recurrence metric is confirmed
- Personal failure, unless your ownership of the missing normalization rule is confirmed
- Claiming that you found the original symptom; an ensemble manager discovered it

### Memory path

Ensemble manager finds two records for one member -> compare source records -> find different emails and reversed name order -> trace exact-email matching -> add order-independent name-token signal -> require human approval -> leave deployment and recurrence unclaimed.

## Story 6 DAS Venture Solution Productization

### Best-fit questions

- Tell me about a time you took on something important outside your responsibility.
- Tell me about a time you invented a simpler way of working.
- Tell me about a time you improved developer productivity.
- Tell me about a time you used AI to help solve an engineering problem.
- Tell me about a time you influenced more experienced developers.
- Tell me about a time you saw a larger opportunity in repeated work.
- Tell me about a time your idea became a wider organizational standard.
- Tell me about a time you worked with limited time or engineering resources.
- Tell me about a time you considered long-term maintenance before moving forward.

### Backup questions

- Tell me about a time feedback caused you to improve your proposal.
- Tell me about a time you used outside ideas to improve how your organization worked.
- Tell me about a time you created clear standards for future teams.
- Tell me about a time you balanced reuse with customization.

### Avoid

- Claiming that projects already shipped three weeks faster; the 12-to-9-week result was a planning estimate
- Personal failure or missed commitment
- Tight deadline
- Tough feedback unless the experienced developers' concerns felt like direct feedback and changed your behavior, not only the proposal

### Memory path

Notice repeated project work -> review Jira and documents -> use AI to break work into capabilities -> define an 80% rule -> propose shared packages -> hear maintenance concerns -> add ownership and quality rules -> organization adopts the framework.

## Current coverage gaps

The six stories do not yet give strong, honest answers for these high-value questions:

- Tell me about a real mistake or failure and what changed afterward.
- Tell me about tough feedback you received and how you changed your behavior.
- Tell me about a commitment or deadline you actually missed.
- Tell me about a project you handed over to another owner.
- Tell me about a time two teams had different goals and you helped align them.
- Tell me about a time an AI tool produced a bad result and changed how you use AI.
- Tell me about a calculated risk you took when speed was critical.

One new story may cover several gaps, but only if the same real event contains those facts.

## How to use this map

When a question is asked, choose the strongest matching story and change the emphasis:

- For investigation, focus on the clue, evidence, root cause, and verification.
- For ownership, focus on why you stepped in and how you followed through.
- For customers, focus on the person's problem and what changed for them.
- For disagreement, focus on the shared goal, both viewpoints, evidence, and commitment.
- For quality, focus on the risk, safeguard, testing, and prevention.
- For learning, focus on the knowledge gap, how you learned, and how your behavior changed.
- For results, focus on the baseline, obstacle, key decisions, and measured outcome.

Do not memorize a different script for every question. Remember the facts and memory path, then answer the part of the story that the interviewer asked about.

## Target interview question shortlist

These are the seven question types we will prepare first. They do not require seven different stories. One story can answer more than one question when the facts support both versions.

### 1 Tell me about a time you helped a teammate succeed

**Best story:** ASU Team Capacity.

**Focus:** How you noticed the teammate needed help, how you approached him, how you helped without taking over, and why you later changed the team's workload plan.

**Missing facts:** The teammate's reaction, the exact help you provided, whether anyone resisted redistribution, and what feedback the team gave you.

### 2 Describe an important project you delivered under a tight deadline

**Current status:** Gap.

None of the six documented stories contains a strong, confirmed tight deadline with clear prioritization and sacrifice. Do not add a deadline to make another story fit.

**Story needed:** Deadline -> scope at risk -> priorities chosen -> work deferred -> communication -> delivery result -> lesson.

### 3 Tell me about a time you worked outside your comfort zone

**Best story:** ASU Hugging Face Disagreement.

**Focus:** Your experience was in full-stack deployment, while the selected ML platform was unfamiliar. Explain how you learned enough to adapt your work and support the team's decision.

**Backup:** DAS Venture Solution Productization, if the unfamiliar area was organization-wide product strategy rather than coding.

### 4 Tell me about a time your work affected other people or teams

**Best current story:** DAS Venture Solution Productization.

**Focus:** The effect on developers, QA, project planning, and future nonprofit teams. Explain the alternatives, the maintenance concerns raised by experienced developers, and how their feedback changed the proposal.

**Backup:** ASU Academic Transfer Credit, but only for cross-team impact. No disagreement is currently documented in that story.

### 5 Tell me about a time customer input changed your approach

**New story:** DAS instrument-needs feature.

**Known starting point:** The customer requested a way to analyze how many players were needed for each instrument. Their marketing team wanted to use that information to create recruitment flyers based on actual instrument needs.

**Facts still needed:** Original product direction, who requested the change, when it arrived, why it mattered, alternatives considered, effect on current scope, stakeholder discussion, implementation ownership, result, and customer feedback.

### 6 Tell me about a time you organized a product initiative across stakeholders

**Best story:** DAS Venture Solution Productization.

**Focus:** How you identified repeated work, gathered information across projects, involved the CTO and experienced developers, responded to maintenance concerns, created the standard, and helped the organization adopt it.

**Business framing:** Limited volunteer time and nonprofit resources made cost and delivery speed more important than creating elaborate reusable components or features that did not address the main problem.

### 7 Describe work beyond your formal responsibilities

**Best story:** DAS Venture Solution Productization.

**Focus:** Why you stepped outside your assigned project work, what organizational problem you saw, what you personally created, and how you made the work maintainable after you left.

This uses the same facts as question 6. The difference is emphasis: question 6 centers on stakeholder coordination; question 7 centers on ownership beyond your role.

## Required follow-up pack for every story

Every finished answer must be followed by preparation notes covering these areas:

### Specific evidence

- Exact metric, scale, time period, or observable result.
- What the number measures and what it does not measure.
- Whether the result was measured, estimated, projected, tested in staging, or observed in production.

### Technical depth

- The minimum technical explanation needed to defend the story.
- The root cause or important design detail.
- The user's exact implementation versus the work completed by teammates.
- Testing, validation, safety, and edge cases.

### Alternatives and tradeoffs

- At least two paths that were seriously considered.
- Why the selected path fit the customer, team, time, cost, or risk.
- What disadvantage came with the selected path.

### Manager and stakeholder feedback

- What the manager, teammate, customer, QA engineer, or stakeholder actually said or questioned.
- How the user responded.
- What changed because of that feedback.
- Do not invent resistance or feedback to make the story sound stronger.

### What I would do differently

- One specific decision or behavior that would change today.
- Why the new approach would be better.
- Evidence that the lesson affected later work, when available.
