+++
id = "001055-pursuit"
ordinal = 1055
kind = "pursuit"
timestamp = "2026-10-05T11:27:06+00:00"
summary = "pursuit prove T0256: WITNESSED — refuses when R29.md's `grader: 0/42` is put back as `graded: 0/42`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "b8b1e645830904961452a7483620fd9d00c467dc5d3f803fbd43e57cb519a13b  .beagle/checks/T0256/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0256/check.sh'
refutes: refuses when R29.md's `grader: 0/42` is put back as `graded: 0/42` (proven 2026-10-05T11:26:09+00:00)
refused after 0s of a 0s check
