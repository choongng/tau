+++
id = "000142-pursuit"
ordinal = 142
kind = "pursuit"
timestamp = "2026-10-03T16:10:59+00:00"
summary = "pursuit open T0048: new_route checks before it spawns, and its successor opens"
metric_command = ""
drains = []
hooks = []
+++

criteria: Per R06.md (dev-notes/itc-runs/R06.md) [tau] classes on new_route, the successor's criteria, 'superseded' wording, the escalation's plan option, and abandoning a milestone successor: pursuit_step new_route runs the done_when checks (_check_problem and already-passes) before it spawns, so a refused route leaves no successor; a sibling_of successor opens with its predecessor's criteria (or beagle's criteria-delta form) and is not refused for drift; a superseded task is described as superseded by its heir, not as a container; pursuit_plan on an open leaf splits into two or more parts and its refusal says that a plan needs two or more; and a successor of a superseded milestone can be abandoned when the driver gives a reason.
decided by: sh -c 'echo "42ca696d944107961b7f9e704483896ae75a971f62343e7d943a2735ebb4bca5  .beagle/checks/T0048/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0048/check.sh'
budget: 80000 tokens
