+++
id = "000497-pursuit"
ordinal = 497
kind = "pursuit"
timestamp = "2026-10-04T03:44:08+00:00"
summary = "pursuit open T0124: Done-by route for a part an earlier commit made pass"
metric_command = ""
drains = []
hooks = []
+++

criteria: A pending part or milestone whose check passes before any work, on a done task's commit in the scope's git log, can be closed done with pursuit_step abandon='done by Tnnnn' (no sub-agent, spent 0, the reason naming Tnnnn and its commit); the same without that task's commit is refused. The already-passes refusal offers that route when it applies; the part abandon text promises no close the pre-run forbids; a pending milestone's refusal offers no new_route; done_when without criteria is refused as 'criteria is missing'.
decided by: sh -c 'echo "5d6665d9fb6724c7ae92d03f832b5721e8c5d069a3f722bb0ec55c7f6cda1fdb  .beagle/checks/T0124/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0124/check.sh'
budget: 150000 tokens
