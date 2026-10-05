+++
id = "001178-pursuit"
ordinal = 1178
kind = "pursuit"
timestamp = "2026-10-05T18:50:28+00:00"
summary = "pursuit prove T0281: WITNESSED — refuses when R34.md's `grader: 7/44 (uncommitted cobs.py graded as wri…` is put back as `graded: 7/44`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "a1e83ccf609ca56fd439992457cb1801f182f1e7abb97b64d30646039b15458d  .beagle/checks/T0281/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0281/check.sh'
refutes: refuses when R34.md's `grader: 7/44 (uncommitted cobs.py graded as wri…` is put back as `graded: 7/44` (proven 2026-10-05T18:49:32+00:00)
refused after 0s of a 0s check
