+++
id = "000177-pursuit"
ordinal = 177
kind = "pursuit"
timestamp = "2026-10-03T18:09:58+00:00"
summary = "pursuit prove T0055: WITNESSED — refuses when R08.md's `grader: 5/42` is put back as `grader: 7/42`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "2ae208e92e51bfceeb75d148b2f73a83bb3fdb482270af92411042a04a7c3b8a  .beagle/checks/T0055/scored.sh" | sha256sum -c --quiet && bash .beagle/checks/T0055/scored.sh R08'
refutes: refuses when R08.md's `grader: 5/42` is put back as `grader: 7/42` (proven 2026-10-03T18:09:37+00:00; refused at Traceback (most recent call last):)
refused after 0s of a 0s check at: Traceback (most recent call last):
refused with: AssertionError: grader line grader: 7/42 != grade.json 5/42
