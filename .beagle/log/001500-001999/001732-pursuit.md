+++
id = "001732-pursuit"
ordinal = 1732
kind = "pursuit"
timestamp = "2026-10-11T01:06:17+00:00"
summary = "pursuit amend T0399"
metric_command = ""
drains = []
hooks = []
+++

the bound check contradicted itself: it requires every offered-then-refused pair seen twice to be a finding, and every kind in such a finding to be a refusals.json kind, but a refused stop's second kind is the stop gate's nudge (a user message, named nudge:<tag> by contradictions.py), which the catalog of tool results never holds. The amended check exempts nudge: kinds from the catalog lookup only; the other kinds in the pair are still checked
was: sh -c 'echo "19f39c0bcb16f8719f4442a26e393d3dbbf75ef9fa4d45fc27b92f9f2baf78fd  .beagle/checks/T0399/T0399.sh" | sha256sum -c --quiet && bash .beagle/checks/T0399/T0399.sh'
  19f39c0bcb16f8719f4442a26e393d3dbbf75ef9fa4d45fc27b92f9f2baf78fd  .beagle/checks/T0399/T0399.sh
now: sh -c 'echo "eafefcc5dd630cebe1defab8842656db26a48e1db1cad4b90bbdc57658969d2c  .beagle/checks/T0399/T0399b.sh" | sha256sum -c --quiet && bash .beagle/checks/T0399/T0399b.sh'
