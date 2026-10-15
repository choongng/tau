+++
id = "003360-pursuit"
ordinal = 3360
kind = "pursuit"
timestamp = "2026-10-15T21:50:00+00:00"
summary = "pursuit open T0651: baseline founding bench on today's tau"
metric_command = ""
drains = []
hooks = []
+++

criteria: Founding baseline on today's harness: F001-F024 = q35/g26/lfm24 x itc/cobs/wrenfold/semver x 2, run by founding_bench.sh grouped by model (one krang load each), each result.json graded; dev-notes/beagle-0.48/founding-bench.md tabulates verdict/flags/found-seconds per run and per model x task, and names the failure classes that dominate.
decided by: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider /home/choong/tautest/itc-harness/test_founding_baseline.py
budget: 150000 tokens
