#!/bin/bash
# T0521: the audit's short checks are amended. T0498, T0508, T0516 and T0518 are
# done and WITNESSED again under their new (v2) checks; T0503, T0512, T0513,
# T0514 and T0516 declare their CI clause untested and name T0523, which is done
# and witnessed; the tests the new checks run are on tau-wt-ops at a488c0d8.
set -e
cd /home/choong/tautest/tau
BEAGLE=/home/choong/beagle-wt/contract-first/plugins/beagle-pursuit/bin/beagle
python3 - "$BEAGLE" <<'PY'
import hashlib, json, re, subprocess, sys
beagle = sys.argv[1]
def show(t):
    out = subprocess.run([beagle, "pursuit", "show", t], capture_output=True, text=True, check=True).stdout
    return json.loads(out)
for t in ("T0498", "T0508", "T0516", "T0518"):
    r = show(t)
    script = f".beagle/checks/{t}/{t}.v2.sh"
    assert r["status"] == "done", (t, r["status"])
    assert script in r["done_when"], (t, "done_when is not the v2 check", r["done_when"])
    sha = hashlib.sha256(open(script, "rb").read()).hexdigest()
    assert f"{sha}  {script}" in r["check_files"], (t, "v2 script is not the one pinned")
    assert r["refutes"] and not r["witness_failed"], (t, "not witnessed", r["witness_failed"])
    amended = re.findall(r"amended check at (\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\+00:00)", r["body"])
    proven = re.search(r"\(proven (\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\+00:00);", r["refutes"])
    assert amended and proven and proven[1] > amended[-1], (t, "witness predates the amend", amended, proven)
for t in ("T0503", "T0512", "T0513", "T0514", "T0516"):
    r = show(t)
    assert r["status"] == "done", (t, r["status"])
    assert any(u.startswith(("beagle CI green", "Tau tests and beagle CI pass")) and "T0523" in u
               for u in r["untested"]), (t, "CI clause not declared untested", r["untested"])
ci = show("T0523")
assert ci["status"] == "done" and ci["refutes"] and not ci["witness_failed"], ("T0523", ci["status"])
assert "bash ci/check.sh" in open(".beagle/checks/T0523/T0523.sh").read()
print("T0521: T0498, T0508, T0516, T0518 witnessed under v2 checks; CI clauses untested -> T0523 done")
PY
tests=$(git -C /home/choong/tautest/tau-wt-ops show a488c0d8:tests/test_beagle_example_extension.py)
echo "$tests" | grep -q "def test_pursuit_step_scopes_the_contract_and_reconcile_itself("
echo "$tests" | grep -q "def test_open_refuses_a_check_whose_program_is_not_here("
echo "T0521: done"
