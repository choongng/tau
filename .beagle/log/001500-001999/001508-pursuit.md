+++
id = "001508-pursuit"
ordinal = 1508
kind = "pursuit"
timestamp = "2026-10-10T04:14:43+00:00"
summary = "pursuit prove T0359: WITNESSED — refuses when beagle.py's `if \"|\" in text and _table_row(text):` is put back as `if False and _table_row(text):`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "38a838e0950554371d4c6bcd4b101a3488fef272b1264278928aa080183230bf  .beagle/checks/T0359/T0359.sh" | sha256sum -c --quiet && bash .beagle/checks/T0359/T0359.sh'
refutes: refuses when beagle.py's `if "|" in text and _table_row(text):` is put back as `if False and _table_row(text):` (proven 2026-10-10T04:14:42+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_result_lines_name_hex_table_rows_not_code_lines)
refused after 1s of a 1m45s check at: FAILED tests/test_beagle_example_extension.py::test_result_lines_name_hex_table_rows_not_code_lines
refused with: 1 failed, 2 passed, 676 deselected in 1.18s
