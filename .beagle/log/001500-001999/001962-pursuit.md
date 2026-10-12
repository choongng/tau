+++
id = "001962-pursuit"
ordinal = 1962
kind = "pursuit"
timestamp = "2026-10-12T05:55:17+00:00"
summary = "pursuit prove T0419: WITNESSED — refuses when R53.md is absent"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "b258b42dae0ed76f5aebedbb6b24ee8a45ee862c7068a396bebed50356ea0d5f  .beagle/checks/T0419/T0419.sh" | sha256sum -c --quiet && bash .beagle/checks/T0419/T0419.sh'
refutes: refuses when R53.md is absent (proven 2026-10-12T05:54:17+00:00)
refused after 0s of a 0s check
standing checks red: T0335, T0336, T0360, T0368, T0386
