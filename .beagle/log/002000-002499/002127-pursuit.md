+++
id = "002127-pursuit"
ordinal = 2127
kind = "pursuit"
timestamp = "2026-10-12T09:14:10+00:00"
summary = "pursuit prove T0455: WITNESSED — refuses when beagle.py's `if names & imported:` is put back as `if False:` and beagle.py's `and task in _founding_milestones(nodes)` is put back as `and False` and beagle.py's `tail = cut.split(\"\\n\", 1)[1] if len(cut) < len(…` is put back as `tail = cut`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "8902c1571bc566df43f23a4835c938660c884d7493b4414d4d63fc3be3a4ec2f  .beagle/checks/T0455/T0455.sh" | sha256sum -c --quiet && bash .beagle/checks/T0455/T0455.sh'
refutes: refuses when beagle.py's `if names & imported:` is put back as `if False:` and beagle.py's `and task in _founding_milestones(nodes)` is put back as `and False` and beagle.py's `tail = cut.split("\n", 1)[1] if len(cut) < len(…` is put back as `tail = cut` (proven 2026-10-12T09:14:09+00:00; refused at
refused after 4s of a 2m45s check at: FAILED tests/test_beagle_example_extension.py::test_already_passes_offers_no_done_by_whose_only_witness_is_an_imported_…
refused with: 3 failed, 800 deselected in 3.60s
