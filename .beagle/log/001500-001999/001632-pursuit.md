+++
id = "001632-pursuit"
ordinal = 1632
kind = "pursuit"
timestamp = "2026-10-10T20:34:10+00:00"
summary = "pursuit prove T0382: WITNESSED — refuses when beagle.py's `guarded = await _cases_test_passing_without_cod…` is put back as `guarded = None`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "51ad8e3a2ff7631b43e3a3b1ea649db7fb4db7d3ada082f43dcba2a8438cc0d2  .beagle/checks/T0382/T0382.sh" | sha256sum -c --quiet && bash .beagle/checks/T0382/T0382.sh'
refutes: refuses when beagle.py's `guarded = await _cases_test_passing_without_cod…` is put back as `guarded = None` (proven 2026-10-10T20:34:09+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_known_answers_close_holds_a_cases_test_that_passes_without_the_code)
refused after 2s of a 1m55s check at: FAILED tests/test_beagle_example_extension.py::test_known_answers_close_holds_a_cases_test_that_passes_without_the_code
refused with: 1 failed, 1 passed, 710 deselected in 1.68s
