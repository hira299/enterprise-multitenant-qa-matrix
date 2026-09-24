# Matrices

Reusable test matrices as CSV, so they open in any spreadsheet and can be read by scripts. The rows are generic examples for a fictional B2B ordering platform; replace them with your own entities, roles, and rules.

| Matrix | One row is | Use it for |
|---|---|---|
| [tenant-role-action.csv](tenant-role-action.csv) | an actor, a target tenant, and an action | tenant isolation and role boundaries per entity |
| [endpoint-role-permission.csv](endpoint-role-permission.csv) | an endpoint and method, with the expected result per role | API-level authorization coverage |
| [auth-state.csv](auth-state.csv) | an account state and an event | login, session, and token lifecycle |
| [business-rules.csv](business-rules.csv) | a rule and one way to break it | business logic, state rules, payments, reconciliation |

## Legend for permission cells

| Value | Meaning | Expected response |
|---|---|---|
| `allow` | permitted | 2xx, and the change is stored |
| `deny` | role not permitted | 403 |
| `own` | permitted only for records the actor owns or is assigned to | 2xx for own records, 403 or 404 otherwise |
| `none` | the record is invisible to this actor (another tenant) | 404, identical to a record that does not exist |
| `n/a` | not applicable | not tested, with a reason in the notes |

Agree the expected codes with the team before testing. If the product uses different conventions, change the legend, not the individual cells.

## Tracking execution

Add columns as you test rather than editing the expectations:

- `result`: pass, fail, blocked, or not run
- `actual`: what happened (status code, observed behavior)
- `defect`: the defect ID if it failed
- `layer`: frontend, backend, or both
- `tested_on`: build or date

A filled matrix is also the coverage report: the empty `result` cells are exactly what was not tested.

For executing a matrix automatically, see the [probe example](../examples/README.md), which uses expected status codes directly.
