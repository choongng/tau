+++
id = "002812-pursuit"
ordinal = 2812
kind = "pursuit"
timestamp = "2026-10-13T21:37:27+00:00"
summary = "pursuit open T0548: beagle contract check: refuse an operation named as an entry id, and a statement duplicating another's (R97)"
metric_command = ""
drains = []
hooks = []
+++

criteria: beagle pursuit contract check (and so seal) refuses an entry whose operation equals an entry id of the contract, naming the entry and saying an operation is the name the code exposes; and refuses an entry whose statement is word-for-word another entry's, naming both. Tests *check_refuses_an_operation_named_as_an_entry_id and *check_refuses_a_duplicated_statement pass on an R97-shaped fixture; ci/check.sh green on rotation-fixes
decided by: sh -c 'echo "1defc5cba0c5e6bac8fffcbaad7d155ed103024d4e4cfd3b5eee15677549c911  .beagle/checks/T0548/T0548.sh" | sha256sum -c --quiet && bash .beagle/checks/T0548/T0548.sh'
budget: 120000 tokens
