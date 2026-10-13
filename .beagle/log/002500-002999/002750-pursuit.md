+++
id = "002750-pursuit"
ordinal = 2750
kind = "pursuit"
timestamp = "2026-10-13T20:04:51+00:00"
summary = "pursuit amend T0523"
metric_command = ""
drains = []
hooks = []
+++

audit 10-13 part 1: the check ran CI in the live worktree, where an untracked __pycache__ from a pytest run turned the plugin-tree gate red; v2 runs it on a clean detached checkout of the tip with the worktree's uv.lock files
was: sh -c 'echo "efc6f520edd04445c565c2dc45e5ca675b97288d90361ab066918767ea230641  .beagle/checks/T0523/T0523.sh" | sha256sum -c --quiet && bash .beagle/checks/T0523/T0523.sh'
  efc6f520edd04445c565c2dc45e5ca675b97288d90361ab066918767ea230641  .beagle/checks/T0523/T0523.sh
now: sh -c 'echo "5fa630f6bc2627a853eae0538380c0e86ebe11548c344843856b64e728087c1c  .beagle/checks/T0523/T0523.v2.sh" | sha256sum -c --quiet && bash .beagle/checks/T0523/T0523.v2.sh'
