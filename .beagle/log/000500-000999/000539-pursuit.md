+++
id = "000539-pursuit"
ordinal = 539
kind = "pursuit"
timestamp = "2026-10-04T06:02:31+00:00"
summary = "pursuit prove T0130: WITNESSED — refuses when R15.md's `grader: 0/42 (no implementation; every op missi…` is put back as `grader: 1/42`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "a5d0a361db42aafceec5f5b3bd767e66029d574b1c6dfc773f880d0c2d49f6d1  .beagle/checks/T0130/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0130/check.sh'
refutes: refuses when R15.md's `grader: 0/42 (no implementation; every op missi…` is put back as `grader: 1/42` (proven 2026-10-04T06:01:39+00:00; refused at Traceback (most recent call last):)
refused after 0s of a 0s check at: Traceback (most recent call last):
refused with: AssertionError: grader line grader: 1/42 != grade.json 0/42
