+++
id = "000224-pursuit"
ordinal = 224
kind = "pursuit"
timestamp = "2026-10-03T19:40:04+00:00"
summary = "pursuit prove T0063: WITNESSED — refuses when R09.md's `grader: 4/42` is put back as `grader: 5/42`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "2ae208e92e51bfceeb75d148b2f73a83bb3fdb482270af92411042a04a7c3b8a  .beagle/checks/T0063/scored.sh" | sha256sum -c --quiet && bash .beagle/checks/T0063/scored.sh R09'
refutes: refuses when R09.md's `grader: 4/42` is put back as `grader: 5/42` (proven 2026-10-03T19:39:32+00:00; refused at Traceback (most recent call last):)
refused after 0s of a 0s check at: Traceback (most recent call last):
refused with: AssertionError: grader line grader: 5/42 != grade.json 4/42
