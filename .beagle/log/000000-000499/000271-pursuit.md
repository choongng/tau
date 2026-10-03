+++
id = "000271-pursuit"
ordinal = 271
kind = "pursuit"
timestamp = "2026-10-03T19:59:00+00:00"
summary = "pursuit prove T0066: WITNESSED — refuses when beagle.py's `if opening & _RERUN_VERBS and not set(words)` is put back as `if False and opening & _RERUN_VERBS and not set…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "13241b4fed186f29c2b7be151bb8dd6650842358caa02561161528fbd34ceaba  .beagle/checks/T0066/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0066/check.sh'
refutes: refuses when beagle.py's `if opening & _RERUN_VERBS and not set(words)` is put back as `if False and opening & _RERUN_VERBS and not set…` (proven 2026-10-03T19:58:30+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_plan_refuses_a_part_that_only_reruns_a_check)
refused after 1s of a 1s check at: FAILED tests/test_beagle_example_extension.py::test_plan_refuses_a_part_that_only_reruns_a_check
refused with: 2 failed, 264 deselected in 0.60s
