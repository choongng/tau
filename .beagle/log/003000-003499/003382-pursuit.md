+++
id = "003382-pursuit"
ordinal = 3382
kind = "pursuit"
timestamp = "2026-10-15T22:35:25+00:00"
summary = "pursuit prove T0616: WITNESSED — refuses when beagle.py's `\"Work out arithmetic, bit layouts and expected …` is put back as `\"Work out arithmetic, bit layouts and expected …`"
metric_command = ""
drains = []
hooks = []
+++

check: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k spec_tied_writes_cases_then_opens_with_cites_and_cases
refutes: refuses when beagle.py's `"Work out arithmetic, bit layouts and expected …` is put back as `"Work out arithmetic, bit layouts and expected …` (proven 2026-10-15T22:35:25+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_pursuit_step_spec_tied_writes_cases_then_opens_with_cites_an
refused after 4s of a 3s check at: FAILED tests/test_beagle_example_extension.py::test_pursuit_step_spec_tied_writes_cases_then_opens_with_cites_and_cases
refused with: 1 failed, 746 deselected in 3.12s
replaces: refuses when beagle.py's `"Work out arithmetic, bit layouts and expected …` is put back as `"Work out arithmetic, bit layouts and expected …` (proven 2026-10-15T01:06:42+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_pursuit_step_spec_tied_writes_cases_then_opens_with_cites_an
