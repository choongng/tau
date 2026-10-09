+++
id = "001368-pursuit"
ordinal = 1368
kind = "pursuit"
timestamp = "2026-10-09T23:24:24+00:00"
summary = "pursuit open T0325: R38 run and score"
metric_command = ""
drains = []
hooks = []
+++

criteria: R38 (mimo-v2.6-9b-q4, itc_prompt.txt, driver thinking medium) ran from a clean ~/itc under the one-hour cap; dev-notes/itc-runs/R38.md names model and prompt and holds the scorecard, the driver's thinking level and the hidden-grader result.
decided by: sh -c 'echo "fb5863ea82e03e3112ca6b48f76f6e99a6cdef99ded67cf16d9b7ad98d5f0633  .beagle/checks/T0325/T0325.sh" | sha256sum -c --quiet && bash .beagle/checks/T0325/T0325.sh'
budget: 20000 tokens
