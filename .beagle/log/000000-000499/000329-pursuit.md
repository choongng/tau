+++
id = "000329-pursuit"
ordinal = 329
kind = "pursuit"
timestamp = "2026-10-03T20:29:29+00:00"
summary = "pursuit sweep at close T0078: 1 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 5777 chunks, 5777 sampled, 16 candidate pair(s) at Jaccard >= 0.70 (code, k=5)
  focused on 1 path(s): 3 identical, 13 diverged; every pair touching them is listed, copies across files first
  1.00  tests/test_beagle_example_extension.py:144 fake_beagle
        tests/test_beagle_example_extension.py:1408 fake_tau
  1.00  tests/test_beagle_example_extension.py:1201 test_host_note_names_worktree_isolation
        tests/test_beagle_example_extension.py:1227 test_host_note_gives_the_worker_spawn_rules
  1.00  tests/test_beagle_example_extension.py:4378 test_worker_argv_caps_turns
        tests/test_beagle_example_extension.py:4399 test_worker_argv_thinking_off
  0.84  tests/test_beagle_example_extension.py:3073 test_already_passes_on_a_container_part_names_the_done_sibling
        tests/test_beagle_example_extension.py:3098 test_already_passes_on_a_root_child_keeps_the_abandon_hint
  0.83  tests/test_beagle_example_extension.py:1104 test_guard_blocks_shell_writes_to_the_goal
        tests/test_beagle_example_extension.py:1129 test_guard_lets_reads_of_the_goal_through
  ... (+11 more in this bucket)
sample_cruft: 1 sampled, 0 flagged
