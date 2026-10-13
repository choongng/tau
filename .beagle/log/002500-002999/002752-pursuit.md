+++
id = "002752-pursuit"
ordinal = 2752
kind = "pursuit"
timestamp = "2026-10-13T20:09:41+00:00"
summary = "pursuit prove T0532: WITNESSED — refuses when eval.md's `| R96 | q35 | wrenfold |` is put back as `| R96? | q35 | wrenfold |`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "950191279767ab22c2615d623c130aec3f06987ade88789683bb42b0959dabad  .beagle/checks/T0532/T0532.sh" | sha256sum -c --quiet && bash .beagle/checks/T0532/T0532.sh'
refutes: refuses when eval.md's `| R96 | q35 | wrenfold |` is put back as `| R96? | q35 | wrenfold |` (proven 2026-10-13T20:08:39+00:00; refused at no R96 row with 50/54 in eval.md)
refused after 0s of a 0s check at: no R96 row with 50/54 in eval.md
refused with: no R96 row with 50/54 in eval.md
