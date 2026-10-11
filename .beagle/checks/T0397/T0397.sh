#!/bin/bash
# T0397: mine/contradictions.py finds refusals whose offered call was refused next,
# refusal kinds alternating on one task, and the same refusal repeated without progress.
set -e
cd /home/choong/tautest/itc-harness
python3 -m pytest -q mine/test_contradictions.py
OUT=$(mktemp -d)
python3 mine/events.py --runs runs --out "$OUT/events.jsonl"
python3 mine/refusals.py --events "$OUT/events.jsonl" --out "$OUT/refusals.json" --rows "$OUT/refused.jsonl"
python3 mine/contradictions.py --events "$OUT/events.jsonl" --refused "$OUT/refused.jsonl" --kinds "$OUT/refusals.json" --out "$OUT/findings.json"
python3 - "$OUT" <<'PY'
import json, sys
out = sys.argv[1]
ev = [json.loads(l) for l in open(f"{out}/events.jsonl")]
refused = {(r["session"], r["line"]): r for r in map(json.loads, open(f"{out}/refused.jsonl"))}
f = json.load(open(f"{out}/findings.json"))
row = {(r["session"], r["line"]): r for r in ev}
offered = f["offered_then_refused"]
assert len(offered) >= 10, f"only {len(offered)} offered-then-refused findings"
for x in offered:
    a, b = (x["session"], x["refusal_line"]), (x["session"], x["next_line"])
    assert a in refused, f"{x}: first line is not a refused result"
    nxt = row.get(b)
    assert nxt is not None, f"{x}: next line not in the table"
    if x.get("next_is_stop"):
        assert nxt["kind"] in ("user_message", "custom_message", "custom"), f"{x}: a refused stop must point at the gate's nudge"
    else:
        assert b in refused, f"{x}: next line is not a refused result"
        call = next((r for r in ev if r["session"] == x["session"] and r["kind"] == "tool_call"
                     and r.get("call_id") and r.get("call_id") == nxt.get("call_id")), None)
        assert call is not None, f"{x}: no tool_call row for the next result"
        text = refused[a].get("text") or row[a].get("text_head") or ""
        assert call["tool"] in text, f"{x}: the next call's tool {call['tool']} is not offered in the refusal"
    # The next call is the driver's next one: no other tool call between.
    between = [r for r in ev if r["session"] == x["session"] and r["kind"] == "tool_call"
               and x["refusal_line"] < r["line"] < x["call_line"]]
    assert not between, f"{x}: {len(between)} other calls in between"
runs = {x["run"] for x in offered}
for need in ("R42", "R43", "R44"):
    assert need in runs, f"no offered-then-refused finding in {need}"
assert any(x["run"] == "R44" and x.get("next_is_stop") for x in offered), "R44's refused stop after the cap's offer not found"
for key in ("alternating", "repeated"):
    assert f[key], f"no {key} findings"
    for x in f[key]:
        lines = x["lines"]
        assert len(lines) >= 3 and all((x["session"], l) in refused for l in lines), f"{key}: {x} lines not all refused"
print(f"OK offered_then_refused={len(offered)} alternating={len(f['alternating'])} repeated={len(f['repeated'])} runs={len(runs)}")
PY
rm -rf "$OUT"
python3 -m ruff check mine/ 2>/dev/null || uvx ruff check mine/
