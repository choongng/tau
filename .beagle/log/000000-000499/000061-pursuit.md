+++
id = "000061-pursuit"
ordinal = 61
kind = "pursuit"
timestamp = "2026-10-03T12:32:37+00:00"
summary = "pursuit open T0028: R02 fix: no re-step of an unprovable check, no abandon of milestones or 'already done', and a gate on the final stop"
metric_command = ""
drains = []
hooks = []
+++

criteria: A pursuit_step whose passing check could not be proven (no defect could be put back) runs no second worker in that step, and a later identical step (same done_when and scope) spawns nothing and returns a refusal naming how to bind a check that imports the code. Abandon is refused for 'already done' reasons and for milestones (root's direct children); 'duplicate of Tnnnn' naming a done/open task closes. ABANDON_HINT no longer offers 'already done'. nothing_ready with a stalled root or abandoned leaves without successors says the pursuit is NOT done and never invites telling the user it is done. In print mode too, a driver stop without tool calls in a founded pursuit whose root is not done queues a follow-up naming the stalled tasks, at most twice per run. CASES_FIRST_NOTE agrees with _check_problem.
decided by: sh -c 'echo "733f2b2c36f0e99f7630d239b332ec5ec7b1676ee7a0f1be5d7fa48d8562a9d1  .beagle/checks/T0028/named_tests.sh" | sha256sum -c --quiet && bash .beagle/checks/T0028/named_tests.sh tests/test_beagle_example_extension.py 7 test_unprovable_restep_spawns_no_worker test_unprovable_first_verdict_stops_attempts test_abandon_already_done_refused test_abandon_duplicate_of_done_task_closes test_abandon_milestone_refused test_nothing_ready_with_stalled_root_says_not_done test_print_mode_stop_gate_queues_followup_twice'
budget: 200000 tokens
