+++
id = "001759-pursuit"
ordinal = 1759
kind = "pursuit"
timestamp = "2026-10-11T02:03:27+00:00"
summary = "pursuit prove T0407: WITNESSED — refuses when beagle.py's `\"--done-when\", check, \"--over\", over]` is put back as `\"--done-when\", check]`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "d79707660917e2d1c209ade16df378fe244fb212b76dc30ff6871fa3ce20de24  .beagle/checks/T0407/T0407.sh" | sha256sum -c --quiet && bash .beagle/checks/T0407/T0407.sh'
refutes: refuses when beagle.py's `"--done-when", check, "--over", over]` is put back as `"--done-when", check]` (proven 2026-10-11T02:03:26+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_done_by_open_passes_over_naming_the_done_task)
refused after 6s of a 2m16s check at: FAILED tests/test_beagle_example_extension.py::test_done_by_open_passes_over_naming_the_done_task
refused with: 2 failed, 741 deselected in 5.37s
