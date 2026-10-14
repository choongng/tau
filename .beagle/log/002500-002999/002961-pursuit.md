+++
id = "002961-pursuit"
ordinal = 2961
kind = "pursuit"
timestamp = "2026-10-14T03:37:26+00:00"
summary = "pursuit prove T0567: WITNESSED — refuses when beagle.py's `[f\"{CONTRACT_DIR}/\", f\"{REFERENCES_DIR}/\"],` is put back as `[f\"{CONTRACT_DIR}/\"],`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "0ee789dc73a491b7693ed698e6ba4e45f2fc4f15f4c0ec7e1ec8e997ef0ff789  .beagle/checks/T0567/T0567.sh" | sha256sum -c --quiet && bash .beagle/checks/T0567/T0567.sh'
refutes: refuses when beagle.py's `[f"{CONTRACT_DIR}/", f"{REFERENCES_DIR}/"],` is put back as `[f"{CONTRACT_DIR}/"],` (proven 2026-10-14T03:37:25+00:00; refused at 1 failed, 1 passed, 719 deselected in 4.92s)
refused after 6s of a 2m56s check at: 1 failed, 1 passed, 719 deselected in 4.92s
refused with: 1 failed, 1 passed, 719 deselected in 4.92s
