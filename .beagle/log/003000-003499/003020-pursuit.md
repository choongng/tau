+++
id = "003020-pursuit"
ordinal = 3020
kind = "pursuit"
timestamp = "2026-10-14T04:31:58+00:00"
summary = "pursuit prove T0226: WITNESSED — refuses when R24.md's `17 of 20 hit the 31-turn cap` is put back as `18 of 20 hit the 31-turn cap`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "d327d2ce69d0fa1d23092d158c1e9f761440068adef4c770eb89446334d99ed6  .beagle/checks/T0226/T0226.v2.sh" | sha256sum -c --quiet && bash .beagle/checks/T0226/T0226.v2.sh'
refutes: refuses when R24.md's `17 of 20 hit the 31-turn cap` is put back as `18 of 20 hit the 31-turn cap` (proven 2026-10-14T04:31:58+00:00; refused at R24.md still says 18 of 20)
refused after 0s of a 1s check at: R24.md still says 18 of 20
refused with: R24.md still says 18 of 20
