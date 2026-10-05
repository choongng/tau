+++
id = "000919-pursuit"
ordinal = 919
kind = "pursuit"
timestamp = "2026-10-05T06:12:11+00:00"
summary = "pursuit prove T0229: WITNESSED — refuses when beagle.py's `return text.replace(\"\\r\\n\", \"\\n\").translate(_NO…` is put back as `return text`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "a761e7b18b5874104e88fe41de2bef3322156f2d63fe3c80402da9eb7c9dfd91  .beagle/checks/T0229/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0229/check.sh'
refutes: refuses when beagle.py's `return text.replace("\r\n", "\n").translate(_NO…` is put back as `return text` (proven 2026-10-05T06:11:58+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_pdf_text_has_no_line_breaks_besides_newline)
refused after 2s of a 1m13s check at: FAILED tests/test_beagle_example_extension.py::test_pdf_text_has_no_line_breaks_besides_newline
refused with: 1 failed in 1.99s
