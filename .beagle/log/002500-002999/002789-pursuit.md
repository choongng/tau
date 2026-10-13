+++
id = "002789-pursuit"
ordinal = 2789
kind = "pursuit"
timestamp = "2026-10-13T20:34:40+00:00"
summary = "pursuit open T0544: recon: what a sealed-entry dispute can build on"
metric_command = ""
drains = []
hooks = []
+++

criteria: dev-notes/contract-first/dispute-recon.md says, with file:line evidence from beagle (contract-first) and the tau extension: what exists today for a sealed contract (seal, the sha check, amend/re-seal or not), where a worker's dispute of one entry would enter, who judges it across a sub-agent boundary without a mid-session prompt change, and the smallest change that lets a sealed acceptance's wrong test be fixed on the record without letting a worker soften a right one
decided by: sh -c 'echo "c4753345852b016afe21b3351d886e7f7074567c8f1cfbf57fdaad379c92f645  .beagle/checks/T0544/T0544.sh" | sha256sum -c --quiet && bash .beagle/checks/T0544/T0544.sh'
budget: 80000 tokens
