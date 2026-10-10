+++
id = "001626-pursuit"
ordinal = 1626
kind = "pursuit"
timestamp = "2026-10-10T20:12:27+00:00"
summary = "pursuit prove T0380: WITNESSED — refuses when R43.md is absent"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "ac5d8f687f5fe7b3c4c0443bd7af7035d19e9bcbdb2f9805e654af33eeb97ca0  .beagle/checks/T0380/T0380.sh" | sha256sum -c --quiet && bash .beagle/checks/T0380/T0380.sh'
refutes: refuses when R43.md is absent (proven 2026-10-10T20:11:29+00:00)
refused after 0s of a 0s check
standing checks red: T0368
