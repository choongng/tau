+++
id = "001271-pursuit"
ordinal = 1271
kind = "pursuit"
timestamp = "2026-10-09T20:58:33+00:00"
summary = "pursuit prove T0306: WITNESSED — refuses when R36.md is absent"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "2882aab7c8d9106055c803f2aa4453fa0645ee355575fa5678f6b7baca1790d2  .beagle/checks/T0306/T0306.sh" | sha256sum -c --quiet && bash .beagle/checks/T0306/T0306.sh'
refutes: refuses when R36.md is absent (proven 2026-10-09T20:57:36+00:00)
refused after 0s of a 0s check
