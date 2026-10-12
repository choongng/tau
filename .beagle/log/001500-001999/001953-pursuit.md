+++
id = "001953-pursuit"
ordinal = 1953
kind = "pursuit"
timestamp = "2026-10-12T04:39:25+00:00"
summary = "pursuit open T0450: Record R52's tau classes as deferred under R0002"
metric_command = ""
drains = []
hooks = []
+++

criteria: dev-notes/itc-runs/deferred.md gives every R52 [tau] class a fix (task) or a deferral with its reason under R0002
decided by: sh -c 'echo "597f978cf487136265e9a2f439860b8c180ea72701f2ccb33ce05a09a983ece2  .beagle/checks/T0450/T0450.sh" | sha256sum -c --quiet && bash .beagle/checks/T0450/T0450.sh'
budget: 150000 tokens
opened over T0419: R0002
