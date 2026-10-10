+++
id = "001440-pursuit"
ordinal = 1440
kind = "pursuit"
timestamp = "2026-10-10T02:34:25+00:00"
summary = "pursuit open T0340: A hanging check shows as exit 124 with its log, not a 120 s bash timeout"
metric_command = ""
drains = []
hooks = []
+++

criteria: The bound beagle's brief puts on a worker's own command is below the worker's bash timeout, so a hanging check ends with exit 124 and its log rather than the bash tool's own timeout; the habit line and the retry note after a check that timed out say exit 124 means the command did not finish and to look for a loop that never advances. Regression tests in tests/test_beagle_example_extension.py.
decided by: sh -c 'echo "4c5a0cf30925f1f7bbb22f16c881575ace49809669fe9949c621b39f6bc040e7  .beagle/checks/T0340/T0340.sh" | sha256sum -c --quiet && bash .beagle/checks/T0340/T0340.sh'
budget: 50000 tokens
