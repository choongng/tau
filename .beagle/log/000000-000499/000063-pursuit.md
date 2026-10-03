+++
id = "000063-pursuit"
ordinal = 63
kind = "pursuit"
timestamp = "2026-10-03T12:42:01+00:00"
summary = "pursuit prove T0028: WITNESSED — refuses when beagle.py's `refused = _abandon_problem(task, abandon, nodes)` is put back as `refused = None`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "733f2b2c36f0e99f7630d239b332ec5ec7b1676ee7a0f1be5d7fa48d8562a9d1  .beagle/checks/T0028/named_tests.sh" | sha256sum -c --quiet && bash .beagle/checks/T0028/named_tests.sh tests/test_beagle_example_extension.py 7 test_unprovable_restep_spawns_no_worker test_unprovable_first_verdict_stops_attempts test_abandon_already_done_refused test_abandon_duplicate_of_done_task_closes test_abandon_milestone_refused test_nothing_ready_with_stalled_root_says_not_done test_print_mode_stop_gate_queues_followup_twice'
refutes: refuses when beagle.py's `refused = _abandon_problem(task, abandon, nodes)` is put back as `refused = None` (proven 2026-10-03T12:41:56+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_abandon_already_done_refused)
refused after 2s of a 2s check at: FAILED tests/test_beagle_example_extension.py::test_abandon_already_done_refused
refused with: 2 failed, 5 passed, 202 deselected in 1.48s
