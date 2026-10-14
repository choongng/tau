+++
id = "002906-pursuit"
ordinal = 2906
kind = "pursuit"
timestamp = "2026-10-14T01:43:44+00:00"
summary = "pursuit open T0564: beagle: refuse a check whose '! cmd' under set -e cannot refuse"
metric_command = ""
drains = []
hooks = []
+++

criteria: open and amend refuse a check script under set -e (set -e, set -eu, set -euo pipefail, bash -e shebang) holding a command negated with ! that is not its last command, naming the line and the rewrite (if CMD; then exit 1; fi); a ! as the last command is allowed; tests negation_under_set_e_refused and negation_as_last_command_allowed pass and ci/check.sh is green.
decided by: sh -c 'echo "3e59e1ec2981786c84105385f25f92b6bde849aa6915eeee0b31b3af04843ad7  .beagle/checks/T0564/T0564.sh" | sha256sum -c --quiet && bash .beagle/checks/T0564/T0564.sh'
budget: 120000 tokens
opened over T0563: runs beside T0559 on a disjoint scope (beagle rotation-fixes); small, and every check written from here on benefits
