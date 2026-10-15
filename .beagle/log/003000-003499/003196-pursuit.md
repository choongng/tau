+++
id = "003196-pursuit"
ordinal = 3196
kind = "pursuit"
timestamp = "2026-10-15T02:30:57+00:00"
summary = "pursuit prove T0619: WITNESSED — refuses when beagle.py's `while start > 0 and first - start < CITE_CONTEX…` is put back as `while False:`"
metric_command = ""
drains = []
hooks = []
+++

check: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py tests/test_beagle_real_step.py -k 'case_lines_match or cited_text_holds or case_line_by_its_test_name'
refutes: refuses when beagle.py's `while start > 0 and first - start < CITE_CONTEX…` is put back as `while False:` (proven 2026-10-15T02:30:00+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_cited_text_holds_the_sentence_a_cited_line_ends)
refused after 6s of a 6s check at: FAILED tests/test_beagle_example_extension.py::test_cited_text_holds_the_sentence_a_cited_line_ends
refused with: 1 failed, 2 passed, 720 deselected in 5.72s
replaces: refuses when beagle.py's `words = words[1:end]` is put back as `pass` (proven 2026-10-15T02:28:50+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_case_lines_match_the_test_name_and_keep_only_the_quoted_words)
standing checks red: T0335, T0360, T0386, T0496, T0508, T0526, T0529, T0530, T0537, T0546, T0548, T0574, T0502, T0505, T0507, T0509, T0519, T0524, T0525, T0536, T0541, T0039
