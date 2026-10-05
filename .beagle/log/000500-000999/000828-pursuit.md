+++
id = "000828-pursuit"
ordinal = 828
kind = "pursuit"
timestamp = "2026-10-05T01:45:38+00:00"
summary = "pursuit prove T0210: WITNESSED — refuses when scored.sh's `assert sha7 in \" \".join(para), f\"{R}.md summary…` is put back as `pass`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "6fdc4946ed4cc0a65f52202f2c106080ea5ab4ab62aed122f9e7cf58a7475be5  .beagle/checks/T0210/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0210/check.sh'
refutes: refuses when scored.sh's `assert sha7 in " ".join(para), f"{R}.md summary…` is put back as `pass` (proven 2026-10-05T01:44:42+00:00; refused at FAIL summary names the wrong tau sha: wanted refuse, got pass)
refused after 1s of a 2s check at: FAIL summary names the wrong tau sha: wanted refuse, got pass
refused with: selftest: 1 failed
replaces: still passes with the defect put back in scored.sh (exit 0), measured 2026-10-05T01:44:29+00:00
