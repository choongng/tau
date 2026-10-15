+++
id = "003299-pursuit"
ordinal = 3299
kind = "pursuit"
timestamp = "2026-10-15T12:37:13+00:00"
summary = "pursuit prove T0637: WITNESSED — refuses when beagle.py's `\"version of it, to check them, for that version…` is put back as `\"variant of it, to check them, for that version…`"
metric_command = ""
drains = []
hooks = []
+++

check: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k 'test_pursuit_step_spec_tied_writes_cases_then_opens_with_cites_and_cases'
refutes: refuses when beagle.py's `"version of it, to check them, for that version…` is put back as `"variant of it, to check them, for that version…` (proven 2026-10-15T12:37:13+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_pursuit_step_spec_tied_writes_cases_then_opens_with_cites_an
refused after 2s of a 1s check at: FAILED tests/test_beagle_example_extension.py::test_pursuit_step_spec_tied_writes_cases_then_opens_with_cites_and_cases
refused with: 1 failed, 731 deselected in 1.37s
