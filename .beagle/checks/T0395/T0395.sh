#!/bin/bash
# T0395: itc-harness/mine/events.py writes one row per tool call, tool result and
# tau-level event for every driver and worker session of every run, and its counts
# agree with an independent recount of the session files.
set -e
cd /home/choong/tautest/itc-harness
python3 -m pytest -q mine/test_events.py
OUT=$(mktemp -d)
python3 mine/events.py --runs runs --out "$OUT/events.jsonl"
python3 - "$OUT/events.jsonl" <<'PY'
import collections, glob, json, os, sys
rows = [json.loads(l) for l in open(sys.argv[1])]
need = {"run", "model", "task", "role", "session", "line", "t", "kind"}
bad = [r for r in rows if not need <= r.keys()]
assert not bad, f"rows missing fields: {sorted(need - bad[0].keys())}"
by = collections.defaultdict(collections.Counter)
for r in rows:
    by[r["session"]][r["kind"]] += 1
sessions = 0
for meta in sorted(glob.glob("runs/*/meta.json")):
    m = json.load(open(meta))
    run = meta.split("/")[1]
    ws = m.get("worker_sessions") or []
    if isinstance(ws, str):
        ws = json.loads(ws.replace("'", '"')) if ws.strip() else []
    paths = [(m["session"], "driver")] + [(p, "worker") for p in ws]
    for p, role in paths:
        sessions += 1
        calls = results = blocked = 0
        for line in open(p):
            e = json.loads(line)
            msg = e.get("message") if e.get("type") == "message" else None
            if not isinstance(msg, dict):
                continue
            content = msg.get("content")
            if msg.get("role") == "assistant" and isinstance(content, list):
                calls += sum(1 for b in content if isinstance(b, dict) and b.get("type") == "toolCall")
            if msg.get("role") == "toolResult":
                results += 1
                text = "".join(b.get("text", "") for b in content or [] if isinstance(b, dict))
                blocked += text.startswith("Tool call blocked")
        got = by.get(p)
        assert got is not None, f"{run} {role} session missing from the table: {p}"
        assert got["tool_call"] == calls, f"{run} {p}: {got['tool_call']} tool_call rows, {calls} in the file"
        assert got["tool_result"] == results, f"{run} {p}: {got['tool_result']} tool_result rows, {results} in the file"
        blk = sum(1 for r in rows if r["session"] == p and r["kind"] == "tool_result" and r.get("blocked"))
        assert blk == blocked, f"{run} {p}: {blk} blocked rows, {blocked} in the file"
roles = collections.Counter(r["role"] for r in rows)
assert sessions >= 400 and roles["driver"] and roles["worker"], (sessions, roles)
events = collections.Counter(r["kind"] for r in rows)
for k in ("thinking_change", "stop"):
    assert events[k], f"no {k} rows"
print(f"OK {sessions} sessions, {len(rows)} rows, {dict(events)}")
PY
rm -rf "$OUT"
python3 -m ruff check mine/ 2>/dev/null || uvx ruff check mine/
