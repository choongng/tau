+++
id = "001387-pursuit"
ordinal = 1387
kind = "pursuit"
timestamp = "2026-10-10T00:37:52+00:00"
summary = "pursuit sweep at close T0329: 2 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 6846 chunks, 6846 sampled, 7 candidate pair(s) at Jaccard >= 0.70 (code, k=5)
  focused on 2 path(s): 2 identical, 5 diverged; every pair touching them is listed, copies across files first
  0.83  examples/extensions/beagle.py:2313 _newline_only
        src/tau_coding/tools.py:953 normalize_to_lf
  0.77  src/tau_coding/rpc.py:546 _required_string
        src/tau_coding/tools.py:1067 _str_arg
  1.00  src/tau_coding/tools.py:549 create_write_tool
        src/tau_coding/tools.py:659 create_edit_tool
  1.00  src/tau_coding/tools.py:1166 _not_found_error
        src/tau_coding/tools.py:1178 _duplicate_error
  0.88  src/tau_coding/tools.py:264 create_read_tool_definition
        src/tau_coding/tools.py:288 execute
  ... (+2 more in this bucket)
sample_cruft: 2 sampled, 0 flagged
