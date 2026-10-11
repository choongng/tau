+++
id = "001772-pursuit"
ordinal = 1772
kind = "pursuit"
timestamp = "2026-10-11T02:37:53+00:00"
summary = "pursuit prove T0410: WITNESSED — refuses when beagle.py's `if status not in {\"\", \"open\", \"pending\"}:` is put back as `if status not in {\"\", \"open\", \"pending\", \"block…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "d2e9c3da64dfe1e8d191679c57a9b0ccc76d2fedd49dc64e1aa488ecbc48e004  .beagle/checks/T0410/T0410.sh" | sha256sum -c --quiet && bash .beagle/checks/T0410/T0410.sh'
refutes: refuses when beagle.py's `if status not in {"", "open", "pending"}:` is put back as `if status not in {"", "open", "pending", "block…` (proven 2026-10-11T02:37:52+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_spawn_refused_at_the_limit_for_a_blocked_task_offers_no_infeasible_
refused after 4s of a 2m25s check at: FAILED tests/test_beagle_example_extension.py::test_spawn_refused_at_the_limit_for_a_blocked_task_offers_no_infeasible_…
refused with: 1 failed, 1 passed, 748 deselected in 3.84s
