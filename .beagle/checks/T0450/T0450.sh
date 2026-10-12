#!/bin/bash
# T0450: R52's [tau] classes each have a fix or a recorded deferral
set -e
f=dev-notes/itc-runs/deferred.md
grep -q 'R0002' $f
grep -q 'routed tests-only' $f && grep -q 'T0452' $f && grep -q 'boundary rows' $f && grep -q 'T0448' $f
