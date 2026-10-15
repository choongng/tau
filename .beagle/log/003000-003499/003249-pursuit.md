+++
id = "003249-pursuit"
ordinal = 3249
kind = "pursuit"
timestamp = "2026-10-15T06:34:28+00:00"
summary = "pursuit prove T0627: WITNESSED — refuses when beagle.py's `if kind == \"gap\":` is put back as `if kind == \"never\":`"
metric_command = ""
drains = []
hooks = []
+++

check: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py tests/test_beagle_real_step.py -k 'test_a_gap_case_is_refuted_by_source_words_anywhere_in_references or test_real_spec_tied_step_takes_the_source_words_a_report_quotes_beside_the_case'
refutes: refuses when beagle.py's `if kind == "gap":` is put back as `if kind == "never":` (proven 2026-10-15T06:33:31+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_a_gap_case_is_refuted_by_source_words_anywhere_in_references)
refused after 9s of a 9s check at: FAILED tests/test_beagle_example_extension.py::test_a_gap_case_is_refuted_by_source_words_anywhere_in_references
refused with: 1 failed, 1 passed, 731 deselected in 8.18s
standing checks red: T0335, T0360, T0386, T0496, T0508, T0526, T0529, T0530, T0537, T0546, T0548, T0574, T0502, T0505, T0507, T0509, T0519, T0524, T0525, T0536, T0541
