+++
id = "002382-pursuit"
ordinal = 2382
kind = "pursuit"
timestamp = "2026-10-12T14:22:10+00:00"
summary = "pursuit prove T0466: WITNESSED — refuses when beagle.py's `passed_on_disk = (pre_rc, pre_out)` is put back as `` and beagle.py's `_NOT_DONE_DEMAND.pop((str(root), task), None) k…` is put back as `kept`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "01deccfed4f7f7fdf105ba23ad0d3290903958edc6ffe73db9e9ab8e54241cb9  .beagle/checks/T0466/T0466.sh" | sha256sum -c --quiet && bash .beagle/checks/T0466/T0466.sh'
refutes: refuses when beagle.py's `passed_on_disk = (pre_rc, pre_out)` is put back as `` and beagle.py's `_NOT_DONE_DEMAND.pop((str(root), task), None) k…` is put back as `kept` (proven 2026-10-12T14:22:09+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_amended_check_passing_on_disk_bri
refused after 4s of a 2m40s check at: FAILED tests/test_beagle_example_extension.py::test_amended_check_passing_on_disk_briefs_witness_note_not_old_demand
refused with: 1 failed, 815 deselected in 3.26s
