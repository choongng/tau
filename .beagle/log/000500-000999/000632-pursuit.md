+++
id = "000632-pursuit"
ordinal = 632
kind = "pursuit"
timestamp = "2026-10-04T11:05:28+00:00"
summary = "pursuit prove T0150: WITNESSED — refuses when beagle.py's `if scope or not (root / \"references\").is_dir():` is put back as `if True:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "4578d4b36fc90b6cb20cefb36f4e46f84da73d76140bc8ff490fe1e321b43885  .beagle/checks/T0150/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0150/check.sh'
refutes: refuses when beagle.py's `if scope or not (root / "references").is_dir():` is put back as `if True:` (proven 2026-10-04T11:04:58+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_opening_a_task_with_no_scope_is_refused)
refused after 3s of a 57s check at: FAILED tests/test_beagle_example_extension.py::test_opening_a_task_with_no_scope_is_refused
refused with: 1 failed in 2.77s
