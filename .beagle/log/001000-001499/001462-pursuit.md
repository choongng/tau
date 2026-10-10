+++
id = "001462-pursuit"
ordinal = 1462
kind = "pursuit"
timestamp = "2026-10-10T02:51:31+00:00"
summary = "pursuit open T0342: The known-answers close refuses a cases test that is a copy of the data test"
metric_command = ""
drains = []
hooks = []
+++

criteria: The known-answers close does not close done when the locked cases test imports no project module and is a near-copy of the data test; it keeps the task open, saying the cases test must import the code and compare each case's answer. The Cases-first refusal offers an existing uncommitted test that reads the cases data instead of naming a fresh file. Regression tests in tests/test_beagle_example_extension.py.
decided by: sh -c 'echo "877cc0b3ebc1596abb8cdf716ddfb5f71e641132f2c61de0b7923ef9afd94a08  .beagle/checks/T0342/T0342.sh" | sha256sum -c --quiet && bash .beagle/checks/T0342/T0342.sh'
budget: 60000 tokens
