+++
id = "002116-pursuit"
ordinal = 2116
kind = "pursuit"
timestamp = "2026-10-12T09:04:09+00:00"
summary = "pursuit open T0453: Done-by refusal of a scope-less call points back to the offered scope, not to a new check (R53)"
metric_command = ""
drains = []
hooks = []
+++

criteria: A scope-less done-by refusal offers back the committed source its check's targets miss (R53). Named test test_done_by_without_scope_offers_the_committed_source_the_check_targets_miss passes, full beagle test file passes, ruff clean.
decided by: sh -c 'echo "e1fc03f2bf5e934160c900afff5fdc294d5db9e6b80cad29477d9c9c3f0a8d51  .beagle/checks/T0453/T0453.sh" | sha256sum -c --quiet && bash .beagle/checks/T0453/T0453.sh'
budget: 150000 tokens
