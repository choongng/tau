+++
id = "002624-pursuit"
ordinal = 2624
kind = "pursuit"
timestamp = "2026-10-13T03:44:46+00:00"
summary = "pursuit prove T0516: WITNESSED — refuses when beagle.py's `return {e for e in own if Path(e).parts[:1] != …` is put back as `return {e for e in own if Path(e).parts[:1] != …`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "01a3a078eee3e10c686fa1b08ed5226b035e3196832872578dcd71033b83fe8a  .beagle/checks/T0516/T0516.sh" | sha256sum -c --quiet && bash .beagle/checks/T0516/T0516.sh'
refutes: refuses when beagle.py's `return {e for e in own if Path(e).parts[:1] != …` is put back as `return {e for e in own if Path(e).parts[:1] != …` (proven 2026-10-13T03:43:48+00:00; refused at 1 failed, 3 passed, 834 deselected in 1.47s)
refused after 2s of a 2s check at: 1 failed, 3 passed, 834 deselected in 1.47s
refused with: 1 failed, 3 passed, 834 deselected in 1.47s
