+++
id = "000588-pursuit"
ordinal = 588
kind = "pursuit"
timestamp = "2026-10-04T08:42:20+00:00"
summary = "pursuit open T0141: Cases-first order on plans, and waits named"
metric_command = ""
drains = []
hooks = []
+++

criteria: pursuit_plan refuses (in tau, before beagle) an ordered plan whose implementation part comes before its known-answers part, saying which part to put first; the cases-first hint names an existing known-answers sibling instead of splitting the task under a new one, and names the data-test done_when; pursuit_step on a task that waits names the task(s) it waits on and which is workable, never 'a container, or it waits'.
decided by: sh -c 'echo "6e81bf2778b2f8f8267798dc68e5ca20dff8eec17b0af55aec17b0678b08cc07  .beagle/checks/T0141/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0141/check.sh'
budget: 70000 tokens
