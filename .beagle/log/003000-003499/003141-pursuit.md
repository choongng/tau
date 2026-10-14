+++
id = "003141-pursuit"
ordinal = 3141
kind = "pursuit"
timestamp = "2026-10-14T22:10:01+00:00"
summary = "pursuit open T0604: smoke S02: q35 wrenfold, 25 min cap, on the port; fix what sinks it"
metric_command = ""
drains = []
hooks = []
+++

criteria: S02, a q35 wrenfold smoke with a 25 min cap, ran on the port (tau beagle-0.48 at or past fb3823e5 via tau-harness, beagle 0.48.0 pinned), ended and was graded; eval.md on beagle-0.48 has its row and a section with its findings. What sank it is fixed on the branch or filed.
decided by: sh -c 'echo "8e7c253c39ece2e16818de58811342c96d168b4f652a2e928110c2abbac94432  .beagle/checks/T0604/T0604.sh" | sha256sum -c --quiet && bash .beagle/checks/T0604/T0604.sh'
budget: 200000 tokens
