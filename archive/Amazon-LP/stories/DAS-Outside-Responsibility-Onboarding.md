# DAS Venture Solution Productization

Status: Version 3.0, needs learning confirmation

## Questions this story can answer

- Tell me about a time you worked outside your responsibilities.
- Tell me about a time you simplified a complex process.
- Tell me about a time you improved developer productivity.
- Tell me about a time you used AI in your work.
- Tell me about a time you faced strong objections.
- Tell me about a time you influenced more experienced people.

## Leadership Principles

- Primary: Invent and Simplify
- Secondary: Ownership; Think Big; Frugality; Earn Trust

## Situation

- **My role:** I was working as a software developer at Digital Aid Seattle.
- **Where:** DAS builds custom software for nonprofit organizations.
- **My project:** I was contributing to an assigned nonprofit project.
- **Pattern:** Different teams repeatedly built the same basic features.
- **Examples:** These included sign-in, profiles, admin pages, loading states, and common configuration.
- **Constraint:** DAS had limited volunteer engineering capacity.
- **Impact:** Repeated work reduced the number of nonprofit projects DAS could support.

## Task

- **My duty:** My formal responsibility was to contribute to my assigned project.
- **Additional ownership:** The repeated-work problem was outside my project assignment.
- **Goal:** I wanted to identify which solutions could safely be reused.
- **Balance:** Reuse had to save time without forcing one design on every nonprofit.
- **Long-term need:** Other teams needed to evaluate and maintain the shared work after I left.

## Action

### 1. I proved that the pattern existed

- **What:** I reviewed work from active and completed DAS projects.
- **How:** I compared Jira tickets, project documents, and code.
- **Why:** I needed evidence that repeated development was an organization-wide problem.

### 2. I created a comparable inventory

- **What:** I broke each project into smaller capabilities.
- **How:** I used AI on the documentation and checked the code when the documentation was incomplete.
- **Why:** Entire projects looked different, but their underlying capabilities could still be compared.

### 3. I defined what qualified for reuse

- **What:** I created a selection rule for reusable components.
- **How:** A component had to appear in more than 80% of projects and remain easy to customize.
- **Why:** Making everything reusable would create more maintenance than value.

### 4. I presented a package-based proposal

- **What:** I proposed storing the selected components as custom npm packages.
- **How:** I presented my cross-project findings and selection rule to the CTO.
- **Why:** Teams needed a standard way to install, version, and maintain shared code.

### 5. I addressed strong objections

- **What:** I revised the proposal after experienced developers objected.
- **How:** I added ownership, documentation, testing, security, monitoring, versioning, and upgrade requirements.
- **Why:** Shared packages could create long-term maintenance problems across several projects.

### 6. I added a project-fit decision

- **What:** I required teams to evaluate a component before reusing it.
- **How:** They compared the effort of adapting the component with building the feature from scratch.
- **Why:** Reuse would not always be the fastest or best choice for a new project.

### 7. I built the initial foundation

- **What:** I created the repository for the shared packages.
- **How:** I researched established component libraries and configured a monorepo using a starter kit.
- **Why:** DAS needed a working foundation instead of only a written proposal.

## Result

- **CTO support:** The CTO supported the revised proposal.
- **Formal adoption:** DAS added my productization criteria to its new-project evaluation framework.
- **Decision process:** Teams gained a formal way to choose between reuse and building from scratch.
- **Documentation:** DAS added the approach and checklist to its internal documentation.
- **Cross-team impact:** QA applied the same idea to shared testing documents.
- **Estimated impact:** The projected MVP timeline changed from 12 weeks to 9 weeks.
- **Accuracy:** This was a planning estimate, not a measured delivery reduction.
- **Learning:** Needs confirmation from the user.
- **What I would do differently:** Needs confirmation from the user.

## Supporting information

### Technical details

- Shared solutions were stored as custom npm packages.
- The packages were maintained in one monorepo.
- Common behavior was separated from project-specific configuration.
- AI helped break project documents into comparable capabilities.
- I checked the code when the documentation was incomplete.

### Alternatives considered

- Continue rebuilding common features for every project.
- Turn every repeated feature into a shared component.
- Reuse only components that passed frequency, customization, maintenance, and project-fit checks.
- I selected the third approach.

### Objections and feedback

- Experienced developers strongly objected to the maintenance burden.
- Dependency changes could affect several projects.
- Every new team would still spend time evaluating whether a component fit.
- The CTO supported the revised proposal.

### Ownership boundaries

- I reviewed the projects and created the selection criteria.
- I wrote the productization document.
- I created and configured the monorepo.
- The 12-to-9-week result was a planning estimate.

### Memory chain

> Repeated work → Jira and AI analysis → 80% rule → npm proposal → objections → productization checks → monorepo → CTO adoption → 12 to 9 weeks

