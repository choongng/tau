+++
id = "000285-pursuit"
ordinal = 285
kind = "pursuit"
timestamp = "2026-10-03T20:02:31+00:00"
summary = "pursuit open T0068: not-done results name implementation written under tests/"
metric_command = ""
drains = []
hooks = []
+++

criteria: (a) A pursuit_step result for a task not closed done runs _implementation_in_tests over the files the worker changed and, when it finds implementation under tests/, says so first: the sub-agent wrote implementation into tests/ (path: class/def names), which is not this task's work. (b) The worker scope guard's refusal of a non-test .py path adds that the implementation is not to go under tests/ either; it is a later task's, so report it. (c) The brief of a task whose check is a data/cases test introduces the user's request as context only, the task being the one above. R09: W4 on T0002 (docs/, tests/) wrote the library to tests/itc/ after src/ was refused; nothing said so for 24 min.
decided by: sh -c 'echo "928cbe58ae12e18b3f9d3bfcd03b64fef82c1712b298b4bd00db7fd98245382c  .beagle/checks/T0068/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0068/check.sh'
budget: 50000 tokens
