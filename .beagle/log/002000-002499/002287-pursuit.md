+++
id = "002287-pursuit"
ordinal = 2287
kind = "pursuit"
timestamp = "2026-10-12T13:14:25+00:00"
summary = "pursuit prove T0425: WITNESSED — refuses when R59.md is absent"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "04e42b0825216a67a38e32adc4e47887841d66ab17f4379d7eebf6a17cd5957f  .beagle/checks/T0425/T0425.sh" | sha256sum -c --quiet && bash .beagle/checks/T0425/T0425.sh'
refutes: refuses when R59.md is absent (proven 2026-10-12T13:13:27+00:00)
refused after 0s of a 0s check
standing checks red: T0335, T0360, T0368, T0386, T0419, T0420, T0421, T0422
