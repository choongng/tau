+++
id = "002558-pursuit"
ordinal = 2558
kind = "pursuit"
timestamp = "2026-10-12T21:10:17+00:00"
summary = "pursuit prove T0498: WITNESSED — refuses when contract.py's `if anchor_hash(lines[n - 1]) != h:` is put back as `if False:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "c0fac397f490bc473128daa42a955f64e42c2618c9a57f8a4a9313f4ca62075a  .beagle/checks/T0498/T0498.sh" | sha256sum -c --quiet && bash .beagle/checks/T0498/T0498.sh'
refutes: refuses when contract.py's `if anchor_hash(lines[n - 1]) != h:` is put back as `if False:` (proven 2026-10-12T21:09:20+00:00; refused at - entry E002's cite '1#000-80#000' spans 80 lines, and a cite holds at most 12: cite the lines that pin the entry down.)
refused after 2s of a 4s check at: - entry E002's cite '1#000-80#000' spans 80 lines, and a cite holds at most 12: cite the lines that pin the entry down.
refused with: - entry E002's cite '1#000-80#000' spans 80 lines, and a cite holds at most 12: cite the lines that pin the entry down.
