# Regression testing

Regression testing answers "did the change break anything that used to work?". In practice there is never time to retest everything, so the skill is choosing what to retest.

```mermaid
stateDiagram-v2
  [*] --> Found: journey, matrix, or charter
  Found --> Isolated: smallest reliable reproduction
  Isolated --> Reported: severity, layer, evidence
  Reported --> Fixed
  Fixed --> Retested: original steps and surrounding flows
  Retested --> Reopened: still fails or regression found
  Reopened --> Fixed
  Retested --> Closed
  Closed --> RegressionCheck: P1 and P2 become regression checks
  RegressionCheck --> [*]
```

## Retesting a fix

1. Run the original reproduction steps exactly.
2. Run the flows around the fix: the same action for other roles and tenants, sibling endpoints (detail, list, bulk, export), and the next step in the journey.
3. Check the layer. If the defect was in the backend, confirm the API now refuses the request; a UI-only fix is not a fix.
4. Look for what the fix touched. Shared components (inputs, validation helpers, permission middleware) spread both fixes and regressions.

Retesting finds second-order problems: a UI fix that exposes a backend failure underneath, or a change to a shared input component that breaks forms elsewhere. Both happen often enough to plan for.

## Building a regression suite

- **From defects.** Every fixed P1 and P2 becomes a regression check. The saved curl request from the defect report is already most of the test.
- **From boundaries.** The negative rows of the permission matrices are cheap to rerun and catch the most damaging regressions.
- **From journeys.** A short version of each core journey per persona, run end to end.
- **From money.** The reconciliation invariants in [payments](../payments/README.md), checked against stored data.

Automate the API-level checks first: they are fast, stable, and cover the highest-risk rules. Keep UI automation for the few journeys that matter most.

## Choosing scope for a release

| Change | Retest at minimum |
|---|---|
| permission or auth middleware | the full permission matrices, auth state matrix |
| a shared UI component | every form that uses it |
| pricing, invoicing, payments | the business-rule matrix and reconciliation checks |
| a new role or permission | that role's matrix column and the roles next to it |
| data model or migration | imports, exports, reports, and relational deletes |
| dependency or framework upgrade | smoke tests of every journey, auth flows |

Use the [regression checklist](../../checklists/regression.md) for the release itself.
