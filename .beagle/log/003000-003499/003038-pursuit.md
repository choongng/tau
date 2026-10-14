+++
id = "003038-pursuit"
ordinal = 3038
kind = "pursuit"
timestamp = "2026-10-14T05:28:21+00:00"
summary = "pursuit open T0517: contract: invalid input the sources do not state becomes a gap the reader is asked about (R84)"
metric_command = ""
drains = []
hooks = []
+++

criteria: dev-notes/contract-first/invalid-silence-recon.md reads, against beagle contract-first (contract.py) and tau choong-dev (beagle.py), with file:line citations, whether the incremental contract (T0554–T0560: per-operation limits-and-invalid slices, coverage slice as a hard gate, gaps with assumptions) now makes a contract whose sources say nothing about malformed input surface that silence as a gap or a question, as R84 needed; states what R98 (~/wrenfold, read-only) did about invalid inputs; ends with one line 'Decision: covered|build|defer' and, for build, the smallest change in beagle and/or tau.
decided by: sh -c 'echo "a6a87351e05f200ec088cef88ca2590af2dae1b56d2b03aa229b10d1fa4d85d1  .beagle/checks/T0517/T0517.sh" | sha256sum -c --quiet && bash .beagle/checks/T0517/T0517.sh'
budget: 50000 tokens
