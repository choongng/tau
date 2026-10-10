+++
id = "001471-pursuit"
ordinal = 1471
kind = "pursuit"
timestamp = "2026-10-10T03:33:37+00:00"
summary = "pursuit prove T0345: WITNESSED — refuses when R40.md's `grader: 0/42` is put back as `grader: 1/42`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "4db98a543bdda27c56290a8fdb6195154b5a90ac7910a9251ef1a9c125681ab4  .beagle/checks/T0345/T0345.sh" | sha256sum -c --quiet && bash .beagle/checks/T0345/T0345.sh'
refutes: refuses when R40.md's `grader: 0/42` is put back as `grader: 1/42` (proven 2026-10-10T03:32:39+00:00; refused at Traceback (most recent call last):)
refused after 0s of a 0s check at: Traceback (most recent call last):
refused with: AssertionError: grader line grader: 1/42 != grade.json 0/42
standing checks red: T0335
