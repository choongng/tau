+++
id = "000865-pursuit"
ordinal = 865
kind = "pursuit"
timestamp = "2026-10-05T03:45:17+00:00"
summary = "pursuit prove T0219: WITNESSED — refuses when R24.md's `grader: 3/42` is put back as `grader: 9/42`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "3b690ad8a24c6aab36166543483263f42d0ada72ffc51b8729aa6cfd2b8fe010  .beagle/checks/T0219/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0219/check.sh'
refutes: refuses when R24.md's `grader: 3/42` is put back as `grader: 9/42` (proven 2026-10-05T03:44:20+00:00; refused at Traceback (most recent call last):)
refused after 0s of a 0s check at: Traceback (most recent call last):
refused with: AssertionError: grader line grader: 9/42 != grade.json 3/42
