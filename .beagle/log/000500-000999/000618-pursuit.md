+++
id = "000618-pursuit"
ordinal = 618
kind = "pursuit"
timestamp = "2026-10-04T09:23:53+00:00"
summary = "pursuit prove T0147: WITNESSED — refuses when beagle.py's `re.split(r\"\\.\\.\\.|…|:\\s\", c)` is put back as `re.split(r\"\\.\\.\\.|…\", c)`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "1c884585a3bbdfaa1c20a3f38a46044ad6b59afec93ec229eba2db6dac2f678c  .beagle/checks/T0147/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0147/check.sh'
refutes: refuses when beagle.py's `re.split(r"\.\.\.|…|:\s", c)` is put back as `re.split(r"\.\.\.|…", c)` (proven 2026-10-04T09:23:16+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_quoted_source_with_a_leading_label_is_found)
refused after 2s of a 49s check at: FAILED tests/test_beagle_example_extension.py::test_quoted_source_with_a_leading_label_is_found
refused with: 1 failed in 1.46s
