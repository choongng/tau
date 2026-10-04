+++
id = "000458-pursuit"
ordinal = 458
kind = "pursuit"
timestamp = "2026-10-04T02:37:24+00:00"
summary = "pursuit prove T0117: WITNESSED — refuses when R13.md's `## Trace analysis` is put back as `## Trace notes`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "b2eb80caa7f9e407a8d125ed32797471421003b5888ac9498db4d48ba3eeb06f  .beagle/checks/T0117/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0117/check.sh'
refutes: refuses when R13.md's `## Trace analysis` is put back as `## Trace notes` (proven 2026-10-04T02:36:35+00:00)
refused after 0s of a 0s check
