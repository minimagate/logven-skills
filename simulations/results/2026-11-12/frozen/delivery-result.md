Fixed duplicate delivery on retry. Each notification now uses a stable provider key containing its account and notification IDs, so retrying after a lost response retrieves the original receipt without sending again. Completed deliveries return their saved receipt.

Timeout errors still propagate, leaving unfinished notifications retryable. Public methods and the gateway contract remain unchanged.

Verified with `ruby -Ilib test/notification_test.rb`: 5 tests, 23 assertions, no failures or errors. Coverage includes completed retries, timeouts before and after acceptance, reconstructed notifications, and separate notifications across accounts. Ruby syntax checks and `git diff --check` passed.
