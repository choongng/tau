+++
id = "002882-pursuit"
ordinal = 2882
kind = "pursuit"
timestamp = "2026-10-14T00:53:12+00:00"
summary = "pursuit open T0493: tau ext: delete the cases-first machinery the contract replaced"
metric_command = ""
drains = []
hooks = []
+++

criteria: The tau extension no longer carries cases-first: the known-answer cases file and its locks, the cases-first split and scope refusals, the source judge and _cases_off are deleted with the tests that exercised only them; every remaining extension test passes outside beagle's venv.
decided by: sh -c 'echo "7cc28365adcc1b556397d8e1802f8990a54cb89390762cc26631eb2a86f4e171  .beagle/checks/T0493/T0493.sh" | sha256sum -c --quiet && bash .beagle/checks/T0493/T0493.sh'
budget: 300000 tokens
