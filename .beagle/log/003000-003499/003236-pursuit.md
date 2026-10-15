+++
id = "003236-pursuit"
ordinal = 3236
kind = "pursuit"
timestamp = "2026-10-15T05:12:36+00:00"
summary = "pursuit open T0625: Fix 14: a spec-tied scope of tests only gains the code its cases import"
metric_command = ""
drains = []
hooks = []
+++

criteria: A source task whose scope holds only its tests opens, after its cases are written, with the module those cases import (<m>.py and <m>/, under src/ when the project has one) added to its scope, says so, and is not sent to the data-test route.
decided by: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k test_pursuit_step_spec_tied_scope_of_tests_only_gains_the_code_its_cases_import
budget: 40000 tokens
