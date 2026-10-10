#!/bin/bash
# Audit 12 (T0337): R38.md's output-limit class names the tests built for it
# (T0330, T0331), names the tau-subagents cause and its commit, and no longer
# says 'upstream: none' now that upstream.md has '## R38'. R38's own diagnose
# check (T0326) still passes.
set -eu
bash .beagle/checks/T0326/T0326.sh >/dev/null
python3 - dev-notes/itc-runs/R38.md <<'PY'
import re, sys
md = open(sys.argv[1]).read()
cls = [c for c in re.split(r"^(?=### )", md, flags=re.M) if c.startswith("### [tau] After a thinking-only cut-off")]
assert len(cls) == 1, "the output-limit class is missing"
c = cls[0]
for t in ["test_nudges_in_a_row_stay_bounded_with_a_steering_message_beside_one",
          "test_thinking_off_request_is_the_nudges_not_a_steering_reply",
          "test_thinking_off_twin_warns_once_when_the_build_fails"]:
    assert t in c, f"class 3 does not name {t}"
assert "reconnaissance finds" not in c, "class 3 still defers its tests to the reconnaissance"
assert "0236dfe" in c and "runtime_provider_config" in c, "class 3 does not name the tau-subagents cause and commit"
assert not re.search(r"^upstream: none", md, re.M), "R38.md still says upstream: none"
assert re.search(r"^upstream: .*## R38", md, re.M), "R38.md does not point at upstream.md's ## R38"
print("OK")
PY
