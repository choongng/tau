#!/bin/bash
set -e
grep -q "^## R26" dev-notes/itc-runs/upstream.md
bash .beagle/checks/runs/v5/diagnosed.sh R26
