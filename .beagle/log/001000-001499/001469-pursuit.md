+++
id = "001469-pursuit"
ordinal = 1469
kind = "pursuit"
timestamp = "2026-10-10T03:04:35+00:00"
summary = "pursuit sweep at close T0344: 1 path(s) changed since open, candidates found"
metric_command = ""
drains = []
hooks = []
+++

sample_similarity: 6889 chunks, 6889 sampled, 79 candidate pair(s) at Jaccard >= 0.70 (code, k=5)
  focused on 1 path(s): 5 identical, 74 diverged; every pair touching them is listed, copies across files first
  1.00  tests/test_beagle_example_extension.py:1209 test_host_note_names_worktree_isolation
        tests/test_beagle_example_extension.py:1235 test_host_note_gives_the_worker_spawn_rules
  1.00  tests/test_beagle_example_extension.py:10426 test_worker_guard_refuses_git_show_of_a_dot_beagle_path
        tests/test_beagle_example_extension.py:10448 test_worker_guard_refuses_git_cat_file_of_dot_beagle
  1.00  tests/test_beagle_example_extension.py:10521 _step_done_txt
        tests/test_beagle_example_extension.py:11404 _step_m
  1.00  tests/test_beagle_example_extension.py:12127 _event_line
        tests/test_beagle_example_extension.py:9745 end
  1.00  tests/test_beagle_example_extension.py:15309 _open_on_done_txt
        tests/test_beagle_example_extension.py:15561 _open_on_notes_txt
  ... (+74 more in this bucket)
sample_cruft: 1 sampled, 0 flagged
