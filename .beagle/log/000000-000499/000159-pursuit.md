+++
id = "000159-pursuit"
ordinal = 159
kind = "pursuit"
timestamp = "2026-10-03T16:33:14+00:00"
summary = "pursuit sweep at close T0051: 1 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 5694 chunks, 5694 sampled, 10 candidate pair(s) at Jaccard >= 0.70 (code, k=5)
  focused on 1 path(s): 3 identical, 7 diverged; every pair touching them is listed, copies across files first
  1.00  tests/test_beagle_example_extension.py:144 fake_beagle
        tests/test_beagle_example_extension.py:1408 fake_tau
  1.00  tests/test_beagle_example_extension.py:1201 test_host_note_names_worktree_isolation
        tests/test_beagle_example_extension.py:1227 test_host_note_gives_the_worker_spawn_rules
  1.00  tests/test_beagle_example_extension.py:3616 test_worker_argv_caps_turns
        tests/test_beagle_example_extension.py:3637 test_worker_argv_thinking_off
  0.83  tests/test_beagle_example_extension.py:1104 test_guard_blocks_shell_writes_to_the_goal
        tests/test_beagle_example_extension.py:1129 test_guard_lets_reads_of_the_goal_through
  0.75  tests/test_beagle_example_extension.py:3309 test_a_worker_may_read_the_pursuit_but_not_change_it
        tests/test_beagle_example_extension.py:3400 test_no_session_writes_beagles_records
  ... (+5 more in this bucket)
sample_cruft: 1 sampled, 0 flagged
