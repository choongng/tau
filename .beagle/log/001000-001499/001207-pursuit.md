+++
id = "001207-pursuit"
ordinal = 1207
kind = "pursuit"
timestamp = "2026-10-05T20:46:02+00:00"
summary = "pursuit prove T0287: WITNESSED — refuses when R35.md's `## Trace analysis` is put back as `## Trace notes`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "a0fa42eca49daf67f28276c033050b60386021dc3696c60cd776ee6f2a6830e8  .beagle/checks/T0287/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0287/check.sh'
refutes: refuses when R35.md's `## Trace analysis` is put back as `## Trace notes` (proven 2026-10-05T20:45:05+00:00)
refused after 0s of a 0s check
