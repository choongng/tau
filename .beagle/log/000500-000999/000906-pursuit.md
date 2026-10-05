+++
id = "000906-pursuit"
ordinal = 906
kind = "pursuit"
timestamp = "2026-10-05T05:55:00+00:00"
summary = "pursuit prove T0227: WITNESSED — refuses when R25.md's `grader: 0/42` is put back as `grader: 9/42`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "6f2062f6f258b48b7bd0ef0b8f7e4c76f6f38b00bc1b22f783f5f04222ec217e  .beagle/checks/T0227/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0227/check.sh'
refutes: refuses when R25.md's `grader: 0/42` is put back as `grader: 9/42` (proven 2026-10-05T05:54:03+00:00; refused at Traceback (most recent call last):)
refused after 0s of a 0s check at: Traceback (most recent call last):
refused with: AssertionError: grader line grader: 9/42 != grade.json 0/42
