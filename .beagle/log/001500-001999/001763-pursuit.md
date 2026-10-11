+++
id = "001763-pursuit"
ordinal = 1763
kind = "pursuit"
timestamp = "2026-10-11T02:09:25+00:00"
summary = "pursuit open T0408: Cases first checks the spawn limit for a holder that is not open"
metric_command = ""
drains = []
hooks = []
+++

criteria: _cases_on_disk_route, for a cases holder that is not open (blocked or pending) whose retry chain is at beagle's spawn limit, offers the infeasible close with the parent's re-plan (_spawn_limit_offer) as the open-holder branch does, never an open/new-route call beagle's attempt limit then refuses (R26: T0011, chain T0007/T0009/T0010/T0011). A holder under the limit still gets today's open offer. Tests named in the check; whole file passes; ruff clean.
decided by: sh -c 'echo "c22dba1730bbd956814a4f17dd2feb3a18bbca57002842bf1d13d29c14725006  .beagle/checks/T0408/T0408.sh" | sha256sum -c --quiet && bash .beagle/checks/T0408/T0408.sh'
budget: 40000 tokens
