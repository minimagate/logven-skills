# Finding Format

Every reviewer returns a list of findings in this format and nothing else.

## Fields

Each finding has these fields, in this order:

- `lens`: the lens that produced it (for example `review-correctness`).
- `severity`: `blocker`, `major`, `minor` or `nit`.
- `location`: `path:line`.
- `claim`: one sentence stating the problem.
- `evidence`: the specific code or fact that shows it, quoted or referenced.
- `falsification`: what you checked that could have disproven the claim, and why it still holds.
- `suggestion`: the smallest fix, in one or two sentences.

## Rules

- Report only findings you can point to in the diff or in the code it touches.
- Do not raise style opinions that the repo guidelines do not support.
- No praise. Do not restate the diff.
- If there are no findings, reply `No findings` and list what you checked.
- Cap at 15 findings. Most severe first.

## Severity guide

- `blocker`: wrong behavior, security hole or data loss.
- `major`: clear violation of a guideline, or a structural problem that will cost soon.
- `minor`: worth fixing in this change.
- `nit`: optional.

## Example

```
- lens: review-correctness
  severity: major
  location: app/services/invoice_sync.rb:42
  claim: The retry loop re-sends invoices that already succeeded, so customers can be charged twice.
  evidence: `retries.each { |inv| push(inv) }` runs over all pending invoices, and `push` does not check `inv.synced_at` first.
  falsification: I checked whether `pending_invoices` already filters out synced rows; its query at line 18 filters on `synced_at IS NULL`, but the retry list is built from the earlier `all_invoices` at line 30, so the filter does not apply.
  suggestion: Build `retries` from `pending_invoices` or skip rows where `synced_at` is set before calling `push`.
```
