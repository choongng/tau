+++
id = "000419-pursuit"
ordinal = 419
kind = "pursuit"
timestamp = "2026-10-04T01:31:00+00:00"
summary = "pursuit prove T0108: WITNESSED — refuses when R12.md's `grader: 12/42` is put back as `grader: 13/42`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "2b0f7b65ad477cf9f08c51d723e39c9a67269e52627bee8d3ab07e9bd87e4267  .beagle/checks/T0108/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0108/check.sh'
refutes: refuses when R12.md's `grader: 12/42` is put back as `grader: 13/42` (proven 2026-10-04T01:30:10+00:00; refused at Traceback (most recent call last):)
refused after 0s of a 0s check at: Traceback (most recent call last):
refused with: AssertionError: grader line grader: 13/42 != grade.json 12/42
