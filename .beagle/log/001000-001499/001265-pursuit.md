+++
id = "001265-pursuit"
ordinal = 1265
kind = "pursuit"
timestamp = "2026-10-09T19:51:07+00:00"
summary = "pursuit prove T0294: WITNESSED — refuses when beagle.py's `if not notes or not bound or _check_problem(bou…` is put back as `if True: return None`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "991be7f859c4cad59e96f6aa734a8acedeb75b350eb0bf5188c1796c983788ba  .beagle/checks/T0294/T0294.sh" | sha256sum -c --quiet && bash .beagle/checks/T0294/T0294.sh'
refutes: refuses when beagle.py's `if not notes or not bound or _check_problem(bou…` is put back as `if True: return None` (proven 2026-10-09T19:51:06+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_open_task_rejected_done_when_already_passes_runs_notes_on_bound_che…)
refused after 3s of a 1m40s check at: FAILED tests/test_beagle_example_extension.py::test_open_task_rejected_done_when_already_passes_runs_notes_on_bound_che…
refused with: 1 failed in 2.82s
