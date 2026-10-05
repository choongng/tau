+++
id = "001084-pursuit"
ordinal = 1084
kind = "pursuit"
timestamp = "2026-10-05T13:10:05+00:00"
summary = "pursuit prove T0262: WITNESSED — refuses when R30.md's `grader: 3/44` is put back as `graded: 3/44`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "3e704a7bd517aeb78b2d43ba493c3acd72157463560faf2f529df0967baa81a0  .beagle/checks/T0262/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0262/check.sh'
refutes: refuses when R30.md's `grader: 3/44` is put back as `graded: 3/44` (proven 2026-10-05T13:09:08+00:00)
refused after 0s of a 0s check
