+++
id = "001428-pursuit"
ordinal = 1428
kind = "pursuit"
timestamp = "2026-10-10T02:28:06+00:00"
summary = "pursuit prove T0054: WITNESSED — refuses when test_beagle_example_extension.py's `def test_found_drops_setup_milestone_and_says_so` is put back as `def test_founding_refuses_when_every_milestone_…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "56c27810037d2d5e6fb95051e1a532a1ae1ce18562d1277ca8ccbe004623244a  .beagle/checks/T0054/T0054.sh" | sha256sum -c --quiet && bash .beagle/checks/T0054/T0054.sh'
refutes: refuses when test_beagle_example_extension.py's `def test_found_drops_setup_milestone_and_says_so` is put back as `def test_founding_refuses_when_every_milestone_…` (proven 2026-10-10T02:28:06+00:00; refused at ERROR tests/test_beagle_example_extension.py)
refused after 3s of a 3s check at: ERROR tests/test_beagle_example_extension.py
refused with: 1 error in 1.98s
