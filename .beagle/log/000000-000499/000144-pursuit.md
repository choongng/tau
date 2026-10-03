+++
id = "000144-pursuit"
ordinal = 144
kind = "pursuit"
timestamp = "2026-10-03T16:17:51+00:00"
summary = "pursuit prove T0048: WITNESSED — refuses when beagle.py's `carried = _carried_criteria(predecessor, root) …` is put back as `carried = \"\"`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "42ca696d944107961b7f9e704483896ae75a971f62343e7d943a2735ebb4bca5  .beagle/checks/T0048/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0048/check.sh'
refutes: refuses when beagle.py's `carried = _carried_criteria(predecessor, root) …` is put back as `carried = ""` (proven 2026-10-03T16:17:34+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_new_route_successor_opens_with_the_predecessors_criteria)
refused after 1s of a 1s check at: FAILED tests/test_beagle_example_extension.py::test_new_route_successor_opens_with_the_predecessors_criteria
refused with: 1 failed, 3 passed, 240 deselected in 1.02s
