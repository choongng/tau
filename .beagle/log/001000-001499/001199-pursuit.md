+++
id = "001199-pursuit"
ordinal = 1199
kind = "pursuit"
timestamp = "2026-10-05T19:34:13+00:00"
summary = "pursuit prove T0285: WITNESSED — refuses when beagle.py's `env = {**os.environ, WORKER_ENV: \"1\", BASH_TIME…` is put back as `env = {**os.environ, WORKER_ENV: \"1\"}`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "5e4aaf375ad8d3a87253ceb820fb5d89e2f724a808b5f5174b6dd3da7c4b5992  .beagle/checks/T0285/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0285/check.sh'
refutes: refuses when beagle.py's `env = {**os.environ, WORKER_ENV: "1", BASH_TIME…` is put back as `env = {**os.environ, WORKER_ENV: "1"}` (proven 2026-10-05T19:34:13+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_worker_bash_default_timeout_is_short)
refused after 3s of a 1m37s check at: FAILED tests/test_beagle_example_extension.py::test_worker_bash_default_timeout_is_short
refused with: 1 failed in 2.81s
