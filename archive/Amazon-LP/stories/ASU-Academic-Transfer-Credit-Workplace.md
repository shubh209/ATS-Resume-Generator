# ASU Academic Transfer Credit Rules

Status: Version 3.0, needs what-I-would-do-differently confirmation

## Questions this story can answer

- Tell me about a time you found a larger pattern behind repeated issues.
- Tell me about a time you used data to influence a decision.
- Tell me about a time you improved a process outside your authority.
- Tell me about a time you balanced automation with accuracy.
- Tell me about a time you proposed and evaluated an experiment.

## Leadership Principles

- Primary: Dive Deep
- Secondary: Ownership; Are Right, A Lot; Bias for Action

## Situation

- **My role:** I was a Data Management Intern with ASU's Academic Transfer Credit team.
- **Where:** We reviewed whether courses from other universities could count toward an ASU degree.
- **My work:** I maintained the transfer-rule process and handled Salesforce issues.
- **Problem:** The system created new rules when a similar course rule already existed.
- **Scale:** Some courses had more than 20 separate validity rules.
- **Impact:** Evaluators had to review every rule before deciding whether a course transferred.

## Task

- **My duties:** I maintained the AZTransfer pipeline, reviewed course requests, and escalated unresolved issues.
- **Immediate responsibility:** I needed to understand why the same Salesforce issue kept returning.
- **Process goal:** I wanted to reduce duplicate rules and manual review time.
- **Safety requirement:** Any change had to protect the accuracy of student academic records.
- **Authority boundary:** I did not own the API and could not implement the system change myself.

## Action

### 1. I raised the repeated pattern

- **What:** I showed my manager that the same issue appeared across many Salesforce tickets.
- **How:** I brought examples from my normal ticket-review work.
- **Why:** Resolving the tickets individually would not stop the problem from returning.

### 2. I investigated two years of evidence

- **What:** I reviewed two years of Salesforce tickets after receiving my manager's approval.
- **How:** I queried the standardized resolution fields and exported the results to a spreadsheet.
- **Why:** I needed enough historical evidence to separate a system pattern from isolated mistakes.

### 3. I compared tickets with the course catalog

- **What:** I checked how each ticket was resolved against the rules already stored.
- **How:** I grouped the cases by institution and country.
- **Why:** I wanted to find where the duplicate-rule behavior occurred most often.

### 4. I identified the likely cause

- **What:** I concluded that the validity-date logic was creating duplicate rules.
- **How:** I found that more than 80% of the tickets returned by my filter involved international institutions.
- **Why:** The repeated pattern did not look like unrelated evaluator mistakes.

### 5. I proposed a narrow decision rule

- **What:** I recommended extending an existing rule only when the course information matched.
- **How:** The validity gap also had to be less than two years; other cases stayed with an evaluator.
- **Why:** I wanted to reduce obvious duplicates without automating uncertain academic decisions.

### 6. I proposed a limited pilot

- **What:** I recommended testing the rule with India, Pakistan, and Saudi Arabia first.
- **How:** My manager helped organize the evidence, and I presented the recommendation to the department head.
- **Why:** Those countries had many affected cases and gave us a bounded way to test the idea.

### 7. I evaluated the prototype

- **What:** I stayed involved after another technical team built the change.
- **How:** For two months, I selected cases, compared behavior, collected evaluator feedback, and measured Salesforce tickets.
- **Why:** I needed measured evidence before recommending that the logic enter the main system.

## Result

- **Review time:** Average manual review time fell from seven minutes to four minutes per ticket.
- **Ticket volume:** Salesforce tickets for this issue fell by about 30% during the pilot.
- **Adoption:** The organization later added the new rule-validity logic to the main system.
- **Ownership boundary:** Another technical team implemented the API change.
- **Learning:** I learned that I could improve a system without owning it.
- **Influence lesson:** I needed to understand the problem, support the idea with data, and work with the people who could make the change.
- **What I would do differently:** Not yet separately confirmed.

## Supporting information

### Specific data

- Two years of Salesforce tickets
- More than 20 validity rules on some courses
- More than 80% of the filtered cases involved international institutions
- Two-year validity-gap threshold
- Two-month pilot
- Review time changed from seven minutes to four minutes
- Related ticket volume fell by about 30%

### Technical details

- Salesforce ticket query using standardized resolution fields
- Spreadsheet comparison against the existing course catalog
- Grouping by institution and country
- Rule extension only when course information matched and the gap was under two years
- Human review for larger gaps or conflicting information

### Alternatives considered

- Continue resolving duplicate-rule tickets one at a time.
- Automate every validity mismatch.
- Use a narrow rule and keep uncertain cases under human review.
- I selected the third option because academic-record accuracy mattered more than full automation.

### Feedback and collaboration

- My manager approved the investigation.
- My manager confirmed that the API behavior needed investigation.
- My manager helped organize the findings for stakeholders.
- I presented the recommendation to the department head.
- Another technical team implemented the prototype.

### Ownership boundaries

- I found the pattern, analyzed the data, proposed the rule, and evaluated the pilot.
- I did not implement the API change.
- More than 80% refers only to the tickets returned by my filter.
- The main-system adoption happened after I left ASU.

### Memory chain

> Repeated tickets → manager approval → two years of data → 80% international → two-year rule → three-country pilot → seven to four minutes → 30% fewer tickets
