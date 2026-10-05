+++
id = "000861-pursuit"
ordinal = 861
kind = "pursuit"
timestamp = "2026-10-05T02:43:20+00:00"
summary = "pursuit prove T0218: WITNESSED — refuses when beagle.py's `self.parts.append(\" | \")` is put back as `pass`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "61f3eeb29b4d7206bbcb4db92493a330f2842b41d706b61c5e9a75e97ee324a8  .beagle/checks/T0218/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0218/check.sh'
refutes: refuses when beagle.py's `self.parts.append(" | ")` is put back as `pass` (proven 2026-10-05T02:43:03+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_html_text_keeps_table_cells_apart_and_drops_page_chrome)
refused after 2s of a 1m09s check at: FAILED tests/test_beagle_example_extension.py::test_html_text_keeps_table_cells_apart_and_drops_page_chrome
refused with: 1 failed in 1.76s
