+++
id = "000756-pursuit"
ordinal = 756
kind = "pursuit"
timestamp = "2026-10-04T17:04:38+00:00"
summary = "pursuit prove T0175: WITNESSED — refuses when beagle.py's `return _read_or_design_only(head) and _read_or_…` is put back as `return _read_or_design_only(bare) or \"docs\" in …`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "9febfcaae5d738364c7ae50f35691eb3daf49e60c6223cbe9780f01d066c76a5  .beagle/checks/T0175/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0175/check.sh'
refutes: refuses when beagle.py's `return _read_or_design_only(head) and _read_or_…` is put back as `return _read_or_design_only(bare) or "docs" in …` (proven 2026-10-04T17:04:13+00:00; predates the task: the task's change is only tests, and one of them refused; refused at FAILED tests/test_beagle_example_ex
refused after 2s of a 1m02s check at: FAILED tests/test_beagle_example_extension.py::test_design_fold_keeps_r17_docs_milestone_beside_known_answers
refused with: 1 failed in 1.39s
