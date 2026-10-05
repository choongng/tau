+++
id = "001098-pursuit"
ordinal = 1098
kind = "pursuit"
timestamp = "2026-10-05T13:28:56+00:00"
summary = "pursuit open T0265: Worker test commands bounded below the worker cap; cases test must compare answers"
metric_command = ""
drains = []
hooks = []
+++

criteria: A worker's own test/check commands run under a memory bound below the worker's own cap (and a timeout below the worker's), so a runaway command dies alone and the worker can report it; when a worker's run ended on the cap with a tool call pending, the step result names the kill and the command instead of 'ended without a report'; _cases_test_problem refuses a cases test whose answers key never reaches an assert or comparison.
decided by: sh -c 'echo "f87bcb586fbcc5c6f17d8bf23b3b6eae003cc1a7cb6b92b4f0cef9e8d245f16a  .beagle/checks/T0265/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0265/check.sh'
budget: 80000 tokens
