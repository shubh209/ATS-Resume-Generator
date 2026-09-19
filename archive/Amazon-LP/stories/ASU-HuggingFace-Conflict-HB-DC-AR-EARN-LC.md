# ASU Hugging Face Deployment Conflict

Status: Version 4.0, ownership boundary user-confirmed September 18, 2026; learning still needs confirmation

## Questions this story can answer

- Tell me about a time you disagreed with a teammate.
- Tell me about a time someone changed your mind.
- Tell me about a time you committed to a decision that was not your first choice.
- Tell me about a time you considered technical tradeoffs.
- Tell me about a time you put the project goal ahead of your preference.

## Leadership Principles

- Primary: Have Backbone; Disagree and Commit
- Secondary: Are Right, A Lot; Earn Trust

## Situation

- **My role:** I was working with a teammate on an ASU machine-learning project.
- **Where:** The project was a fake-review detection application.
- **Project:** We used a RoBERTa NLP model to detect fake reviews.
- **Decision:** We needed to choose how to deploy the application.
- **Disagreement:** I preferred Vercel and Render, while my teammate preferred Hugging Face Spaces.

## Task

- **My duty:** I needed to help select a deployment approach for the project.
- **Options:** We could separate the frontend and backend or use one ML-focused platform.
- **Goal:** We needed an approach that presented the model clearly and allowed us to ship the project.
- **Team responsibility:** I also needed to support the final decision even if it was not my first choice.

## Action

### 1. I proposed Vercel and Render

- **What:** I recommended Vercel for the frontend and Render for the backend.
- **How:** I designed the option around separate services and a custom API.
- **Why:** It gave us more infrastructure control and resembled a production web architecture.

### 2. I listened to my teammate's proposal

- **What:** I considered his recommendation to use Hugging Face Spaces.
- **How:** We discussed its ML hosting, optional free GPU inference, and faster setup.
- **Why:** I needed to judge his option on its value rather than defend my original preference.

### 3. I compared the maintenance tradeoff

- **What:** I compared the number of services each option required.
- **How:** I weighed two maintained services against a single ML-focused environment.
- **Why:** More control would also create more setup and maintenance work.

### 4. I compared the project risk

- **What:** I considered deployment speed and cold-start latency risk.
- **How:** I compared the risks of Vercel and Render with the lower setup effort of Hugging Face.
- **Why:** The platform had to support a reliable demo without unnecessary infrastructure work.

### 5. I returned to the main goal

- **What:** I evaluated which option best presented the project's core value.
- **How:** I separated the value of the RoBERTa model from the value of backend architecture.
- **Why:** The model was the main part we wanted ML-focused reviewers to evaluate.

### 6. I committed to Hugging Face

- **What:** I agreed that Hugging Face Spaces was the better choice for this project.
- **How:** I moved forward with the selected option instead of continuing the argument.
- **Why:** Its tradeoffs matched the goal of this specific ML project better.

### 7. I integrated the Gradio frontend

- **What:** I handled the Gradio frontend integration and the contract between the frontend and backend.
- **How:** I connected the interface to the model-serving flow and aligned the request and response shapes across both sides.
- **Why:** Committing to the decision meant making my owned integration work with the team's chosen platform.

## Result

- **Final outcome:** The team deployed the project on Hugging Face Spaces.
- **Technical outcome:** I integrated the Gradio frontend and defined the frontend–backend contract used by the demo.
- **Ownership boundary:** I did not own the entire deployment.
- **Team impact:** I supported my teammate's approach after we made the decision.
- **Learning:** Needs confirmation from the user.
- **What I would do differently:** Needs confirmation from the user.

## Supporting information

### Technical details

- Model: RoBERTa
- Deployment options: Vercel plus Render or Hugging Face Spaces
- Interface used on Hugging Face: Gradio
- Hugging Face offered optional free GPU inference
- Vercel and Render supported a separate frontend, backend, and custom API

### Alternatives considered

- Vercel plus Render offered more control and a production-style web architecture.
- Hugging Face offered faster setup and an environment designed for ML projects.
- We selected Hugging Face because the model was the project's main value.

### Ownership boundaries

- The disagreement was between me and my teammate.
- I initially supported Vercel and Render.
- My teammate initially supported Hugging Face.
- I owned the Gradio frontend integration and frontend–backend contract, not the entire Spaces deployment.

### Memory chain

> RoBERTa project → two deployment options → control versus speed → model was core → choose Hugging Face → integrate Gradio frontend and API contract
