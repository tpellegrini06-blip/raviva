---
name: dossier-resolver
description: Use this skill when the user mentions a concrete administrative, financial, supplier, utility, insurance, banking, tax, subscription, debt, contract, complaint, or service dossier and asks what happened, what is owed, whether something is active, what a notice means, whether a reply was received, what the deadline is, or what to do next. Reconstruct the case from source evidence before advising.
---

# Dossier Resolver

## Purpose

Resolve a real-world dossier from evidence. Build the timeline, determine the current state, identify contradictions, and produce the smallest correct next action.

## Source hierarchy

Prefer:

1. official notices/contracts/invoices;
2. original emails and attachments;
3. account statements or transaction evidence;
4. authoritative websites/current law when needed;
5. user recollection as context, not as sole proof when documents are available.

Use Gmail, Drive, files, or other connected sources when available. Do not ask the user to manually locate information that can be retrieved directly.

## Workflow

1. Identify dossier:
   - organization;
   - service/contract/account;
   - question to answer;
   - time period.

2. Search all relevant source material, including:
   - names and aliases of the organization;
   - contract/account references;
   - invoice numbers;
   - amounts;
   - keywords such as unpaid, rejection, reminder, formal notice, suspension, termination, payment, refund, dispute.

3. Build a chronological timeline:
   `date | event | amount | source | consequence`.

4. Reconcile money:
   - invoiced;
   - paid;
   - rejected;
   - credited/refunded;
   - outstanding;
   - penalties/fees;
   - next scheduled amount.

   Never add amounts from different periods/contracts without proving they belong together.

5. Determine current operational status:
   - active;
   - suspended;
   - terminated;
   - unknown.

   Cite the strongest evidence.

6. Separate:
   - CERTAIN;
   - PROBABLE;
   - UNKNOWN / TO VERIFY.

7. Identify deadlines and consequences.
   For high-stakes legal, financial, tax, insurance or regulatory conclusions, verify current authoritative information when needed.

8. Decide the next action:
   - no action;
   - pay;
   - wait for reply;
   - send evidence;
   - dispute;
   - call only if written channels cannot resolve it;
   - prepare a formal message;
   - escalate.

9. If a message is needed, draft it from established facts only.
   Never manufacture references, dates, legal claims, payments, or attachments.

## Output

# Situation
3–6 lines explaining where the dossier stands now.

# Timeline
Compact chronological table/list.

# Money
- Paid
- Outstanding
- Disputed
- Next due
- Unexplained

# Certain / Uncertain
Explicit separation.

# Deadline & risk
Exact date where known.

# Recommended action
One primary action and, only if useful, one fallback.

# Ready to send
Include a draft only when a message is genuinely the next step.

## Final checks

- Did I inspect the full relevant thread/attachments rather than one isolated message?
- Are all amounts tied to a period/reference?
- Did I distinguish service status from notification/app problems?
- Did I verify high-stakes current rules when relevant?
- Did I avoid unnecessary phone calls when written evidence is preferable?
