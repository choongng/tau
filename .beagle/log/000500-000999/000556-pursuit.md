+++
id = "000556-pursuit"
ordinal = 556
kind = "pursuit"
timestamp = "2026-10-04T06:53:09+00:00"
summary = "pursuit open T0134: Plan parts: split multi-line parts, cut long titles, decide one-part in tau"
metric_command = ""
drains = []
hooks = []
+++

criteria: pursuit_plan splits a part that holds several lines into one part per line, dropping a line that only reruns a check (e.g. 'Run the check: ...') with a note in its result; a plan left with one part on a leaf is refused by tau before beagle is called, with tau's own text; a part whose title would exceed beagle's 200-character cap is cut at ' — ' or '::' (title before, the rest as its intent) as founding already does, and never reaches beagle over the cap.
decided by: sh -c 'echo "b0a6fea68adec4aef5fab135bd06fc26df6a59fb9279bb272f0f4476f20cf3ad  .beagle/checks/T0134/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0134/check.sh'
budget: 80000 tokens
