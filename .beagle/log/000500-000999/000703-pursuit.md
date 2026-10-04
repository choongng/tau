+++
id = "000703-pursuit"
ordinal = 703
kind = "pursuit"
timestamp = "2026-10-04T14:08:21+00:00"
summary = "pursuit prove T0165: WITNESSED — refuses when beagle.py's `\"found\",` is put back as `\"unfound\",`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "b191e9d45013854e710b5a92635942c4b9a04da252393bd2e4a0839f3adf91a8  .beagle/checks/T0165/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0165/check.sh'
refutes: refuses when beagle.py's `"found",` is put back as `"unfound",` (proven 2026-10-04T14:07:55+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_founding_drops_a_found_the_pursuit_milestone)
refused after 2s of a 1m01s check at: FAILED tests/test_beagle_example_extension.py::test_founding_drops_a_found_the_pursuit_milestone
refused with: 1 failed in 1.33s
