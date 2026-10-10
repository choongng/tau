#!/bin/bash
# usage: selftest.sh — builds fixture runs in a temp dir and shows the v7
# checks pass a good one and refuse each bad one. Exits 0 only if they do.
# Fixture runs record model m9b; ITC_MODEL_MAP maps short name "small" to it,
# and "other" to a model no fixture uses, for the wrong-model case.
# Fixtures record task itc and the itc fixture prompt unless MK_TASK (a task,
# or "none" for no task field) and MK_PROMPT (a prompt file) say otherwise.
# The note's header and summary name the fixture's model, prompt and tau sha
# unless MK_HDR_MODEL, MK_HDR_PROMPT or MK_HDR_SHA say otherwise; the project's
# first commit is 10s after meta.start unless MK_FIRST (seconds after start,
# or "null") says otherwise. MK_UNFOUNDED=yes records a run that never
# founded: founded False, commits 0, record_commits 0, in scorecard and note.
set -eu
here=$(cd "$(dirname "$0")" && pwd)
T=${TAU_REPO:-/home/choong/tautest/tau}
tmp=$(mktemp -d); trap 'rm -rf "$tmp"' EXIT
export ITC_RUNS_DIR=$tmp/runs ITC_NOTES_DIR=$tmp/notes ITC_PROMPT=$tmp/prompt.txt TAU_REPO=$T
COBS_PROMPT=$tmp/cobs_prompt.txt
export ITC_MODEL_MAP="small=m9b other=x9b"
mkdir -p "$ITC_RUNS_DIR" "$ITC_NOTES_DIR"
printf "build it, don't ask.\n\nhttps://example.org/x.pdf\n" > "$ITC_PROMPT"
printf "stuff the bytes.\n\nhttps://example.org/cobs\n" > "$COBS_PROMPT"
sha=$(git -C "$T" rev-parse HEAD)
fails=0

