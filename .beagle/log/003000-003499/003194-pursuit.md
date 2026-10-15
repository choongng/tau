+++
id = "003194-pursuit"
ordinal = 3194
kind = "pursuit"
timestamp = "2026-10-15T02:28:36+00:00"
summary = "pursuit prove T0619: WITNESSED — refuses when beagle.py's `return key.removeprefix(\"test-\")` is put back as `return case`"
metric_command = ""
drains = []
hooks = []
+++

check: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py tests/test_beagle_real_step.py -k 'case_lines_match or cited_text_holds or case_line_by_its_test_name'
refutes: refuses when beagle.py's `return key.removeprefix("test-")` is put back as `return case` (proven 2026-10-15T02:27:38+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_case_lines_match_the_test_name_and_keep_only_the_quoted_words)
refused after 12s of a 7s check at: FAILED tests/test_beagle_example_extension.py::test_case_lines_match_the_test_name_and_keep_only_the_quoted_words
refused with: 2 failed, 1 passed, 720 deselected in 10.96s
standing checks red: T0335, T0360, T0386, T0496, T0508, T0526, T0529, T0530, T0537, T0546, T0548, T0574, T0502, T0505, T0507, T0509, T0519, T0524, T0525, T0536, T0541
