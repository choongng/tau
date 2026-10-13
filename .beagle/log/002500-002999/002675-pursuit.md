+++
id = "002675-pursuit"
ordinal = 2675
kind = "pursuit"
timestamp = "2026-10-13T06:16:00+00:00"
summary = "pursuit open T0521: audit 2026-10-12: amend the short checks (T0498 positive anchor text, T0503/T0512-T0514/T0516 full beagle CI, T0508 eval prose, T0518 open-time refusal)"
metric_command = ""
drains = []
hooks = []
+++

criteria: T0498, T0508, T0516 and T0518 are done and WITNESSED again under amended v2 checks that test their whole criteria (T0498: brief, SHAPE, pursuit.md and tau's milestone teach anchors; T0508: eval.md's Line anchors section notes R75, R77, R79 stopped; T0516: Contract and Reconcile scopes; T0518: pursuit_step's open-time refusal), the new tests on tau-wt-ops a488c0d8; T0503, T0512, T0513, T0514 and T0516 declare their beagle CI clause untested, naming T0523, a done, witnessed standing task running beagle's ci/check.sh. (Work done before this open: the audit's amends were the task.)
decided by: sh -c 'echo "efc37ce416ee7039e459349d241bb89c86848ced502ea5456d4bb7d14f1628b9  .beagle/checks/T0521/T0521.sh" | sha256sum -c --quiet && bash .beagle/checks/T0521/T0521.sh'
budget: 150000 tokens
opened over T0493, T0517: the audit's amends are the task and were done before this open, under the driver's T0521 dispatch; opening records them
