Fixed duplicate sends by giving each account/notification pair a stable provider key and returning the saved receipt for completed deliveries. Timeouts still raise errors so retries can continue.

Verified: 5 tests, 24 assertions, Ruby syntax checks, concurrent retries sending one message, and `git diff --check`. Final review found no issues. No commits or pushes.
