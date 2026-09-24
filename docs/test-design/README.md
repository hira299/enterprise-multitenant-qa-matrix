# Test design: negative, boundary, and permission cases

Positive tests show a feature works. Negative, boundary, and permission tests show what it refuses, which is where the costly defects are.

## Writing a test case

A good test case can be run by someone else and fails for one reason. Use the [test case template](../../templates/test-case.md):

- **Actor:** tenant, role, and account state. "As a user" is not enough.
- **Preconditions:** the data that must exist, and its state.
- **Steps:** at the level where the risk is. For permission tests that is usually one API request.
- **Expected result:** the response *and* the stored state. "It works" is not an expected result.
- **Risk:** what goes wrong if this fails (data leak, money, lockout). It sets the priority.

## Negative tests

For every rule, write the case that should be rejected:

- the wrong actor (role, tenant, owner, account state)
- the wrong state (already paid, cancelled, expired)
- the wrong input (missing, malformed, out of range, extra fields)
- the wrong order (step skipped, step repeated)
- the wrong time (expired promotion, expired token, after a deadline)

Assert both that the request is refused and that nothing changed. A "rejected" request that still wrote a record is a worse defect than one that was accepted openly.

## Boundary values

Test at, just inside, and just outside each limit:

| Kind | Example boundaries |
|---|---|
| Quantities | 0, 1, max, max + 1, negative, decimal where integers are expected |
| Money | 0.00, 0.01, the exact outstanding balance, balance + 0.01, currency precision |
| Dates | start and end of a validity window, time-zone edges, leap days, far past and future |
| Text | empty, whitespace only, max length, max + 1, Unicode, right-to-left text, emoji |
| Collections | empty list, one item, the pagination limit, the limit + 1 |
| Files | 0 bytes, the size limit, a wrong type with the right extension |

Money boundaries deserve special care: a payment of exactly the outstanding amount, one cent more, and a second payment after the balance reached zero are three different tests.

## Permission cases

Generate these from the matrices rather than writing them by hand. Each cell in the [endpoint matrix](../../matrices/endpoint-role-permission.csv) is a test case: actor = role, step = request, expected = the cell value. The [probe example](../../examples/README.md) runs a matrix directly.

## Prioritizing

When there is not time for everything, order by impact and likelihood:

1. money movement and financial records
2. cross-tenant access and account takeover paths
3. role escalation and user management
4. irreversible actions (delete, dispatch, send)
5. everything else

## Severity

A consistent scale keeps triage fast. One that works in practice:

| Severity | Meaning |
|---|---|
| P1 critical | security or data exposure, financial corruption, or a core journey blocked with no workaround |
| P2 major | a significant function wrong or unavailable, with a workaround |
| P3 minor | incorrect behavior with limited impact |
| P4 trivial | cosmetic or wording |

Record the layer (frontend, backend, both) alongside severity. It tells the team where the fix belongs.
