+++
id = "002402-pursuit"
ordinal = 2402
kind = "pursuit"
timestamp = "2026-10-12T14:33:16+00:00"
summary = "pursuit prove T0470: WITNESSED — refuses when beagle.py's `f\"pursuit_step: {successor} not opened — \" not …` is put back as `False`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "94dd89e2142597aa47cdc4e5b1d475c6e9d5a86b92b94f1b2c24feb8e9c134c8  .beagle/checks/T0470/T0470.sh" | sha256sum -c --quiet && bash .beagle/checks/T0470/T0470.sh'
refutes: refuses when beagle.py's `f"pursuit_step: {successor} not opened — " not …` is put back as `False` (proven 2026-10-12T14:33:15+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_new_route_successor_killed_at_its_wall_is_not_reported_as_not_opened)
refused after 4s of a 2m42s check at: FAILED tests/test_beagle_example_extension.py::test_new_route_successor_killed_at_its_wall_is_not_reported_as_not_opened
refused with: 1 failed, 818 deselected in 3.35s
