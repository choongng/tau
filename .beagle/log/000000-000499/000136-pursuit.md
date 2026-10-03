+++
id = "000136-pursuit"
ordinal = 136
kind = "pursuit"
timestamp = "2026-10-03T16:03:54+00:00"
summary = "pursuit open T0047: Cycles through a superseded task are refused or named with their --drop"
metric_command = ""
drains = []
hooks = []
+++

criteria: Per R06.md classes 1 and 6 (dev-notes/itc-runs/R06.md, the [tau] sections 'The driver can add a hard depend…' and 'A milestone successor cannot be abandoned…'): the driver pursuit guard steers a bash 'beagle pursuit depend' without --drop to the pursuit tools (a --drop passes); when pursuit_step finds nothing ready, it reads tree --json, follows superseded tasks to their heir, and when the hard waits form a cycle names the cycle and the exact 'beagle pursuit depend A B --drop' (or a tool call) that breaks it, preferring the edge the driver added; and the nothing-ready text names each unfinished task's blocking edge rather than offering only plan/new_route.
decided by: sh -c 'echo "43734393499d6de39f825a1b474e88d8458bbfb2d72ea4c9be68966abf8647d8  .beagle/checks/T0047/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0047/check.sh'
budget: 80000 tokens
