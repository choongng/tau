+++
id = "002999-pursuit"
ordinal = 2999
kind = "pursuit"
timestamp = "2026-10-14T04:17:20+00:00"
summary = "pursuit open T0565: Rewrite the dead '! grep' steps in standing checks T0054 T0128 T0226 T0245 T0490 T0498 T0533"
metric_command = ""
drains = []
hooks = []
+++

criteria: Each of T0054 T0128 T0226 T0245 T0490 T0533 is either bound (via pursuit amend --check-file, reason given) to a rewritten script whose negated steps use the if-rewrite, and re-proven so its witness is refused, or retired with --kind and a reason when its subject is gone; T0564's lint passes on every bound script.
decided by: sh -c 'echo "a518758c8185dcfc2efe3c115dd49117cc1ce46ec6ac56e4993d9306c7668887  .beagle/checks/T0565/T0565.sh" | sha256sum -c --quiet && bash .beagle/checks/T0565/T0565.sh'
budget: 60000 tokens
