+++
id = "001071-pursuit"
ordinal = 1071
kind = "pursuit"
timestamp = "2026-10-05T11:40:23+00:00"
summary = "pursuit sweep at close T0258: 1 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 6352 chunks, 6352 sampled, 35 candidate pair(s) at Jaccard >= 0.70 (code, k=5)
  focused on 1 path(s): 2 identical, 33 diverged; every pair touching them is listed, copies across files first
  1.00  tests/test_coding_session.py:6071 fail_provider_creation
        tests/test_updater.py:174 fail_launch
  0.78  tests/test_coding_session.py:7587 bash
        tests/test_repeat_breaker_reset.py:24 execute
  0.72  tests/test_coding_session.py:7438 iterator
        tests/test_request_gate.py:41 iterator
  0.70  tests/test_coding_session.py:539 _CountingStorage
        tests/test_project_trust.py:334 _Storage
  1.00  tests/test_coding_session.py:3316 test_reserved_prompts_template_cannot_shadow_picker_command
        tests/test_coding_session.py:3346 test_reserved_tools_template_cannot_shadow_picker_command
  ... (+30 more in this bucket)
sample_cruft: 1 sampled, 0 flagged
