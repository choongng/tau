+++
id = "003326-pursuit"
ordinal = 3326
kind = "pursuit"
timestamp = "2026-10-15T16:16:17+00:00"
summary = "pursuit open T0643: Fix 30: a url source with a fragment is read from the page on disk"
metric_command = ""
drains = []
hooks = []
+++

criteria: _fetched_source drops a URL's fragment and returns a reference already fetched for that URL without running beagle refs fetch; a page not yet on disk is fetched once without its fragment
decided by: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k 'test_pursuit_step_reads_a_url_source_with_a_fragment_from_the_page_on_disk'
budget: 40000 tokens
