+++
id = "000847-pursuit"
ordinal = 847
kind = "pursuit"
timestamp = "2026-10-05T02:19:04+00:00"
summary = "pursuit prove T0215: WITNESSED — refuses when beagle.py's `if not text or not Path(text).expanduser().is_a…` is put back as `if True:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "900d6a72355d3dd0e3a058235c8cfd7db86416fe7c68a8289e9764153b947b13  .beagle/checks/T0215/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0215/check.sh'
refutes: refuses when beagle.py's `if not text or not Path(text).expanduser().is_a…` is put back as `if True:` (proven 2026-10-05T02:18:44+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_absolute_scope_under_root_is_matched_root_relative)
refused after 2s of a 1m08s check at: FAILED tests/test_beagle_example_extension.py::test_absolute_scope_under_root_is_matched_root_relative
refused with: 1 failed in 1.50s
