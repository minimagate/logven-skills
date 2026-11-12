Fixed retries by giving each account’s notification a stable delivery key. Retrying after a lost response now returns the original receipt without sending twice. Timeout errors still propagate, so retries remain possible.

Added three regression tests. All 4 tests pass with 20 assertions; Ruby syntax and whitespace checks also pass.
