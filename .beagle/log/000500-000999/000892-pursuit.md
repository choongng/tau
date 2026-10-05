+++
id = "000892-pursuit"
ordinal = 892
kind = "pursuit"
timestamp = "2026-10-05T04:27:24+00:00"
summary = "pursuit open T0224: Cases first names the known-answers task that already holds the data file"
metric_command = ""
drains = []
hooks = []
+++

criteria: When Cases first refuses a step because a known-answers task is needed, and a live (open or pending) task already holds the data file in its scope or pending locks, the refusal names that task in a pursuit_step call instead of proposing a new part; a new part is proposed only when no live task holds it.
decided by: sh -c 'echo "615e49d89244fdc03378875bad98b0d609661855633a3fbdd19d4db237f59d22  .beagle/checks/T0224/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0224/check.sh'
budget: 60000 tokens
