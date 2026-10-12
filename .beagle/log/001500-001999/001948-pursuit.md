+++
id = "001948-pursuit"
ordinal = 1948
kind = "pursuit"
timestamp = "2026-10-12T04:28:24+00:00"
summary = "pursuit open T0452: Step keeps the last non-empty worker report, and the brief's Scope line is the call's scope (R52)"
metric_command = ""
drains = []
hooks = []
+++

criteria: When a later attempt in one pursuit_step leaves no report, the step result shows the earlier attempt's non-empty report, not an empty one (named test). When pursuit_step runs with a scope different from the record's, the worker's brief carries one Scope line naming the call's scope, the one the write guard enforces (named test). Full suite and ruff pass.
decided by: sh -c 'echo "d39f3ef876cf5afebe407e663a07d6a8facde8b482e45d3bd8857126eda81c00  .beagle/checks/T0452/T0452.sh" | sha256sum -c --quiet && bash .beagle/checks/T0452/T0452.sh'
budget: 150000 tokens
