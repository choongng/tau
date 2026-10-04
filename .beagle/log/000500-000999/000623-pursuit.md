+++
id = "000623-pursuit"
ordinal = 623
kind = "pursuit"
timestamp = "2026-10-04T10:50:47+00:00"
summary = "pursuit prove T0148: WITNESSED — refuses when R17.md's `grader: 6/42 (itc/itc.py, working tree incl. T0…` is put back as `grader: 1/42`"
metric_command = ""
drains = []
hooks = []
+++

check: bash .beagle/checks/T0148/check.sh # sha256=5cb516950a2517544f59f4f400d47ed2c3be067463ddd7627f63af607645ef45
refutes: refuses when R17.md's `grader: 6/42 (itc/itc.py, working tree incl. T0…` is put back as `grader: 1/42` (proven 2026-10-04T10:49:56+00:00; refused at Traceback (most recent call last):)
refused after 0s of a 0s check at: Traceback (most recent call last):
refused with: AssertionError: grader line grader: 1/42 != grade.json 6/42
