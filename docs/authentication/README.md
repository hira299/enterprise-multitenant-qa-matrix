# Authentication and session testing

Authentication answers "who is this?". Most authentication defects are not in the login form but in account states and transitions: what happens to a session when the account behind it changes.

## Account states

Test login and existing sessions for every state the product has. The [authentication state matrix](../../matrices/auth-state.csv) lists the common ones with expected outcomes:

- active and verified
- registered but not verified (email, phone, or OTP pending)
- pending approval (an admin or partner must approve)
- deactivated or suspended
- deleted
- locked after failed attempts
- password recently changed or reset
- role changed or tenant membership removed
- invited but not accepted

Patterns I have seen on a real platform: deactivated users still able to log in, unverified accounts authenticating without completing OTP verification or admin approval, and a password reset flow that locked users out of their own accounts. Each is an account state nobody tested end to end.

## Session lifecycle

For each event, check both new logins and **existing sessions** in another browser or with a saved token:

| Event | Existing sessions should |
|---|---|
| logout | end (the token no longer works, not only the cookie removed) |
| password change | end everywhere else, or per product policy |
| password reset | end everywhere |
| deactivation | end immediately |
| role change | reflect the new permissions |
| removal from tenant | lose access to that tenant |
| token expiry | be refused; refresh follows its own rules |

Useful checks:
- Replay a token after logout.
- Use a refresh token after the account was deactivated.
- Change the password in session A, then act in session B.
- Check that session identifiers change after login (session fixation).

## Login and recovery flows

- Error messages and timing should not reveal which emails are registered.
- Rate limiting or lockout on login, OTP, and reset endpoints; OTP codes expire and are single use.
- Reset links expire, are single use, and are invalidated by a newer reset.
- Reset and verification tokens are not in URLs that end up in logs or referrers where avoidable.
- The reset flow cannot be used to change another user's password (user ID in the request).

## Where credentials leak

Look beyond the login flow:

- **Audit and activity logs.** A serious pattern I have seen: audit logs recording request payloads, so users with audit access could read password hashes, active session tokens, and live one-time verification codes. Logging is a feature that needs security testing.
- API responses that include password hashes, tokens, or internal fields
- Error pages and stack traces
- Browser storage, URLs, and analytics events
- Exports and backups available to tenant users

## Reporting

State the account state, the event, which session was used, and what access remained. Where a token still worked after it should not, include the time between the event and the request.
