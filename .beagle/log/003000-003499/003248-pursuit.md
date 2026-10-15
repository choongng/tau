+++
id = "003248-pursuit"
ordinal = 3248
kind = "pursuit"
timestamp = "2026-10-15T06:28:24+00:00"
summary = "pursuit open T0627: Fix 16: a case correction reads the source words quoted beside it"
metric_command = ""
drains = []
hooks = []
+++

criteria: A changed pinned case is accepted when its CASE words, or a quoted span on a report line naming the case or its test, are held by its cited paragraph (by any reference, for kind=gap), ignoring spacing around brackets and commas; the reason names the words.
decided by: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py tests/test_beagle_real_step.py -k 'test_a_gap_case_is_refuted_by_source_words_anywhere_in_references or test_real_spec_tied_step_takes_the_source_words_a_report_quotes_beside_the_case'
budget: 40000 tokens
