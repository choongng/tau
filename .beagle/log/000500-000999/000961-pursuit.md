+++
id = "000961-pursuit"
ordinal = 961
kind = "pursuit"
timestamp = "2026-10-05T07:37:33+00:00"
summary = "pursuit prove T0241: WITNESSED — refuses when session.py's `first_kept_index = self._cut_for_half_threshold…` is put back as `pass`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "b7803d8738f5d0f78bbaceade8352b878e8330f1141b7b25ccc5a0937bd71f37  .beagle/checks/T0241/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0241/check.sh'
refutes: refuses when session.py's `first_kept_index = self._cut_for_half_threshold…` is put back as `pass` (proven 2026-10-05T07:36:35+00:00; refused at FAILED tests/test_coding_session.py::test_compaction_leaves_half_threshold_headroom[asyncio])
refused after 1s of a 3s check at: FAILED tests/test_coding_session.py::test_compaction_leaves_half_threshold_headroom[asyncio]
refused with: 1 failed in 0.79s
