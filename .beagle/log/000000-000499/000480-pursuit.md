+++
id = "000480-pursuit"
ordinal = 480
kind = "pursuit"
timestamp = "2026-10-04T03:15:27+00:00"
summary = "pursuit prove T0121: WITNESSED — refuses when R14.md's `grader: 5/42 (paper 3/7, norm 2/6, leq 0/5, joi…` is put back as `grader: 6/42 (x)`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "57a3b1e09dbffd4c0684d52fa60321fe877f57d932ef06a7217d4baba36fa005  .beagle/checks/T0121/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0121/check.sh'
refutes: refuses when R14.md's `grader: 5/42 (paper 3/7, norm 2/6, leq 0/5, joi…` is put back as `grader: 6/42 (x)` (proven 2026-10-04T03:14:29+00:00; refused at Traceback (most recent call last):)
refused after 0s of a 0s check at: Traceback (most recent call last):
refused with: AssertionError: grader line grader: 6/42 != grade.json 5/42
