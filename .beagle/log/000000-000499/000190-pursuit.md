+++
id = "000190-pursuit"
ordinal = 190
kind = "pursuit"
timestamp = "2026-10-03T18:20:02+00:00"
summary = "pursuit prove T0057: WITNESSED — refuses when beagle.py's `if task not in (named, str(heirs.get(named) or …` is put back as `if task != named:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "bb4f181212580737f46459271a20d3a5346691ba4d7890be3c67b28105791b57  .beagle/checks/T0057/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0057/check.sh'
refutes: refuses when beagle.py's `if task not in (named, str(heirs.get(named) or …` is put back as `if task != named:` (proven 2026-10-03T18:19:39+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_abandon_releases_a_wait_routed_through_its_heir)
refused after 1s of a 1s check at: FAILED tests/test_beagle_example_extension.py::test_abandon_releases_a_wait_routed_through_its_heir
refused with: 1 failed, 1 passed, 252 deselected in 0.86s
