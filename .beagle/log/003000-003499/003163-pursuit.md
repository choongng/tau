+++
id = "003163-pursuit"
ordinal = 3163
kind = "pursuit"
timestamp = "2026-10-15T00:56:14+00:00"
summary = "pursuit prove T0612: WITNESSED — refuses when beagle.py's `settled = _settle_case_edits(task, report, root)` is put back as `settled = ''`"
metric_command = ""
drains = []
hooks = []
+++

check: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_real_step.py -k 'corrects_from_the_source or changed_without_the_source_words'
refutes: refuses when beagle.py's `settled = _settle_case_edits(task, report, root)` is put back as `settled = ''` (proven 2026-10-15T00:56:14+00:00; predates the task: the fix was committed on beagle-0.48 and merged before the task was opened (audit 10-14: opened late); the needle is the task's own line (74
refused after 9s of a 10s check at: FAILED tests/test_beagle_real_step.py::test_real_spec_tied_step_amends_a_case_the_code_worker_corrects_from_the_source
refused with: 2 failed, 4 deselected in 8.71s
