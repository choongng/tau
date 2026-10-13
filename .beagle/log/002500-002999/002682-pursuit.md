+++
id = "002682-pursuit"
ordinal = 2682
kind = "pursuit"
timestamp = "2026-10-13T07:01:25+00:00"
summary = "pursuit prove T0524: WITNESSED — refuses when contract.py's `if os.environ.get(ACCEPTANCE_ENV):` is put back as `if False:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "8d7a464a230155b87ba938436b93918fbdfe37a6ce1dc71a9a60ad47244a3ab6  .beagle/checks/T0524/T0524.sh" | sha256sum -c --quiet && bash .beagle/checks/T0524/T0524.sh'
refutes: refuses when contract.py's `if os.environ.get(ACCEPTANCE_ENV):` is put back as `if False:` (proven 2026-10-13T07:00:26+00:00; refused at 1 failed, 52 deselected in 0.13s)
refused after 0s of a 1s check at: 1 failed, 52 deselected in 0.13s
refused with: 1 failed, 52 deselected in 0.13s
