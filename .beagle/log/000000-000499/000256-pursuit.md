+++
id = "000256-pursuit"
ordinal = 256
kind = "pursuit"
timestamp = "2026-10-03T19:53:56+00:00"
summary = "pursuit open T0070: cut read names file lines and next offset; explicit limit fills the char window"
metric_command = ""
drains = []
hooks = []
+++

criteria: A read result cut to its head window says which lines of the file are shown and where to continue: 'lines A-B of the file are shown (of A-C asked); continue with offset=B+1' (file line numbers, using the read's offset). A read with an explicit limit is cut by window_chars only, not WINDOW_LINES, so limit=300 of short lines shows all 300 when they fit. Also covers audit-3's T0060 follow-up (T0076): a test through the CodingSession tool path with an offset read asserts the outline and marker carry the file's line numbers.
decided by: sh -c 'echo "06dd477427036a9299beadee58da41a3168810b76e6e790d084e6a80cf881f00  .beagle/checks/T0070/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0070/check.sh'
budget: 50000 tokens
