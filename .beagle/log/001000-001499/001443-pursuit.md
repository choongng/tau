+++
id = "001443-pursuit"
ordinal = 1443
kind = "pursuit"
timestamp = "2026-10-10T02:36:40+00:00"
summary = "pursuit sweep at close T0339: 2 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 6871 chunks, 6871 sampled, 8 candidate pair(s) at Jaccard >= 0.70 (code, k=5)
  focused on 2 path(s): 2 identical, 6 diverged; every pair touching them is listed, copies across files first
  0.83  examples/extensions/beagle.py:2313 _newline_only
        src/tau_coding/tools.py:953 normalize_to_lf
  0.80  tests/test_tool_cut_off_arguments.py:28 test_cut_off_bash_does_not_run
        tests/test_tool_missing_argument.py:38 test_non_string_path_still_says_must_be_a_string
  1.00  src/tau_coding/tools.py:549 create_write_tool
        src/tau_coding/tools.py:659 create_edit_tool
  1.00  src/tau_coding/tools.py:1178 _not_found_error
        src/tau_coding/tools.py:1190 _duplicate_error
  0.88  src/tau_coding/tools.py:264 create_read_tool_definition
        src/tau_coding/tools.py:288 execute
  ... (+3 more in this bucket)
sample_cruft: 2 sampled, 0 flagged
