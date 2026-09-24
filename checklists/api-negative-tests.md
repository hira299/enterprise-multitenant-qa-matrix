# API negative-test checklist

For each important endpoint. Each item is a request that should fail; assert the status code, the body, and that nothing changed in stored data.

## Authentication
- [ ] No token
- [ ] Malformed token
- [ ] Expired token
- [ ] Token after logout
- [ ] Token of a deactivated or deleted account
- [ ] Token from another environment

## Authorization
- [ ] Role without permission (403)
- [ ] Another tenant's record by ID (404, same as nonexistent)
- [ ] A peer's record where only own records are allowed
- [ ] Identifier moved: path versus query versus body versus nested object
- [ ] Bulk request mixing own and foreign IDs
- [ ] Action hidden in the UI for this role

## Input validation
- [ ] Required field missing
- [ ] Field `null`, empty string, or whitespace
- [ ] Wrong type (string for number, object for array)
- [ ] Out of range: negative, zero, maximum + 1, too many decimals
- [ ] Too long: strings, arrays, file size
- [ ] Unicode, emoji, right-to-left text, control characters
- [ ] Invalid enum value
- [ ] Invalid dates: impossible dates, wrong format, far past or future
- [ ] Extra fields the client should not set: `tenant_id`, `role`, `status`, `price`, `total`, `created_by`
- [ ] Malformed JSON; wrong `Content-Type`
- [ ] Duplicate keys in JSON

## State and business rules
- [ ] Action on a record in a terminal state
- [ ] Step skipped (for example dispatch before approve)
- [ ] Step repeated
- [ ] Two conflicting requests at the same time
- [ ] Amount above the allowed limit or balance
- [ ] Expired promotion, coupon, invitation, or link

## Idempotency and retries
- [ ] Same request sent twice in quick succession
- [ ] Retry after a client-side timeout
- [ ] Same idempotency key with a different body (if supported)

## Responses
- [ ] Error body contains a useful message and no stack trace, SQL, or internal paths
- [ ] Error body contains no data from other tenants
- [ ] Success body contains no fields this role should not see
- [ ] Status codes consistent with similar endpoints

## Limits
- [ ] Pagination: page size above the maximum; negative page; very large offset
- [ ] Rate limits enforced where specified
