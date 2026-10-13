#!/bin/bash
# T0544: the dispute recon note exists and answers its four questions, each with
# file:line evidence from beagle and the tau extension.
set -e
F=/home/choong/tautest/tau/dev-notes/contract-first/dispute-recon.md
[ -f "$F" ] || { echo "no $F"; exit 1; }
for h in "## What exists" "## Where a dispute enters" "## Who judges it" "## Smallest change"; do
  grep -qF "$h" "$F" || { echo "missing section: $h"; exit 1; }
done
n=$(grep -cE '[a-z_/]+\.(py|md):[0-9]+' "$F")
[ "$n" -ge 6 ] || { echo "only $n file:line citations"; exit 1; }
echo "T0544: dispute recon written, $n citations"
