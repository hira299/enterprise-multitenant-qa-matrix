# Regression checklist

Run on the release candidate build. Scope it using the change table in the [regression guide](../docs/regression/README.md#choosing-scope-for-a-release); the items below are the baseline.

## Fixed defects
- [ ] Every defect fixed in this release retested with its original reproduction steps
- [ ] For each fix: same action as other roles and tenants
- [ ] For each fix: sibling endpoints (detail, list, bulk, export) checked
- [ ] For each backend defect: the API itself now refuses the request, not only the UI
- [ ] Shared components touched by fixes (inputs, validators, permission middleware) checked in their other uses

## Boundaries
- [ ] Negative rows of the endpoint × role matrix (all `deny` and `none` cells for high and critical rows)
- [ ] Cross-tenant read and write by ID for the main entities
- [ ] Deactivated account and logged-out token refused
- [ ] Unauthenticated requests refused on every endpoint

## Money
- [ ] Reconciliation invariants: invoice = sum of lines; outstanding = total − payments − credits; outstanding ≥ 0
- [ ] One full partial-payment sequence
- [ ] One return and credit note

## Core journeys
- [ ] Short version of each core journey, per persona, end to end
- [ ] Final states verified in stored data

## Previously failing areas
- [ ] Areas with defect clusters in earlier cycles re-explored briefly
- [ ] Any defect reopened in the past retested again

## Sign-off
- [ ] Results recorded against the build number
- [ ] New defects triaged; release blockers identified
