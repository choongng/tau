+++
id = "001657-pursuit"
ordinal = 1657
kind = "pursuit"
timestamp = "2026-10-10T21:31:21+00:00"
summary = "pursuit open T0387: R44 run and score"
metric_command = ""
drains = []
hooks = []
+++

criteria: R44 (mimo, itc) ran under launch.sh on a clean tau at or after e870feb2 (R43's fixes T0382-T0386 in), driver thinking medium (sent) and workers thinking at the driver's level, under the one-hour cap and MemoryMax 8G; runs/R44 holds meta, exit, grade, scorecard and stdout, committed in itc-harness; dev-notes/itc-runs/R44.md records the run and its score (the scorecard's facts, the grade, and both thinking levels) as R43.md's run and score part does.
decided by: sh -c 'echo "2917c36f75c0677c778fd5ce183aaf810688c8db82db2adc8f706800f02bafc2  .beagle/checks/T0387/T0387.sh" | sha256sum -c --quiet && bash .beagle/checks/T0387/T0387.sh'
budget: 60000 tokens
