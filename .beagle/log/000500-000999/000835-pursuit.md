+++
id = "000835-pursuit"
ordinal = 835
kind = "pursuit"
timestamp = "2026-10-05T02:05:29+00:00"
summary = "pursuit prove T0213: WITNESSED — refuses when R23.md's `grader: 0/44` is put back as `grader: 9/44`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "a77392aa902160824cde1b312dd2c7c1ff08661fd78f73960d65f4bd24acbb7b  .beagle/checks/T0213/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0213/check.sh'
refutes: refuses when R23.md's `grader: 0/44` is put back as `grader: 9/44` (proven 2026-10-05T02:04:32+00:00; refused at Traceback (most recent call last):)
refused after 0s of a 0s check at: Traceback (most recent call last):
refused with: AssertionError: grader line grader: 9/44 != grade.json 0/44
