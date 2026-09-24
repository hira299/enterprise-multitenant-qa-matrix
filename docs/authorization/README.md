# Authorization testing

Authorization answers "may this actor do this, to this record, now?". It has three parts, and each needs its own tests:

1. **Role:** is this kind of user allowed this action at all? See [RBAC](../rbac/README.md).
2. **Scope:** is the record inside the actor's tenant, organization, or location? See [multi-tenancy](../multi-tenancy/README.md).
3. **State and ownership:** is the actor assigned to this record, and does the record's current state allow the action?

Most authorization defects pass one of these and skip another: the role is right but the record belongs to someone else, or the record is yours but it is already approved and should be locked.

## Object-level checks

For every endpoint that takes an identifier, try:

- your own record (control)
- a peer's record in the same tenant and role
- a record in another tenant
- a record that does not exist
- a record in a state that should block the action (cancelled, paid, archived)
- an identifier in a different position: path versus body versus query, or nested inside a payload (`order.customer_id`)

Compare responses. Differences between "not yours" and "does not exist" leak information; differences between path and body handling usually mean one of them is unchecked.

## Field-level checks

- **Mass assignment:** add fields the form never sends (`role`, `tenant_id`, `price`, `status`, `approved_by`) and see if they are stored.
- **Read exposure:** responses that include fields the role should not see (cost price, other users' contact details, internal notes).
- **Computed values:** totals, discounts, and prices must be computed on the server; sending a different total should not change what is charged.

## State-based checks

Many actions are allowed only in some states. For each state machine (order, invoice, return, approval), try each action in each state:

- actions on terminal states (edit a delivered order, refund a refunded payment)
- skipping steps (dispatch before approval)
- repeating steps (approve twice, submit proof of delivery twice)
- concurrent transitions (two users approve and reject at the same time)

The [business-rule matrix](../../matrices/business-rules.csv) has rows for state rules alongside pricing and payment rules.

## Frontend versus backend parity

Run a dedicated sweep: for each role, list the actions the UI hides or disables, and call the endpoints directly. Also run the reverse: actions the UI offers that the API rejects silently, leaving the user thinking it worked. Record the layer of every finding.
