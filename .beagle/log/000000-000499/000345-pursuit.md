+++
id = "000345-pursuit"
ordinal = 345
kind = "pursuit"
timestamp = "2026-10-03T20:45:59+00:00"
summary = "pursuit open T0081: setup detector ends the title at ' - ' and counts a title naming beagle as setup"
metric_command = ""
drains = []
hooks = []
+++

criteria: _setup_milestone ends a title at '::', ':', ' - ' or ' — ' (whichever comes first), and counts as setup a title that names beagle or pursuit setup/infrastructure/configuration. R10: 'Setup beagle pursuit infrastructure - configure project for beagle workflows' is dropped at founding with the setup note; of R10's six milestones only that one is dropped; 'Implement core clock operations - create, increment, merge, and compare clocks' is kept.
decided by: sh -c 'echo "85aeb4c6c581b236fd9a25b5205bc5ec1cddd09a9f27a9fc54f2a1777f74d7cb  .beagle/checks/T0081/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0081/check.sh'
budget: 25000 tokens
