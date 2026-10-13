+++
id = "002614-pursuit"
ordinal = 2614
kind = "pursuit"
timestamp = "2026-10-13T01:01:07+00:00"
summary = "pursuit prove T0512: WITNESSED — refuses when contract.py's `defined.setdefault(bare(op), (op, _text(entry.g…` is put back as `defined.setdefault(op, (op, _text(entry.get(\"id…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "aad4b0e5ec2c2c48564bcd64d2ccb12637d03bbab49788e1881607772c911bc6  .beagle/checks/T0512/T0512.sh" | sha256sum -c --quiet && bash .beagle/checks/T0512/T0512.sh'
refutes: refuses when contract.py's `defined.setdefault(bare(op), (op, _text(entry.g…` is put back as `defined.setdefault(op, (op, _text(entry.get("id…` (proven 2026-10-13T01:00:08+00:00; refused at - acceptance directory contract/ holds no test: write the one that loads contract/contract.json and runs every
refused after 1s of a 1s check at: - acceptance directory contract/ holds no test: write the one that loads contract/contract.json and runs every entry th…
refused with: - acceptance directory contract/ holds no test: write the one that loads contract/contract.json and runs every entry there.
replaces: still passes with the defect put back in contract.py (exit 0), measured 2026-10-13T01:00:02+00:00
