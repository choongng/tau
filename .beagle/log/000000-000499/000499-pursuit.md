+++
id = "000499-pursuit"
ordinal = 499
kind = "pursuit"
timestamp = "2026-10-04T03:56:42+00:00"
summary = "pursuit prove T0124: WITNESSED — refuses when beagle.py's `because = f\"satisfied by {done}'s commit {sha[:…` is put back as `return \"pursuit_step: not closed\"`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "5d6665d9fb6724c7ae92d03f832b5721e8c5d069a3f722bb0ec55c7f6cda1fdb  .beagle/checks/T0124/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0124/check.sh'
refutes: refuses when beagle.py's `because = f"satisfied by {done}'s commit {sha[:…` is put back as `return "pursuit_step: not closed"` (proven 2026-10-04T03:55:54+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_part_whose_check_passes_on_a_done_tasks_commit_closes_done_by_it)
refused after 1s of a 32s check at: FAILED tests/test_beagle_example_extension.py::test_part_whose_check_passes_on_a_done_tasks_commit_closes_done_by_it
refused with: 1 failed in 0.71s
