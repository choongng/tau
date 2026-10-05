+++
id = "001125-pursuit"
ordinal = 1125
kind = "pursuit"
timestamp = "2026-10-05T14:31:15+00:00"
summary = "pursuit prove T0269: WITNESSED — refuses when beagle.py's `if python is not None and _source_reads_store(b…` is put back as `if False:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "16fbc9bd0e64d7648ed0f285d34e6cce90a05e3f3d564bf310e3e1786e89a553  .beagle/checks/T0269/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0269/check.sh'
refutes: refuses when beagle.py's `if python is not None and _source_reads_store(b…` is put back as `if False:` (proven 2026-10-05T14:31:15+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_worker_guard_refuses_heredoc_store_read)
refused after 3s of a 1m31s check at: FAILED tests/test_beagle_example_extension.py::test_worker_guard_refuses_heredoc_store_read
refused with: 1 failed, 2 passed in 2.19s
