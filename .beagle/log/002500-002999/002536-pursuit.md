+++
id = "002536-pursuit"
ordinal = 2536
kind = "pursuit"
timestamp = "2026-10-12T17:31:51+00:00"
summary = "pursuit prove T0490: WITNESSED — refuses when beagle.py's `[BEAGLE_BIN, \"refs\", \"fetch\", *urls, f\"--reques…` is put back as `[BEAGLE_BIN, \"refs\", \"fetch\", *urls, \"--no-excl…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "39dfdcc9799799b12452399986687b90342d51b854b4ccedf6273908e6f8c2b2  .beagle/checks/T0490/T0490.sh" | sha256sum -c --quiet && bash .beagle/checks/T0490/T0490.sh'
refutes: refuses when beagle.py's `[BEAGLE_BIN, "refs", "fetch", *urls, f"--reques…` is put back as `[BEAGLE_BIN, "refs", "fetch", *urls, "--no-excl…` (proven 2026-10-12T17:30:54+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_references_are_fetched_by_beagle_refs)
refused after 1s of a 27s check at: FAILED tests/test_beagle_example_extension.py::test_references_are_fetched_by_beagle_refs
refused with: 1 failed, 2 passed, 827 deselected in 0.81s
