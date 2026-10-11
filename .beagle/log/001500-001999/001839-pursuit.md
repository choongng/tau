+++
id = "001839-pursuit"
ordinal = 1839
kind = "pursuit"
timestamp = "2026-10-11T23:06:01+00:00"
summary = "pursuit prove T0441: WITNESSED — refuses when beagle.py's `if len(chain) > SPAWN_LIMIT:` is put back as `if len(chain) >= SPAWN_LIMIT:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "c6949f502314dc74ccd5b44655cc26e6618b639cab8273fa3c5ea5aca1980e24  .beagle/checks/T0441/T0441.sh" | sha256sum -c --quiet && bash .beagle/checks/T0441/T0441.sh'
refutes: refuses when beagle.py's `if len(chain) > SPAWN_LIMIT:` is put back as `if len(chain) >= SPAWN_LIMIT:` (proven 2026-10-11T23:05:59+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_attempt_limit_arithmetic_reads_true)
refused after 8s of a 4m35s check at: FAILED tests/test_beagle_example_extension.py::test_attempt_limit_arithmetic_reads_true
refused with: 1 failed, 4 passed, 766 deselected in 6.58s
