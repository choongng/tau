+++
id = "000928-pursuit"
ordinal = 928
kind = "pursuit"
timestamp = "2026-10-05T06:23:49+00:00"
summary = "pursuit open T0231: A step's first worker hears the last check failure"
metric_command = ""
drains = []
hooks = []
+++

criteria: The first worker of a pursuit_step on an open task whose last check run failed is briefed with that failure (exit code and the tail of its output, plus the no-test-function explanation on pytest exit 5); the implementation-in-tests runner note names only files the bound check runs or that they import.
decided by: sh -c 'echo "55b6110fd00786bb784d4b2f70983cef0649bf71d3ad1864ea059030f39e92f3  .beagle/checks/T0231/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0231/check.sh'
budget: 70000 tokens
