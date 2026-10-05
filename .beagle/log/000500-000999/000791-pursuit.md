+++
id = "000791-pursuit"
ordinal = 791
kind = "pursuit"
timestamp = "2026-10-05T00:24:08+00:00"
summary = "pursuit prove T0203: WITNESSED — refuses when R22.md's `grader: 3/44` is put back as `grader: 9/44`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "3564f5cd38bc86f5ae14cb98aa273adea837582290f57ca6d820c02aa3b70cfe  .beagle/checks/T0203/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0203/check.sh'
refutes: refuses when R22.md's `grader: 3/44` is put back as `grader: 9/44` (proven 2026-10-05T00:23:11+00:00; refused at Traceback (most recent call last):)
refused after 0s of a 0s check at: Traceback (most recent call last):
refused with: AssertionError: grader line grader: 9/44 != grade.json 3/44
