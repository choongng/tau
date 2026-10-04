+++
id = "000786-pursuit"
ordinal = 786
kind = "pursuit"
timestamp = "2026-10-04T23:21:43+00:00"
summary = "pursuit open T0202: Worker guard: explain a truncated tool call; inline script after cd; scratch-path refusal text"
metric_command = ""
drains = []
hooks = []
+++

criteria: The worker guard blocks a call whose arguments are only _raw_arguments with a reason saying the call was cut off after N characters and nothing was written, and to write the file in parts; inline-script write targets resolve against the directory a leading cd chain leaves; a refused scratch/explore script outside the project is not told the implementation does not go under tests/.
decided by: sh -c 'echo "e0c287dcb4010fd208abd21d2a804086075c58f46a09a313bdcc0dbd824d53a5  .beagle/checks/T0202/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0202/check.sh'
budget: 120000 tokens
