+++
id = "000860-pursuit"
ordinal = 860
kind = "pursuit"
timestamp = "2026-10-05T02:39:23+00:00"
summary = "pursuit open T0218: Fetched reference HTML keeps table cells apart and drops navigation"
metric_command = ""
drains = []
hooks = []
+++

criteria: The reference fetch's HTML-to-text keeps adjacent table cells apart and puts each row on its own line, so cell values cannot run together; page chrome (nav, header, footer, aside, script, style) is left out of the text; ordinary paragraphs read as before.
decided by: sh -c 'echo "61f3eeb29b4d7206bbcb4db92493a330f2842b41d706b61c5e9a75e97ee324a8  .beagle/checks/T0218/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0218/check.sh'
budget: 50000 tokens
