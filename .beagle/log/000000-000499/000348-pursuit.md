+++
id = "000348-pursuit"
ordinal = 348
kind = "pursuit"
timestamp = "2026-10-03T20:49:20+00:00"
summary = "pursuit prove T0081: WITNESSED — refuses when beagle.py's `title = re.split(r\":| - | — \", _split_part(part…` is put back as `title = _split_part(part)[0].split(\":\")[0]`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "85aeb4c6c581b236fd9a25b5205bc5ec1cddd09a9f27a9fc54f2a1777f74d7cb  .beagle/checks/T0081/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0081/check.sh'
refutes: refuses when beagle.py's `title = re.split(r":| - | — ", _split_part(part…` is put back as `title = _split_part(part)[0].split(":")[0]` (proven 2026-10-03T20:48:40+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_setup_milestone_titled_with_a_dash_and_naming_beagle_is_dropped)
refused after 1s of a 1s check at: FAILED tests/test_beagle_example_extension.py::test_setup_milestone_titled_with_a_dash_and_naming_beagle_is_dropped
refused with: 1 failed, 1 passed, 284 deselected in 0.97s
replaces: still passes with the defect put back in beagle.py (exit 0), measured 2026-10-03T20:48:22+00:00
