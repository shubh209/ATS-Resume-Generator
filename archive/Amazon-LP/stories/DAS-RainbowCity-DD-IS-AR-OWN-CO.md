# DAS Rainbow City Duplicate Member

Status: Version 4.0, core incident user-confirmed September 18, 2026; learning still needs confirmation

## Questions this story can answer

- Tell me about a time customer input changed your approach.
- Tell me about a time you found the root cause of a problem.
- Tell me about a time you solved more than the immediate issue.
- Tell me about a time your work affected another person's decision.
- Tell me about a time you balanced automation with risk.

## Leadership Principles

- Primary: Customer Obsession; Dive Deep
- Secondary: Ownership; Earn Trust; Invent and Simplify

## Situation

- **My role:** I was a developer maintaining the Rainbow City membership management system.
- **Where:** I worked on the project through Digital Aid Seattle.
- **My area:** I maintained integrations with Stripe, Zeffy, and Mailchimp.
- **Problem:** An ensemble manager saw two records and believed they represented two people with the same name.
- **Impact:** He used that information to plan a practice session.
- **Discovery:** At the practice, he learned that both records belonged to one person.

## Task

- **My duty:** I owned the third-party data integration pipeline.
- **Immediate responsibility:** I needed to explain the incorrect data to the ensemble manager.
- **Technical responsibility:** I needed to find why the pipeline had created two Member records.
- **Long-term goal:** I needed to prevent the same pattern from creating another silent duplicate.
- **Safety requirement:** The fix could not merge two different people by mistake.

## Action

### 1. I compared the two records

- **What:** I pulled both Member records and compared every field.
- **How:** I checked the values side by side across the source data.
- **Why:** I needed to find the smallest difference that prevented the match.

### 2. I isolated the mismatched fields

- **What:** I found different email addresses and reversed name order.
- **How:** I compared `firstname lastname` in one source with `lastname firstname` in the other.
- **Why:** Those were the only differences between records that otherwise represented the same person.

### 3. I traced the matching logic

- **What:** I reviewed how the pipeline resolved a person's identity.
- **How:** I followed the records through the exact-email matching rule.
- **Why:** I wanted the root cause instead of deleting one duplicate row.

### 4. I explained the problem to the manager

- **What:** I corrected the ensemble manager's understanding immediately.
- **How:** I told him that both records belonged to one person before the code change shipped.
- **Why:** He needed accurate information for practice planning without waiting for the technical fix.

### 5. I added a second matching signal

- **What:** I added name-token comparison.
- **How:** I compared the words in each name without depending on their order.
- **Why:** Reversed first and last names should still be detected as a possible match.

### 6. I rejected automatic merging

- **What:** I kept the new name signal from merging records by itself.
- **How:** The system flagged a possible match and required a person to approve it.
- **Why:** Two different people can have the same name.

### 7. I kept the fail-safe design

- **What:** I made the new detection rule work with the existing human review process.
- **How:** I used the name tokens as supporting evidence rather than final identity proof.
- **Why:** A missed match was safer than silently connecting data to the wrong person.

## Result

- **Root cause:** The pipeline relied only on exact email and silently created two Member records.
- **Implemented change:** I added order-independent name-token matching as a possible-match signal.
- **Safety outcome:** A person still approved the final merge.
- **Evidence boundary:** No deployment result or recurrence metric has been confirmed.
- **Learning:** Needs confirmation from the user.
- **What I would do differently:** Needs confirmation from the user.

## Supporting information

### Technical details

- Data sources: Stripe, Zeffy, and Mailchimp
- Original identity signal: exact email
- Failure pattern: different emails and reversed name order
- Added signal: normalized name-token comparison
- Safety control: human approval before merge

### Alternatives considered

- Delete only the duplicate record.
- Automatically merge records with matching name tokens.
- Detect a possible match and require human approval.
- I selected the third option because it fixed recurrence without risking an incorrect automatic merge.

### Ownership boundaries

- I maintained the third-party integration pipeline.
- I compared the source records and traced the matching logic.
- I added the name-token signal.
- No deployment result or recurrence metric has been confirmed.

### Feedback

- The ensemble manager reported the customer impact.
- Manager feedback has not been confirmed.

### Memory chain

> Manager planned from duplicate → compare records → emails differ → names reversed → exact-email root cause → token match → human approval
