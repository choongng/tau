+++
id = "001287-pursuit"
ordinal = 1287
kind = "pursuit"
timestamp = "2026-10-09T21:16:24+00:00"
summary = "pursuit prove T0309: WITNESSED — refuses when beagle.py's `|\\(([^()]{12,})\\)|` is put back as `|`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "3dfd10fc0dec3e1ec8345b1d05fdaf913edb25337e991993a250310ee53048c4  .beagle/checks/T0309/T0309.sh" | sha256sum -c --quiet && bash .beagle/checks/T0309/T0309.sh'
refutes: refuses when beagle.py's `|\(([^()]{12,})\)|` is put back as `|` (proven 2026-10-09T21:16:24+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_quotes_reference_finds_parenthesised_quote_after_file_line_label)
refused after 3s of a 1m41s check at: FAILED tests/test_beagle_example_extension.py::test_quotes_reference_finds_parenthesised_quote_after_file_line_label
refused with: 1 failed in 2.54s
