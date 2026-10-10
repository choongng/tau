+++
id = "001658-pursuit"
ordinal = 1658
kind = "pursuit"
timestamp = "2026-10-10T22:54:00+00:00"
summary = "pursuit prove T0387: WITNESSED — refuses when R44.md is absent"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "2917c36f75c0677c778fd5ce183aaf810688c8db82db2adc8f706800f02bafc2  .beagle/checks/T0387/T0387.sh" | sha256sum -c --quiet && bash .beagle/checks/T0387/T0387.sh'
refutes: refuses when R44.md is absent (proven 2026-10-10T22:53:01+00:00)
refused after 0s of a 0s check
standing checks red: T0368
