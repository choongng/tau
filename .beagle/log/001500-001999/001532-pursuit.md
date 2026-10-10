+++
id = "001532-pursuit"
ordinal = 1532
kind = "pursuit"
timestamp = "2026-10-10T05:00:29+00:00"
summary = "pursuit prove T0351: WITNESSED — refuses when beagle.py's `and _answers_compared(tree, answers, against=ow…` is put back as `and not _answers_compared(tree, answers, agains…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "2fc90b8125fa266bdbe447a420144dd386054493d39567e2557787023cdcc2cc  .beagle/checks/T0351/T0351.sh" | sha256sum -c --quiet && bash .beagle/checks/T0351/T0351.sh'
refutes: refuses when beagle.py's `and _answers_compared(tree, answers, against=ow…` is put back as `and not _answers_compared(tree, answers, agains…` (proven 2026-10-10T05:00:28+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_cases_test_problem_flags_in_file_implementation)
refused after 1s of a 1m51s check at: FAILED tests/test_beagle_example_extension.py::test_cases_test_problem_flags_in_file_implementation
refused with: 1 failed, 1 passed, 687 deselected in 0.71s
