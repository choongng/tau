+++
id = "002660-pursuit"
ordinal = 2660
kind = "pursuit"
timestamp = "2026-10-13T06:07:46+00:00"
summary = "pursuit prove T0518: WITNESSED — refuses when beagle.py's `missing = _missing_program(argv[0], root)` is put back as `missing = \"\"`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "274ff75d7d8ec0f8d91631bf606efdcd6aef3533c3b3568f972e13b198133416  .beagle/checks/T0518/T0518.v2.sh" | sha256sum -c --quiet && bash .beagle/checks/T0518/T0518.v2.sh'
refutes: refuses when beagle.py's `missing = _missing_program(argv[0], root)` is put back as `missing = ""` (proven 2026-10-13T06:07:46+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_open_refuses_a_check_whose_program_is_not_here)
refused after 4s of a 4s check at: FAILED tests/test_beagle_example_extension.py::test_open_refuses_a_check_whose_program_is_not_here
refused with: 1 failed, 848 deselected in 1.57s
