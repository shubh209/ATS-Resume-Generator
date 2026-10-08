---
name: startup-job-messages
description: >-
  Write Shubh Kapadia's YC and Wellfound startup application introductions, founder or teammate LinkedIn
  connection notes tied to a startup opening, and company LinkedIn job messages.
  Use a supplied JD and recipient context. Includes Wellfound's company-interest
  introduction field; excludes other formal application questions,
  cover letters, resumes, and networking unrelated to a startup opening.
---

# Startup job messages

Produce one clear, human message per requested recipient that helps them decide
whether to continue a hiring conversation. Any human response, including a
rejection, counts toward the user's reply goal; do not solicit rejection for its
own sake. No wording can guarantee a reply.

## Route

Read only this context:

1. The supplied JD, recipient profile, application instructions, and current user
   constraints. The JD is the source for company and role claims; do not browse
   routinely or assume the user has tried the product.
2. `.kiro/steering/output-preferences.md` and `.kiro/steering/fit-scoring.md`.
   Fit scoring applies only when the user requests a fit assessment; it is not a
   message-quality or reply-probability score.
3. `references/research.md` in this skill for evidence and its limits.
4. `career-tools/reference/candidate-communication-standard.md`,
   `career-tools/reference/candidate-voice.md`, and
   `career-tools/reference/humanizer.md`.
5. `resume-system/governance/FACT_RULES.md` and
   `resume-system/facts/work-experience.md`.
6. When project evidence is useful, list only `resume-system/facts/projects/`
   and read relevant current selectable masters. Do not scan the repository.

Confirm candidate claims in the authoritative masters. Motivation files inform
voice and preferences, not accomplishments. Do not use old drafts, session
history, legacy resumes, or career stories as factual evidence. Ask when an
essential fact is absent from the routed sources.

## Channel decisions

These channel rules replace the shared standard's universal story-first rule
for this skill. Do not import the separate networking playbook's mandatory
question, line count, or metadata format.

| Channel | Purpose and content | Length |
|---|---|---|
| YC application message | Introduce the person behind the resume, establish relevant ability, and explain genuine interest in this work. Do not repeat the role title when the application already attaches it. Follow any explicit application requests. | Honor a supplied limit; otherwise choose a concise length that preserves context. |
| Wellfound application introduction / company-interest field | Answer the literal interest question early and show relevance to the specific opening within the first two sentences. Add one contextual example of contribution, rather than repeat job history. The profile and uploaded resume are also available to the company. | Honor a supplied limit; otherwise use one or two short paragraphs, normally about 60–120 words. |
| Personal LinkedIn connection note | Start a conversation with a founder or teammate about the opening. Name the role because the recipient has no application context. Use a clear reason to contact this person; do not squeeze in a project story. | 300 characters unless the user supplies a different limit. |
| Company LinkedIn message | Identify the opening, explain one relevant contribution with enough context, and make a direct, easy-to-route hiring request. No founder biography personalization. | 750 characters unless the user supplies a different limit. |

If the channel cannot be inferred from the request, ask which destination the
message is for. For multiple openings, preserve the user's stated interest in
both; do not imply they have applied. For multiple recipients, produce one note
each. Differentiate only where the profiles support it; never invent duties to
make the notes look different.

## Select the message's substance

- Identify the work the JD actually asks this hire to do. Choose one verified
  experience that best supports it, rather than automatically reusing the last
  payment or AI story.
- Technical evidence and product judgment belong together when relevant:
  explain the problem, Shubh's personal contribution, and its consequence.
  Name a tool only when it explains how he solved the problem or made a decision.
- In longer messages, preserve who faced the problem and why it mattered. Do
  not assume a company name explains Shubh's role or the users of his work.
  Cut secondary technologies and filler before cutting essential context.
- An intended prototype benefit is not a realized customer outcome. Preserve
  ownership, collaboration, maturity, and metric framing from FACT_RULES.
- Add information that helps interpret the resume; relevant evidence may overlap
  with the resume. Do not exclude technical substance merely to avoid repetition.
- Choose technical depth from the JD and recipient context. Infrastructure or
  agent roles may reward a concrete implementation detail; product roles may
  reward a user-facing decision. Do not impose a technical/product percentage.
- A product idea is optional. Use one only when supported by a genuine supplied
  observation; do not diagnose an unseen product or assert internal bottlenecks.
- Follow special application requests literally, such as personal contribution,
  a difficult decision, or an improvement. Do not carry those requirements into
  unrelated applications.
- For Wellfound company-interest answers, connect genuine motivation to the
  actual work or environment. A supported internship may call for learning,
  feedback, reliable delivery, and gradually increasing responsibility; do not
  force founder access, complete autonomy, or large ownership claims into every
  startup answer. Establish ability as well as what Shubh hopes to gain.
- Wellfound's advice to quantify impact does not require a number in every
  answer. Use meaningful, authorized metrics only when they improve the story.
  A relevant existing demo can provide proof; never invent a link or require
  custom unpaid work as a condition of writing an application.

## Voice and ask

Use a casual, soft opening and plain, natural sentences. Do not manufacture a
fun fact, joke, personal passion, or product-use claim. Avoid em and en dashes,
generic praise, slogans, recipient biography recitation, and technology lists.
Do not explain the recipient's business back to them as the reason to hire Shubh.

Confirmed user preferences for this workflow: understanding users' problems and
making their work easier; quick feedback, broad ownership, and close work with
founders. These are motivations, not evidence of past experience or a mandatory
closing sentence. Do not invent industry passion.

Questions are optional. Use at most one when it naturally advances the intended
conversation, is easy for this recipient to answer, and is not already answered
in the supplied JD/profile. Do not attach a generic question merely to seek any
reply, ask for unsolicited consulting, or hide a hiring request as networking.
A straightforward expression of interest or offer to share relevant work is
also valid. Do not ask about sponsorship when the supplied information already
answers it; do not infer authorization from ambiguous wording either.

Ask a focused clarification before drafting if an essential personal contribution,
motivation, application status, or consequential fact is missing. Do not ask
the user to pick an angle when the sources support a reasonable choice.

## Rejection pass

Check every draft internally. Flag the specific failing sentence and revise it;
do not return the audit unless asked.

1. **Truth:** Can every factual claim be traced to a routed source? Are prototype
   maturity, personal ownership, and outcomes accurate?
2. **Comprehension:** Could a reader unfamiliar with the project explain what
   Shubh did and why it mattered? For connection notes, is the reason for contact
   clear without a compressed story?
3. **Role relevance:** Does the evidence demonstrate a responsibility in this
   JD, beyond sharing a tool name?
4. **Personalization:** Does the connection explain genuine relevance instead
   of repeating company marketing or the recipient's biography? Mere name
   substitution fails; a relevant adjacent experience need not be unique.
5. **Human voice:** Would Shubh understand and defend every sentence? Remove
   cleverness, technical jargon, or praise that obscures meaning.
6. **Next step:** Is the intent apparent, and is any question useful rather than
   obligatory? Avoid questions whose answers are already supplied.
7. **Channel:** Are explicit application requests met, role context included
   where needed, and the exact final copy within the destination's limit?

If a message is too long, choose less material rather than leaving a confusing
fragment. A compliant character count cannot compensate for missing context.

## Delivery

Count the exact final copy with a tool, including spaces and line breaks for
character-limited channels. Return only the paste-ready copy and its verified
count outside the copy. Label recipients only when returning multiple notes.
No alternatives, scoring, research citations, or drafting explanation in normal
message output unless requested. Do not save generated messages or send them
externally without explicit authorization.
