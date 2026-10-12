#!/bin/bash
# T0508: q35 re-run on itc and cobs with line anchors, on a beagle that has T0498 and T0503 and a
# tau whose workers, task or not, read references by `contract refs` (T0502, T0505, T0507);
# both graded, and dev-notes/contract-first/eval.md reports the grades the graders give.
set -e
H=/home/choong/tautest/itc-harness
cd "$H"
python3 - <<'PY'
import json, os, re, subprocess, sys
PLAN = {  # run: (model, task)
    "R81": ("qwen3.6-35b-q6-mtp-thinking-coding", "itc"),
    "R82": ("qwen3.6-35b-q6-mtp-thinking-coding", "cobs"),
}
# The beagle each ran holds T0503's bare-cite refusal (after T0498's anchors), and
# the tau holds T0502, T0505 and T0507: every worker may run `contract refs`, uncounted.
ANCHORS = "fce5dac"
TAU_GUARD = "eab231f1"
notes = open("/home/choong/tautest/tau/dev-notes/contract-first/eval.md").read()
progress = subprocess.run([sys.executable, "progress.py"], capture_output=True, text=True, check=True).stdout
for run, (model, task) in PLAN.items():
    d = f"runs/{run}"
    meta, ex = json.load(open(f"{d}/meta.json")), json.load(open(f"{d}/exit.json"))
    assert (meta["model"], meta["task"]) == (model, task), (run, meta["model"], meta["task"])
    assert meta["tau_dirty_code_files"] == 0, (run, meta["tau_dirty_code_paths"])
    if run.startswith("R"):
        assert meta["arm"] == "full" and meta["beagle_version"] == "beagle 0.47.0", (run, meta["beagle_version"])
        assert meta["beagle_rev"].startswith("contract-first ") and meta["beagle_dirty_code_files"] == 0, (run, meta["beagle_rev"])
        assert meta["beagle_root"].endswith("/beagle-wt/contract-first"), run
        sha = meta["beagle_rev"].split()[1]
        assert subprocess.run(["git", "-C", meta["beagle_root"], "merge-base", "--is-ancestor", ANCHORS, sha]).returncode == 0, (run, sha)
        assert subprocess.run(["git", "-C", "/home/choong/tautest/tau", "merge-base", "--is-ancestor", TAU_GUARD, meta["tau_sha"]]).returncode == 0, (run, meta["tau_sha"])
        assert os.path.exists(f"{d}/scorecard.json"), run
    # The grade on file is the grader's, re-run now over the run's adapter.
    out = subprocess.run([sys.executable, f"grade_{task}.py", "--adapter", f"{d}/adapter.py", "--json"],
                         capture_output=True, text=True, timeout=900)
    g, kept = json.loads(out.stdout), json.load(open(f"{d}/grade.json"))
    assert (g["passed"], g["total"]) == (kept["passed"], kept["total"]), (run, g["passed"], kept["passed"])
    grade = f"{g['passed']}/{g['total']}"
    assert re.search(rf"^{run}\s+\S+\s+{task}\s+{grade}\s", progress, re.M), (run, grade)
    assert re.search(rf"^\|\s*{run}\s*\|.*\|\s*{grade}\s*\|", notes, re.M), (run, grade, "not in eval.md")
print("T0508: R81 itc and R82 cobs on q35 with anchors, graded, grades re-derived and in eval.md")
PY
