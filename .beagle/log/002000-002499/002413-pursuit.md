+++
id = "002413-pursuit"
ordinal = 2413
kind = "pursuit"
timestamp = "2026-10-12T14:49:19+00:00"
summary = "pursuit amend T0472"
metric_command = ""
drains = []
hooks = []
+++

the named test is parametrized over lean and full (both arms are a clause), so it reports 2 passed; the check counted 1. The count is raised to 2, which is stricter
was: sh -c 'echo "9275a91888a826f2d141b74870d26c1d15d21c173eea4c3d47b4c5007def3a44  .beagle/checks/T0472/T0472.sh" | sha256sum -c --quiet && bash .beagle/checks/T0472/T0472.sh'
  9275a91888a826f2d141b74870d26c1d15d21c173eea4c3d47b4c5007def3a44  .beagle/checks/T0472/T0472.sh
now: sh -c 'echo "c0b40d1031be441b4a4890c7ef9fab7dbed4b70c4eabad174b5b73fe256832c5  .beagle/checks/T0472/T0472.sh" | sha256sum -c --quiet && bash .beagle/checks/T0472/T0472.sh'
