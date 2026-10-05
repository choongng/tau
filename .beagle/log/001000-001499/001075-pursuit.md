+++
id = "001075-pursuit"
ordinal = 1075
kind = "pursuit"
timestamp = "2026-10-05T11:53:47+00:00"
summary = "pursuit open T0261: Non-code task under tests/ refused at open; unproven with no module offers abandon"
metric_command = ""
drains = []
hooks = []
+++

criteria: pursuit_step refuses opening a task whose check reads only non-.py files under tests/ and whose scope holds no source or cases data, naming the file and offering to fold it into the known-answers task or abandon; pursuit_plan refuses a part that is only reading a reference (judged on the head before ':'); a not-proven result for a task whose scope holds no module offers pursuit_step abandon instead of mutating a module.
decided by: sh -c 'echo "bfbf97b549e6895bbe51d741ac79e1f02cdfabc66c4b070ec412ef2c5977471d  .beagle/checks/T0261/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0261/check.sh'
budget: 70000 tokens
