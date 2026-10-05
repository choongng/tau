+++
id = "001013-pursuit"
ordinal = 1013
kind = "pursuit"
timestamp = "2026-10-05T09:35:14+00:00"
summary = "pursuit prove T0247: WITNESSED — refuses when R27.md's `grader: 0/44` is put back as `graded: 0/44`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "2d0586c976bb424ada97c40c35a530c2eaba1c38878828c4c525112b2e56adac  .beagle/checks/T0247/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0247/check.sh'
refutes: refuses when R27.md's `grader: 0/44` is put back as `graded: 0/44` (proven 2026-10-05T09:34:18+00:00)
refused after 0s of a 0s check
