+++
id = "002505-pursuit"
ordinal = 2505
kind = "pursuit"
timestamp = "2026-10-12T17:02:14+00:00"
summary = "pursuit open T0488: tau ext: founding seeds the contract and points criteria at it"
metric_command = ""
drains = []
hooks = []
+++

criteria: pursuit_found writes beagle's [contract] table (path contract/contract.json, second contract/contract.second.json, acceptance 'sh contract/accept.sh', files ['contract/']) into pursuit.toml, adds the contract criterion (shown in the read-back), and splits the root --ordered into Contract, Second extraction, then the driver's milestones; a milestone that names the known answers is dropped (with a note), read/design-only ones fold into the work; the founding result and the load-time prompt carry CONTRACT_FIRST_NOTE (with DRIVER_STEERS_NOTE), not CASES_FIRST_NOTE. Both named tests pass, the whole extension suite passes, ruff check and format are clean.
decided by: sh -c 'echo "363f2aa59eb8137437eade1709ccd9e46d1c7b0dd71be744bb5d20482001f415  .beagle/checks/T0488/T0488.sh" | sha256sum -c --quiet && bash .beagle/checks/T0488/T0488.sh'
budget: 80000 tokens
