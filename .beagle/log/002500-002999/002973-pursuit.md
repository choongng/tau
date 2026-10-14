+++
id = "002973-pursuit"
ordinal = 2973
kind = "pursuit"
timestamp = "2026-10-14T03:50:49+00:00"
summary = "pursuit prove T0568: WITNESSED — refuses when beagle.py's `words = argv[1 : argv.index(\"--\")] if \"--\" in a…` is put back as `words = argv[1:]`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "974ca3bcd698ecadc71f0421d87883550ec4b452e06ca97eba93fc611e658885  .beagle/checks/T0568/T0568.sh" | sha256sum -c --quiet && bash .beagle/checks/T0568/T0568.sh'
refutes: refuses when beagle.py's `words = argv[1 : argv.index("--")] if "--" in a…` is put back as `words = argv[1:]` (proven 2026-10-14T03:50:48+00:00; refused at 1 failed, 1 passed, 721 deselected in 0.75s)
refused after 1s of a 3m58s check at: 1 failed, 1 passed, 721 deselected in 0.75s
refused with: 1 failed, 1 passed, 721 deselected in 0.75s
