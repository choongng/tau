+++
id = "001563-pursuit"
ordinal = 1563
kind = "pursuit"
timestamp = "2026-10-10T15:23:03+00:00"
summary = "pursuit prove T0357: WITNESSED — refuses when B03.md is absent"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "b63be7246d3e557d8b137afb21479dd590e49a33a39f9912dad53a712340b292  .beagle/checks/T0357/T0357.sh" | sha256sum -c --quiet && bash .beagle/checks/T0357/T0357.sh'
refutes: refuses when B03.md is absent (proven 2026-10-10T15:23:03+00:00)
refused after 0s of a 0s check
