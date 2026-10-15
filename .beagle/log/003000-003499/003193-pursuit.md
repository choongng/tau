+++
id = "003193-pursuit"
ordinal = 3193
kind = "pursuit"
timestamp = "2026-10-15T02:27:18+00:00"
summary = "pursuit amend T0619"
metric_command = ""
drains = []
hooks = []
+++

the check named $PY literally; it is the venv python
was: $PY -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py tests/test_beagle_real_step.py -k 'case_lines_match or cited_text_holds or case_line_by_its_test_name'
now: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py tests/test_beagle_real_step.py -k 'case_lines_match or cited_text_holds or case_line_by_its_test_name'
