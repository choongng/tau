+++
id = "000933-pursuit"
ordinal = 933
kind = "pursuit"
timestamp = "2026-10-05T06:31:50+00:00"
summary = "pursuit open T0232: The brief states the worker turn cap and reference sizes"
metric_command = ""
drains = []
hooks = []
+++

criteria: The worker brief pursuit_step writes states the worker's tool-call cap (from the same setting that caps it) and asks for files written by about half of it; the references brief gives each reference file's line count and the reads it costs at the read tool's window, computed from the files on disk; a data task's brief says to read cited lines by range.
decided by: sh -c 'echo "422298ae662f3972f4a39ddbaee21d88b7fa40d2b99a92ad91b228c62e426d21  .beagle/checks/T0232/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0232/check.sh'
budget: 50000 tokens
