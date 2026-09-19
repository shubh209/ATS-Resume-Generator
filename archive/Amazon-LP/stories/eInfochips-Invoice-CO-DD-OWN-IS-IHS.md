# eInfochips Failed Sprint Demo

Status: Version 3.0, ready for review

## Questions this story can answer

- Tell me about a time you failed.
- Tell me about a time you received difficult feedback.
- Tell me about a time your work did not meet expectations.
- Tell me about a mistake you made.
- Tell me about a time you rebuilt trust.
- Tell me about a time you improved quality after finding a gap.

## Leadership Principles

- Primary: Ownership; Earn Trust
- Secondary: Dive Deep; Insist on the Highest Standards; Learn and Be Curious

## Situation

- **My role:** I was a software engineering intern at eInfochips.
- **Where:** I was working on an internal payment-tracking tool.
- **Team:** I worked on the backend and coordinated with the UI team.
- **Event:** We had an initial sprint demo for accountants using the tool.
- **Problem:** The accountants entered invalid values into different fields during the demo.
- **Failure:** The UI broke because I had tested the happy path but missed proper error-path testing.
- **Timing:** This was an initial sprint demo, not the final demo, and no final deadline was missed.

## Task

- **My duty:** I was responsible for the backend API response contract.
- **Integration responsibility:** The API responses had to match what the UI expected.
- **Immediate goal:** I needed to find why the UI failed on invalid input.
- **Recovery goal:** I needed to prepare the complete flow for the follow-up demo.
- **Quality goal:** I needed to test failure behavior as carefully as successful behavior.

## Action

### 1. I accepted the feedback

- **What:** I accepted my manager's criticism after the failed demo.
- **How:** I listened without blaming the UI team or the sprint timeline.
- **Why:** He was right that my preparation was not good enough.

### 2. I identified my incorrect assumption

- **What:** I reviewed how I had decided the demo was ready.
- **How:** I compared my test coverage with the invalid inputs used during the demo.
- **Why:** I had treated a working happy path as proof that the full flow worked.

### 3. I investigated with the UI team

- **What:** I reviewed the failed cases with the UI team.
- **How:** We traced the invalid requests from the form through the backend response and UI handling.
- **Why:** The failure crossed the API boundary, so both sides needed to inspect the same cases.

### 4. I found the contract mismatch

- **What:** I identified inconsistent backend error-response formats.
- **How:** I compared the returned errors with the structures the frontend expected.
- **Why:** The UI could not handle errors reliably when the response shape changed by case.

### 5. I standardized the API responses

- **What:** I created consistent response structures.
- **How:** I covered success, validation errors, authentication errors, and missing-data cases.
- **Why:** The UI needed a predictable contract for every outcome.

### 6. I expanded the end-to-end checks

- **What:** I added checks for both happy paths and error paths.
- **How:** I tested valid input and invalid input through the complete backend-to-UI flow.
- **Why:** Unit-level success was not enough to prove that the user experience worked.

### 7. I prepared for the follow-up demo

- **What:** I tested the complete flow before presenting it again.
- **How:** I repeated the valid and invalid field cases that had exposed the original gap.
- **Why:** I needed evidence that we had fixed the preparation problem, not only the first visible error.

## Result

- **Follow-up outcome:** The follow-up demo went smoothly.
- **Technical outcome:** The backend and UI had a clearer API contract.
- **Team impact:** The consistent response structure reduced confusion between the backend and UI teams.
- **Trust:** I rebuilt trust by owning the miss instead of blaming another team or the timeline.
- **Learning:** Direct feedback is useful when it is true.
- **Behavior change:** Before a demo, I now test how the system fails, not only how it succeeds.
- **Deadline clarification:** The first demo failed during an initial sprint, but the final deadline was not missed.

## Supporting information

### Technical details

- Boundary: backend API responses and frontend handling
- Cases standardized: success, validation, authentication, and missing data
- Testing added: end-to-end happy-path and error-path checks

### Root cause

- I tested successful input but did not test invalid input properly.
- Backend error responses did not consistently match the UI contract.
- The UI broke instead of handling the failed requests predictably.

### Alternatives considered

- No alternatives have been confirmed.
- Do not claim that I compared several solutions unless more facts are added.

### Feedback

- My manager said my preparation was not good enough.
- I accepted the feedback because the error paths had not been properly tested.

### Ownership boundaries

- I owned the backend API response contract.
- I investigated the mismatch with the UI team.
- I did not blame the frontend for failing to handle an inconsistent contract.

### Memory chain

> Initial sprint demo → invalid input → UI breaks → direct feedback → contract mismatch → standard responses → end-to-end error tests → smooth follow-up

