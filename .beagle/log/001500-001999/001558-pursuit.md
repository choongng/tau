+++
id = "001558-pursuit"
ordinal = 1558
kind = "pursuit"
timestamp = "2026-10-10T15:12:37+00:00"
summary = "pursuit open T0365: Driver edit refusal names the step for the ready task"
metric_command = ""
drains = []
hooks = []
+++

criteria: In a founded pursuit, make_driver_edit_guard's refusal (write/edit outside .beagle/, project-changing bash, the agent tool) names the pursuit_step call for the task beagle pursuit next offers: 'pursuit_step with task=<id>', the open task first, else the first ready one; with neither (or next failing), pursuit_step with no arguments. The refusal still says a sub-agent does the work and to put the intended change in the step's notes. The killed-check route (_KILLED_NOT_OPENED) keeps its own call. The task-naming lookup is one helper shared with _founded_dispatch_refusal, whose text stays as it is. No change to the tool list (owner: refusal-only). Workers, an unfounded project and BEAGLE_TAU_DRIVER_EDITS=1 stay unrefused. Tests test_driver_edit_refusal_names_the_step_for_the_ready_task, test_driver_edit_refusal_without_a_ready_task_names_bare_step; whole file passes, ruff clean.
decided by: sh -c 'echo "3911a126e28c0bed548ae56dc388ab008dafe4d19790bb7c59e04fe5331b6ba5  .beagle/checks/T0365/T0365.sh" | sha256sum -c --quiet && bash .beagle/checks/T0365/T0365.sh'
budget: 60000 tokens
