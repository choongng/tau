+++
id = "000707-pursuit"
ordinal = 707
kind = "pursuit"
timestamp = "2026-10-04T14:08:42+00:00"
summary = "pursuit open T0166: A setup task's .beagle refusal says abandon it, and the abandon succeeds"
metric_command = ""
drains = []
hooks = []
+++

criteria: When pursuit_step is sent for a task whose title is a setup milestone (as _setup_milestone reads it) and is refused, the refusal leads by saying the task is the setup pursuit_found already did and to abandon it 'done by founding'; and that abandon succeeds without naming a done task, after which the tasks waiting on it are ready.
decided by: sh -c 'echo "3928a90bbc3598073f70af99a00d60ab872ceec2b0636abe0215b5780adee89e  .beagle/checks/T0166/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0166/check.sh'
budget: 40000 tokens
