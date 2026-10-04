+++
id = "000637-pursuit"
ordinal = 637
kind = "pursuit"
timestamp = "2026-10-04T11:11:38+00:00"
summary = "pursuit prove T0151: WITNESSED — refuses when beagle.py's `amend_problem = _amend_problem(` is put back as `amend_problem = None and _amend_problem(`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "7c809ee8d1f6132f53b7b905d020a5969c8d3e6e04adcae8696737b0ec4da341  .beagle/checks/T0151/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0151/check.sh'
refutes: refuses when beagle.py's `amend_problem = _amend_problem(` is put back as `amend_problem = None and _amend_problem(` (proven 2026-10-04T11:11:07+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_amend_refuses_a_collect_only_check)
refused after 2s of a 56s check at: FAILED tests/test_beagle_example_extension.py::test_amend_refuses_a_collect_only_check
refused with: 1 failed, 1 passed in 2.16s
