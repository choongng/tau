+++
id = "001364-pursuit"
ordinal = 1364
kind = "pursuit"
timestamp = "2026-10-09T23:23:55+00:00"
summary = "pursuit prove T0323: WITNESSED — refuses when beagle.py's `paired = pair` is put back as `paired = None`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "016bdf7be03afa22ccab36a2e487a870ba6c0f221effbd0ef2ffd920ee5ffa21  .beagle/checks/T0323/T0323.sh" | sha256sum -c --quiet && bash .beagle/checks/T0323/T0323.sh'
refutes: refuses when beagle.py's `paired = pair` is put back as `paired = None` (proven 2026-10-09T23:23:55+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_unquoted_verdict_points_at_the_lines_holding_case_values)
refused after 3s of a 1m43s check at: FAILED tests/test_beagle_example_extension.py::test_unquoted_verdict_points_at_the_lines_holding_case_values
refused with: 1 failed in 2.89s
