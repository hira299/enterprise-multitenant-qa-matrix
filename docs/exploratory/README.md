# Exploratory testing

Scripted tests check what someone expected. Exploratory testing looks for what nobody expected, by learning the system and testing it at the same time. It is not random clicking: it is structured by charters, time-boxed, and recorded.

## Journeys first

Start with end-to-end journeys run as each real persona: sign up, configure, order, deliver, invoice, pay, return, report. A journey is complete only when its final state is checked. Journeys give breadth and a map of the product; the risky areas they reveal become charters.

Group journeys by area (for example order to delivery, payments and finance, returns, security and boundaries) so coverage can be reported per area.

## Charters

A charter is a short mission for one session. Use the [charter template](../../templates/exploratory-charter.md):

> Explore **the return and credit-note flow** with **a customer user and a supplier manager** to discover **whether credited amounts can exceed delivered quantities or be applied twice**.

Good charters name a risk. "Test returns" is not a charter.

## Heuristics that find boundary defects

| Heuristic | Try |
|---|---|
| Change the actor | the same action as another role, tenant, or account state |
| Change the order | skip, repeat, or reverse steps |
| Interrupt | refresh, go back, lose the network, close the tab mid-action |
| Go around the UI | replay the request with changed values |
| Follow the data | where does this value show up next, and does it still agree? |
| Look at what is logged | audit logs, activity feeds, notifications, emails |
| Stress the edges | zero, one, many, maximum, empty, very long |
| Undo | cancel, delete, deactivate, then see what remains |

## Session notes

Record while testing, not afterwards: what you tried, what you saw, questions, and defects. Keep the network log open. At the end, note what was covered, what was not, and what the next charter should be. The notes are the evidence that the session happened and the input to the next plan.

## Isolating a defect

When several symptoms appear, reduce them before reporting:

1. Find the smallest set of steps that reproduces it reliably.
2. Vary one thing at a time (role, tenant, data, browser) to find what matters.
3. Check whether other symptoms disappear when this one does; they may share a cause.

One report for a root cause is worth more than ten reports for its symptoms.
