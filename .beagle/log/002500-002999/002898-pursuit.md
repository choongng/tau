+++
id = "002898-pursuit"
ordinal = 2898
kind = "pursuit"
timestamp = "2026-10-14T01:37:01+00:00"
summary = "pursuit amend T0558"
metric_command = ""
drains = []
hooks = []
+++

under set -e, bash does not exit on a failing command negated with !, so the mid-script '! grep' step never refused; rewritten as if grep ...; then exit 1 (found at T0493's prove)
was: sh -c 'echo "6401105ad360796b48c045d76c7565c2ddd97ef7b32210d0061c7b4c91bf3cbb  .beagle/checks/T0558/T0558.sh" | sha256sum -c --quiet && bash .beagle/checks/T0558/T0558.sh'
  6401105ad360796b48c045d76c7565c2ddd97ef7b32210d0061c7b4c91bf3cbb  .beagle/checks/T0558/T0558.sh
now: sh -c 'echo "4f6530038a9890959abc763d4206f646bea8834ccbe1c9b5e989a0351b7ac8ca  .beagle/checks/T0558/T0558.v2.sh" | sha256sum -c --quiet && bash .beagle/checks/T0558/T0558.v2.sh'
