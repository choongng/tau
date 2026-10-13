+++
id = "002658-pursuit"
ordinal = 2658
kind = "pursuit"
timestamp = "2026-10-13T06:07:04+00:00"
summary = "pursuit prove T0516: WITNESSED — refuses when beagle.py's `scope, done_when = list(fixed[0]), fixed[1]` is put back as `scope, done_when = scope, done_when`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "9e2d4cc3bef4cc449025e9525ef933e1ef2ab392a91839d135df5838753248ec  .beagle/checks/T0516/T0516.v2.sh" | sha256sum -c --quiet && bash .beagle/checks/T0516/T0516.v2.sh'
refutes: refuses when beagle.py's `scope, done_when = list(fixed[0]), fixed[1]` is put back as `scope, done_when = scope, done_when` (proven 2026-10-13T06:07:04+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_pursuit_step_scopes_the_contract_and_reconcile_itself[Contract-beag…)
refused after 7s of a 7s check at: FAILED tests/test_beagle_example_extension.py::test_pursuit_step_scopes_the_contract_and_reconcile_itself[Contract-beag…
refused with: 2 failed, 847 deselected in 2.48s
