+++
id = "002940-pursuit"
ordinal = 2940
kind = "pursuit"
timestamp = "2026-10-14T03:04:40+00:00"
summary = "pursuit open T0574: harness: a run's PATH does not lead with the tau-harness venv (S01 #11)"
metric_command = ""
drains = []
hooks = []
+++

criteria: launch.sh no longer puts tau-harness/.venv/bin on the PATH the run inherits: it runs tau by its absolute path in that venv, keeps beagle's CLI first on PATH, and --dry-run prints a 'run PATH: <the PATH the run gets>' line; the dry run shows the tau path.
decided by: sh -c 'echo "888c847eeb59be8774b6ada5030b57cec3412b1e34baa5a281de72d61079960b  .beagle/checks/T0574/T0574.sh" | sha256sum -c --quiet && bash .beagle/checks/T0574/T0574.sh'
budget: 40000 tokens
opened over T0565, T0575, T0569, T0572, T0573: a different lane (itc-harness) from the tau and beagle fixes; one line, and every run's environment depends on it
