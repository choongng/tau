+++
id = "000918-pursuit"
ordinal = 918
kind = "pursuit"
timestamp = "2026-10-05T06:06:48+00:00"
summary = "pursuit open T0229: Reference text has only newline line breaks"
metric_command = ""
drains = []
hooks = []
+++

criteria: Every reference text tau writes (PDF-extracted or fetched) contains no character that str.splitlines() treats as a line break other than \n, so line numbers by split('\n') and splitlines() agree; tested on text carrying form feed and \x1c-\x1e.
decided by: sh -c 'echo "a761e7b18b5874104e88fe41de2bef3322156f2d63fe3c80402da9eb7c9dfd91  .beagle/checks/T0229/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0229/check.sh'
budget: 50000 tokens
