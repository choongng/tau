+++
id = "002386-pursuit"
ordinal = 2386
kind = "pursuit"
timestamp = "2026-10-12T14:22:38+00:00"
summary = "pursuit open T0467: A new route held at close sends its notes to a worker (R57)"
metric_command = ""
drains = []
hooks = []
+++

criteria: A new route on a judge-held task whose check passes on disk runs a worker briefed with the held demand and notes, instead of prove-and-hold with no worker (R57). Named test test_new_route_held_at_close_sends_its_notes_to_a_worker passes; suite and ruff pass.
decided by: sh -c 'echo "710605bb253c14579d62c74d30178b3592f3395f82fb3071674ce1e91c32880b  .beagle/checks/T0467/T0467.sh" | sha256sum -c --quiet && bash .beagle/checks/T0467/T0467.sh'
budget: 150000 tokens
