+++
id = "000267-pursuit"
ordinal = 267
kind = "pursuit"
timestamp = "2026-10-03T19:57:41+00:00"
summary = "pursuit open T0076: T0060 follow-up: session wiring and line-prefix tests"
metric_command = ""
drains = []
hooks = []
+++

criteria: A test drives an offset read through CodingSession and asserts the outline carries file line numbers; a test feeds prefixed read text to the outline (both landed in T0070's commit 779903b).
decided by: sh -c 'echo "046fa8749ef5e333f87f5a872ea0ebc2a83338eed1a46f70e111fb0c39a47889  .beagle/checks/T0076/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0076/check.sh'
budget: 5000 tokens
