+++
id = "001570-pursuit"
ordinal = 1570
kind = "pursuit"
timestamp = "2026-10-10T16:26:07+00:00"
summary = "pursuit prove T0366: WITNESSED — refuses when R41.md is absent"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "5f32aa4f8efb2ae3cc0638630fc39bdfc0b54947affa93cf9eea2dcaee1a376f  .beagle/checks/T0366/T0366.sh" | sha256sum -c --quiet && bash .beagle/checks/T0366/T0366.sh'
refutes: refuses when R41.md is absent (proven 2026-10-10T16:26:06+00:00)
refused after 0s of a 0s check
