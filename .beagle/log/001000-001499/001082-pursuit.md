+++
id = "001082-pursuit"
ordinal = 1082
kind = "pursuit"
timestamp = "2026-10-05T12:08:25+00:00"
summary = "pursuit sweep at close T0259: 1 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 6369 chunks, 6369 sampled, 67 candidate pair(s) at Jaccard >= 0.70 (code, k=5)
  focused on 1 path(s): 7 identical, 60 diverged; every pair touching them is listed, copies across files first
  1.00  tests/test_beagle_example_extension.py:148 fake_beagle
        tests/test_beagle_example_extension.py:1441 fake_tau
  1.00  tests/test_beagle_example_extension.py:1205 test_host_note_names_worktree_isolation
        tests/test_beagle_example_extension.py:1231 test_host_note_gives_the_worker_spawn_rules
  1.00  tests/test_beagle_example_extension.py:6765 test_worker_argv_caps_turns
        tests/test_beagle_example_extension.py:6786 test_worker_argv_thinking_off
  1.00  tests/test_beagle_example_extension.py:9103 test_worker_guard_refuses_git_show_of_a_dot_beagle_path
        tests/test_beagle_example_extension.py:9125 test_worker_guard_refuses_git_cat_file_of_dot_beagle
  1.00  tests/test_beagle_example_extension.py:9198 _step_done_txt
        tests/test_beagle_example_extension.py:10036 _step_m
  ... (+62 more in this bucket)
sample_cruft: 1 sampled, 0 flagged
