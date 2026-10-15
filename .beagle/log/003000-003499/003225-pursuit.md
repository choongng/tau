+++
id = "003225-pursuit"
ordinal = 3225
kind = "pursuit"
timestamp = "2026-10-15T04:04:12+00:00"
summary = "pursuit prove T0623: WITNESSED — refuses when beagle.py's `and len(workable) == 1` is put back as `and len(workable) == 0`"
metric_command = ""
drains = []
hooks = []
+++

check: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k 'test_pursuit_step_takes_a_described_task_as_the_one_workable_task or test_pursuit_step_keeps_refusing_a_task_id_that_is_not_workable'
refutes: refuses when beagle.py's `and len(workable) == 1` is put back as `and len(workable) == 0` (proven 2026-10-15T04:03:14+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_pursuit_step_takes_a_described_task_as_the_one_workable_task)
refused after 4s of a 1s check at: FAILED tests/test_beagle_example_extension.py::test_pursuit_step_takes_a_described_task_as_the_one_workable_task
refused with: 1 failed, 1 passed, 719 deselected in 3.18s
standing checks red: T0335, T0360, T0386, T0496, T0508, T0526, T0529, T0530, T0537, T0546, T0548, T0574, T0502, T0505, T0507, T0509, T0519, T0524, T0525, T0536, T0541, T0039
