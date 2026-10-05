+++
id = "000984-pursuit"
ordinal = 984
kind = "pursuit"
timestamp = "2026-10-05T08:09:33+00:00"
summary = "pursuit prove T0243: WITNESSED — refuses when session.py's `reserved = \"x\" * COMPACTION_SUMMARY_MAX_CHARS` is put back as `reserved = \"x\"`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "275593124c74ffa70159899328709805282f1ed1930d89c2d93554477245188a  .beagle/checks/T0243/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0243/check.sh'
refutes: refuses when session.py's `reserved = "x" * COMPACTION_SUMMARY_MAX_CHARS` is put back as `reserved = "x"` (proven 2026-10-05T08:08:36+00:00; refused at FAILED tests/test_coding_session.py::test_compaction_headroom_holds_for_a_long_summary[asyncio])
refused after 1s of a 3s check at: FAILED tests/test_coding_session.py::test_compaction_headroom_holds_for_a_long_summary[asyncio]
refused with: 1 failed in 0.85s
