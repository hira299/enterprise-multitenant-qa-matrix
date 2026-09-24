# Business-logic testing

Business-logic defects pass every form validation. The order submits, the invoice renders, the dashboard loads, and the numbers are wrong. They are found by testing the rules the business depends on, then checking the stored result.

## Collect the rules

Write down each rule as a testable statement, with its source (spec, product owner, contract):

- "A promotional price applies only between its start and end dates."
- "A payment cannot exceed the invoice's outstanding balance."
- "A return quantity cannot exceed the delivered quantity."
- "An order can be dispatched only after approval."
- "Overdue status is derived from the due date and the unpaid balance."

Put them in the [business-rule validation matrix](../../matrices/business-rules.csv): rule, how to break it, expected behavior, and where to verify the result.

## How to break a rule

| Technique | Example |
|---|---|
| Expired values | use a promotion, coupon, token, or price after its window |
| Out-of-order steps | dispatch before approval; refund before payment |
| Repeated steps | submit, approve, or pay twice; double-click; replay the request |
| Partial operations | partial payment, partial delivery, partial return, then the rest |
| Cancel and recreate | cancel a batch or order and create it again; check that nothing is counted twice |
| Concurrency | two users change the same record at once; two payments at once |
| Retries and timeouts | the client times out, the server succeeded; the client retries |
| Client-supplied values | send a different price, total, discount, or status |
| Boundaries | exact limits, one past the limit, zero, negative |

Patterns I have seen on a real platform: expired promotional pricing still honored at checkout, and invoice line quantities doubled when orders were re-batched after a batch was cancelled. Both passed every screen-level check.

## Verify in stored data

After each action, check the record, not only the response:

- line totals match quantity × unit price, after discounts
- header totals match the sum of lines
- ledgers and balances match the sum of transactions
- derived statuses (overdue, fully paid, delivered) match the underlying data
- dashboards and reports match the records they summarize

Use read-only database access, an admin view, or a follow-up API call. A correct-looking screen can sit on top of an incorrect record, and a report can be right while the record it summarizes is wrong.

## Gamified and progress systems

For points, levels, streaks, or completion tracking, the rule is usually "progress reflects real activity". Try completing the same item repeatedly, completing items out of order, replaying the completion request, and changing values in the request. On an AI education platform, I found a progress exploit of exactly this kind.
