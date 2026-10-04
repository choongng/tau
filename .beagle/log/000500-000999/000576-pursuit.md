+++
id = "000576-pursuit"
ordinal = 576
kind = "pursuit"
timestamp = "2026-10-04T08:18:49+00:00"
summary = "pursuit prove T0138: WITNESSED — refuses when R16.md's `grader: 0/42 (no implementation; every op missi…` is put back as `grader: 1/42`"
metric_command = ""
drains = []
hooks = []
+++

check: bash .beagle/checks/T0138/check.sh # sha256=a8b47fb25243f8be5be7eda2635851cbaa4efa409609a887fab50cef7e437daf
refutes: refuses when R16.md's `grader: 0/42 (no implementation; every op missi…` is put back as `grader: 1/42` (proven 2026-10-04T08:17:55+00:00; refused at Traceback (most recent call last):)
refused after 0s of a 0s check at: Traceback (most recent call last):
refused with: AssertionError: grader line grader: 1/42 != grade.json 0/42
