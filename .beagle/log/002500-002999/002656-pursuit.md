+++
id = "002656-pursuit"
ordinal = 2656
kind = "pursuit"
timestamp = "2026-10-13T06:05:41+00:00"
summary = "pursuit prove T0508: WITNESSED — refuses when eval.md's `- **R77** (stopped): a worker` is put back as `- **R77**: a worker`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "6ff9f0f47d6de83e6272f3d00f918c181c30d18bcff535e277813fbed6c34cca  .beagle/checks/T0508/T0508.v2.sh" | sha256sum -c --quiet && bash .beagle/checks/T0508/T0508.v2.sh'
refutes: refuses when eval.md's `- **R77** (stopped): a worker` is put back as `- **R77**: a worker` (proven 2026-10-13T06:05:41+00:00; refused at Traceback (most recent call last):)
refused after 0s of a 0s check at: Traceback (most recent call last):
refused with: AssertionError: R77's stopped run is not noted
