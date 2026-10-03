+++
id = "000165-pursuit"
ordinal = 165
kind = "pursuit"
timestamp = "2026-10-03T16:59:45+00:00"
summary = "pursuit prove T0052: WITNESSED — refuses when R07.md's `tasks_total 0` is put back as `tasks_total 3`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "14fa7929a0520fd0374acabd6a8f6eb1230c61c1cd626161bd07108b7a628817  .beagle/checks/T0052/scored.sh" | sha256sum -c --quiet && bash .beagle/checks/T0052/scored.sh R07'
refutes: refuses when R07.md's `tasks_total 0` is put back as `tasks_total 3` (proven 2026-10-03T16:59:45+00:00; refused at Traceback (most recent call last):)
refused after 0s of a 0s check at: Traceback (most recent call last):
refused with: AssertionError: Scorecard tasks_total 3 != scorecard.json 0
replaces: still passes with the defect put back in R07.md (exit 0), measured 2026-10-03T16:59:41+00:00
