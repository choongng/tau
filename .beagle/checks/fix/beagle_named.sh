#!/bin/bash
# usage: beagle_named.sh FILE N name1 name2 ... — in beagle's contract-first
# worktree, exactly these N tests exist and pass, then FILE's whole suite passes.
set -eu
B=${BEAGLE_WT:-/home/choong/beagle-wt/contract-first}/plugins/beagle-pursuit/tooling/beagle
f=$1; n=$2; shift 2
k=$(printf ' or %s' "$@"); k=${k# or }
cd "$B"
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1
export UV_PROJECT_ENVIRONMENT=${XDG_CACHE_HOME:-$HOME/.cache}/beagle/venv-contract-first-dev
export PYTHONPYCACHEPREFIX=${XDG_CACHE_HOME:-$HOME/.cache}/beagle/pycache
run() { timeout 900 uv run --quiet --with pytest --with pytest-xdist --extra browser python -m pytest -q -p no:cacheprovider "$@" 2>&1; }
out=$(run "$f" -k "$k") || { echo "$out" | tail -30; exit 1; }
echo "$out" | tail -2
echo "$out" | grep -qE "^$n passed" || { echo "expected exactly $n passed"; exit 1; }
out=$(run "$f" -n auto) || { echo "$out" | tail -30; exit 1; }
echo "$out" | tail -1
