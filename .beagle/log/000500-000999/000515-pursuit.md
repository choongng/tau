+++
id = "000515-pursuit"
ordinal = 515
kind = "pursuit"
timestamp = "2026-10-04T04:31:40+00:00"
summary = "pursuit prove T0125: WITNESSED — refuses when beagle.py's `want = entry[\"sha256\"]` is put back as `return None`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "970fd38cbf0ded4961d6c81f723a140fab5c82b2dd5c81970a3a3bae78d7062b  .beagle/checks/T0125/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0125/check.sh'
refutes: refuses when beagle.py's `want = entry["sha256"]` is put back as `return None` (proven 2026-10-04T04:30:50+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_restore_locked_undoes_a_change_made_to_the_store_as_well)
refused after 1s of a 33s check at: FAILED tests/test_beagle_example_extension.py::test_restore_locked_undoes_a_change_made_to_the_store_as_well
refused with: 1 failed in 0.61s
