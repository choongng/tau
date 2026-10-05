+++
id = "001173-pursuit"
ordinal = 1173
kind = "pursuit"
timestamp = "2026-10-05T17:37:29+00:00"
summary = "pursuit open T0280: Workers stop re-reading past half the turn cap with nothing written; output-cap cut-offs end the worker on the second over the run"
metric_command = ""
drains = []
hooks = []
+++

criteria: The worker scope guard refuses a further read once the worker has used half its turn cap and written nothing in scope, naming the file to write; a worker cut off at the output cap a second time over the whole run (not only in a row) is ended with a report naming the cut-off, and the write-it-in-parts advice sizes each part to the output limit.
decided by: sh -c 'echo "88133e6cd85e5e6f2481ba4ade51b4de6dbd638a85875cae58f9d631a0379ce1  .beagle/checks/T0280/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0280/check.sh'
budget: 70000 tokens
