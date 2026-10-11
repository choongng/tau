+++
id = "001848-pursuit"
ordinal = 1848
kind = "pursuit"
timestamp = "2026-10-11T23:17:46+00:00"
summary = "pursuit prove T0438: WITNESSED — refuses when beagle.py's `given.setdefault(named[lock] or first, [])` is put back as `given.setdefault(first, [])` and beagle.py's `done_when, [scope, _predecessor_scope(record, r…` is put back as `done_when, [scope, _predecessor_scope(record, r…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "ad9d719fdcdc613fb1f3b08a2739a6081f6650831f985580227600bd0f97ba13  .beagle/checks/T0438/T0438.sh" | sha256sum -c --quiet && bash .beagle/checks/T0438/T0438.sh'
refutes: refuses when beagle.py's `given.setdefault(named[lock] or first, [])` is put back as `given.setdefault(first, [])` and beagle.py's `done_when, [scope, _predecessor_scope(record, r…` is put back as `done_when, [scope, _predecessor_scope(record, r…` (proven 2026-10-11T23:17:45+00:00; refused at FAILED
refused after 10s of a 2m50s check at: FAILED tests/test_beagle_example_extension.py::test_split_hands_each_lock_to_the_part_that_names_it
refused with: 3 failed, 774 deselected in 9.43s
