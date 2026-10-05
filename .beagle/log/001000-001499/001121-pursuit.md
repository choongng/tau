+++
id = "001121-pursuit"
ordinal = 1121
kind = "pursuit"
timestamp = "2026-10-05T14:24:42+00:00"
summary = "pursuit prove T0268: WITNESSED — refuses when beagle.py's `if _in_tests_dir(rel) and (root / rel).is_file(…` is put back as `if False:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "942d53faec5f26f1369af04ca8a6008e7ac2a7071840977bc5678963ef03205b  .beagle/checks/T0268/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0268/check.sh'
refutes: refuses when beagle.py's `if _in_tests_dir(rel) and (root / rel).is_file(…` is put back as `if False:` (proven 2026-10-05T14:24:41+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_oracle_with_code_ignores_unimported_helper_under_tests_dir)
refused after 1s of a 1m30s check at: FAILED tests/test_beagle_example_extension.py::test_oracle_with_code_ignores_unimported_helper_under_tests_dir
refused with: 1 failed in 0.80s
