# AI workflow reliability checklist

For an AI agent or LLM-based workflow before release. The model's answers cannot be made certain; everything around the model can be tested. See the [AI workflows guide](../docs/ai-workflows/README.md).

## Output handling
- [ ] Parser tested with fixed outputs: valid, fenced in markdown, single object instead of list, truncated, prose, empty
- [ ] Required fields, types, and allowed values validated in code, not by the model
- [ ] Invalid output is rejected with a reason and routed (retry, review, or dead-letter), not passed on
- [ ] One invalid item does not stop a batch
- [ ] Raw output kept (truncated, personal data removed) for rejected items

## Tools and actions
- [ ] Every tool validates its arguments independently of the model
- [ ] Tools enforce the calling user's permissions and tenant; the prompt is not the permission check
- [ ] Tool errors, timeouts, and unexpected response shapes handled
- [ ] Irreversible actions (send, pay, delete) require confirmation or human approval where the risk warrants it
- [ ] Allow-lists for anything the model can choose (tool, endpoint, table, command)

## Retries and duplicates
- [ ] Retries bounded, with backoff
- [ ] Side effects happen once when the same trigger arrives twice
- [ ] Side effects happen once when the workflow retries after a partial failure

## State
- [ ] Workflow stopped after each step and restarted: resumes or fails visibly
- [ ] Work in progress is visible (status, owner, timestamps)
- [ ] Failures end somewhere a person will see them

## Inputs
- [ ] Empty, very long, and non-English inputs
- [ ] Instructions embedded in user content (prompt injection) do not change permissions or tools
- [ ] Requests for other users' or tenants' data refused by the tool layer
- [ ] Inputs that mimic system markers or output format

## Business rules
- [ ] Model proposals checked against deterministic rules (limits, balances, policies) before acting
- [ ] Facts in generated content that must be true (prices, names, dates) checked against source data

## Regression and monitoring
- [ ] Fixed evaluation set with known-good and known-bad cases, including past production failures
- [ ] Deterministic parts asserted exactly; model outputs asserted by properties and pass rate over repeated runs
- [ ] Evaluation rerun on prompt, model, model version, or tool changes
- [ ] Per-run log: input ID, model and version, prompt version, validation result, tool calls, retries, final action
- [ ] Alerts on rising rejection rates, retries, or human-review volume

## Reporting
- [ ] Quality reported as measured rates on a described test set, not as a guarantee
