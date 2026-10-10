+++
id = "001374-pursuit"
ordinal = 1374
kind = "pursuit"
timestamp = "2026-10-10T00:30:09+00:00"
summary = "pursuit prove T0327: WITNESSED — refuses when R38.md is absent"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "8be4e6f2cbf91fe94001c7da4d6550110a88226d02cf7b0a90d02ef1932d2121  .beagle/checks/T0327/T0327.sh" | sha256sum -c --quiet && bash .beagle/checks/T0327/T0327.sh'
refutes: refuses when R38.md is absent (proven 2026-10-10T00:29:12+00:00)
refused after 0s of a 0s check
replaces: refuses when R38.md is absent (proven 2026-10-10T00:28:12+00:00)
