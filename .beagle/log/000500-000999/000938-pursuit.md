+++
id = "000938-pursuit"
ordinal = 938
kind = "pursuit"
timestamp = "2026-10-05T06:44:00+00:00"
summary = "pursuit prove T0233: WITNESSED — refuses when beagle.py's `and str(n.get(\"id\")) not in subtree` is put back as `and not node.get(\"parent\")`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "05c25a5ddfae27fe40ce81e90d3a53cc9ea7cb45818ec80103ec9f21ca2cdae1  .beagle/checks/T0233/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0233/check.sh'
refutes: refuses when beagle.py's `and str(n.get("id")) not in subtree` is put back as `and not node.get("parent")` (proven 2026-10-05T06:43:50+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_plan_under_nonroot_refuses_part_duplicating_pending_task)
refused after 3s of a 1m16s check at: FAILED tests/test_beagle_example_extension.py::test_plan_under_nonroot_refuses_part_duplicating_pending_task
refused with: 1 failed, 1 passed in 2.30s
