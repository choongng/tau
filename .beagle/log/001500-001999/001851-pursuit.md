+++
id = "001851-pursuit"
ordinal = 1851
kind = "pursuit"
timestamp = "2026-10-11T23:20:07+00:00"
summary = "pursuit prove T0416: WITNESSED — refuses when B05.md is absent"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "b761ba908bcb8f142816fa22981f3ea758c9a3b1310005251029b8889e65324b  .beagle/checks/T0416/T0416.sh" | sha256sum -c --quiet && bash .beagle/checks/T0416/T0416.sh'
refutes: refuses when B05.md is absent (proven 2026-10-11T23:19:09+00:00)
refused after 0s of a 0s check
standing checks red: T0335, T0336, T0360, T0368, T0386
