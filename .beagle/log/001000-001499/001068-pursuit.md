+++
id = "001068-pursuit"
ordinal = 1068
kind = "pursuit"
timestamp = "2026-10-05T11:38:15+00:00"
summary = "pursuit open T0258: Compaction summary truncation tested over the cap"
metric_command = ""
drains = []
hooks = []
+++

criteria: A summary longer than COMPACTION_SUMMARY_MAX_CHARS is cut at a line break to at most the cap with the truncation marker, and the compacted context with it stays at or under half the threshold; a test drives the over-cap path.
decided by: sh -c 'echo "5c18901a8afccb93666871c260e4cddc49743fb5d6ac9056555c46a288bb7db6  .beagle/checks/T0258/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0258/check.sh'
budget: 40000 tokens
