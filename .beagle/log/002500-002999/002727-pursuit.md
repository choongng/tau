+++
id = "002727-pursuit"
ordinal = 2727
kind = "pursuit"
timestamp = "2026-10-13T19:25:34+00:00"
summary = "pursuit open T0536: beagle: contract seal refuses an acceptance that passes with no project code"
metric_command = ""
drains = []
hooks = []
+++

criteria: beagle 'pursuit contract seal' runs the acceptance once in a scratch copy holding only the contract directory and references/ (no project code) and refuses to seal while any entry passes there, naming those entries and why (an entry that passes with no code does not test the code; e.g. an invalid entry whose expected error is the ImportError). Tests test_seal_refuses_an_acceptance_that_passes_with_no_code and test_seal_accepts_an_acceptance_that_fails_every_entry_with_no_code pass; ci/check.sh green on branch rotation-fixes.
decided by: sh -c 'echo "539b160a87933bb6093834aa6ac8f7807b574a9ce4f88478ad0f6dda26a276ef  .beagle/checks/T0536/T0536.sh" | sha256sum -c --quiet && bash .beagle/checks/T0536/T0536.sh'
budget: 150000 tokens
