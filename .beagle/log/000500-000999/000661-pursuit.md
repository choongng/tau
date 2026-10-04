+++
id = "000661-pursuit"
ordinal = 661
kind = "pursuit"
timestamp = "2026-10-04T11:45:13+00:00"
summary = "pursuit prove T0156: WITNESSED — refuses when test_beagle_example_extension.py's `\"fork: takes a clock and makes a new representa…` is put back as `\"fork: something else entirely, not the referen…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "58a69bca34a7c2d6b2a65ed70ff2edb53faf616b49402b66cd7665ed3429b98b  .beagle/checks/T0156/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0156/check.sh'
refutes: refuses when test_beagle_example_extension.py's `"fork: takes a clock and makes a new representa…` is put back as `"fork: something else entirely, not the referen…` (proven 2026-10-04T11:44:44+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_r15_full_cases_file_all_quote_the_ref
refused after 2s of a 56s check at: FAILED tests/test_beagle_example_extension.py::test_r15_full_cases_file_all_quote_the_reference
refused with: 1 failed in 1.37s
replaces: still passes with the defect put back in test_beagle_example_extension.py (exit 0), measured 2026-10-04T11:43:36+00:00
