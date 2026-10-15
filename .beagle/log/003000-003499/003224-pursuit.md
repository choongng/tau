+++
id = "003224-pursuit"
ordinal = 3224
kind = "pursuit"
timestamp = "2026-10-15T04:03:08+00:00"
summary = "pursuit open T0623: Fix 12: pursuit_step takes a described task as the one workable task"
metric_command = ""
drains = []
hooks = []
+++

criteria: A pursuit_step whose task is prose, with one task workable, opens that task with the prose in its worker's notes and says so; an unworkable task id is still refused.
decided by: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k 'test_pursuit_step_takes_a_described_task_as_the_one_workable_task or test_pursuit_step_keeps_refusing_a_task_id_that_is_not_workable'
budget: 40000 tokens
