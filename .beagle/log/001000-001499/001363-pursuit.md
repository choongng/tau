+++
id = "001363-pursuit"
ordinal = 1363
kind = "pursuit"
timestamp = "2026-10-09T23:14:25+00:00"
summary = "pursuit open T0323: R37 class 2: the unsourced-case verdict points at the reference lines holding each case's values"
metric_command = ""
drains = []
hooks = []
+++

criteria: The unsourced-case verdict, for each flagged case it names (up to the three it lists), names the reference line holding the case's input values (as a run of tokens, in any form the value matchers read: hex bytes, decimals or the string) and the line after it, quoted, with file:line, and tells the worker to copy one of those lines as the source; when no reference line holds the values, it says so for that case.
decided by: sh -c 'echo "016bdf7be03afa22ccab36a2e487a870ba6c0f221effbd0ef2ffd920ee5ffa21  .beagle/checks/T0323/T0323.sh" | sha256sum -c --quiet && bash .beagle/checks/T0323/T0323.sh'
budget: 100000 tokens
