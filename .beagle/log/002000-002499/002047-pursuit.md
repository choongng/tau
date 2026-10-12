+++
id = "002047-pursuit"
ordinal = 2047
kind = "pursuit"
timestamp = "2026-10-12T08:01:58+00:00"
summary = "pursuit prove T0421: WITNESSED — refuses when R55.md is absent"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "d6fe54a9240b2b320774b49fdcf3a70e0494ee64d55a60b750ecf3bd8d2cbbda  .beagle/checks/T0421/T0421.sh" | sha256sum -c --quiet && bash .beagle/checks/T0421/T0421.sh'
refutes: refuses when R55.md is absent (proven 2026-10-12T08:01:58+00:00)
refused after 0s of a 0s check
