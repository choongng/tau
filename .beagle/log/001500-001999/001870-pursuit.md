+++
id = "001870-pursuit"
ordinal = 1870
kind = "pursuit"
timestamp = "2026-10-12T00:49:36+00:00"
summary = "pursuit open T0444: R51 fix: a locked cases test no code can pass is refused at the close"
metric_command = ""
drains = []
hooks = []
+++

criteria: _cases_test_problem refuses a cases test no code can pass: two cases routed to the same call (agreeing on every case input key the test reads) that expect different answers, named with the unread keys; and an attribute both called as a method and read as a value, including a value read inside a literal or passed on. The worker brief's locked-files text says a locked test no code can pass is reported and the step ended. Tests that distinguish their cases are not refused. q35 R51. Tests named in the check; whole file passes; ruff clean.
decided by: sh -c 'echo "ca99d49d06f201087cd656b71de0e18ae834ecf58f964c52171b58f089579d4a  .beagle/checks/T0444/T0444.sh" | sha256sum -c --quiet && bash .beagle/checks/T0444/T0444.sh'
budget: 150000 tokens
