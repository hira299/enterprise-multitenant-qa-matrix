# Pre-launch QA checklist

For a B2B SaaS release. Items are grouped by risk; the first three groups are the ones that cause incidents customers notice. Mark each item done, not applicable (with a reason), or open (with a defect ID).

## Tenant isolation
- [ ] Two or more test tenants set up with every role
- [ ] Every entity type read, updated, and deleted by ID from another tenant: 404, nothing changed
- [ ] List, search, export, report, and dashboard results contain only the tenant's own data
- [ ] "Not yours" and "does not exist" return the same response
- [ ] Tenant is taken from the session, never from request fields
- [ ] Attachments and file URLs require a valid session for the right tenant
- [ ] Notifications and emails go only to the tenant's own users

## Authentication and sessions
- [ ] Unverified, pending-approval, deactivated, and deleted accounts cannot log in
- [ ] Deactivation, password reset, and removal from a tenant end existing sessions
- [ ] Logout invalidates the token on the server
- [ ] Login, OTP, and reset endpoints are rate limited; OTP and reset links are single use and expire
- [ ] Error messages do not reveal which emails are registered
- [ ] No credentials, tokens, or OTP codes in logs, audit trails, responses, or URLs

## Authorization
- [ ] Endpoint × role matrix executed at the API for all high-risk rows
- [ ] Actions hidden in each role's UI refused by the API
- [ ] Ownership rules tested with two users of the same role
- [ ] Tenant admins cannot edit system roles or grant roles above their own
- [ ] Role changes take effect on existing sessions

## Money and business rules
- [ ] Prices, discounts, and totals computed on the server
- [ ] Promotions and prices respect validity windows
- [ ] Overpayment, duplicate payment, and concurrent payment refused
- [ ] Invoice, payment, and ledger totals reconciled in stored data after partial payments, returns, and cancel-and-recreate
- [ ] Dashboards and reports match the records they summarize
- [ ] State machines refuse skipped, repeated, and out-of-order transitions

## Core journeys
- [ ] Every core journey completed end to end as each persona that performs it in production
- [ ] Final state of each journey checked in stored data
- [ ] Journeys repeated on the supported browsers and devices

## Data integrity
- [ ] Imports report rejected rows; accepted plus rejected equals input
- [ ] Deletes do not leave orphaned records
- [ ] No duplicate records from double submission or retries
- [ ] Migrations applied to a copy of realistic data without loss

## Errors and resilience
- [ ] Timeouts and failed calls leave records in a consistent state
- [ ] Retried requests do not duplicate side effects
- [ ] Error pages and API errors do not expose stack traces, queries, or other tenants' data
- [ ] Background jobs and scheduled tasks run with the correct tenant context

## AI features (if any)
- [ ] [AI workflow reliability checklist](ai-workflow-reliability.md) completed

## Release decision
- [ ] All P1 defects fixed and retested; P2 defects fixed or accepted in writing
- [ ] Regression run on the release build ([regression checklist](regression.md))
- [ ] Known issues and accepted risks listed in the [QA summary report](../templates/qa-summary-report.md)
