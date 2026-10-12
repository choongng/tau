+++
id = "002463-pursuit"
ordinal = 2463
kind = "pursuit"
timestamp = "2026-10-12T16:11:07+00:00"
summary = "pursuit open T0481: beagle: contract seal, status, run, and the order and drift gates"
metric_command = ""
drains = []
hooks = []
+++

criteria: beagle (branch contract-first): 'contract seal' refuses a contract whose full check fails, else writes .beagle/contract-seal.json (sha256 per sealed file); 'contract status [--json]' (no bare form) says none, draft, ready, sealed or altered with counts, assumptions and altered paths; 'contract run' runs acceptance under [run] contain with its exit code (3 if none declared). Order gate: declared and unsealed, open refuses a task whose scope is empty or outside the sealed paths and references/, unless --before-contract "<why>", kept on the task. Drift gate: sealed, a done close of non-contract work is refused while a sealed file differs from its seal. A check may run contract check|status|diff|run, not seal. 9 named tests in tests/test_contract.py; the file passes.
decided by: sh -c 'echo "ec15a3634a13bc3c579fffd90997d29a99b3cae837f8a1eca46562092226955f  .beagle/checks/T0481/T0481.sh" | sha256sum -c --quiet && bash .beagle/checks/T0481/T0481.sh'
budget: 400000 tokens
