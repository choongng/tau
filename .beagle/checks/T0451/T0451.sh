#!/bin/bash
# T0451: each fix task since the 2026-10-12 audit has its code commits findable by a Task: trailer
set -e
for t in T0447 T0449 T0452; do
  n=$(git log --format=%H --grep="^Task: $t\$" -- examples/extensions/beagle.py | wc -l)
  [ "$n" -ge 1 ] || { echo "no beagle.py commit carries 'Task: $t'"; exit 1; }
  echo "$t: $n beagle.py commit(s) with its trailer"
done
