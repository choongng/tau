+++
id = "002657-pursuit"
ordinal = 2657
kind = "pursuit"
timestamp = "2026-10-13T06:06:42+00:00"
summary = "pursuit amend T0516"
metric_command = ""
drains = []
hooks = []
+++

audit 2026-10-12 (T0521): the check tested only the Second extraction's forced scope, though the criteria say pursuit_step gives each of Contract, Second extraction and Reconcile its scope and check. The new check adds test_pursuit_step_scopes_the_contract_and_reconcile_itself (tau-wt-ops a488c0d8), run on that worktree; the full-suite clause is declared untested, with beagle CI moved to T0523.
was: sh -c 'echo "01a3a078eee3e10c686fa1b08ed5226b035e3196832872578dcd71033b83fe8a  .beagle/checks/T0516/T0516.sh" | sha256sum -c --quiet && bash .beagle/checks/T0516/T0516.sh'
  01a3a078eee3e10c686fa1b08ed5226b035e3196832872578dcd71033b83fe8a  .beagle/checks/T0516/T0516.sh
now: sh -c 'echo "9e2d4cc3bef4cc449025e9525ef933e1ef2ab392a91839d135df5838753248ec  .beagle/checks/T0516/T0516.v2.sh" | sha256sum -c --quiet && bash .beagle/checks/T0516/T0516.v2.sh'
