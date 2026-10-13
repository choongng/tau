+++
id = "002654-pursuit"
ordinal = 2654
kind = "pursuit"
timestamp = "2026-10-13T06:05:12+00:00"
summary = "pursuit prove T0498: WITNESSED — refuses when pursuit.md's `Each entry cites the lines it was read from by …` is put back as `Each entry quotes the lines it was read from:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "4c4c65dbdf81ee6ab9d2c0f3f17ac8a261f7effcea37a91e06fb88248ae8d058  .beagle/checks/T0498/T0498.v2.sh" | sha256sum -c --quiet && bash .beagle/checks/T0498/T0498.v2.sh'
refutes: refuses when pursuit.md's `Each entry cites the lines it was read from by …` is put back as `Each entry quotes the lines it was read from:` (proven 2026-10-13T06:05:12+00:00; refused at pursuit.md does not teach the anchor cite)
refused after 6s of a 7s check at: pursuit.md does not teach the anchor cite
refused with: pursuit.md does not teach the anchor cite
