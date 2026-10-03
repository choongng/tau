#!/bin/bash
set -eu
f=dev-notes/itc-runs/fang-ideas.md
test -s "$f"
# each idea is a "### " heading with a fang source citation and a tau target
n=$(grep -c '^### ' "$f")
test "$n" -ge 5
c=$({ grep -cE '(~/fang|/home/choong/fang)/[^ ]+' "$f" || true; })
test "$c" -ge 5
t=$({ grep -cE 'src/tau_[a-z_]+/' "$f" || true; })
test "$t" -ge 3
echo OK
