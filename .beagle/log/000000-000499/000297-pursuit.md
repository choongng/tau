+++
id = "000297-pursuit"
ordinal = 297
kind = "pursuit"
timestamp = "2026-10-03T20:10:25+00:00"
summary = "pursuit open T0069: closed-done result marks a stale failing worker report as superseded"
metric_command = ""
drains = []
hooks = []
+++

criteria: In pursuit_step's closed-done result, when the sub-agent report claims a failure (N failed, exit 1, unfixed, remaining failures, error), a line before the report says the check passed at close, so the failures it names are from before the worker's last edit and are fixed; a report with no failure claim is printed as before. R09: W14 said '2 failed … Remaining failures (unfixed)', T0009 closed done, and the driver chased those failures into the T0010 loop.
decided by: sh -c 'echo "88ed18552cdf0da9d8134cc39ecf33b9893c3a201fd89060ad5d1ab2480d733d  .beagle/checks/T0069/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0069/check.sh'
budget: 25000 tokens
