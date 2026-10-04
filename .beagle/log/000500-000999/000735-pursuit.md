+++
id = "000735-pursuit"
ordinal = 735
kind = "pursuit"
timestamp = "2026-10-04T16:29:15+00:00"
summary = "pursuit prove T0171: WITNESSED — refuses when beagle.py's `held = [rel for rel in _locked(goal) if rel in …` is put back as `held = []`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "40f2f3ea70b0650b079f1ba8b4f2175863f7fa892642dab54dbcaf80762d43c0  .beagle/checks/T0171/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0171/check.sh'
refutes: refuses when beagle.py's `held = [rel for rel in _locked(goal) if rel in …` is put back as `held = []` (proven 2026-10-04T16:28:54+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_step_refuses_a_scope_that_names_a_locked_file)
refused after 2s of a 1m05s check at: FAILED tests/test_beagle_example_extension.py::test_step_refuses_a_scope_that_names_a_locked_file
refused with: 1 failed in 1.66s