# mkrun NAME CAP DIRTY MODELFLAG — a run whose scorecard and note agree.
mkrun() {
  local R=$1 H=$ITC_RUNS_DIR/$1 prompt cmd
  mkdir -p "$H"
  prompt=$(cat "${MK_PROMPT:-$ITC_PROMPT}"; printf x); prompt=${prompt%x}
  if [ "$4" = yes ]; then cmd=(timeout 3600 tau -p --provider bane --model m9b "$prompt")
  else cmd=(timeout 3600 tau -p --provider bane "$prompt"); fi
  CMD=$(printf '%q ' "${cmd[@]}") TASK=${MK_TASK:-itc} CAP=$2 DIRTY=$3 SHA=${5:-$sha} FIRST=${MK_FIRST:-10} UNF=${MK_UNFOUNDED:-no} python3 - "$H" <<'PY'
import json, os, sys
h = sys.argv[1]
json.dump({"run": os.path.basename(h), "model": "m9b", "launch_command": os.environ["CMD"],
           "wall_cap_s": int(os.environ["CAP"]), "tau_sha": os.environ["SHA"],
           "tau_dirty_files": int(os.environ["DIRTY"]), "session": "/x.jsonl", "start": 1791000000.5,
           **({} if os.environ["TASK"] == "none" else {"task": os.environ["TASK"]})},
          open(f"{h}/meta.json", "w"))
json.dump({"code": 0}, open(f"{h}/exit.json", "w"))
unf = os.environ["UNF"] == "yes"
json.dump({"workers": [], "tasks_total": 3, "tasks_done": 1, "commits": 0 if unf else 2,
           "founded": not unf, "record_commits": 0 if unf else 1, "uncommitted_files": 0,
           "first_commit_ts": None if os.environ["FIRST"] == "null" else int(1791000000.5 + float(os.environ["FIRST"]))},
          open(f"{h}/scorecard.json", "w"))
json.dump({"passed": 4, "total": 9}, open(f"{h}/grade.json", "w"))
PY
  local t=${MK_TASK:-itc} commits=2 founded=True; [ "$t" = none ] && t=itc
  [ "${MK_UNFOUNDED:-no}" = yes ] && commits=0 founded=False
  printf '# %s — %s — %s\n\ntau %s (fixture). Capped.\n\n## Scorecard\n\n```\ntasks_total 3\ntasks_done 1\ncommits %s\nfounded %s\nuncommitted_files 0\n```\n\ngrader: 4/9\n' "$R" "${MK_HDR_MODEL:-m9b}" "${MK_HDR_PROMPT:-${t}_prompt.txt}" "${MK_HDR_SHA:-${5:-$sha}}" "$commits" "$founded" | sed 's/^tau \([0-9a-f]\{7\}\)[0-9a-f]*/tau \1/' > "$ITC_NOTES_DIR/$R.md"
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

mkrun R01 3600 0 yes;                 expect pass   "good run"            scored R01 small itc
mkrun R02 1800 0 yes;                 expect refuse "wrong cap"           scored R02 small itc
mkrun R03 3600 0 no;                  expect refuse "missing --model"     scored R03 small itc
mkrun R04 3600 2 yes;                 expect refuse "dirty tau"           scored R04 small itc
mkrun R05 3600 0 yes 0123456789abcdef0123456789abcdef01234567
                                      expect refuse "tau_sha not a commit" scored R05 small itc
mkrun R06 3600 0 yes; printf 'other\n' > "$tmp/p2"
ITC_PROMPT=$tmp/p2                    expect refuse "different prompt"    scored R06 small itc
mkrun R07 3600 0 yes;                 expect refuse "wrong model"         scored R07 other itc
                                      expect refuse "unknown model"       scored R07 nope itc
                                      expect refuse "missing model"       scored R07 itc
                                      expect refuse "missing task"        scored R07 small
                                      expect refuse "unknown task"        scored R07 small nope
                                      expect refuse "wrong task"          scored R07 small cobs
MK_TASK=none mkrun R08 3600 0 yes;    expect pass   "no task field is itc" scored R08 small itc
                                      expect refuse "no task field as cobs" scored R08 small cobs
MK_TASK=cobs MK_PROMPT=$COBS_PROMPT mkrun R09 3600 0 yes
ITC_PROMPT=$COBS_PROMPT               expect pass   "good cobs run"       scored R09 small cobs
                                      expect refuse "cobs run scored as itc" scored R09 small itc
MK_TASK=cobs mkrun R10 3600 0 yes
ITC_PROMPT=$COBS_PROMPT               expect refuse "cobs run launched with the itc prompt" scored R10 small cobs
MK_PROMPT=$COBS_PROMPT mkrun R15 3600 0 yes
                                      expect refuse "itc run launched with the cobs prompt" scored R15 small itc
MK_HDR_MODEL=x9b mkrun R16 3600 0 yes
                                      expect refuse "header names the wrong model" scored R16 small itc
MK_HDR_MODEL=m9b-q4 mkrun R17 3600 0 yes
                                      expect refuse "header model not the full id" scored R17 small itc
MK_HDR_PROMPT=cobs_prompt.txt mkrun R18 3600 0 yes
                                      expect refuse "header names the wrong prompt" scored R18 small itc
MK_HDR_SHA=0123456789abcdef mkrun R19 3600 0 yes
                                      expect refuse "summary names the wrong tau sha" scored R19 small itc
MK_FIRST=-60 mkrun R20 3600 0 yes;    expect refuse "first commit before the run" scored R20 small itc
MK_FIRST=-3 mkrun R21 3600 0 yes;     expect pass   "first commit within 5s slack" scored R21 small itc
MK_FIRST=null mkrun R22 3600 0 yes;   expect refuse "no first commit" scored R22 small itc
MK_FIRST=null MK_UNFOUNDED=yes mkrun R24 3600 0 yes
                                      expect pass   "never founded, no first commit" scored R24 small itc
MK_FIRST=-60 MK_UNFOUNDED=yes mkrun R25 3600 0 yes
                                      expect refuse "never founded, first commit before the run" scored R25 small itc
MK_TASK=cobs MK_PROMPT=$COBS_PROMPT MK_HDR_PROMPT=itc_prompt.txt mkrun R23 3600 0 yes
ITC_PROMPT=$COBS_PROMPT               expect refuse "cobs run's header names itc_prompt.txt" scored R23 small cobs

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
