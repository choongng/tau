+++
id = "000888-pursuit"
ordinal = 888
kind = "pursuit"
timestamp = "2026-10-05T04:26:55+00:00"
summary = "pursuit prove T0223: WITNESSED — refuses when beagle.py's `f\"{task} is worked on this call's scope {json.d…` is put back as `f\"{task} works on its scope {json.dumps(scope)}…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "eb07158d64a2cf1e42ca94350517657b03a606315b4cd72f6fec0026e7388f2e  .beagle/checks/T0223/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0223/check.sh'
refutes: refuses when beagle.py's `f"{task} is worked on this call's scope {json.d…` is put back as `f"{task} works on its scope {json.dumps(scope)}…` (proven 2026-10-05T04:26:50+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_step_with_same_done_when_names_the_scope_it_kept)
refused after 1s of a 1m22s check at: FAILED tests/test_beagle_example_extension.py::test_step_with_same_done_when_names_the_scope_it_kept
refused with: 1 failed in 0.82s
