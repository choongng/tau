+++
id = "002408-pursuit"
ordinal = 2408
kind = "pursuit"
timestamp = "2026-10-12T14:48:31+00:00"
summary = "pursuit prove T0471: WITNESSED — refuses when beagle.py's `ranked = _RANKED_BELOW.search(opened) if rc != …` is put back as `ranked = None`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "e877cc6537ede3e29b748757707fc5ec8d7993a33c374b15278e93ae544b2280  .beagle/checks/T0471/T0471.sh" | sha256sum -c --quiet && bash .beagle/checks/T0471/T0471.sh'
refutes: refuses when beagle.py's `ranked = _RANKED_BELOW.search(opened) if rc != …` is put back as `ranked = None` (proven 2026-10-12T14:48:30+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_rank_refusal_of_a_step_open_offers_no_flag_the_driver_cannot_pass)
refused after 4s of a 2m40s check at: FAILED tests/test_beagle_example_extension.py::test_rank_refusal_of_a_step_open_offers_no_flag_the_driver_cannot_pass
refused with: 1 failed, 819 deselected in 3.43s
