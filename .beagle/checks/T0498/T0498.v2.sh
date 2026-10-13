#!/bin/bash
# T0498: a contract entry cites its source by line anchor (83#a1f), read off `contract refs`,
# and beagle supplies the text; nobody retypes the source (R71-R73's contract sink).
set -e
WT=/home/choong/beagle-wt/contract-first
B=$WT/plugins/beagle-pursuit/tooling/beagle
BEAGLE=$WT/plugins/beagle-pursuit/bin/beagle
D=$(cd "$(dirname "$0")" && pwd)
tmp=$(mktemp -d "$HOME/.cache/t0498.XXXXXX"); trap 'rm -rf "$tmp"' EXIT

# R71's and R73's own references and contracts, every quote replaced by the anchors of the lines it
# was found on. R73's itc2008 is PDF text whose symbols (⇐⇒, `t` for ⊔) a model cannot retype.
for run in r71 r73; do
  cp -r "$D/$run" "$tmp/$run"
  (cd "$tmp/$run" && "$BEAGLE" pursuit contract check --draft --json > spans.json) || true
  python3 - "$tmp/$run" "$BEAGLE" <<'PY'
import json, re, subprocess, sys
root, beagle = sys.argv[1], sys.argv[2]
rep = json.load(open(f"{root}/spans.json"))
assert rep["ok"], rep["problems"]
c = json.load(open(f"{root}/contract/contract.json"))
anchors = {}
for name in c["sources"]:
    out = subprocess.run([beagle, "pursuit", "contract", "refs", name], cwd=root,
                         capture_output=True, text=True, check=True).stdout
    rows = [re.match(r"^(\d+)#([0-9a-f]{3})\| ", l) for l in out.splitlines()]
    assert rows and all(rows), f"refs {name} is not `N#hhh| text` on every line"
    anchors[name] = {int(m[1]): m[2] for m in rows}
by_id = {s["entry"]: s for s in rep["spans"]}
for e in c["entries"]:
    s, a = by_id[e["id"]], anchors[e["source"]]
    cite = f"{s['first']}#{a[s['first']]}"
    if s["last"] != s["first"]:
        cite += f"-{s['last']}#{a[s['last']]}"
    e.pop("quote"); e["cite"] = cite
for i, x in enumerate(c.get("excluded", [])):
    s, a = rep["excluded"][i], anchors[x["source"]]
    x.pop("quote"); x["cite"] = f"{s['first']}#{a[s['first']]}" + (
        f"-{s['last']}#{a[s['last']]}" if s["last"] != s["first"] else "")
json.dump(c, open(f"{root}/contract/contract.json", "w"), indent=1, ensure_ascii=False)
print(f"{root.rsplit('/', 1)[1]}: {len(c['entries'])} entries now cite by anchor")
PY
  (cd "$tmp/$run" && "$BEAGLE" pursuit contract check --draft)
  # beagle supplies each cited passage's text in the report.
  (cd "$tmp/$run" && "$BEAGLE" pursuit contract check --draft --json) | python3 -c '
import json, sys; r = json.load(sys.stdin)
assert r["ok"] and all(s["quote"].strip() for s in r["spans"]), "a cited span has no text"'
done

# A wrong anchor is refused with the right one named; so is a cite past the span limit.
python3 - "$tmp/r71/contract/contract.json" <<'PY'
import json, sys
p = sys.argv[1]; c = json.load(open(p))
first = int(c["entries"][0]["cite"].split("#")[0])
c["entries"][0]["cite"] = f"{first}#zzz".replace("zzz", "000" if not c["entries"][0]["cite"].endswith("000") else "fff")
c["entries"][1]["cite"] = "1#000-80#000"
json.dump(c, open(p, "w"), indent=1)
PY
out=$(cd "$tmp/r71" && "$BEAGLE" pursuit contract check --draft) && { echo "bad anchors passed"; exit 1; }
echo "$out" | grep -E "E001.*[0-9]+#[0-9a-f]{3}" >/dev/null || { echo "no right anchor named for E001:"; echo "$out"; exit 1; }
echo "$out" | grep -q "E002.*lines" || { echo "an 80-line cite was not refused:"; echo "$out"; exit 1; }

# What a worker is told: anchors, and the command that prints them.
cd "$B"
grep -q "contract refs" src/beagle/contract.py
! grep -qiE "each entry quotes|quoted from its source" src/beagle/contract.py ../../commands/pursuit.md
! grep -q "quoted from its source" /home/choong/tautest/tau/examples/extensions/beagle.py
export UV_PROJECT_ENVIRONMENT=$HOME/.cache/beagle-cf-venv
mkdir -p "$HOME/.cache/beagle-pytest"
uv run --with pytest pytest -q -p no:cacheprovider --basetemp="$HOME/.cache/beagle-pytest/T0498" \
  tests/test_contract.py -k "anchor or cite or refs or contract"
find "$WT/plugins" -name __pycache__ -prune -exec rm -rf {} +

# T0521: and positively, what each worker is told teaches anchors.
# beagle's brief to contract work carries SHAPE, which teaches the anchor cite.
cd "$B"
UV_PROJECT_ENVIRONMENT=$HOME/.cache/beagle-cf-venv uv run --quiet python - "$tmp" <<'PY2'
import sys
from pathlib import Path
from beagle import contract
root = Path(sys.argv[1]) / "brief"
(root / ".beagle").mkdir(parents=True)
(root / ".beagle" / "pursuit.toml").write_text(
    '[goal]\nstatement="x"\ncriteria=["y"]\n[contract]\npath="contract/contract.json"\nfiles=["contract/"]\n')
said = "\n".join(contract.brief_lines(root, ["contract/contract.json"]))
for want in ('A cite is the anchor of the line an entry was read from, "83#a1f"',
             "`beagle pursuit contract refs NAME` prints the source with an anchor on every line",
             "Copy anchors from it; do not retype the source's words"):
    assert want in contract.SHAPE, f"SHAPE lacks: {want}"
    assert want in said, f"the contract brief lacks: {want}"
PY2
find "$WT/plugins" -name __pycache__ -prune -exec rm -rf {} +
P=$WT/plugins/beagle-pursuit/commands/pursuit.md
grep -qF 'Each entry cites the lines it was read from by anchor:' "$P" || { echo "pursuit.md does not teach the anchor cite"; exit 1; }
grep -qF '`beagle pursuit contract refs <source>` prints the source as `83#a1f| text`' "$P" || { echo "pursuit.md does not name contract refs"; exit 1; }
# tau's Contract milestone (implicitly concatenated literals, joined here) and founding note.
python3 - /home/choong/tautest/tau/examples/extensions/beagle.py <<'PY2'
import re, sys
src = re.sub(r'"\s*\n\s*(?:#[^\n]*\n\s*)*f?"', "", open(sys.argv[1]).read())
milestone = re.search(r'"Contract::(.*?)",\n', src)
assert milestone and "citing its source by line anchor" in milestone[1], "the Contract milestone does not teach line anchors"
note = re.search(r"CONTRACT_FIRST_NOTE = \((.*?)\n\)", src, re.S)
assert note and "citing its source by line anchor" in note[1], "CONTRACT_FIRST_NOTE does not teach line anchors"
PY2
echo "T0498: R71 and R73 contracts check with every entry cited by anchor; bad anchors refused; brief, SHAPE, pursuit.md and tau teach anchors"
