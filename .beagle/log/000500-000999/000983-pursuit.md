+++
id = "000983-pursuit"
ordinal = 983
kind = "pursuit"
timestamp = "2026-10-05T08:06:08+00:00"
summary = "pursuit open T0243: Compaction headroom holds for a real summary"
metric_command = ""
drains = []
hooks = []
+++

criteria: After an automatic compaction whose summary is longer than the template (several thousand chars), the estimated context is still at most half the threshold: the cut either reserves a bounded summary size the summary is held to, or is re-checked after summarising; tested with a long summary.
decided by: sh -c 'echo "275593124c74ffa70159899328709805282f1ed1930d89c2d93554477245188a  .beagle/checks/T0243/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0243/check.sh'
budget: 50000 tokens
