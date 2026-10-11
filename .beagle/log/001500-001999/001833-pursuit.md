+++
id = "001833-pursuit"
ordinal = 1833
kind = "pursuit"
timestamp = "2026-10-11T22:56:40+00:00"
summary = "pursuit open T0439: An infeasible close that seals its parent says so"
metric_command = ""
drains = []
hooks = []
+++

criteria: When a close --outcome infeasible leaves its parent unable ever to be all-done (a terminal undone leaf with no heir among its accountable leaves), the close result says the parent is now sealed and that only the owner can re-scope or abandon it, and to stop and ask; the offer of an infeasible close (hints that suggest it) says beforehand that it would seal the parent; and the Stop hook and status do not tell the driver to add the missing work with pursuit_plan under a sealed container, they say to ask the owner (q35 10-11: T0011 infeasible sealed T0002 at 11:23, and 60 min of plan parts followed). Tests named in the check; whole file passes; ruff clean.
decided by: sh -c 'echo "b9b6218813da7a28fa2a0a8530a9a6c092a746dfc915382164393010bffb5abb  .beagle/checks/T0439/T0439.sh" | sha256sum -c --quiet && bash .beagle/checks/T0439/T0439.sh'
budget: 300000 tokens
