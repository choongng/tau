+++
id = "000937-pursuit"
ordinal = 937
kind = "pursuit"
timestamp = "2026-10-05T06:36:08+00:00"
summary = "pursuit open T0233: pursuit_plan repairs bare part labels and catches duplicates off the root"
metric_command = ""
drains = []
hooks = []
+++

criteria: pursuit_plan never passes beagle a part whose title is a bare task id or label; it rebuilds each part as title::intent before the duplicate, clash and split steps, and refuses a part that duplicates a pending or open task outside the split task's subtree, under any task, not only the root. upstream.md records that beagle pursuit amend has no --scope (R23/T0216).
decided by: sh -c 'echo "05c25a5ddfae27fe40ce81e90d3a53cc9ea7cb45818ec80103ec9f21ca2cdae1  .beagle/checks/T0233/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0233/check.sh'
budget: 50000 tokens
