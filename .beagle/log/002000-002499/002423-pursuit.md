+++
id = "002423-pursuit"
ordinal = 2423
kind = "pursuit"
timestamp = "2026-10-12T14:58:50+00:00"
summary = "pursuit prove T0474: WITNESSED — refuses when beagle.py's `tau.on(\"tool_call\", make_record_guard())` is put back as `tau.on(\"tool_call\", make_bash_hooks()) tau.on(\"…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "424bc5a62fed0540b5acad2a3c0c7ad73321b168e2ecd783610cdc8d918cc26b  .beagle/checks/T0474/T0474.sh" | sha256sum -c --quiet && bash .beagle/checks/T0474/T0474.sh'
refutes: refuses when beagle.py's `tau.on("tool_call", make_record_guard())` is put back as `tau.on("tool_call", make_bash_hooks()) tau.on("…` (proven 2026-10-12T14:58:49+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_worker_git_commit_gets_the_worker_refusal_not_commit_claims_advice)
refused after 3s of a 2m45s check at: FAILED tests/test_beagle_example_extension.py::test_worker_git_commit_gets_the_worker_refusal_not_commit_claims_advice
refused with: 1 failed, 823 deselected in 3.07s
