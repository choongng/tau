+++
id = "000138-pursuit"
ordinal = 138
kind = "pursuit"
timestamp = "2026-10-03T16:10:41+00:00"
summary = "pursuit prove T0047: WITNESSED — refuses when beagle.py's `if state.get(nxt) == 1:` is put back as `if False:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "43734393499d6de39f825a1b474e88d8458bbfb2d72ea4c9be68966abf8647d8  .beagle/checks/T0047/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0047/check.sh'
refutes: refuses when beagle.py's `if state.get(nxt) == 1:` is put back as `if False:` (proven 2026-10-03T16:10:26+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_step_names_the_drop_for_a_cycle_when_nothing_is_ready)
refused after 1s of a 1s check at: FAILED tests/test_beagle_example_extension.py::test_step_names_the_drop_for_a_cycle_when_nothing_is_ready
refused with: 2 failed, 1 passed, 236 deselected in 0.67s
