+++
id = "001441-pursuit"
ordinal = 1441
kind = "pursuit"
timestamp = "2026-10-10T02:36:26+00:00"
summary = "pursuit prove T0339: WITNESSED — refuses when tools.py's `if name not in arguments:` is put back as `if False:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "ed21da1d870abaa734360a977d78831164ce93cd6918ead698eec9b9bc7344de  .beagle/checks/T0339/T0339.sh" | sha256sum -c --quiet && bash .beagle/checks/T0339/T0339.sh'
refutes: refuses when tools.py's `if name not in arguments:` is put back as `if False:` (proven 2026-10-10T02:35:29+00:00; refused at FAILED tests/test_tool_missing_argument.py::test_missing_path_names_the_missing_argument[asyncio])
refused after 1s of a 2s check at: FAILED tests/test_tool_missing_argument.py::test_missing_path_names_the_missing_argument[asyncio]
refused with: 2 failed, 1 passed in 0.37s
standing checks red: T0335, T0049
