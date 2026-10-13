+++
id = "002721-pursuit"
ordinal = 2721
kind = "pursuit"
timestamp = "2026-10-13T19:21:07+00:00"
summary = "pursuit prove T0533: WITNESSED — refuses when grade_semver.py's `(\"leading_zero_major\", \"01.1.1\")` is put back as `(\"leading_zero_major\", \"1.1.1\")`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "d54b9081f18886fc91c313d4c9b9bdb749a1cc214d4a95ae4d4f369cacb1690f  .beagle/checks/T0533/T0533.sh" | sha256sum -c --quiet && bash .beagle/checks/T0533/T0533.sh'
refutes: refuses when grade_semver.py's `("leading_zero_major", "01.1.1")` is put back as `("leading_zero_major", "1.1.1")` (proven 2026-10-13T19:20:06+00:00)
refused after 0s of a 4s check
