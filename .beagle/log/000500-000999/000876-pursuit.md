+++
id = "000876-pursuit"
ordinal = 876
kind = "pursuit"
timestamp = "2026-10-05T03:54:32+00:00"
summary = "pursuit open T0221: The module a known-answers test imports always has a scope home outside tests/"
metric_command = ""
drains = []
hooks = []
+++

criteria: A non-test .py under a tests directory is neither counted as a written module nor treated as a test; pursuit_step refuses it as a scope entry with a call naming the root-level module path instead; a known-answers check that imports a module nothing in its scope can write is rebound to the data-only test or refused with a call that scopes the module at its root path.
decided by: sh -c 'echo "65bc62f2e2dc3f411a980b96305bf9c14f47d9a04c384ba6650c283fca5766e4  .beagle/checks/T0221/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0221/check.sh'
budget: 90000 tokens
