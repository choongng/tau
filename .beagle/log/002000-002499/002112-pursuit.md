+++
id = "002112-pursuit"
ordinal = 2112
kind = "pursuit"
timestamp = "2026-10-12T09:03:51+00:00"
summary = "pursuit prove T0422: WITNESSED — refuses when R56.md is absent"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "cafe34b56d16d2ea10256e77d7afb467d9d7704e7b6bdfcc90f9f5eeb5464bdb  .beagle/checks/T0422/T0422.sh" | sha256sum -c --quiet && bash .beagle/checks/T0422/T0422.sh'
refutes: refuses when R56.md is absent (proven 2026-10-12T09:02:53+00:00)
refused after 0s of a 0s check
standing checks red: T0335, T0360, T0368, T0386, T0336
