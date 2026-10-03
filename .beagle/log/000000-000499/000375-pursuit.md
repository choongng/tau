+++
id = "000375-pursuit"
ordinal = 375
kind = "pursuit"
timestamp = "2026-10-03T21:18:15+00:00"
summary = "pursuit prove T0086: WITNESSED — refuses when beagle.py's `added = [path for path in staged if path not in…` is put back as `added = list(staged)`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "bba9d5ef5049333297e51238e0b366313867a3720454c34bb73d4c42b216c5f3  .beagle/checks/T0086/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0086/check.sh'
refutes: refuses when beagle.py's `added = [path for path in staged if path not in…` is put back as `added = list(staged)` (proven 2026-10-03T21:17:31+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_failed_setup_commit_keeps_the_users_own_staging)
refused after 1s of a 1s check at: FAILED tests/test_beagle_example_extension.py::test_failed_setup_commit_keeps_the_users_own_staging
refused with: 1 failed, 298 deselected in 0.51s
