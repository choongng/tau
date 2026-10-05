+++
id = "001140-pursuit"
ordinal = 1140
kind = "pursuit"
timestamp = "2026-10-05T15:53:15+00:00"
summary = "pursuit open T0273: Data-route refusal runs the close's own checks, never re-proposes the bound check, keeps the notes; refusals lead with their call"
metric_command = ""
drains = []
hooks = []
+++

criteria: _data_route_on_disk says an open task closes on its data test only when the close's own cases checks (_unread_cases, _cases_test_problem) pass on disk, otherwise it names what is missing; when the done_when it would propose equals the task's bound check it says to leave done_when out; a pursuit_step on an open task whose done_when is rejected still runs the notes against the bound check instead of refusing the call; a refusal that ends in a call leads with that call.
decided by: sh -c 'echo "1b16afaba18a5cfbc3981348b99a6c8792b47802f541dea442ce62b6b55e6862  .beagle/checks/T0273/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0273/check.sh'
budget: 80000 tokens
