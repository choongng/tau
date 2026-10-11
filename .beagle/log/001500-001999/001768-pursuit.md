+++
id = "001768-pursuit"
ordinal = 1768
kind = "pursuit"
timestamp = "2026-10-11T02:29:16+00:00"
summary = "pursuit prove T0409: WITNESSED — refuses when beagle.py's `refused = await passing_refused(f\"python3 -m py…` is put back as `refused = None`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "7082ebfea49d44786be383021bc866bc74327688fb25cc2089d790f7c1ab6968  .beagle/checks/T0409/T0409.sh" | sha256sum -c --quiet && bash .beagle/checks/T0409/T0409.sh'
refutes: refuses when beagle.py's `refused = await passing_refused(f"python3 -m py…` is put back as `refused = None` (proven 2026-10-11T02:29:15+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_locked_test_offer_does_not_name_a_locked_test_that_already_passes)
refused after 5s of a 2m35s check at: FAILED tests/test_beagle_example_extension.py::test_locked_test_offer_does_not_name_a_locked_test_that_already_passes
refused with: 1 failed, 2 passed, 746 deselected in 4.63s
