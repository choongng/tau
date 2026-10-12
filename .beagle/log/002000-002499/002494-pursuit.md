+++
id = "002494-pursuit"
ordinal = 2494
kind = "pursuit"
timestamp = "2026-10-12T16:46:27+00:00"
summary = "pursuit prove T0487: WITNESSED — refuses when pursuit-run.md's `- **exit 3, every leaf is settled, with a `[con…` is put back as `- **exit 3, every leaf is settled** → read the …`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "fb68dc049e92719a74fee7eb0bfa7317d4af92f747f2513b01513d880c1286d1  .beagle/checks/T0487/T0487.sh" | sha256sum -c --quiet && bash .beagle/checks/T0487/T0487.sh'
refutes: refuses when pursuit-run.md's `- **exit 3, every leaf is settled, with a `[con…` is put back as `- **exit 3, every leaf is settled** → read the …` (proven 2026-10-12T16:45:59+00:00)
refused after 0s of a 59s check
standing checks red: T0335, T0360, T0368, T0386, T0419, T0420, T0421, T0422, T0423, T0424, T0425, T0426
