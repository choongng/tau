+++
id = "000787-pursuit"
ordinal = 787
kind = "pursuit"
timestamp = "2026-10-04T23:25:49+00:00"
summary = "pursuit prove T0202: WITNESSED — refuses when beagle.py's `cut_off = _truncated_call(arguments)` is put back as `cut_off = None`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "e0c287dcb4010fd208abd21d2a804086075c58f46a09a313bdcc0dbd824d53a5  .beagle/checks/T0202/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0202/check.sh'
refutes: refuses when beagle.py's `cut_off = _truncated_call(arguments)` is put back as `cut_off = None` (proven 2026-10-04T23:25:27+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_worker_guard_explains_a_truncated_tool_call_instead_of_a_missing_pa…)
refused after 2s of a 1m04s check at: FAILED tests/test_beagle_example_extension.py::test_worker_guard_explains_a_truncated_tool_call_instead_of_a_missing_pa…
refused with: 1 failed in 1.57s
