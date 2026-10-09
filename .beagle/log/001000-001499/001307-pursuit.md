+++
id = "001307-pursuit"
ordinal = 1307
kind = "pursuit"
timestamp = "2026-10-09T21:39:35+00:00"
summary = "pursuit prove T0311: WITNESSED — refuses when beagle.py's `if demand: return _judge_escalation(task, count…` is put back as `if False: return _judge_escalation(task, count,…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "02a0d9ac999ebb0ad1b44c6386eb55ea602551057474734afeb5759b97b770b5  .beagle/checks/T0311/T0311.sh" | sha256sum -c --quiet && bash .beagle/checks/T0311/T0311.sh'
refutes: refuses when beagle.py's `if demand: return _judge_escalation(task, count…` is put back as `if False: return _judge_escalation(task, count,…` (proven 2026-10-09T21:39:35+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_not_done_escalation_offers_notes_rerun_when_only_close_kept_
refused after 3s of a 1m41s check at: FAILED tests/test_beagle_example_extension.py::test_not_done_escalation_offers_notes_rerun_when_only_close_kept_open
refused with: 1 failed in 2.46s
