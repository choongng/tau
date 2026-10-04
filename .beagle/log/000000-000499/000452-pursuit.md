+++
id = "000452-pursuit"
ordinal = 452
kind = "pursuit"
timestamp = "2026-10-04T02:28:33+00:00"
summary = "pursuit prove T0116: WITNESSED — refuses when R13.md's `grader: 0/42 (no implementation written; adapte…` is put back as `grader: 1/42 (x)`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "7a52f441d380e74dda40a9734d5ee7248dd358d52f44c4bf346306b6eb949767  .beagle/checks/T0116/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0116/check.sh'
refutes: refuses when R13.md's `grader: 0/42 (no implementation written; adapte…` is put back as `grader: 1/42 (x)` (proven 2026-10-04T02:27:44+00:00; refused at Traceback (most recent call last):)
refused after 0s of a 0s check at: Traceback (most recent call last):
refused with: AssertionError: grader line grader: 1/42 != grade.json 0/42
