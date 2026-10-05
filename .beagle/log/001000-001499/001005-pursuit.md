+++
id = "001005-pursuit"
ordinal = 1005
kind = "pursuit"
timestamp = "2026-10-05T08:24:43+00:00"
summary = "pursuit prove T0242: WITNESSED — refuses when beagle.py's `if _at_spawn_limit(task, fresh := _tree_nodes(r…` is put back as `if False and (fresh := _tree_nodes(root))`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "39c4e937a88194b31576a21bcfe1910c567b45122042948691cf9727f9394278  .beagle/checks/T0242/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0242/check.sh'
refutes: refuses when beagle.py's `if _at_spawn_limit(task, fresh := _tree_nodes(r…` is put back as `if False and (fresh := _tree_nodes(root))` (proven 2026-10-05T08:24:36+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_unproven_step_at_spawn_limit_offers_infeasible_not_new_route)
refused after 2s of a 1m19s check at: FAILED tests/test_beagle_example_extension.py::test_unproven_step_at_spawn_limit_offers_infeasible_not_new_route
refused with: 1 failed in 2.02s
