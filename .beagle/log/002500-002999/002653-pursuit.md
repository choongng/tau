+++
id = "002653-pursuit"
ordinal = 2653
kind = "pursuit"
timestamp = "2026-10-13T06:04:56+00:00"
summary = "pursuit amend T0498"
metric_command = ""
drains = []
hooks = []
+++

audit 2026-10-12 (T0521): the check only grepped that quoting was gone; the clause 'the brief, SHAPE, pursuit.md and tau's contract milestone teach anchors' was never asserted. The new check adds positive assertions: SHAPE and the contract brief name the anchor cite and contract refs, pursuit.md teaches the anchor cite, tau's Contract milestone and CONTRACT_FIRST_NOTE say 'citing its source by line anchor'.
was: sh -c 'echo "c0fac397f490bc473128daa42a955f64e42c2618c9a57f8a4a9313f4ca62075a  .beagle/checks/T0498/T0498.sh" | sha256sum -c --quiet && bash .beagle/checks/T0498/T0498.sh'
  c0fac397f490bc473128daa42a955f64e42c2618c9a57f8a4a9313f4ca62075a  .beagle/checks/T0498/T0498.sh
now: sh -c 'echo "4c4c65dbdf81ee6ab9d2c0f3f17ac8a261f7effcea37a91e06fb88248ae8d058  .beagle/checks/T0498/T0498.v2.sh" | sha256sum -c --quiet && bash .beagle/checks/T0498/T0498.v2.sh'
