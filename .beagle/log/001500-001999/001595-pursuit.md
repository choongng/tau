+++
id = "001595-pursuit"
ordinal = 1595
kind = "pursuit"
timestamp = "2026-10-10T17:26:08+00:00"
summary = "pursuit prove T0372: WITNESSED — refuses when beagle.py's `_THINKING_OFF_NEXT[root_key] = task` is put back as `pass`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "4bc5d9bc406bf3df181b3bdd872ecd7d7ad411e1e01d3cca10f11777e682bee8  .beagle/checks/T0372/T0372.sh" | sha256sum -c --quiet && bash .beagle/checks/T0372/T0372.sh'
refutes: refuses when beagle.py's `_THINKING_OFF_NEXT[root_key] = task` is put back as `pass` (proven 2026-10-10T17:26:07+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_next_attempt_runs_thinking_off_after_reasoning_cut_offs)
refused after 4s of a 1m54s check at: FAILED tests/test_beagle_example_extension.py::test_next_attempt_runs_thinking_off_after_reasoning_cut_offs
refused with: 1 failed, 1 passed, 704 deselected in 4.06s
