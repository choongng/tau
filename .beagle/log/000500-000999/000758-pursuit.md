+++
id = "000758-pursuit"
ordinal = 758
kind = "pursuit"
timestamp = "2026-10-04T17:04:49+00:00"
summary = "pursuit sweep at close T0175: 1 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 6117 chunks, 6117 sampled, 59 candidate pair(s) at Jaccard >= 0.70 (code, k=5)
  focused on 1 path(s): 5 identical, 54 diverged; every pair touching them is listed, copies across files first
  1.00  tests/test_beagle_example_extension.py:146 fake_beagle
        tests/test_beagle_example_extension.py:1417 fake_tau
  1.00  tests/test_beagle_example_extension.py:1203 test_host_note_names_worktree_isolation
        tests/test_beagle_example_extension.py:1229 test_host_note_gives_the_worker_spawn_rules
  1.00  tests/test_beagle_example_extension.py:6227 test_worker_argv_caps_turns
        tests/test_beagle_example_extension.py:6248 test_worker_argv_thinking_off
  1.00  tests/test_beagle_example_extension.py:8138 test_worker_guard_refuses_git_show_of_a_dot_beagle_path
        tests/test_beagle_example_extension.py:8160 test_worker_guard_refuses_git_cat_file_of_dot_beagle
  1.00  tests/test_beagle_example_extension.py:8233 _step_done_txt
        tests/test_beagle_example_extension.py:9071 _step_m
  ... (+54 more in this bucket)
sample_cruft: 1 sampled, 0 flagged
