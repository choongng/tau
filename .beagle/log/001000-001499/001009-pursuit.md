+++
id = "001009-pursuit"
ordinal = 1009
kind = "pursuit"
timestamp = "2026-10-05T08:33:15+00:00"
summary = "pursuit prove T0244: WITNESSED — refuses when beagle.py's `notes = f\"Make {test} import the module it test…` is put back as `notes = None`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "81d5b87f1d25bb6c29c6d16d6841aad2441f02b33062adc3523848cebdfa7e18  .beagle/checks/T0244/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0244/check.sh'
refutes: refuses when beagle.py's `notes = f"Make {test} import the module it test…` is put back as `notes = None` (proven 2026-10-05T08:33:10+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_unproven_call_tests_only_scope_importing_nothing_gives_step)
refused after 2s of a 1m21s check at: FAILED tests/test_beagle_example_extension.py::test_unproven_call_tests_only_scope_importing_nothing_gives_step
refused with: 1 failed in 2.03s
