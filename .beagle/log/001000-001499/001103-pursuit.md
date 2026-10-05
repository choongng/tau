+++
id = "001103-pursuit"
ordinal = 1103
kind = "pursuit"
timestamp = "2026-10-05T14:05:32+00:00"
summary = "pursuit prove T0266: WITNESSED — refuses when R31.md's `grader: 0/44` is put back as `graded: 0/44`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "bd5f2bf0192f2c226d54690f51e0489a761c97cc4b489981f1ca6d2edf14c522  .beagle/checks/T0266/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0266/check.sh'
refutes: refuses when R31.md's `grader: 0/44` is put back as `graded: 0/44` (proven 2026-10-05T14:04:36+00:00)
refused after 0s of a 0s check
