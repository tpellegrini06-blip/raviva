---
name: ceo-control-tower
description: Use this skill when the user wants to know what needs attention across business and administrative life, asks what is urgent, asks where things stand, wants a daily/weekly executive brief, or has multiple emails, calendar items, documents, payments, suppliers, stores, or pending replies to coordinate. It should pull from connected systems when available and convert noise into a short prioritized action queue.
---

# CEO Control Tower

## Purpose

Turn scattered information into a prioritized operating view. The user should finish with fewer open loops, not a prettier summary.

## Tool behavior

When connected and relevant, inspect available sources directly instead of asking the user to copy data manually:

- Gmail for incoming messages, replies, bills, notices, suppliers, banks, insurers and pending threads;
- Calendar for deadlines, meetings and schedule conflicts;
- Drive for supporting documents;
- other connected tools when they contain the authoritative status.

Read actions may be performed directly when allowed. For sensitive or irreversible writes, payments, cancellations, legal commitments, or important external messages, obtain the required approval unless the user has explicitly authorized that action and the tool policy permits it.

## Workflow

1. Determine the control window:
   - Today by default for "what do I need to do?";
   - 7 days for weekly review;
   - preserve any explicit period.

2. Gather signals from connected sources where available.

3. Deduplicate by dossier/topic. One real-world issue equals one item even if it appears in several emails.

4. Classify each item:
   - URGENT;
   - MONEY;
   - ADMIN;
   - STORES / OPERATIONS;
   - WAITING FOR SOMEONE;
   - DEADLINE;
   - DELEGABLE;
   - INFORMATION ONLY.

5. For every actionable item determine:
   - exact status;
   - next action;
   - deadline;
   - consequence of doing nothing;
   - whether Work/agent can execute it;
   - whether the user personally must decide.

6. Rank using:
   `priority = urgency × consequence × reversibility × blocking effect`.
   Do not let noisy low-value messages outrank quiet high-consequence deadlines.

7. Execute safe low-risk actions directly when requested/authorized and tools allow it.
   Examples: retrieve information, compare documents, prepare a draft, organize the evidence.
   Do not perform sensitive commitments without the required approval.

8. Reduce the user's personal queue.
   Aim to leave no more than 3 "YOU MUST DECIDE" items when possible.

## Output

# Now
Maximum 3 items requiring action today.
For each:
- Status
- Why it matters
- Next action
- Deadline
- Who should do it: WORK / DELEGATE / USER

# Waiting
Items blocked by replies or external events, with last action date if known.

# Money & deadlines
Only meaningful amounts, due dates, risks, or anomalies.

# Can be executed without you
Actions that the agent can take or prepare now.

# No action
Important items reviewed that require nothing.

## Final checks

- Did I search connected sources instead of making the user repeat available information?
- Did I distinguish a real deadline from a marketing/notification date?
- Did I merge duplicate threads?
- Did I identify who owns the next action?
- Did I minimize the user's queue?
- Did I avoid claiming an action was executed unless a tool confirmed it?
