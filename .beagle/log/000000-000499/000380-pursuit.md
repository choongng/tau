+++
id = "000380-pursuit"
ordinal = 380
kind = "pursuit"
timestamp = "2026-10-03T21:21:02+00:00"
summary = "pursuit prove T0087: WITNESSED — refuses when beagle.py's `_implementation_in_tests_lead(root, scope) + f\"…` is put back as `\"\" + f\"{route}{undid}{task} — {title}: the chec…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "994302d18896d2522429f640f63685a213d53d9145ce56b2051b4f35c6c10e6d  .beagle/checks/T0087/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0087/check.sh'
refutes: refuses when beagle.py's `_implementation_in_tests_lead(root, scope) + f"…` is put back as `"" + f"{route}{undid}{task} — {title}: the chec…` (proven 2026-10-03T21:20:17+00:00; predates the task: T0087 adds tests only: the audit found T0068's lead untested on this branch, so the witness puts back an
refused after 1s of a 1s check at: FAILED tests/test_beagle_example_extension.py::test_prove_refused_step_names_implementation_written_under_tests
refused with: 1 failed, 2 passed, 298 deselected in 0.88s
