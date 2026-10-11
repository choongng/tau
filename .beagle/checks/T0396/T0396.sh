#!/bin/bash
# T0396: mine/refusals.py groups every refused tool result into kinds and ties each
# kind to the source line that writes it today, or shows no source writes it now.
set -e
cd /home/choong/tautest/itc-harness
python3 -m pytest -q mine/test_refusals.py
OUT=$(mktemp -d)
python3 mine/events.py --runs runs --out "$OUT/events.jsonl"
python3 mine/refusals.py --events "$OUT/events.jsonl" --out "$OUT/refusals.json" --rows "$OUT/refused.jsonl"
python3 - "$OUT" <<'PY'
import collections, json, os, sys
out = sys.argv[1]
events = [json.loads(l) for l in open(f"{out}/events.jsonl")]
cat = json.load(open(f"{out}/refusals.json"))
refused = [json.loads(l) for l in open(f"{out}/refused.jsonl")]
kinds = {k["id"]: k for k in cat["kinds"]}
assert len(kinds) >= 20, f"only {len(kinds)} kinds"
# Every tau-blocked result is a refused row with a kind.
key = lambda r: (r["session"], r["line"])
ref = {key(r): r for r in refused}
blocked = [r for r in events if r["kind"] == "tool_result" and r.get("blocked")]
miss = [key(r) for r in blocked if key(r) not in ref]
assert not miss, f"{len(miss)} blocked results not in refused rows, e.g. {miss[:2]}"
assert all(r["refusal"] in kinds for r in refused), "a refused row names an unknown kind"
# Beagle's own result-text refusals are caught too, not only tau's guard.
pursuit = [r for r in refused if str(r.get("tool", "")).startswith("pursuit")]
assert len(pursuit) >= 500, f"only {len(pursuit)} pursuit-tool refusals"
counts = collections.Counter(r["refusal"] for r in refused)
SRC = ["/home/choong/tautest/tau/src", "/home/choong/tautest/tau/examples", "/home/choong/beagle/plugins"]
assert all(os.path.isdir(b) for b in SRC), SRC
def source_files():
    for base in SRC:
        for d, _, fs in os.walk(base):
            for f in fs:
                if f.endswith(".py"):
                    yield os.path.join(d, f)
corpus = "\n".join(open(p, encoding="utf-8", errors="replace").read() for p in source_files())
live = dead = 0
for k in kinds.values():
    assert k["count"] == counts[k["id"]], f"{k['id']}: count {k['count']} != {counts[k['id']]} rows"
    assert k["runs"] and k["models"] and k["example"], f"{k['id']}: runs/models/example missing"
    if k["live"]:
        live += 1
        path, line = k["site"].rsplit(":", 1)
        lines = open(path, encoding="utf-8").read().splitlines()
        q = k["quote"]
        assert len(q) >= 15, f"{k['id']}: quote too short"
        near = "\n".join(lines[max(0, int(line) - 4): int(line) + 3])
        assert q in near, f"{k['id']}: quote not within 3 lines of {k['site']}"
        assert q in k["example"] or q.replace("\\n", "\n") in k["example"], f"{k['id']}: quote not in the traced text"
    else:
        dead += 1
        pieces = k["pieces"]
        assert pieces and all(len(p) >= 15 for p in pieces), f"{k['id']}: dead kind needs pieces of 15+ chars"
        assert all(p in k["example"] for p in pieces), f"{k['id']}: a piece is not in the traced text"
        found = [p for p in pieces if p in corpus]
        assert not found, f"{k['id']}: marked not live but {found[0]!r} is in today's source"
assert live and dead, (live, dead)
print(f"OK {len(kinds)} kinds ({live} live, {dead} not), {len(refused)} refused rows, {len(pursuit)} from pursuit tools")
PY
rm -rf "$OUT"
python3 -m ruff check mine/ 2>/dev/null || uvx ruff check mine/
