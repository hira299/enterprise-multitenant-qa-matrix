# Sample defect report (fictional)

A filled-in [defect report](../templates/defect-report.md) for defect D1 in the demo API.

---

**Title:** Another tenant's order returns 403 instead of 404, confirming the order exists

| Field | Value |
|---|---|
| ID | DEMO-001 |
| Severity | P2 major |
| Layer | Backend |
| Area | Tenant isolation / Orders API |
| Environment | local demo API, build as in this repository |
| Actor | `globex-manager` (tenant globex, role manager) |
| Found by | permission matrix row ORD-READ |
| Status | Open |

## Summary

Requesting an order that belongs to another tenant returns 403 Forbidden, while requesting an order that does not exist returns 404. A user of one tenant can therefore confirm which order IDs exist in other tenants. No order data is returned.

## Steps to reproduce

```bash
# 1. Another tenant's order
curl -s -w "\n%{http_code}\n" -H "Authorization: Bearer $TOKEN_GLOBEX_MANAGER" \
  http://127.0.0.1:8099/api/orders/A-100

# 2. Control: an order that does not exist
curl -s -w "\n%{http_code}\n" -H "Authorization: Bearer $TOKEN_GLOBEX_MANAGER" \
  http://127.0.0.1:8099/api/orders/DOES-NOT-EXIST
```

## Expected result

Both requests return 404 with the same body. A record in another tenant should be indistinguishable from a record that does not exist.

## Actual result

1. `403 {"error": "forbidden"}`
2. `404 {"error": "not found"}`

## Impact

With predictable IDs (`A-100`, `A-101`, ...), a user can enumerate another tenant's order IDs and estimate its order volume. The same pattern on other entities (invoices, customers) would reveal more. Severity is P2 rather than P1 because no record content is exposed.

## Scope checked

- `GET /api/invoices/{id}` and `POST /api/orders/{id}/approve` return 404 for other tenants (not affected).
- Only the order detail endpoint is affected.

## Suggested fix

Apply the tenant filter in the lookup itself (`WHERE id = ? AND tenant = ?`), so another tenant's record is simply not found.

## Retest notes

Retest both requests above, then rerun the ORD-READ and ORD-MISSING rows of the permission matrix for all actors.
