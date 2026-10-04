+++
id = "000749-pursuit"
ordinal = 749
kind = "pursuit"
timestamp = "2026-10-04T16:53:42+00:00"
summary = "pursuit open T0173: Open closes without a worker when uncommitted work already passes"
metric_command = ""
drains = []
hooks = []
+++

criteria: When pursuit_step opens a task whose check already passes and passes only by uncommitted work, no worker is dispatched: the step goes straight to the pre-close checks and the proof, and closes if they pass; when the only proof found is the file-absent fallback, one worker is sent with a brief asking only for a mutation that shows the check can refuse.
decided by: sh -c 'echo "a374cb5d572a865d8cf84fba328dedda3712a04f18caaa47807e63654918f998  .beagle/checks/T0173/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0173/check.sh'
budget: 50000 tokens
