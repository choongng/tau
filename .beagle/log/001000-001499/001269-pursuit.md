+++
id = "001269-pursuit"
ordinal = 1269
kind = "pursuit"
timestamp = "2026-10-09T19:51:47+00:00"
summary = "pursuit open T0306: R36 run and score"
metric_command = ""
drains = []
hooks = []
+++

criteria: R36 (gemma4-12b-q4, itc_prompt.txt, driver thinking medium) ran from a clean ~/itc under the one-hour cap; dev-notes/itc-runs/R36.md names model and prompt and holds the scorecard, the driver's thinking level and the hidden-grader result.
decided by: sh -c 'echo "2882aab7c8d9106055c803f2aa4453fa0645ee355575fa5678f6b7baca1790d2  .beagle/checks/T0306/T0306.sh" | sha256sum -c --quiet && bash .beagle/checks/T0306/T0306.sh'
budget: 40000 tokens
