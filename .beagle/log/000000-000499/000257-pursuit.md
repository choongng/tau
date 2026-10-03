+++
id = "000257-pursuit"
ordinal = 257
kind = "pursuit"
timestamp = "2026-10-03T19:56:10+00:00"
summary = "pursuit prove T0065: WITNESSED — refuses when beagle.py's `if not container or container in roots: return …` is put back as `if True: return f\"{text} {ABANDON_HINT}\"`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "690a04302e1bcaecc7e9a07f89238a0278d87942bd49bf3b8e1497898e52b52c  .beagle/checks/T0065/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0065/check.sh'
refutes: refuses when beagle.py's `if not container or container in roots: return …` is put back as `if True: return f"{text} {ABANDON_HINT}"` (proven 2026-10-03T19:55:38+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_already_passes_on_a_container_part_names_the_done_sibling)
refused after 1s of a 1s check at: FAILED tests/test_beagle_example_extension.py::test_already_passes_on_a_container_part_names_the_done_sibling
refused with: 1 failed, 1 passed, 262 deselected in 0.69s
standing checks red: T0060
