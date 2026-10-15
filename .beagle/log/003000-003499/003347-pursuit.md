+++
id = "003347-pursuit"
ordinal = 3347
kind = "pursuit"
timestamp = "2026-10-15T21:40:51+00:00"
summary = "pursuit prove T0647: WITNESSED — refuses when beagle.py's `brief += \"\\n\\n\" + WITNESS_PENDING_NOTE` is put back as `brief += \"\"`"
metric_command = ""
drains = []
hooks = []
+++

check: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k 'warns_a_fresh_worker or hands_a_refused_witness or takes_the_work_away'
refutes: refuses when beagle.py's `brief += "\n\n" + WITNESS_PENDING_NOTE` is put back as `brief += ""` (proven 2026-10-15T21:39:52+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_pursuit_step_warns_a_fresh_worker_not_to_rewrite_a_check_that_alrea…)
refused after 2s of a 2s check at: FAILED tests/test_beagle_example_extension.py::test_pursuit_step_warns_a_fresh_worker_not_to_rewrite_a_check_that_alrea…
refused with: 1 failed, 2 passed, 739 deselected in 1.55s
standing checks red: T0335, T0360, T0386, T0496, T0508, T0526, T0529, T0530, T0537, T0546, T0548, T0574, T0086, T0088, T0089, T0226, T0502, T0505, T0507, T0509, T0519, T0524, T0525, T0536, T0541
