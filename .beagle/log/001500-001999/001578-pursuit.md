+++
id = "001578-pursuit"
ordinal = 1578
kind = "pursuit"
timestamp = "2026-10-10T16:42:51+00:00"
summary = "pursuit prove T0368: WITNESSED — refuses when progress.py's `for prefix in (\"R\", \"B\")` is put back as `for prefix in (\"R\",)`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "45692c9b40f8b7a69e087bdd174de8d6459c5938c032a01b8d89a445c766b331  .beagle/checks/T0368/T0368.sh" | sha256sum -c --quiet && bash .beagle/checks/T0368/T0368.sh'
refutes: refuses when progress.py's `for prefix in ("R", "B")` is put back as `for prefix in ("R",)` (proven 2026-10-10T16:41:53+00:00; refused at Traceback (most recent call last):)
refused after 0s of a 0s check at: Traceback (most recent call last):
refused with: AssertionError: repo_of wrong: {'R39': '/home/choong/cobs.b03', 'B01': 'None', 'B03': 'None', 'R40': '/home/choong/itc', 'B02': 'None'}
