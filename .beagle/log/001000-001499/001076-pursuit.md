+++
id = "001076-pursuit"
ordinal = 1076
kind = "pursuit"
timestamp = "2026-10-05T12:03:39+00:00"
summary = "pursuit prove T0261: WITNESSED — refuses when beagle.py's `or _doc_only_check_problem(done_when, scope, ta…` is put back as `or None`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "bfbf97b549e6895bbe51d741ac79e1f02cdfabc66c4b070ec412ef2c5977471d  .beagle/checks/T0261/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0261/check.sh'
refutes: refuses when beagle.py's `or _doc_only_check_problem(done_when, scope, ta…` is put back as `or None` (proven 2026-10-05T12:03:39+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_open_refuses_doc_only_check_under_tests)
refused after 3s of a 1m26s check at: FAILED tests/test_beagle_example_extension.py::test_open_refuses_doc_only_check_under_tests
refused with: 1 failed in 2.97s
