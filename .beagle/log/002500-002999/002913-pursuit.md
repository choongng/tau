+++
id = "002913-pursuit"
ordinal = 2913
kind = "pursuit"
timestamp = "2026-10-14T01:55:46+00:00"
summary = "pursuit open T0563: beagle: R71/R73 real contracts as slice fixtures in beagle's tests"
metric_command = ""
drains = []
hooks = []
+++

criteria: R71's and R73's references and contracts from .beagle/checks/T0498/{r71,r73} are ported to beagle tests/r71_itc and tests/r73_itc as sealed slices (contract/slices/NN-*) in the current layout; tests real_contract_slices_check_clean (each passes contract check), real_contract_anchor_drift_refused (an edited source line refuses its citing entry) and real_contract_coverage_counts (contract coverage reports a fixed count, pinned) pass; ci/check.sh green.
decided by: sh -c 'echo "71727a163ac14d7b51c46cf385a682c968a721a5d225840ac823c3042c8fd100  .beagle/checks/T0563/T0563.sh" | sha256sum -c --quiet && bash .beagle/checks/T0563/T0563.sh'
budget: 120000 tokens
opened over T0565: inside the incremental-contract build the owner paused runs for; T0565 is check upkeep outside it
