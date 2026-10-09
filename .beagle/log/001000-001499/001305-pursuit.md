+++
id = "001305-pursuit"
ordinal = 1305
kind = "pursuit"
timestamp = "2026-10-09T21:33:41+00:00"
summary = "pursuit prove T0310: WITNESSED — refuses when beagle.py's `Criteria kept from {task}; yours went into the …` is put back as `Criteria kept from {task}`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "b698edfbc5359aed63e12c35be58853b6a89448e0c136987f4ab29025765127c  .beagle/checks/T0310/T0310.sh" | sha256sum -c --quiet && bash .beagle/checks/T0310/T0310.sh'
refutes: refuses when beagle.py's `Criteria kept from {task}; yours went into the …` is put back as `Criteria kept from {task}` (proven 2026-10-09T21:33:41+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_new_route_changed_criteria_kept_and_moved_to_notes)
refused after 2s of a 2m05s check at: FAILED tests/test_beagle_example_extension.py::test_new_route_changed_criteria_kept_and_moved_to_notes
refused with: 1 failed in 1.25s
