+++
id = "000327-pursuit"
ordinal = 327
kind = "pursuit"
timestamp = "2026-10-03T20:29:16+00:00"
summary = "pursuit prove T0078: WITNESSED — refuses when beagle.py's `if any(_state(t, nodes) in (\"abandoned\", \"stall…` is put back as `if any(_state(t, nodes) in (\"stalled\",) for t i…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "954b68843c64ad3d9d3b1fa8c3514602c661b0479b806bbd255a626bda3995e3  .beagle/checks/T0078/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0078/check.sh'
refutes: refuses when beagle.py's `if any(_state(t, nodes) in ("abandoned", "stall…` is put back as `if any(_state(t, nodes) in ("stalled",) for t i…` (proven 2026-10-03T20:28:34+00:00; predates the task: T0078 only adds tests for T0057's existing abandoned-target branch; this is the line they pin; refused a
refused after 1s of a 1s check at: FAILED tests/test_beagle_example_extension.py::test_dead_wait_on_an_abandoned_leaf_in_r08_shape
refused with: 2 failed, 282 deselected in 0.58s
