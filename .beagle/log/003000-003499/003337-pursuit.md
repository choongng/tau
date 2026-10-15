+++
id = "003337-pursuit"
ordinal = 3337
kind = "pursuit"
timestamp = "2026-10-15T17:20:48+00:00"
summary = "pursuit prove T0645: WITNESSED — refuses when beagle.py's `or _tau_nudges_cut(message)` is put back as `or getattr(message, \"stop_reason\", None) == \"le…`"
metric_command = ""
drains = []
hooks = []
+++

check: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k 'stop_gate'
refutes: refuses when beagle.py's `or _tau_nudges_cut(message)` is put back as `or getattr(message, "stop_reason", None) == "le…` (proven 2026-10-15T17:19:49+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_stop_gate_follows_up_the_cut_off_that_tau_no_longer_nudges)
refused after 1s of a 1s check at: FAILED tests/test_beagle_example_extension.py::test_stop_gate_follows_up_the_cut_off_that_tau_no_longer_nudges
refused with: 1 failed, 7 passed, 732 deselected in 1.12s
standing checks red: T0335, T0360, T0386, T0496, T0508, T0526, T0529, T0530, T0537, T0546, T0548, T0574, T0086, T0088, T0089, T0226, T0502, T0505, T0507, T0509, T0519, T0524, T0525, T0536, T0541
