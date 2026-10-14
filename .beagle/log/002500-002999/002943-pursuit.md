+++
id = "002943-pursuit"
ordinal = 2943
kind = "pursuit"
timestamp = "2026-10-14T03:06:41+00:00"
summary = "pursuit prove T0574: WITNESSED — refuses when launch.sh's `\"$TAU_SRC/.venv/bin/tau\" -p \"${extensions[@]}\" …` is put back as `tau -p \"${extensions[@]}\" --provider \"$provider…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "888c847eeb59be8774b6ada5030b57cec3412b1e34baa5a281de72d61079960b  .beagle/checks/T0574/T0574.sh" | sha256sum -c --quiet && bash .beagle/checks/T0574/T0574.sh'
refutes: refuses when launch.sh's `"$TAU_SRC/.venv/bin/tau" -p "${extensions[@]}" …` is put back as `tau -p "${extensions[@]}" --provider "$provider…` (proven 2026-10-14T03:05:44+00:00)
refused after 1s of a 1s check
standing checks red: T0335, T0360, T0386, T0496, T0519, T0039
