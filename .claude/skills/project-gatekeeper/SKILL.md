---
name: project-gatekeeper
description: Use this skill whenever the user proposes, revisits, expands, or becomes excited about a new business, product, SaaS, app, service, content project, feature, or side project and needs to decide whether to pursue it. Its job is to prevent dispersion by comparing the opportunity with active priorities and forcing a clear KILL, PARK, TEST, or BUILD decision before substantial execution.
---

# Project Gatekeeper

## Purpose

Protect execution focus. Do not reward every new idea with a full build plan. First determine whether the idea deserves scarce time, money, attention, and execution capacity.

## Default context

Assume the user:

- runs operating businesses and has limited time;
- often has many promising ideas in parallel;
- wants small, monetizable, practical products rather than elegant projects with no buyer;
- prefers a fast proof over a long speculative build;
- values direct evidence and contradiction more than encouragement.

## Inputs

Use whatever is available:

- idea or problem statement;
- target customer;
- current projects and their next milestones;
- rough budget/time available;
- evidence already gathered;
- existing files, emails, notes, market research, or connected app data when relevant.

If information can be retrieved from available tools or connected sources, retrieve it instead of asking the user to restate it.

## Workflow

1. Restate the real opportunity in one sentence:
   `For [specific buyer], solve [specific painful job] by [mechanism], creating [measurable benefit].`

2. Separate:
   - observed problem;
   - proposed solution;
   - assumptions;
   - evidence.

3. Score each dimension from 0–10:
   - pain severity;
   - frequency;
   - willingness to pay;
   - access to first users;
   - user-specific unfair advantage;
   - differentiation;
   - MVP simplicity;
   - time to first proof;
   - recurring revenue potential;
   - maintenance burden, reverse-scored.

4. Check current project load.
   - Identify active BUILD or TEST projects.
   - Find their next unresolved milestone.
   - Do not authorize another BUILD if doing so would materially delay a higher-priority active project unless the new opportunity is clearly superior.

5. Run the anti-excitement test:
   - What would make this a bad business?
   - What existing behavior/software already solves enough of it?
   - What assumption is most likely to be false?
   - What would make acquisition expensive?
   - What part creates ongoing support or operational burden?

6. Choose exactly one verdict:
   - KILL: evidence or economics are poor.
   - PARK: interesting but not worth attention now.
   - TEST: uncertainty is high but cheap evidence is obtainable.
   - BUILD: enough proof exists to justify execution.

7. If TEST:
   - define one test;
   - maximum 7 days unless external dependency requires longer;
   - define success threshold before starting;
   - prefer interviews, fake-door, manual concierge, prototype, landing page, or use of the user's own stores/businesses as a laboratory.

8. If BUILD:
   - define only the next milestone;
   - hand off execution to `mvp-executor` when available.

## Output

Return:

# Verdict
KILL / PARK / TEST / BUILD

# Why
Maximum 5 bullets, evidence first.

# Score
Total /100 with the 10 component scores.

# Biggest risk
One sentence.

# Next proof
One concrete action, owner, and success threshold.

# What not to do
Name the tempting but unnecessary next action to avoid.

## Final checks

Before completing:

- Did I distinguish problem evidence from solution enthusiasm?
- Did I compare this against active priorities?
- Did I avoid inventing market facts?
- If current market facts matter, did I verify them?
- Is there exactly one verdict?
- Is the next step a proof-producing action rather than more brainstorming?
