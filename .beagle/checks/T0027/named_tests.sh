#!/bin/bash
# usage: named_tests.sh FILE N name1 name2 ... — exactly these N tests exist and pass.
set -eu
f=$1; n=$2; shift 2
k=$(printf ' or %s' "$@"); k=${k# or }
out=$(timeout 600 uv run --no-sync pytest -q -p no:cacheprovider "$f" -k "$k" 2>&1) || { echo "$out" | tail -30; exit 1; }
echo "$out" | tail -3
echo "$out" | grep -qE "^$n passed" || { echo "expected exactly $n passed"; exit 1; }
