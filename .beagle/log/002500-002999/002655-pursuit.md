+++
id = "002655-pursuit"
ordinal = 2655
kind = "pursuit"
timestamp = "2026-10-13T06:05:40+00:00"
summary = "pursuit amend T0508"
metric_command = ""
drains = []
hooks = []
+++

audit 2026-10-12 (T0521): the check asserted the R81/R82 grades in eval.md but not the clause 'what anchors and contract refs access changed (R75, R77 and R79's stopped runs noted)'. The new check also asserts eval.md's 'Line anchors: R75–R82' section names N#hhh anchors and contract refs and notes R75, R77 and R79 as stopped.
was: sh -c 'echo "2bfb637bdd129b2d35d3ec44b9b2896d49a83f0244b862015316c5069401dc57  .beagle/checks/T0508/T0508.sh" | sha256sum -c --quiet && bash .beagle/checks/T0508/T0508.sh'
  2bfb637bdd129b2d35d3ec44b9b2896d49a83f0244b862015316c5069401dc57  .beagle/checks/T0508/T0508.sh
now: sh -c 'echo "6ff9f0f47d6de83e6272f3d00f918c181c30d18bcff535e277813fbed6c34cca  .beagle/checks/T0508/T0508.v2.sh" | sha256sum -c --quiet && bash .beagle/checks/T0508/T0508.v2.sh'
