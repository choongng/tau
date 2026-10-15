+++
id = "003286-pursuit"
ordinal = 3286
kind = "pursuit"
timestamp = "2026-10-15T11:22:38+00:00"
summary = "pursuit prove T0635: WITNESSED — refuses when beagle.py's `resume = run.transcript.stem continue` is put back as `resume = \"\" continue`"
metric_command = ""
drains = []
hooks = []
+++

check: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k 'refused_witness_back_to_the_same_worker'
refutes: refuses when beagle.py's `resume = run.transcript.stem continue` is put back as `resume = "" continue` (proven 2026-10-15T11:21:41+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_pursuit_step_hands_a_refused_witness_back_to_the_same_worker)
refused after 1s of a 1s check at: FAILED tests/test_beagle_example_extension.py::test_pursuit_step_hands_a_refused_witness_back_to_the_same_worker
refused with: 1 failed, 730 deselected in 1.09s
standing checks red: T0335, T0360, T0386, T0496, T0508, T0526, T0529, T0530, T0537, T0546, T0548, T0574, T0502, T0505, T0507, T0509, T0519, T0524, T0525, T0536, T0541
