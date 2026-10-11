+++
id = "001754-pursuit"
ordinal = 1754
kind = "pursuit"
timestamp = "2026-10-11T01:55:26+00:00"
summary = "pursuit prove T0406: WITNESSED — refuses when beagle.py's `if done_by and unwitnessed:` is put back as `if done_by and unwitnessed and False:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "72d7d223fd3177f9de395b8568898ac45b86e6291179021fd22f7ae2fcdcb801  .beagle/checks/T0406/T0406.sh" | sha256sum -c --quiet && bash .beagle/checks/T0406/T0406.sh'
refutes: refuses when beagle.py's `if done_by and unwitnessed:` is put back as `if done_by and unwitnessed and False:` (proven 2026-10-11T01:55:26+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_already_passes_offers_no_done_by_that_needs_a_witness_it_lacks)
refused after 6s of a 2m37s check at: FAILED tests/test_beagle_example_extension.py::test_already_passes_offers_no_done_by_that_needs_a_witness_it_lacks
refused with: 2 failed, 1 passed, 738 deselected in 5.18s
