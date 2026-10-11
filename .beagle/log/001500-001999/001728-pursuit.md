+++
id = "001728-pursuit"
ordinal = 1728
kind = "pursuit"
timestamp = "2026-10-11T00:40:59+00:00"
summary = "pursuit open T0398: Detect the other bug and opportunity indicators"
metric_command = ""
drains = []
hooks = []
+++

criteria: itc-harness/mine/indicators.py (--events --refused --kinds --out) writes indicators.json: time (per run: wall, driver model/tool minutes, worker model/tool minutes), sinks (the longest single tool calls, by seconds, with run/role/tool/line and args head), workers (each worker session once, an outcome such as reported/capped/breaker/length/provider_error/no_report, with evidence), stops (every stop other than toolUse/stop, with stop_by and the refused streak before it), driver_work (driver write/edit calls and driver bash calls that write files or run tests: the driver doing a worker's job), recovery (per driver refusal kind, how many were followed by a successful pursuit_* result on the same task before the session ended, and how many were not). Tests in mine/test_indicators.py; ruff clean.
decided by: sh -c 'echo "806bfd099655b93325fe4e723e4b84950ac88d1526edb9099c12456810b6f607  .beagle/checks/T0398/T0398.sh" | sha256sum -c --quiet && bash .beagle/checks/T0398/T0398.sh'
budget: 140000 tokens
