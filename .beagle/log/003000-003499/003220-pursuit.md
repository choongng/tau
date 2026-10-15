+++
id = "003220-pursuit"
ordinal = 3220
kind = "pursuit"
timestamp = "2026-10-15T04:02:29+00:00"
summary = "pursuit prove T0622: WITNESSED — refuses when beagle.py's `source, unfetched = await asyncio.to_thread(_fe…` is put back as `unfetched = \"\"`"
metric_command = ""
drains = []
hooks = []
+++

check: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k 'test_pursuit_step_fetches_a_url_source_before_its_cases_worker or test_pursuit_step_does_not_run_a_cases_worker_on_a_url_it_cannot_fetch'
refutes: refuses when beagle.py's `source, unfetched = await asyncio.to_thread(_fe…` is put back as `unfetched = ""` (proven 2026-10-15T04:02:29+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_pursuit_step_fetches_a_url_source_before_its_cases_worker)
refused after 4s of a 2s check at: FAILED tests/test_beagle_example_extension.py::test_pursuit_step_fetches_a_url_source_before_its_cases_worker
refused with: 2 failed, 717 deselected in 3.95s
