+++
id = "000584-pursuit"
ordinal = 584
kind = "pursuit"
timestamp = "2026-10-04T08:42:00+00:00"
summary = "pursuit prove T0140: WITNESSED — refuses when beagle.py's `and \" \".join(done_when.split()) == data_route[2]` is put back as `and False`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "480c5858eb7ca098c4cfa12aa008e0dc241541f66d70fdb0271a285f3b19a4a1  .beagle/checks/T0140/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0140/check.sh'
refutes: refuses when beagle.py's `and " ".join(done_when.split()) == data_route[2]` is put back as `and False` (proven 2026-10-04T08:41:24+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_escalation_takes_its_proposed_data_test_done_when_as_new_route)
refused after 2s of a 50s check at: FAILED tests/test_beagle_example_extension.py::test_escalation_takes_its_proposed_data_test_done_when_as_new_route
refused with: 1 failed, 3 passed in 2.18s
