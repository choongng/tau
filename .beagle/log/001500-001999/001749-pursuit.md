+++
id = "001749-pursuit"
ordinal = 1749
kind = "pursuit"
timestamp = "2026-10-11T01:45:34+00:00"
summary = "pursuit prove T0405: WITNESSED — refuses when beagle.py's `\"close\": \"pursuit_step, which closes a task on …` is put back as `\"close\": \"pursuit_step, which closes a task on …`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "0b8343793aecdea0785198f098d6c5f1e0b4ec19d00a0e57bdb7822994031234  .beagle/checks/T0405/T0405.sh" | sha256sum -c --quiet && bash .beagle/checks/T0405/T0405.sh'
refutes: refuses when beagle.py's `"close": "pursuit_step, which closes a task on …` is put back as `"close": "pursuit_step, which closes a task on …` (proven 2026-10-11T01:45:34+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_bash_close_steer_on_a_milestone_offers_no_abandon)
refused after 4s of a 2m12s check at: FAILED tests/test_beagle_example_extension.py::test_bash_close_steer_on_a_milestone_offers_no_abandon
refused with: 2 failed, 1 passed, 735 deselected in 3.24s
