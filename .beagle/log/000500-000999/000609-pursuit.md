+++
id = "000609-pursuit"
ordinal = 609
kind = "pursuit"
timestamp = "2026-10-04T09:13:46+00:00"
summary = "pursuit prove T0145: WITNESSED — refuses when beagle.py's `python = _past_runner(words)` is put back as `python = words`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "9f972080f3a728ae47ad11e24c94e14a430979ebf2bc1afab1036faa63aa6c29  .beagle/checks/T0145/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0145/check.sh'
refutes: refuses when beagle.py's `python = _past_runner(words)` is put back as `python = words` (proven 2026-10-04T09:13:12+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_check_refuses_uv_run_python_c_that_judges_nothing)
refused after 1s of a 52s check at: FAILED tests/test_beagle_example_extension.py::test_check_refuses_uv_run_python_c_that_judges_nothing
refused with: 1 failed in 0.81s
