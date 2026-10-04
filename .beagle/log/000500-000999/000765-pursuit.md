+++
id = "000765-pursuit"
ordinal = 765
kind = "pursuit"
timestamp = "2026-10-04T21:37:31+00:00"
summary = "pursuit open T0177: harness: second task cobs"
metric_command = ""
drains = []
hooks = []
+++

criteria: The harness runs and scores a second task. launch.sh takes RNN mimo|qwen [itc|cobs] (default itc): project dir ~/<task>, prompt ~/tautest/<task>_prompt.txt byte for byte, task recorded in meta.json, sessions found for that dir, previous dir set aside per task. A hidden grader grade_cobs.py (adapter: encode/decode) has >=40 cases incl. Wikipedia's examples; a reference adapter passes all, a broken one fails some. scored.sh v4 takes RNN model task and checks meta's task and that prompt; its selftest refuses a wrong task.
decided by: sh -c 'echo "0700f47f7309612bd7c2fc14ecd0f6eced3eb99770a50834abc1dfc16407e13c  .beagle/checks/T0177/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0177/check.sh'
budget: 120000 tokens
