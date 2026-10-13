+++
id = "002668-pursuit"
ordinal = 2668
kind = "pursuit"
timestamp = "2026-10-13T06:14:30+00:00"
summary = "pursuit amend T0512"
metric_command = ""
drains = []
hooks = []
+++

audit 2026-10-12 (T0521): the criteria claim beagle CI green but the check runs a -k subset of tests/test_contract.py; adding ci/check.sh to each check would multiply the standing set's run time, so the clause is declared untested here and run once for the branch by standing task T0523
