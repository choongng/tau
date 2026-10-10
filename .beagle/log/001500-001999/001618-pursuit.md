+++
id = "001618-pursuit"
ordinal = 1618
kind = "pursuit"
timestamp = "2026-10-10T18:56:55+00:00"
summary = "pursuit prove T0375: WITNESSED — refuses when beagle.py's `and any(map(_is_cases_data, changed)):` is put back as `:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "4b1e84f496d530e19fbce82537fc364e675001b1a89a0ed7748be36ec71dbeec  .beagle/checks/T0375/T0375.sh" | sha256sum -c --quiet && bash .beagle/checks/T0375/T0375.sh'
refutes: refuses when beagle.py's `and any(map(_is_cases_data, changed)):` is put back as `:` (proven 2026-10-10T18:56:54+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_close_does_not_lock_docs_and_test_of_a_task_that_wrote_no_cases)
refused after 1s of a 1m52s check at: FAILED tests/test_beagle_example_extension.py::test_close_does_not_lock_docs_and_test_of_a_task_that_wrote_no_cases
refused with: 1 failed, 1 passed, 706 deselected in 1.13s
