+++
id = "003015-pursuit"
ordinal = 3015
kind = "pursuit"
timestamp = "2026-10-14T04:23:24+00:00"
summary = "pursuit prove T0565: WITNESSED — refuses when T0245.v2.sh's `if grep -q \"has no infeasible verdict\" $f; then…` is put back as `! grep -q \"has no infeasible verdict\" $f`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "a518758c8185dcfc2efe3c115dd49117cc1ce46ec6ac56e4993d9306c7668887  .beagle/checks/T0565/T0565.sh" | sha256sum -c --quiet && bash .beagle/checks/T0565/T0565.sh'
refutes: refuses when T0245.v2.sh's `if grep -q "has no infeasible verdict" $f; then…` is put back as `! grep -q "has no infeasible verdict" $f` (proven 2026-10-14T04:23:23+00:00; refused at Traceback (most recent call last):)
refused after 4s of a 6s check at: Traceback (most recent call last):
refused with: beagle.pursuit.PursuitError: this check has `! grep -q "has no infeasible verdict" $f` on line 4 under `set -e`, where bash does not exit when a command negated with `!` fails (POSIX exempts it), so this step can never refuse. Write `if grep -q "has no infeasible verdict" $f; then echo "forbidden found"; exit 1; fi` instead; a `!` on the last command is fine, its status being the script's.
