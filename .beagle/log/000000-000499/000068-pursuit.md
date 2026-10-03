+++
id = "000068-pursuit"
ordinal = 68
kind = "pursuit"
timestamp = "2026-10-03T12:52:09+00:00"
summary = "pursuit prove T0029: WITNESSED — refuses when beagle.py's `brief = _without_commit_steps(brief)` is put back as `pass`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "b19f9e84d3f7274e6bea88314d4504508bde641c1ccc43d13e4f7439b00b229d  .beagle/checks/T0029/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0029/check.sh'
refutes: refuses when beagle.py's `brief = _without_commit_steps(brief)` is put back as `pass` (proven 2026-10-03T12:52:02+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_step_brief_has_no_commit_steps)
refused after 1s of a 2s check at: FAILED tests/test_beagle_example_extension.py::test_step_brief_has_no_commit_steps
refused with: 1 failed, 6 passed, 209 deselected in 0.82s
