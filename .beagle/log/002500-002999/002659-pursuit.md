+++
id = "002659-pursuit"
ordinal = 2659
kind = "pursuit"
timestamp = "2026-10-13T06:07:32+00:00"
summary = "pursuit amend T0518"
metric_command = ""
drains = []
hooks = []
+++

audit 2026-10-12 (T0521): the check tested only _run_check's 127; the clause 'so pursuit_step refuses it at open instead of reading it as failing' was untested. The new check adds test_open_refuses_a_check_whose_program_is_not_here (tau-wt-ops a488c0d8), run on that worktree, asserting pursuit_step's open refusal names what is here and nothing is opened.
was: sh -c 'echo "3161c693e2fb9e32e39d1c03ce8593116a0248e1d2b3a4d8d164506708894936  .beagle/checks/T0518/T0518.sh" | sha256sum -c --quiet && bash .beagle/checks/T0518/T0518.sh'
  3161c693e2fb9e32e39d1c03ce8593116a0248e1d2b3a4d8d164506708894936  .beagle/checks/T0518/T0518.sh
now: sh -c 'echo "274ff75d7d8ec0f8d91631bf606efdcd6aef3533c3b3568f972e13b198133416  .beagle/checks/T0518/T0518.v2.sh" | sha256sum -c --quiet && bash .beagle/checks/T0518/T0518.v2.sh'
