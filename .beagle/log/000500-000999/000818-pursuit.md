+++
id = "000818-pursuit"
ordinal = 818
kind = "pursuit"
timestamp = "2026-10-05T01:32:11+00:00"
summary = "pursuit prove T0208: WITNESSED — refuses when beagle.py's `return os.path.normpath(rel) in named` is put back as `return os.path.normpath(rel) in named or rel in…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "546d67499b2c1c2d4dc7dfe070d783687e4b156638318e699e360a5088e2b194  .beagle/checks/T0208/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0208/check.sh'
refutes: refuses when beagle.py's `return os.path.normpath(rel) in named` is put back as `return os.path.normpath(rel) in named or rel in…` (proven 2026-10-05T01:31:51+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_sibling_check_ignores_a_path_named_only_in_a_title)
refused after 2s of a 1m07s check at: FAILED tests/test_beagle_example_extension.py::test_sibling_check_ignores_a_path_named_only_in_a_title
refused with: 1 failed, 3 passed in 1.52s
