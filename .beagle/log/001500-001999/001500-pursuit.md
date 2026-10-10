+++
id = "001500-pursuit"
ordinal = 1500
kind = "pursuit"
timestamp = "2026-10-10T04:09:05+00:00"
summary = "pursuit prove T0353: WITNESSED — refuses when progress.py's `if passed > 0: return \"any-pass\"` is put back as `if passed > 99: return \"any-pass\"`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "d488d5c0099c1153594ca9c593fe843f06ebc9c533e563cf31573b139c20dad2  .beagle/checks/T0353/T0353.sh" | sha256sum -c --quiet && bash .beagle/checks/T0353/T0353.sh'
refutes: refuses when progress.py's `if passed > 0: return "any-pass"` is put back as `if passed > 99: return "any-pass"` (proven 2026-10-10T04:08:05+00:00; refused at stage wrong for R34: R34 qwen cobs 7/44 implementation)
refused after 0s of a 0s check at: stage wrong for R34: R34 qwen cobs 7/44 implementation
refused with: stage wrong for R34: R34 qwen   cobs     7/44  implementation
standing checks red: T0074
