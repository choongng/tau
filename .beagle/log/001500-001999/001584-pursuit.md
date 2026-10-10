+++
id = "001584-pursuit"
ordinal = 1584
kind = "pursuit"
timestamp = "2026-10-10T16:57:28+00:00"
summary = "pursuit prove T0367: WITNESSED — refuses when R41.md's `## Failure classes` is put back as `## Classes`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "196c6c4c47cd04c4d0cc78f6806f0607fad43ec664169524816ba54b0d48c760  .beagle/checks/T0367/T0367.sh" | sha256sum -c --quiet && bash .beagle/checks/T0367/T0367.sh'
refutes: refuses when R41.md's `## Failure classes` is put back as `## Classes` (proven 2026-10-10T16:57:28+00:00)
refused after 0s of a 0s check
