# Examples

All examples are fictional and generic. The demo application, its tenants, roles, and data were written for this repository.

## Matrix-driven testing against a demo API

[demo-api/](demo-api/) contains:

- [`demo_api.py`](demo-api/demo_api.py): a small multi-tenant ordering API (two tenants, four roles, a deactivated account) with five deliberate defects. Python standard library only; binds to 127.0.0.1.
- [`permission-matrix.csv`](demo-api/permission-matrix.csv): the endpoint × actor matrix for it, with the expected HTTP status in each cell.
- [`probe.py`](demo-api/probe.py): runs every cell of the matrix, then three business-rule scenarios, and reports what does not match.

```bash
cd examples/demo-api
python3 demo_api.py &          # http://127.0.0.1:8099
python3 probe.py
kill %1
```

Output:

```
permission matrix: 60/72 cells as expected

row                 actor             request                                    expected  actual  risk
ORD-LIST            acme-deactivated  GET /api/orders                                 401     200  medium
ORD-READ            globex-manager    GET /api/orders/A-100                           404     403  high
ORD-READ            acme-deactivated  GET /api/orders/A-100                           401     200  high
ORD-MISSING         acme-deactivated  GET /api/orders/DOES-NOT-EXIST                  401     404  low
ORD-CREATE          acme-deactivated  POST /api/orders                                401     201  medium
ORD-CREATE-INVALID  acme-deactivated  POST /api/orders                                401     400  medium
ORD-APPROVE         acme-viewer       POST /api/orders/A-100/approve                  403     200  high
ORD-APPROVE         acme-deactivated  POST /api/orders/A-100/approve                  401     200  high
DEL-PROOF           acme-manager      POST /api/deliveries/DL-1/proof                 403     200  high
DEL-PROOF           acme-deactivated  POST /api/deliveries/DL-1/proof                 401     200  high
INV-READ            acme-deactivated  GET /api/invoices/INV-1                         401     200  high
INV-PAY             acme-deactivated  POST /api/invoices/INV-1/payments               401     403  critical

business-rule scenarios
  ok    tenant list isolation: globex list excludes acme orders
  FAIL  overpayment rejected and outstanding never below zero  (payment of 600 on a 500 balance returned 201; outstanding now -100.0)
  ok    repeated approval is refused
```

## Reading the result

Twelve failing cells and one failing scenario, but only **five defects**:

| Defect | Evidence | Kind |
|---|---|---|
| D1 existence leak | ORD-READ as `globex-manager`: 403 instead of 404 | tenant isolation |
| D2 manager can act as the assigned agent | DEL-PROOF as `acme-manager`: 200 | horizontal authorization |
| D3 deactivated account keeps access | every `acme-deactivated` cell | authentication / account state |
| D4 overpayment accepted | overpayment scenario: outstanding −100 | business logic / payments |
| D5 viewer can approve through the API | ORD-APPROVE as `acme-viewer`: 200 | UI versus API parity |

D3 accounts for nine of the twelve cells. Reporting nine defects would send developers after symptoms; one report with the nine cells as evidence points at the cause (the token check ignores account state). Group by root cause before reporting.

Two cells are subtle. `ORD-MISSING` as the deactivated user returns 404, which looks like a correct denial but is not: the request was authenticated. And `INV-PAY` as the deactivated manager returns 403, so the role check happened to block it, but only because that account is a manager rather than an admin.

A worked report for D1 is in [sample-defect-report.md](sample-defect-report.md).

## Using the probe on a real system

1. Copy `permission-matrix.csv` and replace the rows and actor columns with your endpoints and roles.
2. Provide a token per actor as `TOKEN_<ACTOR>` environment variables (`TOKEN_TENANT_B_MANAGER`), never in the CSV.
3. Run against a test environment only. Without a reset endpoint, pass `--reset-path ""` and order the rows so writes do not break later reads, or use records created for the test.
4. Replace `scenarios()` with checks for your own business rules.
