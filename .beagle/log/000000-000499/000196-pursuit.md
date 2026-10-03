+++
id = "000196-pursuit"
ordinal = 196
kind = "pursuit"
timestamp = "2026-10-03T18:23:55+00:00"
summary = "pursuit prove T0058: WITNESSED — refuses when beagle.py's `if container and container not in roots:` is put back as `if False:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "6d864dcf508333c64e09a2d752c4c66a5ffa934144acc2e8472c74f0d3570a72  .beagle/checks/T0058/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0058/check.sh'
refutes: refuses when beagle.py's `if container and container not in roots:` is put back as `if False:` (proven 2026-10-03T18:23:32+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_duplicate_abandon_of_a_part_is_refused_because_it_stalls_its_contai…)
refused after 1s of a 1s check at: FAILED tests/test_beagle_example_extension.py::test_duplicate_abandon_of_a_part_is_refused_because_it_stalls_its_contai…
refused with: 1 failed, 254 deselected in 0.58s
