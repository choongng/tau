+++
id = "000088-pursuit"
ordinal = 88
kind = "pursuit"
timestamp = "2026-10-03T13:08:54+00:00"
summary = "pursuit prove T0033: WITNESSED — refuses when beagle.py's `milestones, repairs = _repair_milestones(milest…` is put back as `repairs = []`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "947dfeb8456476d5f44c36903af4bb7be8c426738b0a313a02506889867be002  .beagle/checks/T0033/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0033/check.sh'
refutes: refuses when beagle.py's `milestones, repairs = _repair_milestones(milest…` is put back as `repairs = []` (proven 2026-10-03T13:08:44+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_found_shortens_long_milestone_title)
refused after 1s of a 1s check at: FAILED tests/test_beagle_example_extension.py::test_found_shortens_long_milestone_title
refused with: 2 failed, 215 deselected in 0.55s
standing checks red: T0024, T0030
