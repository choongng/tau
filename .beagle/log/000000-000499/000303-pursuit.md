+++
id = "000303-pursuit"
ordinal = 303
kind = "pursuit"
timestamp = "2026-10-03T20:13:19+00:00"
summary = "pursuit open T0072: bare-label milestone and part titles take their title from the intent; drop .beagle criteria at founding"
metric_command = ""
drains = []
hooks = []
+++

criteria: Where a 'title::intent' part or milestone is split (_add_children, the founding repair), a title matching ^[A-Za-z]{0,3}[0-9]+$ (M1, P4, 3) is replaced by _task_title(intent), and the intent kept. At founding, a criterion about .beagle/ or being a 'beagle pursuit project' is dropped, with a note in the founding result as for the setup milestone. R09: tasks titled M1..M4, P1..P5; the criterion 'packaged as a beagle pursuit project (.beagle/ present, tracked)' was kept and T0002's step named .beagle/ in scope.
decided by: sh -c 'echo "1176926bca2c74510ff4c2ef05e291223decae471a8f68c35e65a93b6eb99616  .beagle/checks/T0072/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0072/check.sh'
budget: 35000 tokens
