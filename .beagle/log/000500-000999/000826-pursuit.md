+++
id = "000826-pursuit"
ordinal = 826
kind = "pursuit"
timestamp = "2026-10-05T01:42:53+00:00"
summary = "pursuit open T0210: scored.sh checks the RNN.md header names model, prompt and tau sha, and the project dir started clean"
metric_command = ""
drains = []
hooks = []
+++

criteria: A v5 copy of the run checks (.beagle/checks/runs/v5) whose scored.sh also asserts that RNN.md's first line is '# RNN — <full model> — <task>_prompt.txt', that its summary names 'tau <sha7>' matching meta.tau_sha, and that the project started clean: scorecard.json's first_commit_ts (new, from scorecard.py: the project repo's root commit time) is at or after meta.start. Its selftest refuses a wrong header, a wrong sha and an early first commit; v4 is unchanged; R22 passes v5.
decided by: sh -c 'echo "6fdc4946ed4cc0a65f52202f2c106080ea5ab4ab62aed122f9e7cf58a7475be5  .beagle/checks/T0210/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0210/check.sh'
budget: 80000 tokens
