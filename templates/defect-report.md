# Defect report template

Copy for each defect. A developer should be able to reproduce it without asking you anything. A filled example is in [examples/sample-defect-report.md](../examples/sample-defect-report.md).

---

**Title:** [what is wrong, where, for whom: "Deactivated users can still log in with existing sessions"]

| Field | Value |
|---|---|
| ID | |
| Severity | P1 critical / P2 major / P3 minor / P4 trivial |
| Layer | Frontend / Backend / Both |
| Area | [module or feature] |
| Environment | [environment name, build or commit, browser and device if relevant] |
| Actor | [tenant, role, account state] |
| Found by | [journey, matrix row, exploratory charter, regression check] |
| Status | Open |

## Summary

[One or two sentences: what happens and why it matters.]

## Preconditions

[Data and state required: accounts, records, their states. Refer to test data by label, not by real customer data.]

## Steps to reproduce

1.
2.
3.

```bash
# The request that shows the defect. Tokens and URLs as variables, never literal values.
curl -s -w "\n%{http_code}\n" -H "Authorization: Bearer $TOKEN" "$BASE_URL/..."
```

## Expected result

[What should happen, including the response and the stored state.]

## Actual result

[What happened: status code, response body (trimmed), stored state, what the UI showed.]

## Evidence

[Request and response, before and after values, screenshots or recordings of the test environment only. Redact tokens, personal data, and anything from real tenants.]

## Impact

[Who is affected, what can go wrong, how likely. For money: amounts before and after.]

## Scope checked

[Other roles, tenants, entities, and endpoints tried, and whether they are affected.]

## Notes

[Suspected cause, related defects, workaround. Mark guesses as guesses.]

## Retest

[Build tested, steps rerun, surrounding flows checked, result.]
