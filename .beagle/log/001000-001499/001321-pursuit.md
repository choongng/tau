+++
id = "001321-pursuit"
ordinal = 1321
kind = "pursuit"
timestamp = "2026-10-09T21:59:15+00:00"
summary = "pursuit open T0315: R36 fix: worker-report markup check knows the <|tool_call>, <tool_call|> and <|channel> forms"
metric_command = ""
drains = []
hooks = []
+++

criteria: beagle.py's _TOOL_CALL_MARKUP matches the pipe-delimited template forms <|tool_call>, <tool_call|>, <|channel> and <channel|> as well as <tool_call> and <function=, so _report_before_markup cuts a worker report at the first of them (R36 W1's tail as fixture), and every other user of _TOOL_CALL_MARKUP sees the same forms. Ordinary angle-bracket text is not matched (negative case in the test). Token syntax only, no model names.
decided by: sh -c 'echo "cd7882e7037a4ff4b18078367b9de78ab1964a9ec2682003f442abb9d637ce61  .beagle/checks/T0315/T0315.sh" | sha256sum -c --quiet && bash .beagle/checks/T0315/T0315.sh'
budget: 60000 tokens
