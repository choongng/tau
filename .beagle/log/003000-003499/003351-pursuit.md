+++
id = "003351-pursuit"
ordinal = 3351
kind = "pursuit"
timestamp = "2026-10-15T21:42:31+00:00"
summary = "pursuit open T0649: founding grader over past rounds"
metric_command = ""
drains = []
hooks = []
+++

criteria: /home/choong/tautest/itc-harness/grade_founding.py grades a founded plan (default: the 'pursuit: found' commit of a project dir; --live: the working tree) per task (itc/cobs/wrenfold/semver, from pursuit.toml or --task) with a fixed rubric: IDLE milestones (name none of the task's operations), MISSING operations (named by no milestone), UNSOURCED milestones (task has a reference and the Source: names no references/ file or link), COUNT > 6; verdict PASS only with none. Over the R104-R129 project dirs: R104, R105, R107, R118, R120, R121, R122, R123, R124, R126 are flagged, each for the class eval.md records (setup/study/fine-grained -> IDLE; count/fork-event-join missing -> MISSING; no or descriptive source -> UNSOURCED); R113, R116 and R117 PASS. --json emits one object per plan.
decided by: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider /home/choong/tautest/itc-harness/test_grade_founding.py
budget: 200000 tokens
