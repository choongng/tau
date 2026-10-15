+++
id = "003219-pursuit"
ordinal = 3219
kind = "pursuit"
timestamp = "2026-10-15T04:02:22+00:00"
summary = "pursuit amend T0622"
metric_command = ""
drains = []
hooks = []
+++

the -k expression was unquoted, so pytest took 'or' and the second name as paths (exit 4)
was: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k test_pursuit_step_fetches_a_url_source_before_its_cases_worker or test_pursuit_step_does_not_run_a_cases_worker_on_a_url_it_cannot_fetch
now: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k 'test_pursuit_step_fetches_a_url_source_before_its_cases_worker or test_pursuit_step_does_not_run_a_cases_worker_on_a_url_it_cannot_fetch'
