+++
id = "001818-pursuit"
ordinal = 1818
kind = "pursuit"
timestamp = "2026-10-11T22:26:29+00:00"
summary = "pursuit prove T0443: WITNESSED — refuses when B04.md is absent"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "64aa6a4222e0252745f10227242b54e3aa7382d4d7adc1c0d06af3736d4dddd9  .beagle/checks/T0443/T0443.sh" | sha256sum -c --quiet && bash .beagle/checks/T0443/T0443.sh'
refutes: refuses when B04.md is absent (proven 2026-10-11T22:25:31+00:00)
refused after 0s of a 0s check
standing checks red: T0335, T0336, T0360, T0368, T0386
