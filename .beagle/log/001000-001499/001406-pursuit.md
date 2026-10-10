+++
id = "001406-pursuit"
ordinal = 1406
kind = "pursuit"
timestamp = "2026-10-10T02:16:33+00:00"
summary = "pursuit prove T0334: WITNESSED — refuses when R39.md's `# R39 — gemma4-12b-q4 — cobs_prompt.txt` is put back as `# R39 — gemma4-12b-q4 — itc_prompt.txt`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "f7192981dc7c7fbaf610872ecee4c68cee2acbc8a4fb5fa8cc57c5b2aa4a660c  .beagle/checks/T0334/T0334.sh" | sha256sum -c --quiet && bash .beagle/checks/T0334/T0334.sh'
refutes: refuses when R39.md's `# R39 — gemma4-12b-q4 — cobs_prompt.txt` is put back as `# R39 — gemma4-12b-q4 — itc_prompt.txt` (proven 2026-10-10T02:15:35+00:00; refused at Traceback (most recent call last):)
refused after 0s of a 0s check at: Traceback (most recent call last):
refused with: AssertionError: R39.md header '# R39 — gemma4-12b-q4 — itc_prompt.txt' != '# R39 — gemma4-12b-q4 — cobs_prompt.txt'
