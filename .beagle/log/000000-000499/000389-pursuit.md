+++
id = "000389-pursuit"
ordinal = 389
kind = "pursuit"
timestamp = "2026-10-03T21:27:41+00:00"
summary = "pursuit prove T0088: WITNESSED — refuses when beagle.py's `elif (why := _rerun_only_part([part])) is not N…` is put back as `elif (why := None) is not None:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "6afe023705e7ae4730724b8f530b9dc7f4f5e60e882a64fa6fdaaae31ec8ec45  .beagle/checks/T0088/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0088/check.sh'
refutes: refuses when beagle.py's `elif (why := _rerun_only_part([part])) is not N…` is put back as `elif (why := None) is not None:` (proven 2026-10-03T21:26:54+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_founding_drops_a_rerun_only_milestone_with_a_note)
refused after 1s of a 1s check at: FAILED tests/test_beagle_example_extension.py::test_founding_drops_a_rerun_only_milestone_with_a_note
refused with: 1 failed, 302 deselected in 0.51s
