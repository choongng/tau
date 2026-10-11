+++
id = "001698-pursuit"
ordinal = 1698
kind = "pursuit"
timestamp = "2026-10-11T00:00:14+00:00"
summary = "pursuit prove T0395: WITNESSED — refuses when events.py's `elif role == \"toolResult\":` is put back as `elif role == \"toolResult\" and not msg.get(\"isEr…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "13242627fc8b347d14e486b94fad8e0604af68afcb58e9dec36f80989e4ea57d  .beagle/checks/T0395/T0395.sh" | sha256sum -c --quiet && bash .beagle/checks/T0395/T0395.sh'
refutes: refuses when events.py's `elif role == "toolResult":` is put back as `elif role == "toolResult" and not msg.get("isEr…` (proven 2026-10-10T23:59:14+00:00; refused at FAILED mine/test_events.py::test_tool_calls_and_results_link_and_count - asse...)
refused after 0s of a 7s check at: FAILED mine/test_events.py::test_tool_calls_and_results_link_and_count - asse...
refused with: 3 failed, 7 passed in 0.03s
standing checks red: T0368
