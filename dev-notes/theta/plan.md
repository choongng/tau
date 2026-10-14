# Theta — a public tau fork with Claude Code plugin support (idea, for later)

Status: parked idea, 2026-10-14. Start after the beagle 0.48 rotation (T0605).
This note names beagle, so it stays in tau's dev-notes and never ships in theta.

## Goal

- **Theta** (public): a fork of tau with
  - the core tau experience;
  - sub-agents;
  - Claude Code plugin support complete enough that beagle's plugin runs on it:
    marketplace/plugin manifests, skills, slash commands, agents and hooks.
- **Beagle** (private for now): gains tau/theta support in its own repo.
  Theta knows nothing about beagle.

## Where things stand (choong-dev vs origin/main, 10-14)

- **Core hardening:** about 3,000 lines in `src/`, all general. It covers
  repeat breaking, refusing chat-template tokens, cutting looping reasoning,
  continuing at the output limit, bash timeouts, refusing a tool run through
  bash, thinking warnings, llama.cpp prompt caching and the TUI CPU fix.
  `src/` never mentions beagle. The only leaks:
  - `session.py`: `pursuit_step` in `WORKSPACE_CHANGING_TOOLS`, plus 3
    comments;
  - `pyproject.toml`: the `real_beagle` marker and the `.beagle` ruff exclude;
  - pursuit tool names used as sample data in 4 test files.
- **Claude compat in core:** only `tau.register_skill_dir()`. The reader for
  `.claude-plugin/marketplace.json` lives inside the beagle extension. Tau
  does not load Claude plugins in general.
- **Beagle integration:** `examples/extensions/beagle.py`, about 17k lines.
  - It registers its own tools (`pursuit_found`/`plan`/`step` …) and commands.
  - It runs about 12 `tool_call` guards (seats, scope, records, bash,
    references).
  - It dispatches workers as `tau` subprocesses and wraps the beagle CLI.
  - It does in code what beagle's Claude plugin leaves to a strong model.
- **History doesn't split:** 1,412 commits past origin/main, of which 1,318 are
  pure beagle, 83 are clean and 11 are mixed. Cherry-picking is not worth it.

## Design

**Split.**
- Theta owns the generic mechanisms: plugin loading, hooks, sub-agents, and
  the extension API.
- Beagle owns its policy: the pursuit tools, guards and worker dispatch, as a
  theta extension shipped from the beagle repo (e.g. `beagle/hosts/theta/`).
  It also owns its plugin content.

This is "beagle decides, hosts carry" moved one level up. The 17k-line
extension shrinks wherever a Claude Code mechanism theta now supports can carry
the job: a guard becomes a PreToolUse hook, a worker becomes an agent.

**Second approach, rejected:** keep the beagle extension inside a private theta
branch. Every theta release would then need a beagle-scrubbed copy, and the
host/policy line would stay blurred. Owning the adapter in beagle keeps theta
public-safe by construction.

**Claude Code surface to support** (enough for beagle):
- **Plugins:** marketplace + `plugin.json` discovery, from user and project
  locations.
- **Skills:** `SKILL.md` under plugin roots; this already exists for tau's
  own dirs.
- **Commands:** `commands/*.md` as slash commands, with arguments.
- **Agents:** `agents/*.md` (model, tools, prompt), run as sub-agents.
- **Hooks:** the `hooks.json` events PreToolUse, PostToolUse, SessionStart,
  Stop and UserPromptSubmit, mapped onto tau's `tool_call`, `tool_result`,
  `session_start`, `agent_end` and `input` events. Hook stdout/exit-code
  semantics follow Claude Code.

**Sub-agents:** make them a core feature: a Task-style tool plus background
runs. Today beagle reaches them through the extension's subprocess dispatch
and the tau-subagents extension.

## Phases

1. **Fork and scrub.** Branch `theta` off current origin/main. Bring
   choong-dev's `src/`, tests (beagle tests excluded), website, `pyproject.toml`
   and `uv.lock` across at file level, and resolve against upstream.
   - Make `WORKSPACE_CHANGING_TOOLS` something an extension can extend.
   - Neutralize the comments and test sample data.
   - Gate: `git grep -iE 'beagle|pursuit'` is empty, and the full suite passes.
2. **Plugin loader:** manifests, skills, commands. Test it on a small public
   plugin, not beagle.
3. **Hooks compat:** Claude Code `hooks.json` onto theta events.
4. **Sub-agents:** agents/*.md and a Task-style tool, run in the background.
5. **Beagle adapter** (beagle repo, private). Port the extension onto theta's
   mechanisms and move what it can into plugin hooks/agents.
   - Gate: rerun the q35 rotation (wrenfold, semver, itc, cobs) through theta.
     It must match tau+extension's scores and times.
6. **Public release** of theta. Keep merging upstream tau (merge, don't
   rebase).

## Open questions

- Rename the package and CLI (`tau-ai`/`tau` → `theta`), or keep the module
  names to ease upstream merges?
- Public home: a new repo vs `choongng/tau`. Keep tau's MIT license and its
  attribution.
- Do core hardening changes still go upstream to tau via `upstream/*` topic
  branches, theta-first or in parallel?
- Does tau-only work (choong-dev) stop once theta exists, with choong-dev
  becoming theta + beagle adapter for the harness?
