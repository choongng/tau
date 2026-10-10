+++
id = "001577-pursuit"
ordinal = 1577
kind = "pursuit"
timestamp = "2026-10-10T16:40:23+00:00"
summary = "pursuit open T0368: progress.py: repo chain across R and B runs"
metric_command = ""
drains = []
hooks = []
+++

criteria: progress.py exposes repo_of(run) -> Path|None (run like 'R39' or 'B02'), and its repo for a run is the moved_previous_to of the next run of the same task in start order across both R and B series, else the meta cwd, else None when that directory is gone; stages use it. R39 -> ~/cobs.r39, B01 -> ~/cobs.b01, B03 -> ~/cobs.b03, R41 -> ~/cobs, R38 -> ~/itc.r38, R40 -> ~/itc.r40, B02 -> ~/itc. T0353's check still passes. baselines.md: the ceiling sentence counts gemma's 4/44, and no longer says R41 is still running (it ran, 0/44, and has no baseline pair); any stage that changes under the fixed mapping is updated in its table.
decided by: sh -c 'echo "45692c9b40f8b7a69e087bdd174de8d6459c5938c032a01b8d89a445c766b331  .beagle/checks/T0368/T0368.sh" | sha256sum -c --quiet && bash .beagle/checks/T0368/T0368.sh'
budget: 30000 tokens
