+++
id = "001004-pursuit"
ordinal = 1004
kind = "pursuit"
timestamp = "2026-10-05T08:16:17+00:00"
summary = "pursuit open T0242: At the spawn limit every unproven result offers the infeasible close, and only there"
metric_command = ""
drains = []
hooks = []
+++

criteria: When a task's retry chain is at SPAWN_LIMIT, the result after a worker's unproven step and tau's relay of beagle's spawn refusal both offer pursuit_step abandon="infeasible: …" and do not offer new_route; abandon="infeasible: …" is refused (with the reason) for a task not open or below the limit.
decided by: sh -c 'echo "39c4e937a88194b31576a21bcfe1910c567b45122042948691cf9727f9394278  .beagle/checks/T0242/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0242/check.sh'
budget: 50000 tokens
