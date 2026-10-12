+++
id = "001855-pursuit"
ordinal = 1855
kind = "pursuit"
timestamp = "2026-10-12T00:35:19+00:00"
summary = "pursuit prove T0417: WITNESSED — refuses when R51.md is absent"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "f1220ff34feb578b3e296dfd26cef325eb498e14439108efb97ab7f4c1e1950a  .beagle/checks/T0417/T0417.sh" | sha256sum -c --quiet && bash .beagle/checks/T0417/T0417.sh'
refutes: refuses when R51.md is absent (proven 2026-10-12T00:34:21+00:00)
refused after 0s of a 0s check
standing checks red: T0335, T0336, T0360, T0368, T0386
