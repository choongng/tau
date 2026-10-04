+++
id = "000708-pursuit"
ordinal = 708
kind = "pursuit"
timestamp = "2026-10-04T14:13:32+00:00"
summary = "pursuit prove T0166: WITNESSED — refuses when beagle.py's `lead[:] = [_setup_lead(task)]` is put back as `pass`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "3928a90bbc3598073f70af99a00d60ab872ceec2b0636abe0215b5780adee89e  .beagle/checks/T0166/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0166/check.sh'
refutes: refuses when beagle.py's `lead[:] = [_setup_lead(task)]` is put back as `pass` (proven 2026-10-04T14:13:06+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_beagle_dir_refusal_on_a_setup_task_says_abandon_it)
refused after 2s of a 1m01s check at: FAILED tests/test_beagle_example_extension.py::test_beagle_dir_refusal_on_a_setup_task_says_abandon_it
refused with: 1 failed in 1.63s
