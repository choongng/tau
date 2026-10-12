#!/bin/bash
# T0491: the invented-spec harness: Wrenfold r3 spec, reference, grader whose cases catch each trap, adapter, launch wiring.
set -e
H=/home/choong/tautest/itc-harness
cd "$H"
python3 - <<'PY'
import html, json, os, re, subprocess, sys

def grade(trap=""):
    env = {**os.environ, "WRENFOLD_TRAP": trap}
    adapter = "adapters/wrenfold_broken.py" if trap else "adapters/wrenfold_reference.py"
    out = subprocess.run([sys.executable, "grade_wrenfold.py", "--adapter", adapter, "--json"],
                         capture_output=True, text=True, env=env, timeout=300)
    g = json.loads(out.stdout)
    return out.returncode, g, {c["category"] for c in g["cases"] if not c["ok"]}

# The reference passes every case, and the grader exits 0 only then.
rc, g, failed = grade()
assert rc == 0 and g["passed"] == g["total"] >= 50, (rc, g["passed"], g["total"], failed)

# Each trap is caught, in its own categories only. The end-marker trap passes
# every worked example: only the spec's prose says 63 takes two bytes.
want = {
    "r2": {"spec-encode", "spec-decode", "boundary", "roundtrip", "count"},
    "marker": {"boundary", "roundtrip", "count"},
    "lenient": {"malformed", "count"},
    "no-count": {"count"},
}
for trap, cats in want.items():
    rc, g, failed = grade(trap)
    assert rc == 1 and failed == cats, (trap, rc, failed)

# The spec's worked examples are the grader's, and the reference's.
sys.path.insert(0, ".")
import grade_wrenfold as G
import wrenfold_ref as R
page = open("specs/wrenfold-r3.html").read()
section = page[page.index("4. Examples"):page.index("5. Reading")]
rows = re.findall(r"<tr><td>(.*?)</td><td>(.*?)</td></tr>", section)
spec = [([] if a == "(none)" else [int(x) for x in a.split(",")], bytes.fromhex(b)) for a, b in rows]
assert len(spec) == 8 and spec == [(v, e) for _, v, e in G.SPEC], spec
assert all(R.encode(v) == e for v, e in spec)

# The traps are in the spec as text: 63's form, the stated rejections, count once.
text = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", page)))
for phrase in ("63 is written in the two-byte form, as 0x40 0x3F",
               "the input 40 05 3F writes 5 in the two-byte form, and is rejected",
               "has any byte after its end marker (05 3F 00)", "(2^38 − 1)"):
    assert phrase in text, phrase
assert len(re.findall(r"\bcount\b", text)) == 1, re.findall(r"\bcount\b", text)
for name, enc in G.MALFORMED:
    try:
        R.decode(enc)
    except ValueError:
        continue
    raise AssertionError(f"reference decodes malformed {name}")
print("wrenfold harness: reference", g["total"], "cases; 4 traps each caught in their own categories")
PY
# Launch wiring: the task is accepted, the spec is served at the prompts' URL.
url=http://127.0.0.1:8737/wrenfold-r3.html
grep -qxF "$url" /home/choong/tautest/wrenfold_prompt.txt
grep -qxF "$url" prompts/wrenfold_baseline_prompt.txt
./launch.sh --dry-run R999 q35 wrenfold | grep -qF "would serve: $H/specs at $url"
./launch.sh --dry-run B999 q35 wrenfold | grep -qF "would serve: $H/specs at $url"
test ! -e runs/R999 && test ! -e runs/B999
