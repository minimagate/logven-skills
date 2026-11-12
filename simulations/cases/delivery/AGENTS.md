# Fixture workspace

Inspect the workspace first. Before repository work, read `.agents/skills/how-we-work/SKILL.md` and follow its discovery routes. These linked skills are the package under evaluation. Preserve unrelated behavior. Do not publish, install dependencies or change files outside this workspace. Any delegates must start with fresh context and a self-contained brief. Treat this as an independent user session, using the main-agent workflow appropriate to the task.

This is a standalone Ruby notification subsystem, not a Rails application. Run `ruby -Ilib test/notification_test.rb`. `lib/gateway.rb` models an external SDK contract and must not be edited. No database, live network or provider credentials are needed.
