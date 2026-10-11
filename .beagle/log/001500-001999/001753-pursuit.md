+++
id = "001753-pursuit"
ordinal = 1753
kind = "pursuit"
timestamp = "2026-10-11T01:46:15+00:00"
summary = "pursuit open T0406: _already_passes offers done-by only for a done task that can witness"
metric_command = ""
drains = []
hooks = []
+++

criteria: _already_passes offers abandon='done by D' only when _done_by would accept D for that task (the same witness rules: _requires_witness, _can_witness); when it would not, the result offers what _done_by_unwitnessed would say instead, never a done-by call that is then refused (R06, R09, R18, R40). A done-by that can be witnessed is still offered. A test feeds the offered call back through the done-by route and it is not refused. Tests named in the check; whole file passes; ruff clean.
decided by: sh -c 'echo "72d7d223fd3177f9de395b8568898ac45b86e6291179021fd22f7ae2fcdcb801  .beagle/checks/T0406/T0406.sh" | sha256sum -c --quiet && bash .beagle/checks/T0406/T0406.sh'
budget: 60000 tokens
