+++
id = "001000-pursuit"
ordinal = 1000
kind = "pursuit"
timestamp = "2026-10-05T08:15:47+00:00"
summary = "pursuit prove T0240: WITNESSED — refuses when beagle.py's `\"pursuit here yet. The pursuit begins with purs…` is put back as `\"pursuit here yet. The pursuit begins with purs…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "cb08e94c696e482bed0d90c69d49cb1527fd1af3a639a6472866c0c554b27872  .beagle/checks/T0240/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0240/check.sh'
refutes: refuses when beagle.py's `"pursuit here yet. The pursuit begins with purs…` is put back as `"pursuit here yet. The pursuit begins with purs…` (proven 2026-10-05T08:15:37+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_dot_beagle_write_before_founding_names_pursuit_found)
refused after 1s of a 1m18s check at: FAILED tests/test_beagle_example_extension.py::test_dot_beagle_write_before_founding_names_pursuit_found
refused with: 1 failed in 0.56s
