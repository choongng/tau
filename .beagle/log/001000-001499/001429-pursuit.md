+++
id = "001429-pursuit"
ordinal = 1429
kind = "pursuit"
timestamp = "2026-10-10T02:29:48+00:00"
summary = "pursuit prove T0226: WITNESSED — refuses when R24.md's `17 of 20 hit the 31-turn cap` is put back as `17 of 20 hit the 31-turn cap (earlier: 18 of 20…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "afcb86835f24d310a545ab2c7dd419812c6e8f3c5a49b61d10a3de56fd8c3b91  .beagle/checks/T0226/T0226.sh" | sha256sum -c --quiet && bash .beagle/checks/T0226/T0226.sh'
refutes: refuses when R24.md's `17 of 20 hit the 31-turn cap` is put back as `17 of 20 hit the 31-turn cap (earlier: 18 of 20…` (proven 2026-10-10T02:29:48+00:00; refused at R24.md still says 18 of 20)
refused after 0s of a 1m42s check at: R24.md still says 18 of 20
refused with: R24.md still says 18 of 20
