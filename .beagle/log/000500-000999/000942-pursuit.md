+++
id = "000942-pursuit"
ordinal = 942
kind = "pursuit"
timestamp = "2026-10-05T07:19:39+00:00"
summary = "pursuit prove T0234: WITNESSED — refuses when R26.md's `grader: 0/44` is put back as `grader: 9/44`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "8ce37f6ab4deeb53189732af0ef6a50a55a8d7c708842a67b1534e9925363f89  .beagle/checks/T0234/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0234/check.sh'
refutes: refuses when R26.md's `grader: 0/44` is put back as `grader: 9/44` (proven 2026-10-05T07:18:42+00:00; refused at Traceback (most recent call last):)
refused after 0s of a 0s check at: Traceback (most recent call last):
refused with: AssertionError: grader line grader: 9/44 != grade.json 0/44
