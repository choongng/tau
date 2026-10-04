+++
id = "000769-pursuit"
ordinal = 769
kind = "pursuit"
timestamp = "2026-10-04T22:55:00+00:00"
summary = "pursuit prove T0198: WITNESSED — refuses when R21.md's `grader: 0/42` is put back as `grader: 1/42`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "910e3ea87c57f49e0137daffa2197ac6d2aa630ee7c89c8ac7b14766cc5fff7c  .beagle/checks/T0198/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0198/check.sh'
refutes: refuses when R21.md's `grader: 0/42` is put back as `grader: 1/42` (proven 2026-10-04T22:54:03+00:00; refused at Traceback (most recent call last):)
refused after 0s of a 0s check at: Traceback (most recent call last):
refused with: AssertionError: grader line grader: 1/42 != grade.json 0/42
