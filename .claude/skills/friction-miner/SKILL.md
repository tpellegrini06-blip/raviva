---
name: friction-miner
description: Use this skill whenever the user describes an annoyance, repetitive manual task, employee workaround, supplier problem, store incident, software limitation, customer complaint, operational bottleneck, or "there should be an easier way" moment and wants to know whether it hides a business or automation opportunity. Convert incidents into evidence-backed frictions, not premature product ideas.
---

# Friction Miner

## Purpose

Capture recurring pain before inventing solutions. Build a structured friction inventory that can later feed opportunity validation.

## Inputs

Accept:

- voice-style descriptions;
- photos/screenshots;
- emails;
- incidents;
- employee messages;
- POS or spreadsheet issues;
- workflows;
- "why can't software do X?" observations.

## Workflow

1. Describe the friction without proposing a product:
   `When [actor] tries to [job], [obstacle] causes [cost/consequence].`

2. Identify:
   - actor;
   - job-to-be-done;
   - current workaround;
   - frequency;
   - time lost;
   - money lost or risk created;
   - emotional/operational annoyance;
   - systems involved;
   - who has budget authority.

3. Distinguish:
   - one-off incident;
   - recurring local friction;
   - likely category-wide friction.

4. Quantify with real numbers when available.
   If not available, mark as unknown rather than inventing estimates.

5. Check automation shape:
   - input available digitally?
   - rule-based or judgment-heavy?
   - APIs/connectors likely?
   - human approval needed?
   - can a manual concierge version test value first?

6. Score /100:
   - pain 15;
   - frequency 15;
   - measurable cost 10;
   - willingness to pay 15;
   - number of potential buyers 10;
   - access to users 10;
   - automation feasibility 10;
   - current solution dissatisfaction 10;
   - proof quality 5.

7. Decide:
   - IGNORE <40;
   - LOG 40–59;
   - INVESTIGATE 60–74;
   - VALIDATE ≥75.

   Score thresholds are guidance, not a substitute for evidence.

8. If VALIDATE, hand off to `opportunity-validator` when available.

## Output

# Friction
One sentence.

# Evidence
Observed facts only.

# Current workaround
What people do now.

# Cost
Time / money / error / risk.

# Buyer
Who experiences it vs who would pay.

# Automation potential
High / Medium / Low + reason.

# Score
/100 with components.

# Decision
IGNORE / LOG / INVESTIGATE / VALIDATE

# Next evidence to collect
Maximum 2 items.

## Final checks

- Did I avoid jumping to a product?
- Did I distinguish user from buyer?
- Did I quantify only what is known?
- Did I capture the workaround?
- Is this repeated enough to deserve attention?
