+++
id = "001834-pursuit"
ordinal = 1834
kind = "pursuit"
timestamp = "2026-10-11T23:00:14+00:00"
summary = "pursuit prove T0439: WITNESSED — refuses when beagle.py's `f\"That close seals {parent}: {task} would end u…` is put back as `f\"That close: {task} would end undone`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "b9b6218813da7a28fa2a0a8530a9a6c092a746dfc915382164393010bffb5abb  .beagle/checks/T0439/T0439.sh" | sha256sum -c --quiet && bash .beagle/checks/T0439/T0439.sh'
refutes: refuses when beagle.py's `f"That close seals {parent}: {task} would end u…` is put back as `f"That close: {task} would end undone` (proven 2026-10-11T23:00:13+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_infeasible_offer_warns_it_would_seal_the_parent)
refused after 8s of a 3m24s check at: FAILED tests/test_beagle_example_extension.py::test_infeasible_offer_warns_it_would_seal_the_parent
refused with: 1 failed, 2 passed, 763 deselected in 6.67s
