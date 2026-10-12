+++
id = "002557-pursuit"
ordinal = 2557
kind = "pursuit"
timestamp = "2026-10-12T21:00:48+00:00"
summary = "pursuit open T0498: beagle contract: cite sources by line anchor, not by quote"
metric_command = ""
drains = []
hooks = []
+++

criteria: beagle pursuit contract refs prints each source line as N#hhh| text; an entry or excluded passage may cite "N#hhh" or "N#hhh-M#hhh" instead of quoting, beagle checks each anchor's hash against its line, names the right anchor when one is wrong, refuses a cite over the span limit, and reports the cited text; R71's and R73's contracts converted to anchors pass contract check --draft; the brief, SHAPE, pursuit.md and tau's contract milestone teach anchors, not quoting
decided by: sh -c 'echo "c0fac397f490bc473128daa42a955f64e42c2618c9a57f8a4a9313f4ca62075a  .beagle/checks/T0498/T0498.sh" | sha256sum -c --quiet && bash .beagle/checks/T0498/T0498.sh'
budget: 150000 tokens
opened over T0493: the eval's finding: contract-first q35 runs all capped on hand-quoting; anchors decide whether the re-run is worth making, and T0493's deletion can follow
