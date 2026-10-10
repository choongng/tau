+++
id = "001484-pursuit"
ordinal = 1484
kind = "pursuit"
timestamp = "2026-10-10T03:52:19+00:00"
summary = "pursuit prove T0347: WITNESSED — refuses when beagle.py's `unanswered = _unanswered_case_note(root)` is put back as `unanswered = \"\"`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "c814e27259f5b887d37f5d85332120b8c406e8931fb57b958027f1108db10149  .beagle/checks/T0347/T0347.sh" | sha256sum -c --quiet && bash .beagle/checks/T0347/T0347.sh'
refutes: refuses when beagle.py's `unanswered = _unanswered_case_note(root)` is put back as `unanswered = ""` (proven 2026-10-10T03:52:18+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_known_answers_unsourced_result_says_replace_the_case)
refused after 2s of a 1m45s check at: FAILED tests/test_beagle_example_extension.py::test_known_answers_unsourced_result_says_replace_the_case
refused with: 2 failed, 675 deselected in 1.22s
