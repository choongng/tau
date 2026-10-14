+++
id = "002895-pursuit"
ordinal = 2895
kind = "pursuit"
timestamp = "2026-10-14T01:34:39+00:00"
summary = "pursuit prove T0493: NOT-DISCRIMINATING — `sh -c 'echo \"7cc28365adcc1b556397d8e1802f8990a54cb89390762cc26631eb2a86f4e171  .beagle/checks/T0493/T0493.sh\" | sha256sum -c --quiet && bash .beagle/checks/T0493/T0493.sh'`"
metric_command = ""
drains = []
hooks = []
+++

criteria: The tau extension no longer carries cases-first: the known-answer cases file and its locks, the cases-first split and scope refusals, the source judge and _cases_off are deleted with the tests that exercised only them; every remaining extension test passes outside beagle's venv.
measured: still passes with the defect put back in beagle.py (exit 0), measured 2026-10-14T01:34:39+00:00
