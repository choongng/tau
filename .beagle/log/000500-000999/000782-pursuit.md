+++
id = "000782-pursuit"
ordinal = 782
kind = "pursuit"
timestamp = "2026-10-04T23:11:48+00:00"
summary = "pursuit open T0201: A check may not run a later sibling's file; not-workable refusals give the escalated task's full call"
metric_command = ""
drains = []
hooks = []
+++

criteria: Open, new_route and amend refuse a check that runs a project file outside the task's scope that an unfinished task waiting on this one names as its own (title or scope), saying to put the file in this task's scope or bind a check of its own files; not-workable refusals, when a listed workable task has reached the escalation count, give that task's complete working call. Decided from tree state and paths only.
decided by: sh -c 'echo "552d522b936663a5de97955e83929d1e32ade80ed15f85fe1dbc2878fb6e7e68  .beagle/checks/T0201/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0201/check.sh'
budget: 150000 tokens
