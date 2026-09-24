# Role-based access control (RBAC) testing

RBAC defines which roles may perform which actions. Testing it means checking every role against every action that matters, at the API, including the actions a role's UI never shows.

## Why a matrix

Six roles and fifteen modules already produce hundreds of role-action combinations, and the defects hide in the cells nobody tried. A matrix makes coverage explicit: every cell is either tested, deliberately skipped, or not yet done.

Use the [endpoint × role × permission matrix](../../matrices/endpoint-role-permission.csv). Each row is one endpoint and method, and each role column holds the expected result: `allow`, `deny`, or `own` (allowed only on records the actor owns or is assigned to).

## Building it

1. List endpoints from the API documentation, the frontend's network traffic, or the route definitions. Include action endpoints (`/approve`, `/dispatch`, `/refund`), not only CRUD.
2. For each endpoint, get the intended permission per role from the product owner or the spec. Where nobody can say, that is already a finding worth raising.
3. Mark the high-risk rows: money, user and role management, data export, and anything irreversible.

## What to test

**Horizontal boundaries between peer roles.** Roles at the same level with different jobs are where authorization is most often missing, because both are "trusted". A pattern I have seen: a manager role able to perform another role's entire operational workflow (starting routes and submitting proof of delivery for a driver) because the API checked "is staff of this tenant" rather than "is the assigned driver".

**Vertical escalation.** Lower roles calling admin endpoints; users changing their own role or permissions; a tenant admin reaching platform-level functions.

**Role and permission management itself.** Can a tenant admin edit or delete system roles? Grant a permission they do not hold? Assign a role above their own?

**Ownership rules (`own`).** A driver sees only their assigned deliveries; a user edits only their own profile. Test with two users of the same role.

**Changes over time.** Remove a permission or change a user's role, then retry the action with the existing session. The change should apply without a new login, or the delay should be known and acceptable.

**UI versus API parity.** For each role, list the actions the UI hides, then call their endpoints directly. A hidden button is not a permission check. Record whether each defect is in the frontend, the backend, or both; a backend defect needs a backend fix.

## Expected responses

| Situation | Expected |
|---|---|
| not authenticated | 401 |
| authenticated, role not allowed | 403 |
| authenticated, record belongs to another tenant | 404 |
| allowed role, record not owned (`own` rule) | 403 or 404, consistently |
| allowed | 2xx, and the change is stored |

Agree these with the team before testing so status codes can be asserted, not interpreted.

## Common defect classes

- Permission checked in the UI only
- Check on the list endpoint but not the detail or action endpoint
- Check on the create endpoint but not update or bulk
- Role checked, ownership not checked
- Cached permissions that outlive a role change
- System roles editable by tenant admins
