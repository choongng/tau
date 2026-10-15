+++
id = "003215-pursuit"
ordinal = 3215
kind = "pursuit"
timestamp = "2026-10-15T04:01:36+00:00"
summary = "pursuit open T0622: Fix 11: a URL source is fetched before its cases worker runs"
metric_command = ""
drains = []
hooks = []
+++

criteria: A task whose source is a URL has it fetched before its cases worker, whose brief names references/<file> and cites by its stem; a URL that cannot be fetched refuses the step with beagle's reason and runs no worker.
decided by: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k test_pursuit_step_fetches_a_url_source_before_its_cases_worker or test_pursuit_step_does_not_run_a_cases_worker_on_a_url_it_cannot_fetch
budget: 40000 tokens
