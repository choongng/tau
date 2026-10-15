+++
id = "003192-pursuit"
ordinal = 3192
kind = "pursuit"
timestamp = "2026-10-15T02:20:18+00:00"
summary = "pursuit open T0619: Fix 8: a code worker's CASE line counts by test name, quoted words, and the cited sentence"
metric_command = ""
drains = []
hooks = []
+++

criteria: A code worker's CASE line for a corrected case is accepted when it names the case by its test function, when words follow the quote, and when the quoted sentence starts on lines above the cited one; the real-CLI step then closes done.
decided by: $PY -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py tests/test_beagle_real_step.py -k 'case_lines_match or cited_text_holds or case_line_by_its_test_name'
budget: 60000 tokens
