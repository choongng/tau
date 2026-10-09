+++
id = "001257-pursuit"
ordinal = 1257
kind = "pursuit"
timestamp = "2026-10-09T19:25:07+00:00"
summary = "pursuit prove T0290: WITNESSED — refuses when beagle.py's `if in_store: return ToolCallHookResult(block=Tr…` is put back as `if False: return ToolCallHookResult(block=True,…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "58c76423721d7ec56be868540f3f858ebbb37c1a7b753a25b9d9535d5688af61  .beagle/checks/T0290/T0290.sh" | sha256sum -c --quiet && bash .beagle/checks/T0290/T0290.sh'
refutes: refuses when beagle.py's `if in_store: return ToolCallHookResult(block=Tr…` is put back as `if False: return ToolCallHookResult(block=True,…` (proven 2026-10-09T19:25:07+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_worker_scope_guard_refuses_writes_into_beagle_store)
refused after 3s of a 1m44s check at: FAILED tests/test_beagle_example_extension.py::test_worker_scope_guard_refuses_writes_into_beagle_store
refused with: 1 failed in 2.56s
