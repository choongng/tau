+++
id = "000717-pursuit"
ordinal = 717
kind = "pursuit"
timestamp = "2026-10-04T16:05:25+00:00"
summary = "pursuit prove T0168: WITNESSED — refuses when R20.md's `grader: 5/42` is put back as `grader: 1/42`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "91161823701ff5b94c8ceaefe4e38cd664ca4f7d2775dec6ef886738df02c44e  .beagle/checks/T0168/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0168/check.sh'
refutes: refuses when R20.md's `grader: 5/42` is put back as `grader: 1/42` (proven 2026-10-04T16:04:32+00:00; refused at Traceback (most recent call last):)
refused after 0s of a 0s check at: Traceback (most recent call last):
refused with: AssertionError: grader line grader: 1/42 != grade.json 5/42
