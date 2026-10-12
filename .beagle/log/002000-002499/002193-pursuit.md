+++
id = "002193-pursuit"
ordinal = 2193
kind = "pursuit"
timestamp = "2026-10-12T09:43:41+00:00"
summary = "pursuit open T0461: A raw report with closing tool-call tags gets the no-report stub (R55)"
metric_command = ""
drains = []
hooks = []
+++

criteria: A raw report in core's closing tool-call form, or a bare tag opening on a parameter, gets the no-report stub (R55). Named test test_raw_report_with_closing_tool_call_tags_gets_the_stub passes; suite and ruff pass.
decided by: sh -c 'echo "4a5b81b5262e7677b2c7d011e04a47f61679fdd949961d499104755bd0d6831e  .beagle/checks/T0461/T0461.sh" | sha256sum -c --quiet && bash .beagle/checks/T0461/T0461.sh'
budget: 150000 tokens
