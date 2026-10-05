+++
id = "000975-pursuit"
ordinal = 975
kind = "pursuit"
timestamp = "2026-10-05T07:58:26+00:00"
summary = "pursuit prove T0239: WITNESSED — refuses when beagle.py's `return bool(nodes) and len(_retry_chain(task, n…` is put back as `return False`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "79d1b9e1609416c09dc3d8e019658e6229a5e03c5741d44f4052fa24e203b4dc  .beagle/checks/T0239/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0239/check.sh'
refutes: refuses when beagle.py's `return bool(nodes) and len(_retry_chain(task, n…` is put back as `return False` (proven 2026-10-05T07:58:17+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_unproven_call_at_spawn_limit_offers_no_new_route)
refused after 2s of a 1m18s check at: FAILED tests/test_beagle_example_extension.py::test_unproven_call_at_spawn_limit_offers_no_new_route
refused with: 1 failed in 1.99s
