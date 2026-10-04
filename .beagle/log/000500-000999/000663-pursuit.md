+++
id = "000663-pursuit"
ordinal = 663
kind = "pursuit"
timestamp = "2026-10-04T11:45:31+00:00"
summary = "pursuit sweep at close T0156: 1 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 6054 chunks, 6054 sampled, 53 candidate pair(s) at Jaccard >= 0.70 (code, k=5)
  focused on 1 path(s): 5 identical, 48 diverged; every pair touching them is listed, copies across files first
  1.00  tests/test_beagle_example_extension.py:146 fake_beagle
        tests/test_beagle_example_extension.py:1417 fake_tau
  1.00  tests/test_beagle_example_extension.py:1203 test_host_note_names_worktree_isolation
        tests/test_beagle_example_extension.py:1229 test_host_note_gives_the_worker_spawn_rules
  1.00  tests/test_beagle_example_extension.py:5793 test_worker_argv_caps_turns
        tests/test_beagle_example_extension.py:5814 test_worker_argv_thinking_off
  1.00  tests/test_beagle_example_extension.py:7702 test_worker_guard_refuses_git_show_of_a_dot_beagle_path
        tests/test_beagle_example_extension.py:7724 test_worker_guard_refuses_git_cat_file_of_dot_beagle
  1.00  tests/test_beagle_example_extension.py:7797 _step_done_txt
        tests/test_beagle_example_extension.py:8557 _step_m
  ... (+48 more in this bucket)
sample_cruft: 1 sampled, 0 flagged
