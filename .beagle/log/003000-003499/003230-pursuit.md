+++
id = "003230-pursuit"
ordinal = 3230
kind = "pursuit"
timestamp = "2026-10-15T04:35:15+00:00"
summary = "pursuit open T0624: Fix 13: founding offers the request's link as a milestone source"
metric_command = ""
drains = []
hooks = []
+++

criteria: pursuit_found's and pursuit_plan's milestone guidance and the source field's description name a link in the user's request as a source, beside a file in references/.
decided by: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k test_found_offers_the_requests_link_as_a_milestone_source
budget: 40000 tokens
