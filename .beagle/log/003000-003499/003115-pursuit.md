+++
id = "003115-pursuit"
ordinal = 3115
kind = "pursuit"
timestamp = "2026-10-14T20:18:09+00:00"
summary = "pursuit open T0600: real-beagle tests: founding, planning and a step's open and close against the pinned 0.48 CLI, stub worker"
metric_command = ""
drains = []
hooks = []
+++

criteria: On branch beagle-0.48 (worktree ~/tautest/tau-wt-048): tests marked real_beagle run tau's beagle extension against the real beagle CLI pinned at ~/beagle-wt/0.48 (not the fake beagle): pursuit_found on a fresh repo, pursuit_plan, and a pursuit_step that opens a milestone, dispatches a stub worker (TAU_BIN a script that makes the change and commits) and closes it done; at least 3 such tests, named for found, step and close, all passing and none skipped; what they expose as broken against 0.48 is fixed in the extension; the extension's full unit suite still passes
decided by: sh -c 'echo "703ad4835298af00caab69e25cd28ae73788285fd146d18d75e7aca193e71d66  .beagle/checks/T0600/T0600.sh" | sha256sum -c --quiet && bash .beagle/checks/T0600/T0600.sh'
budget: 400000 tokens
