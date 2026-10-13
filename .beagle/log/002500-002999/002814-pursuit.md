+++
id = "002814-pursuit"
ordinal = 2814
kind = "pursuit"
timestamp = "2026-10-13T21:37:28+00:00"
summary = "pursuit open T0550: tau ext: a task whose check passed is not dispatched to a second worker (R97 T0005)"
metric_command = ""
drains = []
hooks = []
+++

criteria: Why R97's T0005 got a second worker after its first passed the check is read from the R97 session (~/.tau/sessions/home-semver-8dc209) and the extension, and fixed: a task whose first worker leaves the check passing with files new since the open is proven by the extension's own witnesses and closed, with no second worker; test *passed_check_is_proven_without_a_second_worker reproduces R97's case and passes; the extension test file fails no test beyond the 37 known
decided by: sh -c 'echo "94ef83db90e1546a47c362a1aed7206e8ea39ce24e03d6f2c9fb441b2cdb25ec  .beagle/checks/T0550/T0550.sh" | sha256sum -c --quiet && bash .beagle/checks/T0550/T0550.sh'
budget: 120000 tokens
