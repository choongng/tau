+++
id = "000173-pursuit"
ordinal = 173
kind = "pursuit"
timestamp = "2026-10-03T17:03:57+00:00"
summary = "pursuit prove T0054: WITNESSED — refuses when beagle.py's `milestones, repairs = _milestones_from_criteria…` is put back as `pass`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "04b3be87fcf27ed0da30e4829c07eb9b6fe739ec7862fb34f950bbc6b8d5024c  .beagle/checks/T0054/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0054/check.sh'
refutes: refuses when beagle.py's `milestones, repairs = _milestones_from_criteria…` is put back as `pass` (proven 2026-10-03T17:03:37+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_founding_seeds_milestones_from_criteria_when_every_one_is_setup)
refused after 1s of a 1s check at: FAILED tests/test_beagle_example_extension.py::test_founding_seeds_milestones_from_criteria_when_every_one_is_setup
refused with: 2 failed, 1 passed, 249 deselected in 0.50s
