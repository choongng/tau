+++
id = "001514-pursuit"
ordinal = 1514
kind = "pursuit"
timestamp = "2026-10-10T04:30:03+00:00"
summary = "pursuit prove T0348: WITNESSED — refuses when beagle.py's `rerun=rerun, split=False)` is put back as `rerun=rerun, split=True)`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "eaec5c476a305e694e39e588d6e170899bceaa5a5bffb1c9ae8de54b740b0618  .beagle/checks/T0348/T0348.sh" | sha256sum -c --quiet && bash .beagle/checks/T0348/T0348.sh'
refutes: refuses when beagle.py's `rerun=rerun, split=False)` is put back as `rerun=rerun, split=True)` (proven 2026-10-10T04:30:03+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_judge_only_escalation_offers_no_split)
refused after 1s of a 1m47s check at: FAILED tests/test_beagle_example_extension.py::test_judge_only_escalation_offers_no_split
refused with: 1 failed, 1 passed, 680 deselected in 1.04s
