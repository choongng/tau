#!/bin/bash
# T0398: mine/indicators.py reports time sinks, worker outcomes, tau-level stops,
# driver-side implementation work and per-kind recovery, each recounted here.
set -e
cd /home/choong/tautest/itc-harness
python3 -m pytest -q mine/test_indicators.py
OUT=$(mktemp -d)
python3 mine/events.py --runs runs --out "$OUT/events.jsonl"
python3 mine/refusals.py --events "$OUT/events.jsonl" --out "$OUT/refusals.json" --rows "$OUT/refused.jsonl"
python3 mine/indicators.py --events "$OUT/events.jsonl" --refused "$OUT/refused.jsonl" --kinds "$OUT/refusals.json" --out "$OUT/ind.json"
python3 - "$OUT" <<'PY'
import json, sys, collections as C
out = sys.argv[1]
ev = [json.loads(l) for l in open(f"{out}/events.jsonl")]
refused = {(r["session"], r["line"]): r for r in map(json.loads, open(f"{out}/refused.jsonl"))}
ind = json.load(open(f"{out}/ind.json"))
for key in ("time", "sinks", "workers", "stops", "driver_work", "recovery"):
    assert key in ind and ind[key], f"{key} missing or empty"
# time: driver model minutes recounted from stop rows
dm = C.defaultdict(float)
for r in ev:
    if r["kind"] == "stop" and r["role"] == "driver":
        dm[r["run"]] += (r.get("duration_s") or 0) / 60
for run, t in ind["time"].items():
    assert abs(t["driver_model_min"] - dm[run]) < 0.05, f"{run} driver_model_min {t['driver_model_min']} != {dm[run]:.2f}"
    for k in ("driver_tool_min", "worker_model_min", "worker_tool_min", "wall_min"):
        assert k in t, f"{run} time lacks {k}"
assert set(ind["time"]) == {r["run"] for r in ev}, "time does not cover every run"
assert len(ind["sinks"]) >= 20 and all({"run", "role", "tool", "seconds", "line"} <= set(s) for s in ind["sinks"])
assert ind["sinks"] == sorted(ind["sinks"], key=lambda s: -s["seconds"]), "sinks not ordered by seconds"
# workers: every worker session exactly once, a named outcome each
ws = {(r["run"], r["session"]) for r in ev if r["role"] != "driver"}
got = [(w["run"], w["session"]) for w in ind["workers"]]
assert len(got) == len(set(got)) and set(got) == ws, f"workers: {len(set(got))} listed, {len(ws)} in the table"
outcomes = C.Counter(w["outcome"] for w in ind["workers"])
assert len(outcomes) >= 4 and all(w.get("evidence") for w in ind["workers"]), outcomes
assert any(w["run"] == "R25" and w["outcome"] == "capped" for w in ind["workers"]), "R25's worker killed by the cap not found"
# stops: every stop that is not toolUse/stop, with its attribution evidence
odd = {(r["session"], r["line"]) for r in ev if r["kind"] == "stop" and r["stop_reason"] not in ("toolUse", "stop")}
listed = {(s["session"], s["line"]) for s in ind["stops"]}
assert listed == odd, f"stops: {len(listed)} listed, {len(odd)} in the table"
for s in ind["stops"]:
    if s.get("stop_by") == "breaker":
        assert s.get("streak", 0) >= 1, f"breaker stop without a refused streak before it: {s}"
# driver work: every driver write/edit call is listed
dw = {(r["session"], r["line"]) for r in ev if r["kind"] == "tool_call" and r["role"] == "driver" and r["tool"] in ("write", "edit")}
dl = {(d["session"], d["line"]) for d in ind["driver_work"]}
assert dw <= dl, f"{len(dw - dl)} driver write/edit calls not listed"
# recovery: per kind, recovered + not recovered == that kind's driver refusals
drv = C.Counter(r["refusal"] for r in refused.values() if r["role"] == "driver")
for k, v in ind["recovery"].items():
    assert v["recovered"] + v["unrecovered"] == drv[k], f"recovery {k}: {v} vs {drv[k]}"
assert set(ind["recovery"]) == set(drv), "recovery does not cover every driver refusal kind"
print(f"OK runs={len(ind['time'])} workers={len(got)} outcomes={dict(outcomes)} stops={len(listed)} driver_work={len(dl)} kinds={len(drv)}")
PY
rm -rf "$OUT"
python3 -m ruff check mine/ 2>/dev/null || uvx ruff check mine/
