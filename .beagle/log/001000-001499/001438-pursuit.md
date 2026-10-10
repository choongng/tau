+++
id = "001438-pursuit"
ordinal = 1438
kind = "pursuit"
timestamp = "2026-10-10T02:34:03+00:00"
summary = "pursuit open T0339: A tool call missing a required string argument says it is missing"
metric_command = ""
drains = []
hooks = []
+++

criteria: A tool call that lacks a required string argument (e.g. write/edit without path) raises ToolInputError naming the argument as missing and listing the keys the call carried; a present non-string value still says 'must be a string'; nothing runs. Regression tests in tests/test_tool_missing_argument.py.
decided by: sh -c 'echo "ed21da1d870abaa734360a977d78831164ce93cd6918ead698eec9b9bc7344de  .beagle/checks/T0339/T0339.sh" | sha256sum -c --quiet && bash .beagle/checks/T0339/T0339.sh'
budget: 15000 tokens
