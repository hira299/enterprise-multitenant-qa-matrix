# Test case template

| Field | Value |
|---|---|
| ID | |
| Title | [the behavior under test: "Other tenant cannot read an order by ID"] |
| Area | |
| Type | Positive / Negative / Boundary / Permission / Regression |
| Risk | Critical / High / Medium / Low, with one line on why |
| Matrix row | [if generated from a matrix] |

**Actor:** [tenant, role, account state]

**Preconditions:** [records and their states; how to create them]

**Steps:**
1.
2.

**Expected result:**
- Response: [status code, key fields]
- Stored state: [what must, and must not, have changed]
- UI (if relevant): [what the user sees]

**Test data:** [labels of test accounts and records]

**Notes:** [related rules, known variations to try]

---

Tips:
- One reason to fail per test case. Split "create and approve" into two.
- Negative cases assert that nothing changed, not only that an error appeared.
- Name the actor precisely; permission defects depend on it.
