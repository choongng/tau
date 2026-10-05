+++
id = "000934-pursuit"
ordinal = 934
kind = "pursuit"
timestamp = "2026-10-05T06:35:44+00:00"
summary = "pursuit prove T0232: WITNESSED — refuses when beagle.py's `f\"You have {cap} tool calls in all. Write the f…` is put back as `f\"Write the files early, \"`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "422298ae662f3972f4a39ddbaee21d88b7fa40d2b99a92ad91b228c62e426d21  .beagle/checks/T0232/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0232/check.sh'
refutes: refuses when beagle.py's `f"You have {cap} tool calls in all. Write the f…` is put back as `f"Write the files early, "` (proven 2026-10-05T06:35:32+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_brief_states_worker_turn_cap)
refused after 2s of a 1m16s check at: FAILED tests/test_beagle_example_extension.py::test_brief_states_worker_turn_cap
refused with: 1 failed in 1.92s
