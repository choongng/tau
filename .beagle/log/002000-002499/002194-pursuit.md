+++
id = "002194-pursuit"
ordinal = 2194
kind = "pursuit"
timestamp = "2026-10-12T09:46:33+00:00"
summary = "pursuit prove T0461: WITNESSED — refuses when beagle.py's `r\"|<[\\w.-]+>\\s*<parameter=|</function>\\s*</tool…` is put back as `r\"\"`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "4a5b81b5262e7677b2c7d011e04a47f61679fdd949961d499104755bd0d6831e  .beagle/checks/T0461/T0461.sh" | sha256sum -c --quiet && bash .beagle/checks/T0461/T0461.sh'
refutes: refuses when beagle.py's `r"|<[\w.-]+>\s*<parameter=|</function>\s*</tool…` is put back as `r""` (proven 2026-10-12T09:46:33+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_raw_report_with_closing_tool_call_tags_gets_the_stub)
refused after 3s of a 2m48s check at: FAILED tests/test_beagle_example_extension.py::test_raw_report_with_closing_tool_call_tags_gets_the_stub
refused with: 1 failed, 809 deselected in 2.99s
