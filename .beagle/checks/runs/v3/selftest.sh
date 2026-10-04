#!/bin/bash
# usage: selftest.sh — builds fixture runs in a temp dir and shows the v3
# checks pass a good one and refuse each bad one. Exits 0 only if they do.
# Fixture runs record model m9b; ITC_MODEL_MAP maps short name "small" to it,
# and "other" to a model no fixture uses, for the wrong-model case.
set -eu
here=$(cd "$(dirname "$0")" && pwd)
T=${TAU_REPO:-/home/choong/tautest/tau}
tmp=$(mktemp -d); trap 'rm -rf "$tmp"' EXIT
export ITC_RUNS_DIR=$tmp/runs ITC_NOTES_DIR=$tmp/notes ITC_PROMPT=$tmp/prompt.txt TAU_REPO=$T
export ITC_MODEL_MAP="small=m9b other=x9b"
mkdir -p "$ITC_RUNS_DIR" "$ITC_NOTES_DIR"
printf "build it, don't ask.\n\nhttps://example.org/x.pdf\n" > "$ITC_PROMPT"
sha=$(git -C "$T" rev-parse HEAD)
fails=0

# mkrun NAME CAP DIRTY MODELFLAG — a run whose scorecard and note agree.
mkrun() {
  local R=$1 H=$ITC_RUNS_DIR/$1 prompt cmd
  mkdir -p "$H"
  prompt=$(cat "$ITC_PROMPT"; printf x); prompt=${prompt%x}
  if [ "$4" = yes ]; then cmd=(timeout 3600 tau -p --provider bane --model m9b "$prompt")
  else cmd=(timeout 3600 tau -p --provider bane "$prompt"); fi
  CMD=$(printf '%q ' "${cmd[@]}") CAP=$2 DIRTY=$3 SHA=${5:-$sha} python3 - "$H" <<'PY'
import json, os, sys
h = sys.argv[1]
json.dump({"run": os.path.basename(h), "model": "m9b", "launch_command": os.environ["CMD"],
           "wall_cap_s": int(os.environ["CAP"]), "tau_sha": os.environ["SHA"],
           "tau_dirty_files": int(os.environ["DIRTY"]), "session": "/x.jsonl"}, open(f"{h}/meta.json", "w"))
json.dump({"code": 0}, open(f"{h}/exit.json", "w"))
json.dump({"workers": [], "tasks_total": 3, "tasks_done": 1, "commits": 2, "founded": True,
           "uncommitted_files": 0}, open(f"{h}/scorecard.json", "w"))
json.dump({"passed": 4, "total": 9}, open(f"{h}/grade.json", "w"))
PY
  printf '# %s\n\n## Scorecard\n\n```\ntasks_total 3\ntasks_done 1\ncommits 2\nfounded True\nuncommitted_files 0\n```\n\ngrader: 4/9\n' "$R" > "$ITC_NOTES_DIR/$R.md"
}

# mknote NAME EVIDENCE ACTION UPSTREAM — a diagnosed note.
mknote() {
  local f=$ITC_NOTES_DIR/$1.md
  { printf '# %s\n\n## Trace analysis\n\nE1 went wrong.\n\n## Failure classes\n\n' "$1"
    printf '### [tau] The step loops\n'
    [ "$2" = yes ] && printf 'Evidence: E4-E9 repeat one call\n'
    printf 'Action: %s\n\n' "$3"
    printf '### [model] It guesses\nEvidence: E12\nDisposition: none needed\n\n## Next\n\nmore.\n'
  } > "$f"
  [ "$4" = yes ] && printf '\n## %s\n\nfiled.\n' "$1" >> "$ITC_NOTES_DIR/upstream.md"
  return 0
}

expect() {  # expect pass|refuse WHAT SCRIPT ARGS...
  local want=$1 what=$2 script=$3; shift 3
  if bash "$here/$script.sh" "$@" > "$tmp/out" 2>&1; then got=pass; else got=refuse; fi
  if [ "$got" = "$want" ]; then echo "ok   $what: $got"
  else echo "FAIL $what: wanted $want, got $got"; sed 's/^/     /' "$tmp/out"; fails=$((fails+1)); fi
}

mkrun R01 3600 0 yes;                 expect pass   "good run"            scored R01 small
mkrun R02 1800 0 yes;                 expect refuse "wrong cap"           scored R02 small
mkrun R03 3600 0 no;                  expect refuse "missing --model"     scored R03 small
mkrun R04 3600 2 yes;                 expect refuse "dirty tau"           scored R04 small
mkrun R05 3600 0 yes 0123456789abcdef0123456789abcdef01234567
                                      expect refuse "tau_sha not a commit" scored R05 small
mkrun R06 3600 0 yes; printf 'other\n' > "$tmp/p2"
ITC_PROMPT=$tmp/p2                    expect refuse "different prompt"    scored R06 small
mkrun R07 3600 0 yes;                 expect refuse "wrong model"         scored R07 other
                                      expect refuse "unknown model"       scored R07 nope
                                      expect refuse "missing model"       scored R07

mknote R11 yes 'fix it in src/tau/beagle.py; tests/test_x.py covers it' yes
                                      expect pass   "good diagnosis"      diagnosed R11
mknote R12 no  'fix it in src/tau/beagle.py' yes
                                      expect refuse "class without Evidence" diagnosed R12
mknote R13 yes 'fix it in src/tau/beagle.py' no
                                      expect refuse "not in upstream.md"  diagnosed R13
printf '\nupstream: none\n' >> "$ITC_NOTES_DIR/R13.md"
                                      expect pass   "says upstream: none" diagnosed R13
mknote R14 yes 'fix the step loop somewhere' yes
                                      expect refuse "[tau] Action names no path" diagnosed R14

[ "$fails" -eq 0 ] && echo "selftest OK" || { echo "selftest: $fails failed"; exit 1; }
