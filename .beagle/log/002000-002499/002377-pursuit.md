+++
id = "002377-pursuit"
ordinal = 2377
kind = "pursuit"
timestamp = "2026-10-12T14:18:55+00:00"
summary = "pursuit prove T0465: WITNESSED — refuses when beagle.py's `if _lean() else \": it reaches` is put back as `if False else \": it reaches`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "9228d8667209dc7df234a917c6eb1eb7ed3274a15d9bd1d9f0d54a82b330b21e  .beagle/checks/T0465/T0465.sh" | sha256sum -c --quiet && bash .beagle/checks/T0465/T0465.sh'
refutes: refuses when beagle.py's `if _lean() else ": it reaches` is put back as `if False else ": it reaches` (proven 2026-10-12T14:18:55+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_ruff_over_root_refusal_names_no_locked_tests_when_none_are_locked)
refused after 3s of a 2m41s check at: FAILED tests/test_beagle_example_extension.py::test_ruff_over_root_refusal_names_no_locked_tests_when_none_are_locked
refused with: 1 failed, 814 deselected in 2.74s
