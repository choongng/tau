---
title: "Extension Skill-Directory Registration"
---

## What was added

`tau.register_skill_dir(path)` — a new extension API that lets an extension add a
directory of Agent Skills discovered directly from disk, with no copying or
symlinking.

- `ExtensionAPI.register_skill_dir(path)` (`extensions/api.py`) forwards to the
  runtime, asserting the load generation first (Pi-style staleness guard).
- `ExtensionRuntime.register_skill_dir(...)` (`extensions/runtime.py`) validates
  the path, deduplicates by resolved path, and records the contribution as
  `(source_id, extension_name, path)`. A missing or non-directory path is a
  warning diagnostic and is not registered.
- `ExtensionRuntime.skill_dirs` exposes the ordered, de-duplicated directories.
- `load_skills` / `load_skills_with_diagnostics` (`skills.py`) gained an optional
  keyword `extra_skill_dirs`, scanned at the *lowest* precedence via a shared
  `_ordered_skill_dirs` helper.
- `CodingSession.load` and `CodingSession.reload` load project extensions before
  resources, then pass `extension_runtime.skill_dirs` into `_load_session_resources`.

## Why it exists

Skills were only discoverable from the fixed resource directories
(`~/.tau/skills`, `~/.agents/skills`, and the project's `.tau/.agents` skill
dirs). A plugin that ships its own skills tree — e.g. a Claude Code marketplace
plugin under `plugins/<name>/skills/<skill>/SKILL.md` — could only be reused by
symlinking every skill into a scanned directory, which is brittle and does not
survive reload cleanly.

Tau already exposes tool/command/provider/prompt registrations to extensions but
had no skill contribution seam. This adds exactly that seam: the plugin owns the
skill tree on disk, the extension points Tau at it, and the normal loader does
the rest.

## Precedence

`extra_skill_dirs` load first (lowest precedence), so the built-in user and
project `skills_dirs` override a same-named plugin skill, with the existing
"overrides lower-precedence resource" diagnostic. The intent is that plugins are
additive defaults and never silently shadow a user's own skill. Registering the
same directory twice (even from two extensions) collapses to one entry.

## Ordering subtlety

Project extensions load after the trust decision but must load before skills are
read so their `register_skill_dir` calls are seen in the same snapshot. The
non-project runtime is loaded before trust resolution (its `project_trust`
deciders still run first), so only the *project* extension load was moved ahead
of `_load_session_resources`; the trust diagnostic is still appended afterwards.
Resume, new-session, and branch all route through `CodingSession.load`, so they
pick up contributed skills too.

## Lifecycle

Contributions are source-owned like prompt sections and tools: `_remove_registrations`,
`retire()`, and `reset_for_reload()` drop them. A failed extension `setup()`
rolls back its registered skill directories. Skills become visible in the
`<available_skills>` index and `/skill:<name>` on the next load or `/reload`.

## How it maps to Pi

Pi has no extension skill-contribution API either; this is a Tau-specific seam
that ports the "plugin brings skills" idea while keeping the Agent Skills spec
(a skill is a directory containing `SKILL.md`) unchanged.

## How to test

- `tests/test_skills.py` — `extra_skill_dirs` loads, precedence/override
  diagnostic, and collapsing an already-scanned directory.
- `tests/test_extensions.py` — registration, missing-path diagnostic,
  de-duplication, failed-setup rollback, retire cleanup, plus a `CodingSession`
  integration test and a reload test showing a plugin skill survives `/reload`.

## See also

- [`../beagle-integration.md`](../beagle-integration.md) — a worked tutorial and
  reference for pointing this seam at the `beagle` Claude Code marketplace plugin.
