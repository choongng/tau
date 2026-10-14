+++
id = "002868-pursuit"
ordinal = 2868
kind = "pursuit"
timestamp = "2026-10-14T00:32:12+00:00"
summary = "pursuit open T0558: beagle docs: pursuit.md 1.5 and per-slice briefs"
metric_command = ""
drains = []
hooks = []
+++

criteria: As incremental-contract.md build task 5 says: pursuit.md §1.5 is the incremental flow (gather, examples slice, work, later slices sealed just ahead of the work, stand-ins, re-reads on evidence, coverage) with no second extraction or Reconcile; the ethos table has a row whose yield is sealing late, kept honest by append-only, stand-ins and coverage; the contract brief's inventory is given per slice kind (examples; one operation's limits and invalid inputs; properties; re-read; coverage). test_brief_slice_inventory_by_kind passes and ci/check.sh, with its markdown gate, is green.
decided by: sh -c 'echo "6401105ad360796b48c045d76c7565c2ddd97ef7b32210d0061c7b4c91bf3cbb  .beagle/checks/T0558/T0558.sh" | sha256sum -c --quiet && bash .beagle/checks/T0558/T0558.sh'
budget: 200000 tokens
