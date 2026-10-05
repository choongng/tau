+++
id = "001031-pursuit"
ordinal = 1031
kind = "pursuit"
timestamp = "2026-10-05T10:38:24+00:00"
summary = "pursuit prove T0251: WITNESSED — refuses when R28.md's `grader: 0/42` is put back as `graded: 0/42`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "7b925ac71100b4eed52e03dc3f8f705d0870ebe16c3c7aa0b73bea66e6c40f6f  .beagle/checks/T0251/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0251/check.sh'
refutes: refuses when R28.md's `grader: 0/42` is put back as `graded: 0/42` (proven 2026-10-05T10:37:26+00:00)
refused after 0s of a 0s check
