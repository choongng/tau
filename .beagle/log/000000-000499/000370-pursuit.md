+++
id = "000370-pursuit"
ordinal = 370
kind = "pursuit"
timestamp = "2026-10-03T21:15:55+00:00"
summary = "pursuit prove T0085: WITNESSED — refuses when beagle.py's `r\"\\b[1-9]\\d* failed\\b|` is put back as `r\"\\b\\d+ failed\\b|`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "95989605a9fdf6f9c34378143a5e4b9659d01f82fd5815e4f77d641fcb370530  .beagle/checks/T0085/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0085/check.sh'
refutes: refuses when beagle.py's `r"\b[1-9]\d* failed\b|` is put back as `r"\b\d+ failed\b|` (proven 2026-10-03T21:15:12+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_report_with_zero_failed_is_not_a_failure_report)
refused after 1s of a 1s check at: FAILED tests/test_beagle_example_extension.py::test_report_with_zero_failed_is_not_a_failure_report
refused with: 1 failed, 1 passed, 296 deselected in 0.46s
