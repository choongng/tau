+++
id = "000823-pursuit"
ordinal = 823
kind = "pursuit"
timestamp = "2026-10-05T01:42:12+00:00"
summary = "pursuit prove T0209: WITNESSED — refuses when beagle.py's `clash = _live_title_clash(task, parts, _tree_no…` is put back as `clash = None`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "fe009b9167866d32acae8d688f8651f7dc71fed228562beb2821d019ad11f2a8  .beagle/checks/T0209/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0209/check.sh'
refutes: refuses when beagle.py's `clash = _live_title_clash(task, parts, _tree_no…` is put back as `clash = None` (proven 2026-10-05T01:41:55+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_root_plan_refuses_a_part_titled_like_a_live_task)
refused after 2s of a 1m09s check at: FAILED tests/test_beagle_example_extension.py::test_root_plan_refuses_a_part_titled_like_a_live_task
refused with: 1 failed in 1.99s
