"""Tests for the Beagle example extension (`examples/extensions/beagle.py`).

The extension is loaded through a real `ExtensionRuntime` against a fake beagle
checkout, so these exercise its wiring without a beagle install.
"""

from __future__ import annotations

import asyncio
import functools
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tomllib
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import pytest

from tau_agent.events import AgentEndEvent, AgentStartEvent
from tau_agent.messages import AssistantMessage, TextContent, UserMessage
from tau_agent.tools import AgentTool, AgentToolResult
from tau_coding.commands import CommandContext
from tau_coding.events import AgentSettledEvent, CompactionEndEvent
from tau_coding.extensions import ExtensionRuntime
from tau_coding.resources import TauResourcePaths, parse_markdown_resource
from tau_coding.skills import parse_skill_invocation
from test_extensions import RecordingSession, RecordingUiBridge


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


EXTENSION = Path(__file__).resolve().parents[1] / "examples" / "extensions" / "beagle.py"


PLUGINS = ("beagle-dev", "beagle-pursuit", "beagle-reference")


def _marketplace(root: Path, plugins: dict[str, str]) -> None:
    """Write beagle's marketplace manifest listing `plugins` (name -> source)."""
    manifest = root / ".claude-plugin" / "marketplace.json"
    manifest.parent.mkdir(parents=True, exist_ok=True)
    entries = [{"name": name, "source": source} for name, source in plugins.items()]
    manifest.write_text(json.dumps({"name": "beagle", "plugins": entries}), encoding="utf-8")


def _skill(plugins: Path, plugin: str, name: str) -> Path:
    skill = plugins / plugin / "skills" / name
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: {name} skill\n---\n\nBody.\n", encoding="utf-8"
    )
    return skill


@pytest.fixture
def beagle(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """A fake beagle checkout: three plugins, listed in a marketplace manifest."""
    root = tmp_path / "beagle"
    plugins = root / "plugins"
    for plugin in PLUGINS:
        manifest = plugins / plugin / ".claude-plugin" / "plugin.json"
        manifest.parent.mkdir(parents=True)
        manifest.write_text(json.dumps({"name": plugin}), encoding="utf-8")
    _marketplace(root, {plugin: f"./plugins/{plugin}" for plugin in PLUGINS})
    _skill(plugins, "beagle-dev", "python-coding")
    _skill(plugins, "beagle-reference", "tilth-usage")
    for name in ("pursuit-dispatch", "offload", "containment", "hook-design"):
        _skill(plugins, "beagle-pursuit", name)
    commands = plugins / "beagle-pursuit" / "commands"
    commands.mkdir()
    (commands / "pursuit.md").write_text(
        "---\ndescription: driver\n---\n\nRead ${CLAUDE_PLUGIN_ROOT}/commands/pursuit.md\n",
        encoding="utf-8",
    )
    (commands / "pursuit-run.md").write_text(
        "---\nname: pursuit-run\n---\n\nArm with ScheduleWakeup; see ${CLAUDE_PLUGIN_ROOT}.\n",
        encoding="utf-8",
    )
    agents = plugins / "beagle-dev" / "agents"
    agents.mkdir()
    (agents / "step-executor.md").write_text(
        "---\nname: step-executor\ndescription: Executes one step: batch edits.\n"
        "tools: Read, Grep, Glob, Bash, Edit, Write, mcp__tilth__tilth_read\nmodel: sonnet\n"
        "---\n\nYou execute one step. See ${CLAUDE_PLUGIN_ROOT}/skills.\n",
        encoding="utf-8",
    )
    (agents / "scout.md").write_text(
        "---\ndescription: Read-only sift.\ntools: Read, Grep\n---\n\nYou sift.\n",
        encoding="utf-8",
    )

    monkeypatch.setenv("BEAGLE_ROOT", str(root))
    monkeypatch.setenv("BEAGLE_TAU_AGENTS_DIR", str(tmp_path / "agents"))
    # Recorded so teardown restores whatever the process had; setup overwrites it.
    monkeypatch.setenv("CLAUDE_PLUGIN_ROOT", "/inherited/beagle-dev")
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", "claude-session")
    monkeypatch.setenv("CLAUDE_PID", "4242")
    monkeypatch.setenv("BEAGLE_HOST", "inherited")
    # Recorded so teardown restores it; setup may put the checkout's bin/ first.
    monkeypatch.setenv("PATH", os.environ.get("PATH", ""))
    monkeypatch.delenv("BEAGLE_TAU_WORKER", raising=False)
    # Workers and checks run uncapped unless a test turns the cap on.
    monkeypatch.setenv("BEAGLE_TAU_MEMORY_MAX", "off")
    # Never the real beagle: a test that wants one takes `fake_beagle`.
    monkeypatch.setenv("BEAGLE_BIN", str(tmp_path / "no-beagle-bin"))
    monkeypatch.chdir(tmp_path)  # the process cwd is not a pursuit unless a test says so
    return root


FAKE_BEAGLE = """\
import json, os, sys
from pathlib import Path

here = Path(os.environ["FAKE_BEAGLE_DIR"])
stdin = sys.stdin.read()
with (here / "calls.jsonl").open("a") as log:
    log.write(json.dumps({"argv": sys.argv[1:], "cwd": os.getcwd(), "stdin": stdin}) + "\\n")
if sys.argv[1:3] == ["loop", "stop"]:  # as beagle does: no run in flight after
    (here / "read.out").unlink(missing_ok=True)
    (here / "read.rc").write_text("3")
if json.loads(stdin or "{}").get("stop_hook_active"):
    sys.exit(0)  # as beagle's Stop hooks do
reply = here / (sys.argv[2] + ".out")
if len(sys.argv) > 3 and (here / f"{sys.argv[2]}-{sys.argv[3]}.out").exists():
    reply = here / f"{sys.argv[2]}-{sys.argv[3]}.out"  # one task's own reply
if len(sys.argv) > 2 and reply.exists():
    sys.stdout.write(reply.read_text())
status = here / (sys.argv[2] + ".rc")
if len(sys.argv) > 2 and status.exists():
    sys.exit(int(status.read_text()))
"""


@pytest.fixture
def fake_beagle(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """A `beagle` that logs each call, prints `<argv[2]>-<argv[3]>.out` or else
    `<argv[2]>.out` when it exists, and exits with `<argv[2]>.rc`'s status (else 0)."""
    here = tmp_path / "fake-beagle"
    here.mkdir()
    script = here / "beagle"
    script.write_text(f"#!{sys.executable}\n{FAKE_BEAGLE}", encoding="utf-8")
    script.chmod(0o755)
    monkeypatch.setenv("BEAGLE_BIN", str(script))
    monkeypatch.setenv("FAKE_BEAGLE_DIR", str(here))
    return here


def _calls(fake: Path) -> list[dict[str, Any]]:
    log = fake / "calls.jsonl"
    if not log.exists():
        return []
    return [json.loads(line) for line in log.read_text().splitlines()]


def _block(reason: str) -> str:
    return json.dumps({"decision": "block", "reason": reason}) + "\n"


def _pursuit_project(tmp_path: Path) -> Path:
    project = tmp_path / "project"
    (project / ".beagle").mkdir(parents=True, exist_ok=True)
    (project / ".beagle" / "pursuit.toml").write_text(
        '[goal]\nstatement = "Ship it"\ncriteria = ["it ships"]\n', encoding="utf-8"
    )
    return project


def _bound(tmp_path: Path, *, ui: bool = True) -> tuple[ExtensionRuntime, RecordingSession]:
    runtime = _load(tmp_path)
    session = RecordingSession(tmp_path / "project", running=False)
    runtime.set_ui_bridge(RecordingUiBridge(has_ui=ui))  # type: ignore[arg-type]
    runtime.bind(session)  # type: ignore[arg-type]
    return runtime, session


def _tool(runtime: ExtensionRuntime, name: str) -> Any:
    [tool] = [t for t in runtime.compose_tools([]) if t.name == name]
    return tool


@functools.cache
def _module() -> Any:
    """The extension module itself, for the helpers no tool reaches."""
    spec = importlib.util.spec_from_file_location("beagle_extension_under_test", EXTENSION)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module  # dataclasses look their module up
    spec.loader.exec_module(module)
    return module


def _load(tmp_path: Path) -> ExtensionRuntime:
    (tmp_path / "project").mkdir(exist_ok=True)
    runtime = ExtensionRuntime()
    runtime.load(
        TauResourcePaths(
            root=tmp_path / "home-tau",
            cwd=tmp_path / "project",
            agents_root=tmp_path / "home-agents",
        ),
        extra_paths=(EXTENSION,),
        include_resource_dirs=False,
        include_user_dir=False,
    )
    assert [d.message for d in runtime.diagnostics] == []
    return runtime


def test_merged_plugin_root_links_every_plugins_skills(tmp_path: Path, beagle: Path) -> None:
    runtime = _load(tmp_path)
    root = tmp_path / "home-tau" / "beagle-plugin"

    assert runtime.skill_dirs == (root / "skills",)
    linked = sorted(p.name for p in (root / "skills").iterdir())
    assert linked == [
        "containment",
        "hook-design",
        "offload",
        "pursuit-dispatch",
        "python-coding",
        "tilth-usage",
    ]
    pursuit = beagle / "plugins" / "beagle-pursuit"
    assert (root / "skills" / "containment").resolve() == pursuit / "skills" / "containment"
    assert (root / "commands").resolve() == pursuit / "commands"
    assert (root / "agents").resolve() == beagle / "plugins" / "beagle-dev" / "agents"
    assert os.environ["CLAUDE_PLUGIN_ROOT"] == str(root)


@pytest.mark.anyio
async def test_layout_follows_the_marketplace_manifest(tmp_path: Path, beagle: Path) -> None:
    # Moved and renamed: the manifest says where each plugin now lives.
    shutil.move(beagle / "plugins", beagle / "pkgs")
    (beagle / "pkgs" / "beagle-pursuit").rename(beagle / "pkgs" / "pursuit")
    _marketplace(
        beagle,
        {
            "beagle-dev": "./pkgs/beagle-dev",
            "beagle-pursuit": "./pkgs/pursuit",
            "beagle-reference": "./pkgs/beagle-reference",
        },
    )
    runtime, _ = _bound(tmp_path)
    await runtime.emit_session_start("startup")

    root = tmp_path / "home-tau" / "beagle-plugin"
    pursuit = beagle / "pkgs" / "pursuit"
    assert (root / "commands").resolve() == pursuit / "commands"
    assert (root / "skills" / "offload").resolve() == pursuit / "skills" / "offload"
    registry = runtime.build_command_registry()
    assert registry.get("pursuit") is not None and registry.get("pursuit-run") is not None
    assert not [s for s in runtime.prompt_sections if s.title == "Beagle extension problems"]


def test_checkout_without_a_manifest_is_scanned(tmp_path: Path, beagle: Path) -> None:
    (beagle / ".claude-plugin" / "marketplace.json").unlink()
    (beagle / "plugins" / "stale-tooling-only").mkdir()  # no plugin.json: not a plugin

    runtime = _load(tmp_path)

    root = tmp_path / "home-tau" / "beagle-plugin"
    assert (root / "commands").resolve() == beagle / "plugins" / "beagle-pursuit" / "commands"
    assert runtime.build_command_registry().get("pursuit-run") is not None


@pytest.mark.anyio
async def test_missing_plugin_and_skill_clash_are_reported(tmp_path: Path, beagle: Path) -> None:
    _marketplace(
        beagle,
        {
            "beagle-dev": "./plugins/beagle-dev",
            "beagle-pursuit": "./plugins/beagle-pursuit",
            "beagle-reference": "./plugins/beagle-reference",
            "beagle-gone": "./plugins/beagle-gone",
        },
    )
    _skill(beagle / "plugins", "beagle-reference", "offload")
    runtime = _load(tmp_path)
    session = RecordingSession(tmp_path / "project", running=False)
    ui = RecordingUiBridge(has_ui=True)
    runtime.set_ui_bridge(ui)  # type: ignore[arg-type]
    runtime.bind(session)  # type: ignore[arg-type]

    await runtime.emit_session_start("startup")

    [(notice, level)] = ui.notifications
    assert level == "warning"
    assert "lists beagle-gone at ./plugins/beagle-gone, which is missing" in notice
    assert "'offload' ships in both beagle-pursuit and beagle-reference" in notice
    offload = tmp_path / "home-tau" / "beagle-plugin" / "skills" / "offload"
    assert offload.resolve() == beagle / "plugins" / "beagle-pursuit" / "skills" / "offload"


def test_merged_plugin_root_prunes_only_stale_symlinks(tmp_path: Path, beagle: Path) -> None:
    skills = tmp_path / "home-tau" / "beagle-plugin" / "skills"
    skills.mkdir(parents=True)
    (skills / "gone").symlink_to(tmp_path / "nowhere", target_is_directory=True)
    (skills / "mine").mkdir()

    _load(tmp_path)
    _load(tmp_path)  # idempotent

    assert not (skills / "gone").is_symlink()
    assert (skills / "mine").is_dir()
    assert (skills / "python-coding").is_symlink()


def test_renamed_checkout_relinks_and_drops_dangling_trees(tmp_path: Path, beagle: Path) -> None:
    root = tmp_path / "home-tau" / "beagle-plugin"
    root.mkdir(parents=True)
    # What a load against the pre-rename layout left behind.
    (root / "commands").symlink_to(
        beagle / "plugins" / "beagle-campaign" / "commands", target_is_directory=True
    )
    (root / "agents").symlink_to(tmp_path / "gone-agents", target_is_directory=True)
    shutil.rmtree(beagle / "plugins" / "beagle-dev" / "agents")

    _load(tmp_path)

    assert (root / "commands").resolve() == beagle / "plugins" / "beagle-pursuit" / "commands"
    assert not (root / "agents").is_symlink()


@pytest.mark.anyio
async def test_missing_driver_is_not_registered_and_is_reported(
    tmp_path: Path, beagle: Path
) -> None:
    shutil.rmtree(beagle / "plugins" / "beagle-pursuit" / "commands")
    runtime = _load(tmp_path)
    session = RecordingSession(tmp_path / "project", running=False)
    ui = RecordingUiBridge(has_ui=True)
    runtime.set_ui_bridge(ui)  # type: ignore[arg-type]
    runtime.bind(session)  # type: ignore[arg-type]

    await runtime.emit_session_start("startup")

    registry = runtime.build_command_registry()
    assert registry.get("pursuit") is None and registry.get("pursuit-run") is None
    assert registry.get("pursuit-view") is not None
    [(notice, level)] = ui.notifications
    assert level == "warning"
    assert "/pursuit-run is not registered" in notice and "pursuit-run.md" in notice
    [section] = [s for s in runtime.prompt_sections if s.title == "Beagle extension problems"]
    assert "Do not offer a command listed here" in section.body


def test_complete_checkout_reports_no_problems(tmp_path: Path, beagle: Path) -> None:
    runtime = _load(tmp_path)

    assert not [s for s in runtime.prompt_sections if s.title == "Beagle extension problems"]


def test_pursuit_driver_spells_out_plugin_root(tmp_path: Path, beagle: Path) -> None:
    runtime = _load(tmp_path)
    session = RecordingSession(tmp_path / "project", running=True)
    runtime.bind(session)  # type: ignore[arg-type]
    registry = runtime.build_command_registry()
    command = registry.get("pursuit")
    assert command is not None

    context = CommandContext(
        session=None,  # type: ignore[arg-type]
        registry=registry,
        text="/pursuit go",
        name="pursuit",
        args="go",
    )
    command.handler(context)

    [turn] = session.followed_up
    root = tmp_path / "home-tau" / "beagle-plugin"
    invocation = parse_skill_invocation(turn)
    assert invocation is not None
    assert invocation.name == "pursuit"
    assert invocation.location == str(root / "commands" / "pursuit.md")
    assert invocation.additional_instructions == "go"
    assert f"Read {root}/commands/pursuit.md" in invocation.content
    assert "${CLAUDE_PLUGIN_ROOT}" not in turn
    assert "description: driver" not in turn


def _ship_cli(beagle: Path) -> Path:
    shim = beagle / "plugins" / "beagle-pursuit" / "bin" / "beagle"
    shim.parent.mkdir()
    shim.write_text("#!/bin/sh\necho beagle 0.0.0\n", encoding="utf-8")
    shim.chmod(0o755)
    return shim


def test_checkout_cli_is_linked_and_first_on_path(
    tmp_path: Path, beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    shim = _ship_cli(beagle)
    stale = tmp_path / "stale-bin"
    monkeypatch.setenv("PATH", os.pathsep.join([str(stale), os.environ["PATH"]]))

    _load(tmp_path)
    _load(tmp_path)  # a reload does not stack a second entry

    bin_dir = tmp_path / "home-tau" / "beagle-plugin" / "bin"
    assert (bin_dir / "beagle").resolve() == shim
    entries = os.environ["PATH"].split(os.pathsep)
    assert entries[0] == str(bin_dir) and entries.count(str(bin_dir)) == 1
    assert shutil.which("beagle") == str(bin_dir / "beagle")


def test_checkout_without_a_cli_leaves_path_alone(tmp_path: Path, beagle: Path) -> None:
    before = os.environ["PATH"]

    _load(tmp_path)

    assert os.environ["PATH"] == before
    assert not (tmp_path / "home-tau" / "beagle-plugin" / "bin").exists()


@pytest.mark.anyio
async def test_pursuit_driver_tool_returns_the_driver(tmp_path: Path, beagle: Path) -> None:
    runtime, session = _bound(tmp_path)
    driver = _tool(runtime, "pursuit_driver")
    root = tmp_path / "home-tau" / "beagle-plugin"

    found = await driver.execute("c1", {"command": "pursuit", "args": "found it"})
    run = await driver.execute("c2", {"command": "pursuit-run"})
    bad = await driver.execute("c3", {"command": "campaign"})

    invocation = parse_skill_invocation(found.text)
    assert invocation is not None and invocation.name == "pursuit"
    assert invocation.additional_instructions == "found it"
    assert f"Read {root}/commands/pursuit.md" in invocation.content
    run_invocation = parse_skill_invocation(run.text)
    assert run_invocation is not None and "Host mapping" in run_invocation.content
    assert "must be 'pursuit' or 'pursuit-run'" in bad.text
    assert session.followed_up == []  # returned in-turn, not queued as a new turn


def test_unfounded_project_is_told_how_to_found_one(tmp_path: Path, beagle: Path) -> None:
    _ship_cli(beagle)

    runtime = _load(tmp_path)

    [section] = [s for s in runtime.prompt_sections if s.title == "Beagle"]
    assert "not a beagle pursuit yet" in section.body
    assert "`pursuit_driver`" in section.body
    assert str(tmp_path / "home-tau" / "beagle-plugin" / "bin" / "beagle") in section.body
    assert "~/.claude/plugins/cache" in section.body
    assert not [s for s in runtime.prompt_sections if s.title == "Beagle pursuit"]


def test_founded_project_gets_no_unfounded_section(
    tmp_path: Path, beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(_pursuit_project(tmp_path))

    runtime = _load(tmp_path)

    titles = [s.title for s in runtime.prompt_sections]
    assert "Beagle pursuit" in titles and "Beagle" not in titles


def test_missing_checkout_registers_no_skills(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("BEAGLE_ROOT", str(tmp_path / "no-beagle"))
    monkeypatch.setenv("CLAUDE_PLUGIN_ROOT", "/inherited")

    runtime = _load(tmp_path)

    assert runtime.skill_dirs == ()
    assert not (tmp_path / "home-tau" / "beagle-plugin").exists()
    assert os.environ["CLAUDE_PLUGIN_ROOT"] == "/inherited"


def _run_command(runtime: ExtensionRuntime, name: str, args: str = "") -> None:
    registry = runtime.build_command_registry()
    command = registry.get(name)
    assert command is not None
    context = CommandContext(
        session=None,  # type: ignore[arg-type]
        registry=registry,
        text=f"/{name} {args}".strip(),
        name=name,
        args=args,
    )
    command.handler(context)


# -- /pursuit-run bridge -------------------------------------------------------


@pytest.mark.anyio
async def test_session_start_names_the_tau_session_to_beagle(tmp_path: Path, beagle: Path) -> None:
    runtime, session = _bound(tmp_path)

    await runtime.emit_session_start("startup")

    assert os.environ["CLAUDE_CODE_SESSION_ID"] == session.session_id
    assert "CLAUDE_PID" not in os.environ


def test_pursuit_run_injects_host_mapping_and_driver(tmp_path: Path, beagle: Path) -> None:
    runtime, session = _bound(tmp_path)
    session.is_running = True

    _run_command(runtime, "pursuit-run")

    [turn] = session.followed_up
    root = tmp_path / "home-tau" / "beagle-plugin"
    invocation = parse_skill_invocation(turn)
    assert invocation is not None
    assert invocation.name == "pursuit-run"
    assert invocation.additional_instructions is None
    body = invocation.content
    # The host mapping qualifies the driver, so it sits inside the block ahead of it.
    assert body.index("Host mapping") < body.index(f"Arm with ScheduleWakeup; see {root}.")
    assert "`pursuit_wakeup`" in body and "`pursuit_dispatch`" in body
    assert "--for N --resuming-in N" in body
    assert "name: pursuit-run" not in turn


def _capture_timers(monkeypatch: pytest.MonkeyPatch) -> list[tuple[float, Any, tuple[Any, ...]]]:
    """Record wakeup timers instead of waiting on them; fire with `_fire`.

    Only a delay of a minute or more is a wakeup's; shorter ones (`sleep`,
    `wait_for`) are asyncio's own and run as normal.
    """
    loop = asyncio.get_running_loop()
    timers: list[tuple[float, Any, tuple[Any, ...]]] = []
    real = loop.call_later

    def record(delay: float, callback: Any, *args: Any) -> Any:
        if delay < 60:
            return real(delay, callback, *args)
        timers.append((delay, callback, args))
        return real(3600, lambda: None)

    monkeypatch.setattr(loop, "call_later", record)
    return timers


async def _fire(timer: tuple[float, Any, tuple[Any, ...]]) -> None:
    _, callback, args = timer
    callback(*args)
    for _ in range(50):  # let a delivery task, and any beagle subprocess, finish
        await asyncio.sleep(0.01)


@pytest.mark.anyio
async def test_wakeup_arms_replaces_and_disarms(tmp_path: Path, beagle: Path) -> None:
    runtime, session = _bound(tmp_path)
    wakeup = _tool(runtime, "pursuit_wakeup")

    armed = await wakeup.execute("c1", {"delay_minutes": 0.2})
    assert "armed" in armed.text and "--resuming-in 1" in armed.text
    again = await wakeup.execute("c2", {"delay_minutes": 90, "prompt": "/pursuit-run"})
    assert "replacing the previous wakeup" in again.text
    assert "--resuming-in 60" in again.text

    stopped = await wakeup.execute("c3", {"stop": True})
    assert stopped.text == "pursuit_wakeup: disarmed before it fired."
    nothing = await wakeup.execute("c4", {"stop": True})
    assert nothing.text.startswith("pursuit_wakeup: nothing was armed")
    assert session.followed_up == []


@pytest.mark.anyio
async def test_wakeup_fire_expands_pursuit_run(
    tmp_path: Path, beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    runtime, session = _bound(tmp_path)
    timers = _capture_timers(monkeypatch)
    await _tool(runtime, "pursuit_wakeup").execute("c1", {"delay_minutes": 2})

    [timer] = timers
    assert timer[0] == 120
    await _fire(timer)

    [turn] = session.followed_up
    invocation = parse_skill_invocation(turn)
    assert invocation is not None and invocation.name == "pursuit-run"
    assert invocation.content.startswith("References are relative to")
    assert "Host mapping" in invocation.content


@pytest.mark.anyio
async def test_wakeup_fire_expands_pursuit(
    tmp_path: Path, beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    runtime, session = _bound(tmp_path)
    timers = _capture_timers(monkeypatch)
    await _tool(runtime, "pursuit_wakeup").execute("c1", {"prompt": "/pursuit next"})
    await _fire(timers[0])

    [turn] = session.followed_up
    invocation = parse_skill_invocation(turn)
    assert invocation is not None and invocation.name == "pursuit"
    assert invocation.additional_instructions == "next"


@pytest.mark.anyio
async def test_wakeup_firing_mid_turn_waits_for_the_settle(
    tmp_path: Path, beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    runtime, session = _bound(tmp_path)
    timers = _capture_timers(monkeypatch)
    await _tool(runtime, "pursuit_wakeup").execute("c1", {"prompt": "resume"})
    session.is_running = True

    await _fire(timers[0])
    assert session.followed_up == []  # nothing queued behind the running turn
    await runtime.emit_event(AgentSettledEvent())

    assert session.followed_up == ["resume"]


@pytest.mark.anyio
async def test_stop_voids_a_fired_wakeup_pending_delivery(
    tmp_path: Path, beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    runtime, session = _bound(tmp_path)
    timers = _capture_timers(monkeypatch)
    wakeup = _tool(runtime, "pursuit_wakeup")
    await wakeup.execute("c1", {"prompt": "resume"})
    session.is_running = True
    await _fire(timers[0])

    stopped = await wakeup.execute("c2", {"stop": True})
    await runtime.emit_event(AgentSettledEvent())

    assert "already fired" in stopped.text and "now voided" in stopped.text
    assert session.followed_up == []


@pytest.mark.anyio
async def test_rearm_voids_a_fired_wakeup_pending_delivery(
    tmp_path: Path, beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    runtime, session = _bound(tmp_path)
    timers = _capture_timers(monkeypatch)
    wakeup = _tool(runtime, "pursuit_wakeup")
    await wakeup.execute("c1", {"prompt": "first"})
    session.is_running = True
    await _fire(timers[0])

    await wakeup.execute("c2", {"prompt": "second", "delay_minutes": 30})
    await runtime.emit_event(AgentSettledEvent())
    await _fire(timers[0])  # the stale timer, had it not been cancelled

    assert session.followed_up == []
    session.is_running = False
    await _fire(timers[1])
    assert session.followed_up == ["second"]


@pytest.mark.anyio
async def test_wakeup_is_dropped_once_its_loop_run_stops(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    project = _pursuit_project(tmp_path)
    (fake_beagle / "read.out").write_text("2026-09-29T10:00:00+00:00\n", encoding="utf-8")
    runtime = _load(tmp_path)
    session = RecordingSession(project, running=False)
    ui = RecordingUiBridge(has_ui=True)
    runtime.set_ui_bridge(ui)  # type: ignore[arg-type]
    runtime.bind(session)  # type: ignore[arg-type]
    timers = _capture_timers(monkeypatch)
    await _tool(runtime, "pursuit_wakeup").execute("c1", {})

    (fake_beagle / "read.out").unlink()
    (fake_beagle / "read.rc").write_text("3", encoding="utf-8")  # `beagle loop stop` ran
    await _fire(timers[0])

    assert session.followed_up == []
    [(notice, _)] = ui.notifications
    assert "no longer in flight" in notice
    reads = [c["argv"] for c in _calls(fake_beagle) if c["argv"][:2] == ["loop", "read"]]
    assert reads == [["loop", "read", "--root", str(project)]] * 2


@pytest.mark.anyio
async def test_wakeup_refuses_without_ui(tmp_path: Path, beagle: Path) -> None:
    runtime, _ = _bound(tmp_path, ui=False)

    result = await _tool(runtime, "pursuit_wakeup").execute("c1", {"delay_minutes": 1})

    assert "REFUSED" in result.text


@pytest.mark.anyio
async def test_commit_claims_block_stops_the_bash_call(
    tmp_path: Path, beagle: Path, fake_beagle: Path
) -> None:
    project = _pursuit_project(tmp_path)
    (fake_beagle / "commit-claims.out").write_text(_block("no Claims block"), encoding="utf-8")
    runtime, _ = _bound(tmp_path)
    bash = _tool_with_hooks(runtime)

    ls = await bash.execute("c0", {"command": "ls"})
    committed = await bash.execute("c1", {"command": "git commit -m wip"})

    assert ls.text == "ran"
    assert committed.text == "Tool call blocked: beagle commit-claims: no Claims block"
    [call] = [c for c in _calls(fake_beagle) if "commit-claims" in c["argv"]]
    assert call["argv"] == ["hook", "commit-claims"]
    assert Path(call["cwd"]) == project
    payload = json.loads(call["stdin"])
    assert payload["tool_name"] == "Bash"
    assert payload["tool_input"] == {"command": "git commit -m wip"}


def _tool_with_hooks(runtime: ExtensionRuntime, name: str = "bash") -> Any:
    async def run(*_: Any, **__: Any) -> AgentToolResult:
        return AgentToolResult(content=[TextContent(text="ran")])

    tool = AgentTool(name=name, label=name, description="", parameters={}, execute_fn=run)
    [wrapped] = [t for t in runtime.compose_tools([tool]) if t.name == name]
    return wrapped


def _end(stop_reason: str = "stop") -> AgentEndEvent:
    message = AssistantMessage(content=[], stop_reason=stop_reason)  # type: ignore[arg-type]
    return AgentEndEvent(messages=[message])


@pytest.mark.anyio
async def test_loop_guard_objection_starts_one_more_turn(
    tmp_path: Path, beagle: Path, fake_beagle: Path
) -> None:
    project = _pursuit_project(tmp_path)
    (fake_beagle / "loop-guard.out").write_text(_block("arm the next turn"), encoding="utf-8")
    runtime, session = _bound(tmp_path)

    await runtime.emit_event(_end())
    await runtime.emit_event(AgentSettledEvent())
    await runtime.emit_event(_end())
    await runtime.emit_event(AgentSettledEvent())

    # The objection became one follow-up; the settle after it went through
    # with stop_hook_active, so the fake's block was not delivered twice.
    assert session.followed_up == ["[beagle loop-guard]\n\narm the next turn"]
    guards = [c for c in _calls(fake_beagle) if "loop-guard" in c["argv"]]
    assert [json.loads(c["stdin"])["stop_hook_active"] for c in guards] == [False, True]
    assert all(Path(c["cwd"]) == project for c in guards)
    assert json.loads(guards[0]["stdin"])["session_id"] == session.session_id


@pytest.mark.anyio
async def test_loop_guard_skips_interrupted_runs_and_print_mode(
    tmp_path: Path, beagle: Path, fake_beagle: Path
) -> None:
    _pursuit_project(tmp_path)
    (fake_beagle / "loop-guard.out").write_text(_block("keep going"), encoding="utf-8")
    runtime, session = _bound(tmp_path)

    await runtime.emit_event(_end("aborted"))
    await runtime.emit_event(AgentSettledEvent())
    # Aborted mid-stream: the run settles without ever reaching `agent_end`.
    await runtime.emit_event(_end())
    await runtime.emit_event(AgentStartEvent())
    await runtime.emit_event(AgentSettledEvent())
    # Cut off at the output limit: an objection would land on a full context.
    await runtime.emit_event(_end("length"))
    await runtime.emit_event(AgentSettledEvent())
    headless, headless_session = _bound(tmp_path, ui=False)
    await headless.emit_event(_end())
    await headless.emit_event(AgentSettledEvent())

    assert session.followed_up == [] and headless_session.followed_up == []
    assert not [c for c in _calls(fake_beagle) if "loop-guard" in c["argv"]]


def _awaiting_worker(
    project: Path, fake: Path, *, driver: str = "session-1", minutes_ago: int = 5
) -> None:
    """A run driven by `driver`, waiting on a worker whose open task owns `src/`."""
    at = (datetime.now(UTC) - timedelta(minutes=minutes_ago)).isoformat()
    record = {
        "started_at": at,
        "driver_session": driver,
        "awaiting": "step-executor on T0002",
        "awaiting_at": at,
        "awaiting_minutes": 30,
    }
    (project / ".beagle" / "loop.json").write_text(json.dumps(record), encoding="utf-8")
    (fake / "read.out").write_text(json.dumps(record), encoding="utf-8")
    (fake / "tree.out").write_text(json.dumps([{"id": "T0002", "status": "open"}]))
    (fake / "show.out").write_text(json.dumps({"id": "T0002", "scope": ["src/", "Makefile"]}))


@pytest.mark.anyio
async def test_driver_is_kept_out_of_an_awaited_workers_scope(
    tmp_path: Path, beagle: Path, fake_beagle: Path
) -> None:
    project = _pursuit_project(tmp_path)
    _awaiting_worker(project, fake_beagle)
    runtime, _ = _bound(tmp_path)
    edit, bash = _tool_with_hooks(runtime, "edit"), _tool_with_hooks(runtime, "bash")

    blocked = [
        await edit.execute("c1", {"path": "src/app.py", "old_text": "a", "new_text": "b"}),
        await bash.execute("c2", {"command": "sed -i s/a/b/ src/app.py"}),
        await bash.execute("c3", {"command": "echo all: > Makefile"}),
        await bash.execute("c4", {"command": "rm -rf src"}),
        await bash.execute("c5", {"command": "git reset --hard"}),
    ]
    allowed = [
        await edit.execute("c6", {"path": "docs/notes.md", "old_text": "a", "new_text": "b"}),
        await bash.execute("c7", {"command": "grep -rn TODO src > /tmp/todo.txt"}),
        await bash.execute("c8", {"command": "pytest src"}),
    ]

    assert all("refusing to write" in r.text for r in blocked), [r.text for r in blocked]
    assert "T0002" in blocked[0].text and "`src/`" in blocked[0].text
    assert "bare `beagle loop tick`" in blocked[0].text
    assert [r.text for r in allowed] == ["ran"] * 3
    # The loop record did not change, so beagle was asked once.
    assert [c["argv"][1] for c in _calls(fake_beagle)] == ["read", "tree", "show"]


@pytest.mark.anyio
@pytest.mark.parametrize(("driver", "minutes_ago"), [("subagent-session", 5), ("session-1", 31)])
async def test_scope_guard_passes_subagents_and_lapsed_waits(
    tmp_path: Path, beagle: Path, fake_beagle: Path, driver: str, minutes_ago: int
) -> None:
    project = _pursuit_project(tmp_path)
    _awaiting_worker(project, fake_beagle, driver=driver, minutes_ago=minutes_ago)
    runtime, _ = _bound(tmp_path)

    result = await _tool_with_hooks(runtime, "write").execute(
        "c1", {"path": "src/app.py", "content": "x"}
    )

    assert result.text == "ran"


@pytest.mark.anyio
async def test_scope_guard_rereads_when_the_wait_is_cleared(
    tmp_path: Path, beagle: Path, fake_beagle: Path
) -> None:
    project = _pursuit_project(tmp_path)
    _awaiting_worker(project, fake_beagle)
    runtime, _ = _bound(tmp_path)
    write = _tool_with_hooks(runtime, "write")

    before = await write.execute("c1", {"path": "src/app.py", "content": "x"})
    cleared = {"started_at": "2026-01-01T00:00:00+00:00", "driver_session": "session-1"}
    (project / ".beagle" / "loop.json").write_text(json.dumps(cleared) + "\n")
    (fake_beagle / "read.out").write_text(json.dumps(cleared))
    after = await write.execute("c2", {"path": "src/app.py", "content": "x"})

    assert "refusing to write" in before.text
    assert after.text == "ran"


def _install_hooks(project: Path, *names: str, timeout: int = 900) -> None:
    """Write `.claude/settings.json` as `beagle hooks install NAMES` would."""
    events = {
        "Stop": {"cadence", "close-out", "loop-guard"},
        "SessionStart": {"cadence-report", "loop-report", "tilth-load"},
    }
    hooks: dict[str, list[Any]] = {}
    for name in names:
        event = next((e for e, members in events.items() if name in members), "PreToolUse")
        entry = {"type": "command", "command": f"beagle hook {name}", "timeout": timeout}
        hooks.setdefault(event, []).append({"hooks": [{**entry, "beagle": name}]})
    settings = project / ".claude" / "settings.json"
    settings.parent.mkdir(parents=True, exist_ok=True)
    settings.write_text(json.dumps({"hooks": hooks}), encoding="utf-8")


@pytest.mark.anyio
async def test_installed_stop_hooks_share_one_objection_per_stop(
    tmp_path: Path, beagle: Path, fake_beagle: Path
) -> None:
    project = _pursuit_project(tmp_path)
    _install_hooks(project, "close-out", "commit-trailer")
    (fake_beagle / "loop-guard.out").write_text(_block("arm the next turn"), encoding="utf-8")
    (fake_beagle / "close-out.out").write_text(_block("gates failed"), encoding="utf-8")
    (fake_beagle / "cadence.out").write_text(_block("not installed"), encoding="utf-8")
    runtime, session = _bound(tmp_path)

    await runtime.emit_event(_end())
    await runtime.emit_event(AgentSettledEvent())
    await runtime.emit_event(_end())
    await runtime.emit_event(AgentSettledEvent())

    # Both objections became one turn; `cadence` is not installed, so it never ran.
    assert session.followed_up == [
        "[beagle loop-guard]\n\narm the next turn\n\n[beagle close-out]\n\ngates failed"
    ]
    stops = [c for c in _calls(fake_beagle) if c["argv"][1] in ("loop-guard", "close-out")]
    assert [c["argv"][1] for c in stops] == ["loop-guard", "close-out"] * 2
    assert [json.loads(c["stdin"])["stop_hook_active"] for c in stops] == [False] * 2 + [True] * 2
    assert all(Path(c["cwd"]) == project for c in stops)
    assert not [c for c in _calls(fake_beagle) if c["argv"][1] == "cadence"]


@pytest.mark.anyio
async def test_installed_close_out_runs_outside_a_pursuit(
    tmp_path: Path, beagle: Path, fake_beagle: Path
) -> None:
    project = tmp_path / "project"
    _install_hooks(project, "cadence")
    (fake_beagle / "cadence.out").write_text(_block("a blocking cadence failed"))
    runtime, session = _bound(tmp_path)

    await runtime.emit_event(_end())
    await runtime.emit_event(AgentSettledEvent())

    assert session.followed_up == ["[beagle cadence]\n\na blocking cadence failed"]
    assert [c["argv"] for c in _calls(fake_beagle)] == [["hook", "cadence"]]


@pytest.mark.anyio
async def test_installed_commit_trailer_joins_commit_claims(
    tmp_path: Path, beagle: Path, fake_beagle: Path
) -> None:
    project = _pursuit_project(tmp_path)
    _install_hooks(project, "commit-trailer")
    (fake_beagle / "commit-trailer.out").write_text(_block("forbidden Co-Authored-By"))
    runtime, _ = _bound(tmp_path)
    bash = _tool_with_hooks(runtime)

    ls = await bash.execute("c0", {"command": "ls"})
    committed = await bash.execute("c1", {"command": "git commit -m wip"})

    assert ls.text == "ran"
    assert committed.text == "Tool call blocked: beagle commit-trailer: forbidden Co-Authored-By"
    calls = _calls(fake_beagle)
    assert [c["argv"] for c in calls] == [["hook", "commit-claims"], ["hook", "commit-trailer"]]
    assert all(Path(c["cwd"]) == project for c in calls)


@pytest.mark.anyio
async def test_cadence_report_joins_the_prompt_and_unbridged_hooks_are_noted_once(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    project = tmp_path / "project"
    _install_hooks(project, "cadence-report", "tilth-load", "transcript-guard", "loop-report")
    (fake_beagle / "cadence-report.out").write_text("beagle: 1 cadence overdue: audit\n")
    monkeypatch.chdir(project)
    runtime = _load(tmp_path)
    ui = RecordingUiBridge(has_ui=True)
    runtime.set_ui_bridge(ui)  # type: ignore[arg-type]
    runtime.bind(RecordingSession(project, running=False))  # type: ignore[arg-type]

    await runtime.emit_session_start("startup")
    await runtime.emit_session_start("resume")

    [section] = [s for s in runtime.prompt_sections if s.title == "Beagle cadences"]
    assert section.body.endswith("beagle: 1 cadence overdue: audit")
    [call] = _calls(fake_beagle)
    assert call["argv"] == ["hook", "cadence-report"]
    assert json.loads(call["stdin"])["source"] == "startup"
    [(notice, level)] = ui.notifications
    assert level == "info"
    assert "tilth-load (" in notice and "transcript-guard (" in notice
    assert "loop-report" not in notice and "cadence-report" not in notice


def test_beagle_subprocesses_are_told_the_host_is_tau(tmp_path: Path, beagle: Path) -> None:
    runtime, session = _bound(tmp_path)
    _run_command(runtime, "pursuit-run")

    assert os.environ["BEAGLE_HOST"] == "tau"
    # The host note says installing hooks switches them on, not to avoid it.
    note = " ".join(session.followed_up[0].split())
    assert "Do not run `beagle hooks install`" not in note
    assert "`commit-trailer` when `beagle hooks install` has put them" in note


def test_loop_report_joins_the_pursuit_section(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    project = _pursuit_project(tmp_path)
    (fake_beagle / "loop-report.out").write_text("beagle: a run is still open here\n")
    monkeypatch.chdir(project)

    runtime = _load(tmp_path)

    [section] = [s for s in runtime.prompt_sections if s.title == "Beagle pursuit"]
    assert "This project is a **pursuit**: Ship it" in section.body
    assert section.body.endswith("beagle: a run is still open here")
    [call] = _calls(fake_beagle)
    assert call["argv"] == ["hook", "loop-report"]
    assert json.loads(call["stdin"])["hook_event_name"] == "SessionStart"


def test_driver_is_told_to_steer_and_a_worker_to_go_piece_by_piece(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    project = _pursuit_project(tmp_path)
    monkeypatch.chdir(project)

    [driver] = [s for s in _load(tmp_path).prompt_sections if s.title == "Beagle pursuit"]
    monkeypatch.setenv("BEAGLE_TAU_WORKER", "1")
    [worker] = [s for s in _load(tmp_path).prompt_sections if s.title == "Beagle pursuit"]

    assert "Do not fetch or read the reference" in driver.body
    assert "one piece per turn" not in driver.body
    assert "Ship it" in worker.body and "Write the concrete cases first" in worker.body
    assert "this session steers" not in worker.body
    assert "Cases first" in driver.body and "Cases first" not in worker.body
    assert "Never set a git identity" in driver.body
    assert "Never set a git identity" in worker.body
    # Run 11c ran `/pursuit-run`, named here, through bash.
    assert "/pursuit" not in driver.body and "call the `pursuit_driver` tool" in driver.body


@pytest.mark.anyio
async def test_worker_runs_no_loop_and_keeps_parent_session(
    tmp_path: Path, beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("BEAGLE_TAU_WORKER", "1")
    runtime, _ = _bound(tmp_path)

    await runtime.emit_session_start("startup")

    assert runtime.build_command_registry().get("pursuit-run") is None
    assert runtime.compose_tools([]) == []  # one step does not dispatch another
    assert os.environ["CLAUDE_CODE_SESSION_ID"] == "claude-session"


def test_beagle_agents_become_subagent_types(tmp_path: Path, beagle: Path) -> None:
    _load(tmp_path)
    agents = tmp_path / "agents"
    assert sorted(p.name for p in agents.iterdir()) == [
        "beagle-dev:scout.md",
        "beagle-dev:step-executor.md",
    ]
    metadata, body = parse_markdown_resource(
        (agents / "beagle-dev:step-executor.md").read_text(encoding="utf-8")
    )
    assert metadata["description"] == "Executes one step: batch edits."
    # Claude tool names map onto Tau's; Grep/Glob fold into bash, MCP drops.
    assert metadata["tools"] == "read, bash, edit, write"
    assert "model" not in metadata  # a Claude alias names no Tau model
    assert "You run as a Tau sub-agent" in body
    assert f"See {tmp_path / 'home-tau' / 'beagle-plugin'}/skills." in body
    scout, _ = parse_markdown_resource((agents / "beagle-dev:scout.md").read_text())
    assert scout["tools"] == "read, bash"


def test_agent_types_keep_user_files_and_prune_stale_ones(tmp_path: Path, beagle: Path) -> None:
    agents = tmp_path / "agents"
    agents.mkdir()
    mine = agents / "beagle-dev:scout.md"
    mine.write_text("---\ndescription: my own scout\n---\nMine.\n", encoding="utf-8")
    stale = agents / "beagle-dev:gone.md"
    stale.write_text("---\ngenerated_by: beagle-tau-extension\n---\nOld.\n", encoding="utf-8")
    unrelated = agents / "reviewer.md"
    unrelated.write_text("Review.\n", encoding="utf-8")

    _load(tmp_path)
    _load(tmp_path)  # idempotent

    assert mine.read_text(encoding="utf-8").endswith("Mine.\n")
    assert not stale.exists()
    assert unrelated.exists()
    assert (agents / "beagle-dev:step-executor.md").exists()


def test_pursuit_run_routes_dispatch_through_background_agents(
    tmp_path: Path, beagle: Path
) -> None:
    runtime, session = _bound(tmp_path)
    session.is_running = True
    _run_command(runtime, "pursuit-run")
    [turn] = session.followed_up
    assert 'subagent_type: "beagle-dev:step-executor"' in " ".join(turn.split())
    assert "run_in_background" in turn
    assert "steer_subagent" in turn and "get_subagent_result" in turn
    assert "pursuit_dispatch" in turn  # the fallback without tau-subagents


# -- ground-truth guard --------------------------------------------------------


@pytest.mark.anyio
@pytest.mark.parametrize(
    "command",
    [
        "echo x > .beagle/pursuit.toml",
        "echo x >> ./.beagle/pursuit.toml 2>&1",
        "printf x | tee -a .beagle/pursuit.toml >/dev/null",
        "sed -i 's/Ship/Skip/' .beagle/pursuit.toml",
        "sed -Ei.bak -e 's/a/b/' .beagle/pursuit.toml",
        "cp /tmp/new.toml .beagle/pursuit.toml",
        "cp /tmp/pursuit.toml .beagle/",
        "mv .beagle/pursuit.toml /tmp/old.toml",
        "cd .beagle && cat > pursuit.toml <<'EOF'\n[goal]\nEOF",
        "bash -c 'truncate -s 0 .beagle/pursuit.toml'",
        "git checkout -- .beagle/pursuit.toml",
    ],
)
async def test_guard_blocks_shell_writes_to_the_goal(
    tmp_path: Path, beagle: Path, command: str
) -> None:
    _pursuit_project(tmp_path)
    runtime, _ = _bound(tmp_path)

    result = await _tool_with_hooks(runtime).execute("c1", {"command": command})

    assert result.text.startswith("Tool call blocked: refusing a shell write to ")


@pytest.mark.anyio
@pytest.mark.parametrize(
    "command",
    [
        "cat .beagle/pursuit.toml",
        "git check-ignore -v .beagle/pursuit.toml > /tmp/ignored.txt",
        "grep -n criteria .beagle/pursuit.toml | tee /tmp/criteria.txt",
        "cp .beagle/pursuit.toml /tmp/backup.toml",
        "sed -n '1,5p' .beagle/pursuit.toml",
        "git add .beagle/pursuit.toml && git commit -m 'Found the pursuit' 2>&1",
        "cat > notes.md <<'EOF'\nnever run: echo x > .beagle/pursuit.toml\nEOF",
        "diff .beagle/pursuit.toml other.toml >/dev/null; echo $?",
    ],
)
async def test_guard_lets_reads_of_the_goal_through(
    tmp_path: Path, beagle: Path, command: str
) -> None:
    _pursuit_project(tmp_path)
    runtime, _ = _bound(tmp_path)

    result = await _tool_with_hooks(runtime).execute("c1", {"command": command})

    assert result.text == "ran"


@pytest.mark.anyio
async def test_guard_falls_back_to_blocking_an_unparseable_write(
    tmp_path: Path, beagle: Path
) -> None:
    _pursuit_project(tmp_path)
    runtime, _ = _bound(tmp_path)

    result = await _tool_with_hooks(runtime).execute(
        "c1", {"command": "echo 'unclosed > .beagle/pursuit.toml"}
    )

    assert result.text.startswith("Tool call blocked:")


@pytest.mark.anyio
async def test_repeat_wakeup_sends_a_stub_until_the_driver_leaves_context(
    tmp_path: Path, beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    runtime, session = _bound(tmp_path)
    timers = _capture_timers(monkeypatch)
    wakeup = _tool(runtime, "pursuit_wakeup")

    await wakeup.execute("c1", {})
    await _fire(timers[0])
    [full] = session.followed_up
    session.messages = (UserMessage(content=full),)  # the driver is now in context
    await wakeup.execute("c2", {})
    await _fire(timers[1])
    session.messages = (UserMessage(content="Summary of the earlier conversation."),)
    await wakeup.execute("c3", {})
    await _fire(timers[2])

    first, stub, after_compaction = session.followed_up
    assert parse_skill_invocation(first) is not None
    assert stub.startswith("/pursuit-run\n\n(A `pursuit_wakeup`.")
    assert "already in this conversation" in stub and "Host mapping" not in stub
    assert after_compaction == first


def test_explicit_pursuit_run_always_sends_the_full_driver(tmp_path: Path, beagle: Path) -> None:
    runtime, session = _bound(tmp_path)

    _run_command(runtime, "pursuit-run")
    session.messages = (UserMessage(content=session.followed_up[0]),)
    _run_command(runtime, "pursuit-run")

    first, second = session.followed_up
    assert first == second and parse_skill_invocation(second) is not None


def test_host_notes_name_the_merged_containment_launcher(tmp_path: Path, beagle: Path) -> None:
    runtime, session = _bound(tmp_path)
    _run_command(runtime, "pursuit-run")

    launcher = tmp_path / "home-tau" / "beagle-plugin" / "skills/containment/scripts"
    assert f"`{launcher}/run_contained.sh`" in " ".join(session.followed_up[0].split())
    worker = (tmp_path / "agents" / "beagle-dev:step-executor.md").read_text(encoding="utf-8")
    assert f"`{launcher}/run_contained.sh`" in " ".join(worker.split())
    assert "${CLAUDE_PLUGIN_ROOT}" not in session.followed_up[0] + worker


def test_host_note_names_worktree_isolation(tmp_path: Path, beagle: Path) -> None:
    runtime, session = _bound(tmp_path)
    _run_command(runtime, "pursuit-run")

    note = " ".join(session.followed_up[0].split())
    assert 'pass `isolation: "worktree"`' in note
    assert "`isolated: true` is not that" in note


@pytest.mark.anyio
@pytest.mark.parametrize(("driver", "noted"), [("session-1", True), ("other-session", False)])
async def test_stopping_a_worker_reminds_the_driver_to_clear_its_wait(
    tmp_path: Path, beagle: Path, fake_beagle: Path, driver: str, noted: bool
) -> None:
    project = _pursuit_project(tmp_path)
    _awaiting_worker(project, fake_beagle, driver=driver)
    runtime, _ = _bound(tmp_path)

    result = await _tool_with_hooks(runtime, "stop_subagent").execute("c1", {"agent_id": "a1"})

    assert result.text.startswith("ran")
    reminded = 'awaiting "step-executor on T0002"' in " ".join(result.text.split())
    assert reminded is noted
    assert ("bare `beagle loop tick`" in result.text) is noted


def test_host_note_gives_the_worker_spawn_rules(tmp_path: Path, beagle: Path) -> None:
    runtime, session = _bound(tmp_path)
    _run_command(runtime, "pursuit-run")

    note = " ".join(session.followed_up[0].split())
    assert "leave `provider` and `model` unset" in note
    assert "Set `max_turns` from the task's budget" in note
    assert "do not poll `get_subagent_result`" in note
    assert "quoted heredoc (`<<'EOF'`), a file, or single quotes, never double quotes" in note


# -- a run whose Tau driver has ended -------------------------------------------


def _left_run(project: Path, fake: Path, driver: str) -> None:
    """A run driven by `driver`, still waiting on its worker."""
    at = datetime.now(UTC).isoformat()
    record = {
        "started_at": at,
        "started_by": "/pursuit-run",
        "driver_session": driver,
        "awaiting": "step-executor on T0003",
        "awaiting_at": at,
        "awaiting_minutes": 120,
    }
    (project / ".beagle" / "loop.json").write_text(json.dumps(record), encoding="utf-8")
    (fake / "read.out").write_text(json.dumps(record), encoding="utf-8")


def _driver_entry(tmp_path: Path, session: str, **record: Any) -> Path:
    path = tmp_path / "home-tau" / "state" / "beagle-drivers" / f"{session}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record), encoding="utf-8")
    return path


def _exited_pid() -> int:
    proc = subprocess.run(
        [sys.executable, "-c", "import os; print(os.getpid())"],
        check=True,
        capture_output=True,
        text=True,
    )
    return int(proc.stdout)


def _stops(fake: Path) -> list[list[str]]:
    return [c["argv"] for c in _calls(fake) if c["argv"][:2] == ["loop", "stop"]]


@pytest.mark.anyio
async def test_load_retires_a_run_whose_tau_driver_exited(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    project = _pursuit_project(tmp_path)
    _left_run(project, fake_beagle, "old-session")
    _driver_entry(tmp_path, "old-session", pid=_exited_pid(), start=None, ended=False)
    monkeypatch.chdir(project)
    runtime = _load(tmp_path)
    ui = RecordingUiBridge(has_ui=True)
    runtime.set_ui_bridge(ui)  # type: ignore[arg-type]
    session = RecordingSession(project, running=True)
    runtime.bind(session)  # type: ignore[arg-type]

    await runtime.emit_session_start("startup")
    _run_command(runtime, "pursuit-run")
    _run_command(runtime, "pursuit-run")

    [stop] = _stops(fake_beagle)
    reason = stop[stop.index("--reason") + 1]
    assert "old-session" in reason and "exited" in reason
    assert "awaiting: step-executor on T0003" in reason
    # Retired before loop-report, which would otherwise say to stand down.
    order = [c["argv"][1] for c in _calls(fake_beagle)]
    assert order.index("stop") < order.index("loop-report")
    assert [level for _, level in ui.notifications] == ["warning"]
    first, second = session.followed_up
    assert first.index("was stopped with `beagle loop stop`") < first.index("Host mapping")
    assert 'awaiting "step-executor on T0003"' in first
    assert "~/.tau/subagents/*/old-session/tasks/" in first
    assert "beagle loop stop" not in second  # said once


@pytest.mark.anyio
@pytest.mark.parametrize("entry", ["live", "unknown"])
async def test_a_live_or_unknown_driver_keeps_its_run(
    tmp_path: Path,
    beagle: Path,
    fake_beagle: Path,
    monkeypatch: pytest.MonkeyPatch,
    entry: str,
) -> None:
    project = _pursuit_project(tmp_path)
    _left_run(project, fake_beagle, "other-session")
    if entry == "live":  # another Tau process, still running
        _driver_entry(tmp_path, "other-session", pid=os.getppid(), start=None, ended=False)
    monkeypatch.chdir(project)
    runtime = _load(tmp_path)
    runtime.bind(RecordingSession(project, running=False))  # type: ignore[arg-type]

    await runtime.emit_session_start("startup")

    assert _stops(fake_beagle) == []


@pytest.mark.anyio
async def test_a_session_that_ends_retires_its_run_at_the_next_start(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    project = _pursuit_project(tmp_path)
    monkeypatch.chdir(project)
    runtime = _load(tmp_path)
    runtime.set_ui_bridge(RecordingUiBridge(has_ui=True))  # type: ignore[arg-type]
    session = RecordingSession(project, running=False)
    runtime.bind(session)  # type: ignore[arg-type]
    await runtime.emit_session_start("startup")
    entry = tmp_path / "home-tau" / "state" / "beagle-drivers" / f"{session.session_id}.json"
    assert json.loads(entry.read_text())["pid"] == os.getpid()
    _left_run(project, fake_beagle, session.session_id)

    # This process is alive, so only the shutdown mark says its workers are gone.
    await runtime.emit_session_start("resume")
    assert _stops(fake_beagle) == []
    await runtime.emit_session_shutdown("resume")
    assert json.loads(entry.read_text())["ended"] is True
    await runtime.emit_session_start("resume")

    [stop] = _stops(fake_beagle)
    assert "closed, replaced or reloaded" in stop[stop.index("--reason") + 1]
    assert json.loads(entry.read_text())["ended"] is False  # re-recorded as live


FAKE_TAU = """\
import json, os, sys
from pathlib import Path

here = Path(os.environ["FAKE_TAU_DIR"])
brief = sys.stdin.read()
runs = here / "runs.jsonl"
with runs.open("a") as log:
    scope = os.environ.get("BEAGLE_TAU_WORKER_SCOPE")
    log.write(json.dumps({"argv": sys.argv[1:], "stdin": brief, "scope": scope}) + "\\n")
attempt = len(runs.read_text().splitlines())
if attempt >= int(os.environ.get("FAKE_TAU_SUCCEEDS_ON", "1")):
    Path("done.txt").write_text("done")
for rel, text in json.loads(os.environ.get("FAKE_TAU_WRITES") or "{}").items():
    Path(rel).parent.mkdir(parents=True, exist_ok=True)
    Path(rel).write_text(text)
tamper = os.environ.get("FAKE_TAU_TAMPERS")
if tamper:
    Path(tamper).write_text("tampered")
message = {
    "role": "assistant",
    "content": [
        {
            "type": "text",
            "text": os.environ.get("FAKE_TAU_REPORT") or f"attempt {attempt}: wrote done.txt",
        }
    ],
    "usage": {"totalTokens": 1000},
    "stopReason": "stop",
}
if os.environ.get("FAKE_TAU_RAMBLES"):
    # A worker that spends its whole output on reasoning: the update events
    # repeat the growing message, one of them past the reader's line limit.
    for size in (1 << 20, 1 << 20, 17 << 20):
        partial = {"role": "assistant", "content": [{"type": "thinking", "thinking": "x" * size}]}
        print(json.dumps({"type": "message_update", "message": partial}))
    message = {
        "role": "assistant",
        "content": [{"type": "thinking", "thinking": "x" * 50_000 + " so the parser"}],
        "usage": {"totalTokens": 1000},
        "stopReason": "length",
    }
    print("worker stderr line", file=sys.stderr)
print(json.dumps({"type": "message_end", "message": {"role": "user", "content": brief}}))
print(json.dumps({"type": "message_end", "message": message}))
"""


@pytest.fixture
def fake_tau(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """A `tau` worker that writes `done.txt` from attempt `FAKE_TAU_SUCCEEDS_ON` on."""
    here = tmp_path / "fake-tau"
    here.mkdir()
    script = here / "tau"
    script.write_text(f"#!{sys.executable}\n{FAKE_TAU}", encoding="utf-8")
    script.chmod(0o755)
    monkeypatch.setenv("TAU_BIN", str(script))
    monkeypatch.setenv("FAKE_TAU_DIR", str(here))
    return here


def _runs(fake: Path) -> list[dict[str, Any]]:
    log = fake / "runs.jsonl"
    return [json.loads(line) for line in log.read_text().splitlines()] if log.exists() else []


def _pursuit_calls(fake: Path, verb: str) -> list[list[str]]:
    return [c["argv"][2:] for c in _calls(fake) if c["argv"][:2] == ["pursuit", verb]]


@pytest.mark.anyio
async def test_pursuit_found_waits_for_the_user_then_roots_and_splits(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    project = tmp_path / "project"
    project.mkdir()
    monkeypatch.chdir(project)
    (fake_beagle / "add.out").write_text('T0001  Ship the "tool"\n')
    runtime, _ = _bound(tmp_path)
    found = _tool(runtime, "pursuit_found")
    args = {
        "statement": 'Ship the "tool"',
        "criteria": ["`make test` exits 0", "README documents usage"],
        "milestones": ["Parser::reads input", "CLI::wires it up"],
    }

    unconfirmed = await found.execute("c1", {**args, "user_confirmed": False})
    assert "nothing written" in unconfirmed.text and "README documents usage" in unconfirmed.text
    assert "ask the user to confirm" in unconfirmed.text and "print mode" not in unconfirmed.text
    assert not (project / ".beagle").exists() and _calls(fake_beagle) == []

    result = await found.execute("c2", {**args, "user_confirmed": True})

    goal = tomllib.loads((project / ".beagle" / "pursuit.toml").read_text())["goal"]
    assert goal["statement"] == 'Ship the "tool"'
    assert goal["criteria"] == args["criteria"]
    assert _pursuit_calls(fake_beagle, "add") == [
        ['Ship the "tool"', "--root-task", "--intent", 'Ship the "tool"']
    ]
    assert _pursuit_calls(fake_beagle, "split") == [
        ["T0001", "Parser::reads input", "CLI::wires it up", "--ordered"]
    ]
    assert "root task T0001" in result.text and "pursuit_step" in result.text
    again = await found.execute("c3", {**args, "user_confirmed": True})
    assert "already exists" in again.text


@pytest.mark.anyio
async def test_founding_mid_session_swaps_in_the_pursuit_prompt(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Run 10 founded in the session it ran in, and kept the "nothing founded
    # yet" orientation all along: after each compaction nothing said how to
    # work the pursuit.
    project = tmp_path / "project"
    project.mkdir()
    monkeypatch.chdir(project)
    (fake_beagle / "add.out").write_text("T0001  Ship it\n")
    runtime, session = _bound(tmp_path)
    assert [s.title for s in runtime.prompt_sections if s.title == "Beagle"] == ["Beagle"]

    await _tool(runtime, "pursuit_found").execute(
        "c1",
        {
            "statement": "Ship it",
            "criteria": ["`make test` exits 0"],
            "milestones": ["Parser::reads input", "CLI::wires it up"],
            "user_confirmed": True,
        },
    )

    sections = {s.title: s.body for s in runtime.prompt_sections}
    assert "Beagle" not in sections
    assert "**pursuit**: Ship it" in sections["Beagle pursuit"]
    assert "How to work it" in sections["Beagle pursuit"]
    assert session.prompt_refreshes == 2


@pytest.mark.anyio
async def test_a_compaction_is_followed_by_the_pursuit_state_from_beagle(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Run 10's summaries said nothing was ready while T0014 was, and listed
    # the driver's own commands as done tasks.
    monkeypatch.chdir(_pursuit_project(tmp_path))
    _ready_task(fake_beagle)
    (fake_beagle / "tree.out").write_text("T0001 Ship it\n  T0002 Parser  pending\n")
    runtime, session = _bound(tmp_path)
    session.is_running = True

    await runtime.emit_event(CompactionEndEvent(reason="threshold", aborted=True))
    assert session.steered == []
    await runtime.emit_event(CompactionEndEvent(reason="threshold"))

    [note] = session.steered
    assert "T0002 Parser  pending" in note and "Ready now: T0002." in note
    assert "trust this over the summary" in note and "call pursuit_step" in note
    focus = runtime.compaction_instructions
    assert any("only from beagle's own output" in text for text in focus)


@pytest.mark.anyio
async def test_state_after_compaction_repeats_last_step_result(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # R10: after compaction the summary paraphrased T0002's refusal, and the
    # driver sent `beagle pursuit next`'s open from bash 11 times.
    monkeypatch.chdir(_pursuit_project(tmp_path))
    _ready_task(fake_beagle)
    runtime, session = _bound(tmp_path)
    session.is_running = True
    refused = await _tool(runtime, "pursuit_step").execute(
        "c1",
        {
            "task": "T0002",
            "criteria": "beagle is configured",
            "done_when": "python3 -m pytest -q",
            "scope": [".beagle/"],
        },
    )
    assert "not opened" in refused.text

    await runtime.emit_event(CompactionEndEvent(reason="threshold"))

    [note] = session.steered
    assert f"Last pursuit_step on T0002 said:\n{refused.text}" in note
    assert "Ready now: T0002." in note


@pytest.mark.anyio
async def test_state_after_compaction_without_a_step_result_is_unchanged(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(_pursuit_project(tmp_path))
    _ready_task(fake_beagle)
    runtime, session = _bound(tmp_path)
    session.is_running = True

    await runtime.emit_event(CompactionEndEvent(reason="threshold"))

    [note] = session.steered
    assert "Last pursuit_step" not in note
    assert note.endswith("pursuit_plan; this session does not do it itself.")


@pytest.mark.anyio
async def test_bash_pursuit_next_is_steered_to_pursuit_step(
    tmp_path: Path, beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # R10 E142-164: `beagle pursuit next` ran from bash and its open was sent 11 times.
    monkeypatch.chdir(_pursuit_project(tmp_path))
    runtime, _ = _bound(tmp_path)
    bash = _tool_with_hooks(runtime, "bash")
    await runtime.emit_session_start("startup")

    result = await bash.execute("c1", {"command": "beagle pursuit next"})

    assert "refusing `beagle pursuit next`" in result.text
    assert "pursuit_step with no arguments, which picks the ready task" in result.text


@pytest.mark.anyio
async def test_a_request_to_set_beagle_up_is_steered_to_found_first(
    tmp_path: Path, beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # The prompt section alone did not hold a 9B driver: it read the reference
    # and spent whole turns designing in its head before founding anything.
    runtime, session = _bound(tmp_path)
    monkeypatch.chdir(tmp_path / "project")
    session.is_running = True

    await runtime.emit_session_start("startup")
    bash = _tool_with_hooks(runtime, "bash")
    await runtime.run_input_hooks("set this project up for beagle pursuit, then build it")
    await runtime.emit_event(AgentStartEvent())
    await runtime.emit_event(AgentStartEvent())

    assert len(session.steered) == 1 and "pursuit_found" in session.steered[0]
    # No URL in the request: the note is the plain one, no references part.
    assert session.steered[0] == _loaded_module().FOUND_FIRST_NOTE
    # Then the steer has teeth: a few calls for setup, and no more.
    setup = [await bash.execute(f"c{i}", {"command": "beagle doctor"}) for i in range(6)]
    assert [r.text for r in setup] == ["ran"] * 6
    refused = await bash.execute("c7", {"command": "curl -o /tmp/ref.html https://x"})
    assert "Call pursuit_found now" in refused.text
    found = await _tool(runtime, "pursuit_found").execute("c8", {})
    assert "refusing" not in found.text and "required" in found.text


@pytest.mark.anyio
async def test_an_unrelated_prompt_is_not_steered_to_found(
    tmp_path: Path, beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    runtime, session = _bound(tmp_path)
    monkeypatch.chdir(tmp_path / "project")
    session.is_running = True

    await runtime.run_input_hooks("fix the typo in README")
    await runtime.emit_event(AgentStartEvent())

    assert session.steered == []


@pytest.mark.anyio
async def test_pursuit_found_takes_a_delegated_goal_and_makes_a_repo(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # "Use your judgement, without further discussion": asking would stall an
    # unattended run, and a bare directory has no git for the guards to use.
    project = tmp_path / "project"
    project.mkdir()
    monkeypatch.chdir(project)
    # No git identity anywhere: the model must say so, not make one up.
    gitconfig = tmp_path / "gitconfig"
    gitconfig.write_text("[user]\n\tuseConfigOnly = true\n")  # no guessing from the host
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", str(gitconfig))
    monkeypatch.setenv("GIT_CONFIG_NOSYSTEM", "1")
    for key in (
        "GIT_AUTHOR_NAME",
        "GIT_AUTHOR_EMAIL",
        "GIT_COMMITTER_NAME",
        "GIT_COMMITTER_EMAIL",
        "EMAIL",
    ):
        monkeypatch.delenv(key, raising=False)
    (fake_beagle / "add.out").write_text("T0001  Build ITC\n")
    runtime, _ = _bound(tmp_path)

    result = await _tool(runtime, "pursuit_found").execute(
        "c1",
        {
            "statement": "Build ITC",
            "criteria": ["`uv run pytest` exits 0"],
            "milestones": ["Read::the reference", "Core::fork, join, event"],
            "user_confirmed": False,
            "user_delegated": True,
        },
    )

    goal = (project / ".beagle" / "pursuit.toml").read_text()
    # pursuit_step closes in the same call it opens: beagle must hold that
    # close to a witnessed check (run 11d closed on import-only checks).
    assert tomllib.loads(goal)["close"] == {"require": "witness"}
    assert "__pycache__/" in (project / ".gitignore").read_text().splitlines()
    assert (project / ".git").is_dir()
    assert "git init" in result.text and "criteria you chose" in result.text
    assert "Do not fetch or read the reference" in result.text
    assert "Cases first" in result.text
    assert "git has no user.name or user.email" in result.text


def _setup_project(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """A git repo with an identity, holding what `beagle init` leaves untracked."""
    project = tmp_path / "project"
    project.mkdir()
    monkeypatch.chdir(project)
    gitconfig = tmp_path / "gitconfig"
    gitconfig.write_text("[user]\n\tname = Tester\n\temail = tester@example.com\n")
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", str(gitconfig))
    monkeypatch.setenv("GIT_CONFIG_NOSYSTEM", "1")
    subprocess.run(["git", "init", "-q"], cwd=project, check=True)
    beagle_dir = project / ".beagle"
    beagle_dir.mkdir()
    for name in ("cadences", "dispatch", "gates", "skills", "track"):
        (beagle_dir / f"{name}.toml").write_text(f"# {name}\n")
    (beagle_dir / "memory-rubric.md").write_text("# rubric\n")
    (project / ".gitignore").write_text(".beagle/scratch/\n")
    (beagle_dir / "scratch").mkdir()
    (beagle_dir / "scratch" / "junk.log").write_text("ignored\n")
    return project


def _git(project: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=project, check=True, capture_output=True, text=True
    ).stdout


async def _found(tmp_path: Path, fake_beagle: Path) -> Any:
    (fake_beagle / "add.out").write_text("T0001  Build ITC\n")
    runtime, _ = _bound(tmp_path)
    return await _tool(runtime, "pursuit_found").execute(
        "c1",
        {
            "statement": "Build ITC",
            "criteria": ["`uv run pytest` exits 0"],
            "milestones": ["Read::the reference", "Core::fork, join, event"],
            "user_confirmed": True,
        },
    )


@pytest.mark.anyio
async def test_founding_commits_beagle_setup_files(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # R08: beagle init's files stayed untracked, so workspace-clean was red
    # from the first task.
    project = _setup_project(tmp_path, monkeypatch)

    result = await _found(tmp_path, fake_beagle)

    assert "uncommitted" not in result.text
    assert _git(project, "status", "--porcelain", "--untracked-files=all") == ""
    committed = _git(project, "show", "--name-only", "--format=", "HEAD").split()
    assert ".gitignore" in committed and ".beagle/pursuit.toml" in committed
    assert ".beagle/memory-rubric.md" in committed
    assert ".beagle/scratch/junk.log" not in committed


@pytest.mark.anyio
async def test_founding_setup_commit_leaves_the_users_files_alone(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    project = _setup_project(tmp_path, monkeypatch)
    (project / "staged.py").write_text("x = 1\n")
    _git(project, "add", "staged.py")
    (project / "notes.txt").write_text("mine\n")

    await _found(tmp_path, fake_beagle)

    committed = _git(project, "show", "--name-only", "--format=", "HEAD").split()
    assert committed and all(p == ".gitignore" or p.startswith(".beagle/") for p in committed)
    status = _git(project, "status", "--porcelain", "--untracked-files=all").splitlines()
    assert sorted(status) == ["?? notes.txt", "A  staged.py"]


@pytest.mark.anyio
async def test_founding_without_identity_says_setup_is_uncommitted(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    project = _setup_project(tmp_path, monkeypatch)
    (tmp_path / "gitconfig").write_text("[user]\n\tuseConfigOnly = true\n")
    for key in (
        "GIT_AUTHOR_NAME",
        "GIT_AUTHOR_EMAIL",
        "GIT_COMMITTER_NAME",
        "GIT_COMMITTER_EMAIL",
        "EMAIL",
    ):
        monkeypatch.delenv(key, raising=False)

    result = await _found(tmp_path, fake_beagle)

    assert "Founded the pursuit" in result.text
    assert "setup (.beagle/, .gitignore) is uncommitted" in result.text
    assert "?? .beagle/pursuit.toml" in _git(project, "status", "--porcelain", "-uall")


@pytest.mark.anyio
async def test_failed_setup_commit_leaves_nothing_staged(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    project = _setup_project(tmp_path, monkeypatch)
    hook = project / ".git" / "hooks" / "pre-commit"
    hook.write_text("#!/bin/sh\nexit 1\n")
    hook.chmod(0o755)

    result = await _found(tmp_path, fake_beagle)

    assert "Founded the pursuit" in result.text
    assert "setup (.beagle/, .gitignore) is uncommitted" in result.text
    assert _git(project, "diff", "--cached", "--name-only") == ""
    assert (project / ".beagle" / "pursuit.toml").is_file()
    assert (project / ".beagle" / "gates.toml").is_file()


@pytest.mark.anyio
async def test_failed_setup_commit_keeps_the_users_own_staging(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    project = _setup_project(tmp_path, monkeypatch)
    _git(project, "add", ".gitignore")
    hook = project / ".git" / "hooks" / "pre-commit"
    hook.write_text("#!/bin/sh\nexit 1\n")
    hook.chmod(0o755)

    result = await _found(tmp_path, fake_beagle)

    assert "setup (.beagle/, .gitignore) is uncommitted" in result.text
    assert _git(project, "diff", "--cached", "--name-only").split() == [".gitignore"]


@pytest.mark.anyio
async def test_pursuit_plan_adds_to_a_container_it_cannot_split(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(_pursuit_project(tmp_path))
    (fake_beagle / "split.out").write_text("beagle: T0001 already has children")
    (fake_beagle / "split.rc").write_text("4")
    runtime, _ = _bound(tmp_path)

    result = await _tool(runtime, "pursuit_plan").execute(
        "c1", {"task": "T0001", "parts": ["Docs::so people can use it", "Release"]}
    )

    assert _pursuit_calls(fake_beagle, "add") == [
        ["Docs", "--parent", "T0001", "--intent", "so people can use it"],
        ["Release", "--parent", "T0001"],
    ]
    assert "pursuit_step" in result.text


@pytest.mark.anyio
async def test_pursuit_found_adds_a_lone_milestone_beagle_would_not_split(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    project = tmp_path / "project"
    project.mkdir()
    monkeypatch.chdir(project)
    (fake_beagle / "add.out").write_text("T0001  Greet\n")
    runtime, _ = _bound(tmp_path)

    result = await _tool(runtime, "pursuit_found").execute(
        "c1",
        {
            "statement": "Greet",
            "criteria": ["hello.txt says hi"],
            "milestones": ["Write::make hello.txt"],
            "user_confirmed": True,
        },
    )

    assert _pursuit_calls(fake_beagle, "split") == []
    assert _pursuit_calls(fake_beagle, "add")[1] == [
        "Write",
        "--parent",
        "T0001",
        "--intent",
        "make hello.txt",
    ]
    assert "Founded the pursuit" in result.text


@pytest.mark.anyio
async def test_found_shortens_long_milestone_title(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Run R01 founded with a 251-character milestone title, which beagle refuses.
    project = tmp_path / "project"
    project.mkdir()
    monkeypatch.chdir(project)
    (fake_beagle / "add.out").write_text("T0001  Implement interval tree clocks\n")
    runtime, _ = _bound(tmp_path)
    limit = _module().MAX_TASK_TITLE
    long_title = " ".join(["Implement fork join and event for interval tree clocks"] * 5)
    assert 240 <= len(long_title) <= 280

    result = await _tool(runtime, "pursuit_found").execute(
        "c1",
        {
            "statement": "Implement interval tree clocks",
            "criteria": ["`python3 -m pytest -q` exits 0"],
            "milestones": ["Parser::reads input", f"{long_title}::the detail"],
            "user_confirmed": True,
        },
    )

    assert "Founded the pursuit" in result.text
    assert "Milestone 2" in result.text and f"{len(long_title)}-character" in result.text
    split = _pursuit_calls(fake_beagle, "split")
    assert len(split) == 1 and split[0][1] == "Parser::reads input"
    title, sep, intent = split[0][2].partition("::")
    assert sep and len(title) <= limit
    assert long_title.startswith(title.removesuffix("…"))
    assert long_title[len(title.removesuffix("…"))] == " "
    assert long_title in intent and "the detail" in intent


@pytest.mark.anyio
async def test_found_accepts_max_length_milestone(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    project = tmp_path / "project"
    project.mkdir()
    monkeypatch.chdir(project)
    (fake_beagle / "add.out").write_text("T0001  Greet\n")
    runtime, _ = _bound(tmp_path)
    title = "x" * _module().MAX_TASK_TITLE
    # The intent after '::' does not count toward the title's length.
    milestones = [f"{title}::{' '.join(['detail'] * 40)}", "CLI::wires it up"]

    result = await _tool(runtime, "pursuit_found").execute(
        "c1",
        {
            "statement": "Greet",
            "criteria": ["hello.txt says hi"],
            "milestones": milestones,
            "user_confirmed": True,
        },
    )

    assert "Founded the pursuit" in result.text
    assert (project / ".beagle" / "pursuit.toml").exists()
    assert _pursuit_calls(fake_beagle, "split") == [["T0001", *milestones, "--ordered"]]


def _tiny_pdf(text: str) -> bytes:
    """A one-page PDF that shows `text`, built by hand so tests need no PDF library."""
    stream = f"BT /F1 12 Tf 72 720 Td ({text}) Tj ET".encode()
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        b"/Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>",
        b"<< /Length %d >>\nstream\n" % len(stream) + stream + b"\nendstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]
    out = b"%PDF-1.4\n"
    offsets = []
    for number, body in enumerate(objects, 1):
        offsets.append(len(out))
        out += b"%d 0 obj\n" % number + body + b"\nendobj\n"
    xref = len(out)
    out += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objects) + 1)
    out += b"".join(b"%010d 00000 n \n" % offset for offset in offsets)
    out += b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (
        len(objects) + 1,
        xref,
    )
    return out


class _FakeResponse:
    def __init__(self, body: bytes, content_type: str) -> None:
        import email.message

        self._body = body
        self.headers = email.message.Message()
        self.headers["Content-Type"] = content_type

    def read(self, limit: int = -1) -> bytes:
        return self._body if limit < 0 else self._body[:limit]

    def __enter__(self) -> _FakeResponse:
        return self

    def __exit__(self, *exc: object) -> None:
        return None


def _fake_web(monkeypatch: pytest.MonkeyPatch, pages: dict[str, tuple[bytes, str]]) -> list[str]:
    """Serve `pages` (url -> body, content type) to urllib; any other URL fails."""
    import urllib.error
    import urllib.request

    asked: list[str] = []

    def urlopen(request: Any, timeout: float | None = None) -> _FakeResponse:
        url = request.full_url if hasattr(request, "full_url") else str(request)
        asked.append(url)
        if url not in pages:
            raise urllib.error.URLError("Name or service not known")
        return _FakeResponse(*pages[url])

    monkeypatch.setattr(urllib.request, "urlopen", urlopen)
    return asked


ITC_PROMPT = (
    "Implement interval tree clocks in Python, as a beagle pursuit. The paper: "
    "https://example.org/papers/itc2008.pdf and a walkthrough "
    "(https://example.org/blog/interval-tree-clocks.html)."
)


@pytest.mark.anyio
async def test_found_fetches_references(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # R02's workers never saw the paper: the driver wrote the domain from its name.
    project = tmp_path / "project"
    project.mkdir()
    monkeypatch.chdir(project)
    (fake_beagle / "add.out").write_text("T0001  Interval tree clocks\n")
    page = (
        b"<html><head><title>t</title><style>p{color:red}</style></head><body>"
        b"<script>var stamp = 1;</script><h1>Interval Tree Clocks</h1>"
        b"<p>A stamp is an id and an event tree.</p></body></html>"
    )
    asked = _fake_web(
        monkeypatch,
        {
            "https://example.org/papers/itc2008.pdf": (
                _tiny_pdf("fork event join"),
                "application/pdf",
            ),
            "https://example.org/blog/interval-tree-clocks.html": (page, "text/html"),
        },
    )
    runtime, _ = _bound(tmp_path)
    await runtime.run_input_hooks(ITC_PROMPT)

    result = await _tool(runtime, "pursuit_found").execute(
        "c1",
        {
            "statement": "Interval tree clocks in Python",
            "criteria": ["`python3 -m pytest -q` exits 0"],
            "milestones": ["Cases::from the paper", "Clock::passes them"],
            "user_confirmed": True,
        },
    )

    assert "Founded the pursuit" in result.text
    assert asked == [
        "https://example.org/papers/itc2008.pdf",
        "https://example.org/blog/interval-tree-clocks.html",
    ]
    refs = project / "references"
    walkthrough = (refs / "interval-tree-clocks.txt").read_text()
    assert "Interval Tree Clocks" in walkthrough and "an id and an event tree" in walkthrough
    assert "var stamp" not in walkthrough and "color:red" not in walkthrough
    index = json.loads((refs / "index.json").read_text())
    assert index["request"] == ITC_PROMPT
    if shutil.which("pdftotext"):
        assert "fork event join" in (refs / "itc2008.txt").read_text()
        assert set(index["fetched"]) == {"itc2008.txt", "interval-tree-clocks.txt"}
    else:
        assert (
            "pdftotext is not installed"
            in index["failed"]["https://example.org/papers/itc2008.pdf"]
        )
    assert "references/" in (project / ".gitignore").read_text().splitlines()
    assert "references/interval-tree-clocks.txt" in result.text


@pytest.mark.anyio
async def test_found_reference_fetch_failure_is_noted(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    project = tmp_path / "project"
    project.mkdir()
    monkeypatch.chdir(project)
    (fake_beagle / "add.out").write_text("T0001  Interval tree clocks\n")
    page = (b"Interval tree clocks, in plain text.", "text/plain")
    _fake_web(monkeypatch, {"https://example.org/blog/interval-tree-clocks.html": page})
    runtime, _ = _bound(tmp_path)
    await runtime.run_input_hooks(ITC_PROMPT)

    result = await _tool(runtime, "pursuit_found").execute(
        "c1",
        {
            "statement": "Interval tree clocks in Python",
            "criteria": ["`python3 -m pytest -q` exits 0"],
            "milestones": ["Cases::from the paper", "Clock::passes them"],
            "user_confirmed": True,
        },
    )

    assert "Founded the pursuit" in result.text
    assert _pursuit_calls(fake_beagle, "split")  # founding went on past the failure
    missed = "could not fetch https://example.org/papers/itc2008.pdf: "
    assert missed in result.text and "Name or service not known" in result.text
    assert not (project / "references" / "itc2008.txt").exists()
    assert (
        (project / "references" / "interval-tree-clocks.txt")
        .read_text()
        .startswith("Interval tree clocks, in plain text.")
    )
    brief = _module()._references_brief(project)
    assert missed in brief and "references/interval-tree-clocks.txt" in brief


def _loaded_module() -> Any:
    """The extension module the last-bound runtime loaded (not a fresh `_module()`)."""
    loaded = [
        m
        for m in list(sys.modules.values())
        if getattr(m, "__file__", None) == str(EXTENSION) and hasattr(m, "_fetch_reference")
    ]
    assert loaded
    return loaded[-1]


ITC_ABSTRACT = (
    "Interval Tree Clocks: A Logical Clock for Dynamic Systems\n\n"
    "Paulo Sergio Almeida, Carlos Baquero, Victor Fonte\n\n"
    "Abstract\n"
    "Causality tracking mechanisms, such as vector clocks and version vectors, rely on "
    "mappings from globally unique identifiers to integer counters. "
    + "An interval tree clock forks, joins and records events on a stamp. "
    * 40
)


def _stub_fetch(monkeypatch: pytest.MonkeyPatch, pages: dict[str, str]) -> list[str]:
    asked: list[str] = []

    def fetch(url: str) -> str:
        asked.append(url)
        if url not in pages:
            raise OSError("Name or service not known")
        return pages[url]

    monkeypatch.setattr(_loaded_module(), "_fetch_reference", fetch)
    return asked


def test_reference_fetch_retries_a_timeout_with_a_longer_timeout(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # R09: itc2008.pdf timed out at 30 s and every worker re-downloaded it.
    import urllib.error

    module = _module()
    paper = "https://example.org/papers/itc2008.pdf"
    timeouts: list[float] = []

    def fetch(url: str, timeout: float = module.REFERENCE_FETCH_TIMEOUT) -> str:
        timeouts.append(timeout)
        if len(timeouts) == 1:
            raise urllib.error.URLError(TimeoutError("timed out"))
        return "Interval tree clocks, the paper."

    monkeypatch.setattr(module, "_fetch_reference", fetch)
    index = module._fetch_references(tmp_path, f"The paper: {paper}")

    assert timeouts == [30.0, 90.0]
    assert module.REFERENCE_FETCH_RETRY_TIMEOUT == 90.0
    assert index["fetched"] == {"itc2008.txt": paper} and index["failed"] == {}
    written = (tmp_path / "references" / "itc2008.txt").read_text()
    assert written == "Interval tree clocks, the paper."

    timeouts.clear()

    def always_slow(url: str, timeout: float = module.REFERENCE_FETCH_TIMEOUT) -> str:
        timeouts.append(timeout)
        raise TimeoutError(f"timed out after {timeout:g} s")

    monkeypatch.setattr(module, "_fetch_reference", always_slow)
    index = module._fetch_references(tmp_path, f"The paper: {paper}")

    assert timeouts == [30.0, 90.0]
    reason = index["failed"][paper]
    assert "timed out after 30 s" in reason and "timed out after 90 s" in reason


def test_reference_fetch_does_not_retry_a_refused_url(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import email.message
    import urllib.error

    module = _module()
    paper = "https://example.org/papers/itc2008.pdf"
    refusals: list[Exception] = [
        urllib.error.HTTPError(paper, 404, "Not Found", email.message.Message(), None),
        urllib.error.URLError(ConnectionRefusedError(111, "Connection refused")),
        ConnectionRefusedError(111, "Connection refused"),
        ValueError("larger than 5 MB"),
        ValueError("it held no text"),
    ]
    for refusal in refusals:
        calls: list[float] = []

        def fetch(
            url: str,
            timeout: float = module.REFERENCE_FETCH_TIMEOUT,
            refusal: Exception = refusal,
            calls: list[float] = calls,
        ) -> str:
            calls.append(timeout)
            raise refusal

        monkeypatch.setattr(module, "_fetch_reference", fetch)
        index = module._fetch_references(tmp_path, f"The paper: {paper}")

        assert calls == [30.0], refusal
        assert index["failed"][paper] == str(refusal)
        assert not (tmp_path / "references" / "itc2008.txt").exists()


@pytest.mark.anyio
async def test_found_first_steer_carries_reference_extracts(
    tmp_path: Path, beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # R02 and R03: criteria about interval trees for a request about interval
    # tree clocks, because nothing of the reference reached the driver first.
    runtime, session = _bound(tmp_path)
    monkeypatch.chdir(tmp_path / "project")
    session.is_running = True
    walkthrough = "https://example.org/blog/interval-tree-clocks.html"
    _stub_fetch(monkeypatch, {walkthrough: ITC_ABSTRACT})

    await runtime.emit_session_start("startup")
    await runtime.run_input_hooks(ITC_PROMPT)
    await runtime.emit_event(AgentStartEvent())

    [note] = session.steered
    module = _loaded_module()
    assert note.startswith(module.FOUND_FIRST_NOTE)
    extract = module._reference_extract(ITC_ABSTRACT)
    assert extract.startswith("Interval Tree Clocks: A Logical Clock for Dynamic Systems")
    assert f"From {walkthrough}" in note and extract in note
    assert "Causality tracking mechanisms" in note
    failed = "Could not fetch https://example.org/papers/itc2008.pdf: Name or service not known"
    assert failed in note
    assert "in the reference's own terms, not from the name alone" in note


@pytest.mark.anyio
async def test_found_reuses_references_fetched_before_founding(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    project = tmp_path / "project"
    runtime, session = _bound(tmp_path)
    monkeypatch.chdir(project)
    session.is_running = True
    (fake_beagle / "add.out").write_text("T0001  Interval tree clocks\n")
    pages = {
        "https://example.org/papers/itc2008.pdf": ITC_ABSTRACT,
        "https://example.org/blog/interval-tree-clocks.html": "Interval Tree Clocks\nA walk.",
    }
    asked = _stub_fetch(monkeypatch, pages)

    await runtime.emit_session_start("startup")
    await runtime.run_input_hooks(ITC_PROMPT)
    await runtime.emit_event(AgentStartEvent())
    result = await _tool(runtime, "pursuit_found").execute(
        "c1",
        {
            "statement": "Interval tree clocks in Python",
            "criteria": ["`python3 -m pytest -q` exits 0"],
            "milestones": ["Cases::from the paper", "Clock::passes them"],
            "user_confirmed": True,
        },
    )

    assert "Founded the pursuit" in result.text
    assert sorted(asked) == sorted(pages)
    assert "references/interval-tree-clocks.txt" in result.text
    assert "references/" in (project / ".gitignore").read_text().splitlines()
    index = json.loads((project / "references" / "index.json").read_text())
    assert index["request"] == ITC_PROMPT


def test_reference_extract_is_title_and_opening() -> None:
    module = _module()
    words = " ".join(f"word{i}" for i in range(1000))
    extract = module._reference_extract(f"\n\n  The Title Line  \nAuthors here\n{words}\n")
    assert extract.startswith("The Title Line\n\n")
    assert len(extract) <= 1600
    assert extract.endswith("\u2026")
    last = extract[:-1].split()[-1]
    assert re.fullmatch(r"word\d+", last) and f" {last} " in f" {words} "
    assert "Authors here" in extract  # no abstract heading: the opening is what follows

    paper = module._reference_extract(ITC_ABSTRACT)
    assert paper.startswith("Interval Tree Clocks: A Logical Clock for Dynamic Systems\n\n")
    assert paper.split("\n\n", 1)[1].startswith("Causality tracking mechanisms")
    assert len(paper) <= 1600

    html_page = "<html><title>ITC paper</title><body><p>Short body.</p></body></html>"
    assert module._reference_extract(html_page) == "ITC paper\n\nShort body."


@pytest.mark.anyio
async def test_step_brief_carries_references_and_prompt(
    tmp_path: Path,
    beagle: Path,
    fake_beagle: Path,
    fake_tau: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    project = _pursuit_project(tmp_path)
    monkeypatch.chdir(project)
    page = (b"<p>Join merges two stamps.</p>", "text/html")
    _fake_web(monkeypatch, {"https://example.org/blog/interval-tree-clocks.html": page})
    _module()._fetch_references(project, ITC_PROMPT)
    _ready_task(fake_beagle)
    runtime, _ = _bound(tmp_path)

    await _tool(runtime, "pursuit_step").execute(
        "c1",
        {
            "task": "T0002",
            "criteria": "done.txt exists",
            "done_when": "grep -q done done.txt",
            "scope": ["done.txt"],
            "notes": "A stamp is a pair of integers.",
        },
    )

    brief = _runs(fake_tau)[0]["stdin"]
    assert "Do the parser." in brief
    assert "read first; outranks the driver's notes" in brief
    assert "- references/interval-tree-clocks.txt (from https://example.org/blog/" in brief
    assert "could not fetch https://example.org/papers/itc2008.pdf" in brief
    assert f"The user's original request, verbatim:\n<<<\n{ITC_PROMPT}\n>>>" in brief
    driver = "From the driver (who has not read the reference):\nA stamp is a pair of integers."
    assert driver in brief
    assert brief.index("references/interval-tree-clocks.txt") < brief.index(driver)


@pytest.mark.anyio
async def test_pursuit_plan_adds_one_part_to_a_container(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(_pursuit_project(tmp_path))
    runtime, _ = _bound(tmp_path)

    result = await _tool(runtime, "pursuit_plan").execute(
        "c1", {"task": "T0001", "parts": ["Docs::so people can use it"]}
    )

    assert _pursuit_calls(fake_beagle, "split") == []
    assert _pursuit_calls(fake_beagle, "add") == [
        ["Docs", "--parent", "T0001", "--intent", "so people can use it"]
    ]
    assert "pursuit_step" in result.text


@pytest.mark.anyio
async def test_pursuit_plan_with_one_part_on_a_leaf_says_to_step_it(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(_pursuit_project(tmp_path))
    (fake_beagle / "add.out").write_text("beagle: T0002 is a pending leaf with work of its own.")
    (fake_beagle / "add.rc").write_text("4")
    runtime, _ = _bound(tmp_path)

    result = await _tool(runtime, "pursuit_plan").execute(
        "c1", {"task": "T0002", "parts": ["Parser::reads input"]}
    )

    assert "already one step" in result.text and "pursuit_step task=T0002" in result.text


def _children_of(fake: Path, task: str, *titles: str) -> None:
    nodes = [{"id": task, "status": "pending", "container": True}] + [
        {"id": f"T00{i}", "parent": task, "title": title, "status": "pending"}
        for i, title in enumerate(titles, start=10)
    ]
    (fake / "tree.out").write_text(json.dumps({"goal": "Ship it", "nodes": nodes}))


@pytest.mark.anyio
async def test_pursuit_plan_does_not_add_a_part_the_task_already_has(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Run 9: a 9B driver re-sent a plan it had made, and every part was added
    # again under the same container, then worked twice.
    monkeypatch.chdir(_pursuit_project(tmp_path))
    _children_of(fake_beagle, "T0004", "interval-tree", "event-counter")
    (fake_beagle / "add.out").write_text(
        "T0012  serializer\n  it reads like T0011. `beagle pursuit close T0012 --outcome "
        'abandoned --reason "duplicate"` retires this one.'
    )
    runtime, _ = _bound(tmp_path)
    plan = _tool(runtime, "pursuit_plan")

    again = await plan.execute(
        "c1", {"task": "T0004", "parts": ["interval-tree::store it", "Event-Counter::count"]}
    )
    one_new = await plan.execute(
        "c2", {"task": "T0004", "parts": ["interval-tree::store it", "serializer::save it"]}
    )

    assert "nothing added" in again.text and "interval-tree (T0010)" in again.text
    assert _pursuit_calls(fake_beagle, "split") == []
    assert _pursuit_calls(fake_beagle, "add") == [
        ["serializer", "--parent", "T0004", "--intent", "save it"]
    ]
    assert "Not added again" in one_new.text and "abandon='duplicate of" in one_new.text


@pytest.mark.anyio
async def test_pursuit_step_abandons_a_task_without_a_worker(
    tmp_path: Path,
    beagle: Path,
    fake_beagle: Path,
    fake_tau: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Refused the bash close, the run 9 driver "abandoned" duplicates by
    # opening them with `true` as the check, and sent a worker at each.
    monkeypatch.chdir(_pursuit_project(tmp_path))
    _ready_task(fake_beagle)
    (fake_beagle / "close.out").write_text("T0021 abandoned — duplicate of T0006\n  finding N1\n")
    # Run 10: what waited on an abandoned task waited for ever.
    waits = [
        {"id": "T0022", "parent": "T0002", "waiting_on": ["T0021"]},
        {"id": "T0023", "parent": "T0002", "waiting_on": ["T0022"]},
    ]
    others = [
        {"id": "T0001", "parent": "", "status": "pending", "container": True},
        {"id": "T0006", "parent": "T0002", "status": "done"},
        # T0058: only a superseded milestone's successor may go as a duplicate.
        {"id": "T0020", "parent": "T0001", "status": "superseded"},
        {"id": "T0021", "parent": "T0001", "status": "pending", "sibling_of": "T0020"},
    ]
    (fake_beagle / "tree.out").write_text(json.dumps({"nodes": others + waits}))
    runtime, _ = _bound(tmp_path)
    step = _tool(runtime, "pursuit_step")

    nameless = await step.execute("c1", {"abandon": "duplicate"})
    result = await step.execute("c2", {"task": "T0021", "abandon": "duplicate of T0006"})

    assert "pass task too" in nameless.text
    assert _pursuit_calls(fake_beagle, "close") == [
        ["T0021", "--outcome", "abandoned", "--reason", "duplicate of T0006"]
    ]
    assert _pursuit_calls(fake_beagle, "depend") == [
        ["T0022", "T0021", "--drop", "--reason", "T0021 abandoned: duplicate of T0006"]
    ]
    assert _pursuit_calls(fake_beagle, "open") == [] and _runs(fake_tau) == []
    assert "T0021 abandoned" in result.text and "finding" not in result.text
    assert "No longer waiting on it: T0022." in result.text


def _ready_task(fake: Path, check: str = "grep -q done done.txt") -> None:
    ready = {"open": [], "ready": [{"id": "T0002", "title": "Parser"}], "ready_total": 1}
    (fake / "next.out").write_text(json.dumps(ready))
    record = {"id": "T0002", "title": "Parser", "intent": "reads input", "status": "pending"}
    (fake / "show.out").write_text(json.dumps({**record, "done_when": check}))
    (fake / "brief.out").write_text("# T0002: Parser\nDo the parser.\n")


@pytest.mark.anyio
async def test_pursuit_step_shows_the_next_task_before_opening_it(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(_pursuit_project(tmp_path))
    _ready_task(fake_beagle)
    runtime, _ = _bound(tmp_path)

    result = await _tool(runtime, "pursuit_step").execute("c1", {})

    assert "Next task: T0002 — Parser" in result.text and "reads input" in result.text
    assert _pursuit_calls(fake_beagle, "open") == []


@pytest.mark.anyio
async def test_pursuit_step_will_not_offer_a_container(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # With the leaves done, a 9B driver reached for the root next.
    monkeypatch.chdir(_pursuit_project(tmp_path))
    _ready_task(fake_beagle)
    runtime, _ = _bound(tmp_path)
    step = _tool(runtime, "pursuit_step")

    root = await step.execute("c1", {"task": "T0001"})
    (fake_beagle / "next.out").write_text(json.dumps({"open": [], "ready": []}))
    (fake_beagle / "next.rc").write_text("3")
    finished = await step.execute("c2", {"task": "T0001"})

    assert "not a task to work now" in root.text and "Workable now: T0002" in root.text
    assert "tell the user the pursuit is done" in finished.text
    assert _pursuit_calls(fake_beagle, "open") == []


@pytest.mark.anyio
async def test_pursuit_step_runs_a_worker_until_the_check_passes_then_closes(
    tmp_path: Path,
    beagle: Path,
    fake_beagle: Path,
    fake_tau: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    project = _pursuit_project(tmp_path)
    monkeypatch.chdir(project)
    monkeypatch.setenv("FAKE_TAU_SUCCEEDS_ON", "2")
    _ready_task(fake_beagle)
    runtime, _ = _bound(tmp_path)

    result = await _tool(runtime, "pursuit_step").execute(
        "c1",
        {
            "task": "T0002",
            "criteria": "done.txt exists",
            "done_when": "grep -q done done.txt",
            "scope": ["done.txt"],
            "notes": "Start in the project root.",
        },
    )

    assert _pursuit_calls(fake_beagle, "open") == [
        [
            "T0002",
            "--criteria",
            "done.txt exists",
            "--done-when",
            "grep -q done done.txt",
            "--scope",
            "done.txt",
        ]
    ]
    first, second = _runs(fake_tau)
    assert first["argv"][:3] == ["-p", "--mode", "json"]
    assert "Do the parser." in first["stdin"] and "Start in the project root." in first["stdin"]
    assert "the check still fails (exit 2)" in second["stdin"]
    [close] = _pursuit_calls(fake_beagle, "close")
    assert close[:3] == ["T0002", "--outcome", "done"]
    assert close[close.index("--spent") + 1] == "2000"
    assert close[close.index("--body") + 1] == "attempt 2: wrote done.txt"
    assert "closed done" in result.text and "pursuit_step with no arguments" in result.text


SUPERSEDED_NOTE = (
    "The check passed at close: failures this report names are from before the "
    "worker's last edit, and are fixed."
)


async def _closed_done_step(
    tmp_path: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch, report: str
) -> str:
    project = _pursuit_project(tmp_path)
    monkeypatch.chdir(project)
    monkeypatch.setenv("FAKE_TAU_REPORT", report)
    _ready_task(fake_beagle)
    runtime, _ = _bound(tmp_path)
    result = await _tool(runtime, "pursuit_step").execute(
        "c1",
        {
            "task": "T0002",
            "criteria": "c",
            "done_when": "grep -q done done.txt",
            "scope": ["done.txt"],
        },
    )
    assert "closed done" in result.text
    return result.text


@pytest.mark.anyio
async def test_closed_done_step_marks_a_failing_report_superseded(
    tmp_path: Path,
    beagle: Path,
    fake_beagle: Path,
    fake_tau: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # R09: W14 reported "2 failed", T0009 closed done, and the driver chased the stale failures.
    report = "wrote done.txt\n2 failed, 10 passed (exit 1)"
    text = await _closed_done_step(tmp_path, fake_beagle, monkeypatch, report)

    assert f"{SUPERSEDED_NOTE}\nSub-agent report:\n{report}" in text


@pytest.mark.anyio
async def test_closed_done_step_leaves_a_passing_report_alone(
    tmp_path: Path,
    beagle: Path,
    fake_beagle: Path,
    fake_tau: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    report = "wrote done.txt; no errors, nothing fails now: 12 passed"
    text = await _closed_done_step(tmp_path, fake_beagle, monkeypatch, report)

    assert SUPERSEDED_NOTE not in text
    assert f"Sub-agent report:\n{report}" in text


def test_report_with_zero_failed_is_not_a_failure_report() -> None:
    # T0085: "0 failed, 12 passed" reports success; only a non-zero count is a failure.
    claims_failure = _module()._report_claims_failure

    assert not claims_failure("pytest: 0 failed, 12 passed")
    assert claims_failure("pytest: 1 failed, 11 passed")
    assert claims_failure("pytest: 10 failed, 2 passed")
    assert claims_failure("exit code 2")
    assert claims_failure("two remaining failures")
    assert claims_failure("FAILED tests/test_x.py::test_y")


def test_report_naming_an_error_is_a_failure_report() -> None:
    # T0085: a report quoting a Python error line still claims a failure.
    claims_failure = _module()._report_claims_failure

    assert claims_failure("ran it:\nTypeError: x")
    assert claims_failure("ValueError: bad stamp")
    assert not claims_failure("no errors, nothing fails now: 12 passed")


WITNESSED_REPORT = (
    "wrote done.txt\n\nWITNESS: src/clock.py\nNEEDLE:\n    return a + b\n"
    "REPLACEMENT:\n    return a - b\nEND WITNESS"
)


def _git_project(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    project = _pursuit_project(tmp_path)
    subprocess.run(["git", "init", "--quiet"], cwd=project, check=True)
    for key, value in (("NAME", "t"), ("EMAIL", "t@example.com")):
        monkeypatch.setenv(f"GIT_AUTHOR_{key}", value)
        monkeypatch.setenv(f"GIT_COMMITTER_{key}", value)
    return project


@pytest.mark.anyio
async def test_pursuit_step_proves_the_workers_witness_then_closes_and_commits(
    tmp_path: Path,
    beagle: Path,
    fake_beagle: Path,
    fake_tau: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Run 11d: every check was NOT PROVEN, and six of seven tasks' work was
    # never committed.
    project = _git_project(tmp_path, monkeypatch)
    monkeypatch.chdir(project)
    monkeypatch.setenv("FAKE_TAU_REPORT", WITNESSED_REPORT)
    (project / "__pycache__").mkdir()
    (project / "__pycache__" / "x.pyc").write_text("")
    _ready_task(fake_beagle)
    (fake_beagle / "prove.out").write_text("T0002: PROVEN — refuses when `a + b` is `a - b`\n")
    (fake_beagle / "commit.out").write_text("T0002: committed abc123, 1 file(s): T0002: Parser\n")
    runtime, _ = _bound(tmp_path)

    result = await _tool(runtime, "pursuit_step").execute(
        "c1",
        {
            "task": "T0002",
            "criteria": "c",
            "done_when": "grep -q done done.txt",
            "scope": ["done.txt"],
        },
    )

    [run] = _runs(fake_tau)
    assert "WITNESS: <path of the source file>" in run["stdin"]
    [prove] = _pursuit_calls(fake_beagle, "prove")
    assert prove[:7] == [
        "T0002",
        "--mutate",
        "src/clock.py",
        "--needle",
        "    return a + b",
        "--replacement",
        "    return a - b",
    ]
    assert _pursuit_calls(fake_beagle, "close")[0][:3] == ["T0002", "--outcome", "done"]
    assert _pursuit_calls(fake_beagle, "commit") == [
        ["T0002", "done.txt", "--subject", "T0002: Parser"]
    ]
    # While still open: a close's workspace-clean sweep excuses only its own writes.
    verbs = [c["argv"][1] for c in _calls(fake_beagle) if c["argv"][0] == "pursuit"]
    assert verbs.index("commit") < verbs.index("close")
    assert "closed done" in result.text and "committed abc123" in result.text


@pytest.mark.anyio
async def test_pursuit_step_takes_the_work_away_when_the_worker_names_no_witness(
    tmp_path: Path,
    beagle: Path,
    fake_beagle: Path,
    fake_tau: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    project = _git_project(tmp_path, monkeypatch)
    monkeypatch.chdir(project)
    _ready_task(fake_beagle)
    (fake_beagle / "prove.out").write_text("T0002: PROVEN — refuses with done.txt gone\n")
    runtime, _ = _bound(tmp_path)

    await _tool(runtime, "pursuit_step").execute(
        "c1",
        {
            "task": "T0002",
            "criteria": "c",
            "done_when": "grep -q done done.txt",
            "scope": ["done.txt"],
        },
    )

    [prove] = _pursuit_calls(fake_beagle, "prove")
    assert prove[:3] == ["T0002", "--absent", "done.txt"]
    assert len(_pursuit_calls(fake_beagle, "close")) == 1


@pytest.mark.anyio
async def test_pursuit_step_keeps_a_task_open_while_its_check_passes_over_a_defect(
    tmp_path: Path,
    beagle: Path,
    fake_beagle: Path,
    fake_tau: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Run 11d closed T0005/T0006 on checks that only imported the module.
    monkeypatch.chdir(_git_project(tmp_path, monkeypatch))
    monkeypatch.setenv("FAKE_TAU_REPORT", WITNESSED_REPORT)
    _ready_task(fake_beagle)
    (fake_beagle / "prove.out").write_text(
        "T0002: NOT PROVEN — the check STILL PASSES with the defect put back\n"
    )
    (fake_beagle / "prove.rc").write_text("9")
    runtime, _ = _bound(tmp_path)

    result = await _tool(runtime, "pursuit_step").execute(
        "c1",
        {
            "task": "T0002",
            "criteria": "c",
            "done_when": "grep -q done done.txt",
            "scope": ["done.txt"],
        },
    )

    first, second = _runs(fake_tau)
    assert "does not test what this task built" in second["stdin"]
    assert len(_pursuit_calls(fake_beagle, "prove")) == 2
    assert _pursuit_calls(fake_beagle, "close") == []
    assert _pursuit_calls(fake_beagle, "commit") == []
    assert "stays open" in result.text and "test of the behaviour itself" in result.text


CASES_SCOPE = ["tests/cases.json", "tests/test_case_data.py"]
CASES_DATA_TEST = (
    "import json\n\n\ndef test_cases():\n    assert json.load(open('tests/cases.json'))\n"
)


def _cases_task(
    tmp_path: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch, data_test: str
) -> Path:
    """A known-answers task whose worker writes only the data file and its test."""
    project = _git_project(tmp_path, monkeypatch)
    monkeypatch.chdir(project)
    writes = {"tests/cases.json": '[{"in": 1, "out": 2}]', "tests/test_case_data.py": data_test}
    monkeypatch.setenv("FAKE_TAU_WRITES", json.dumps(writes))
    _ready_task(fake_beagle, "grep -q out tests/cases.json")
    (fake_beagle / "prove.out").write_text("T0002: PROVEN — refuses with tests/cases.json gone\n")
    return project


async def _step_cases(tmp_path: Path, **extra: Any) -> Any:
    runtime, _ = _bound(tmp_path)
    return await _tool(runtime, "pursuit_step").execute(
        "c1",
        {
            "task": "T0002",
            "criteria": "the known answers are written",
            "done_when": "grep -q out tests/cases.json",
            "scope": CASES_SCOPE,
            **extra,
        },
    )


@pytest.mark.anyio
async def test_cases_task_proves_by_absent_data_file(
    tmp_path: Path,
    beagle: Path,
    fake_beagle: Path,
    fake_tau: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Run R04: a data-only task had no source file to take away, and never closed.
    _cases_task(tmp_path, fake_beagle, monkeypatch, CASES_DATA_TEST)

    result = await _step_cases(tmp_path)

    [prove] = _pursuit_calls(fake_beagle, "prove")
    assert prove[:3] == ["T0002", "--absent", "tests/cases.json"]
    assert "--absent" not in prove[3:]
    assert _pursuit_calls(fake_beagle, "close")[0][:3] == ["T0002", "--outcome", "done"]
    assert "closed done" in result.text


@pytest.mark.anyio
async def test_cases_task_locks_scope_when_none_given(
    tmp_path: Path,
    beagle: Path,
    fake_beagle: Path,
    fake_tau: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    project = _cases_task(tmp_path, fake_beagle, monkeypatch, CASES_DATA_TEST)

    result = await _step_cases(tmp_path)

    assert "Locked: tests/cases.json, tests/test_case_data.py" in result.text
    store = project / ".beagle" / "locked"
    assert (store / "tests" / "cases.json").read_text() == '[{"in": 1, "out": 2}]'
    assert (store / "tests" / "test_case_data.py").read_text() == CASES_DATA_TEST
    assert not (store / "done.txt").exists()


@pytest.mark.anyio
async def test_unproven_text_for_tests_only_scope_does_not_say_import(
    tmp_path: Path,
    beagle: Path,
    fake_beagle: Path,
    fake_tau: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _cases_task(tmp_path, fake_beagle, monkeypatch, CASES_DATA_TEST)
    (fake_beagle / "prove.out").write_text("T0002: NOT PROVEN — the file predates the task\n")
    (fake_beagle / "prove.rc").write_text("9")

    runtime, _ = _bound(tmp_path)  # one runtime: the unproven memory is the module's
    step = _tool(runtime, "pursuit_step")
    result = await step.execute(
        "c1",
        {
            "task": "T0002",
            "criteria": "the known answers are written",
            "done_when": "grep -q out tests/cases.json",
            "scope": CASES_SCOPE,
        },
    )
    (fake_beagle / "next.out").write_text(json.dumps({"open": ["T0002"], "ready": []}))
    again = await step.execute("c2", {"task": "T0002", "scope": CASES_SCOPE})

    assert "stays open" in result.text
    for text in (result.text, again.text):
        assert "import the code" not in text
        assert "the data file's absence is the proof" in text
        assert "ImportError" not in text
    assert again.text.startswith("pursuit_step: T0002 not run"), again.text
    assert _pursuit_calls(fake_beagle, "close") == []


@pytest.mark.anyio
async def test_cases_task_with_implementation_in_test_file_stays_open(
    tmp_path: Path,
    beagle: Path,
    fake_beagle: Path,
    fake_tau: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Run R04: W1 wrote `class IntervalTreeClock` into the cases test.
    data_test = (
        "import pytest\n\n\nclass IntervalTreeClock:\n    pass\n\n\n"
        "def join(a, b):\n"
        + "    a = a\n"
        * 15
        + "    return a\n\n\n@pytest.fixture\ndef cases():\n    return []\n\n\n"
        "def _load():\n    return []\n\n\n" + CASES_DATA_TEST.split("\n\n\n", 1)[1]
    )
    project = _cases_task(tmp_path, fake_beagle, monkeypatch, data_test)

    result = await _step_cases(tmp_path)

    assert "stays open" in result.text
    assert "implementation belongs in the module the test imports, not the test file" in (
        result.text
    )
    assert "tests/test_case_data.py: class IntervalTreeClock" in result.text
    assert "tests/test_case_data.py: def join" in result.text
    assert "def cases" not in result.text and "def _load" not in result.text
    assert _pursuit_calls(fake_beagle, "close") == []
    assert _pursuit_calls(fake_beagle, "commit") == []
    assert not (project / ".beagle" / "locked").exists()


def test_a_witness_block_is_read_from_the_end_of_a_report() -> None:
    witness = _module()._witness
    assert witness(WITNESSED_REPORT) == ("src/clock.py", "    return a + b", "    return a - b")
    multi = "WITNESS: `a.py`\nNEEDLE:\nif x:\n    y()\nREPLACEMENT:\nEND WITNESS"
    assert witness(multi) == ("a.py", "if x:\n    y()", "")
    assert witness("no witness here") is None
    assert witness("WITNESS: a.py\nNEEDLE:\n\nREPLACEMENT:\nx\nEND WITNESS") is None


@pytest.mark.anyio
async def test_a_worker_with_no_report_gets_a_short_stub_not_its_event_stream(
    tmp_path: Path,
    beagle: Path,
    fake_beagle: Path,
    fake_tau: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Run 7: a worker ended on `length` with no text, and its whole stdout --
    # 822 MB of message_update events -- became the step's result.
    project = _pursuit_project(tmp_path)
    monkeypatch.chdir(project)
    monkeypatch.setenv("FAKE_TAU_RAMBLES", "1")
    _ready_task(fake_beagle)
    runtime, _ = _bound(tmp_path)

    result = await _tool(runtime, "pursuit_step").execute(
        "c1",
        {
            "task": "T0002",
            "criteria": "done.txt exists",
            "done_when": "grep -q done done.txt",
            "scope": ["done.txt"],
        },
    )

    assert len(result.text) < 20_000
    assert "wrote no report: it ended on stopReason=length" in result.text
    assert result.text.count("so the parser") == 1  # the tail of its thinking
    [run, *_] = _runs(fake_tau)
    session_id = run["argv"][run["argv"].index("--session-id") + 1]
    assert f"{session_id}.jsonl" in result.text
    [close] = _pursuit_calls(fake_beagle, "close")
    assert "Worker transcript" not in close[close.index("--body") + 1]


@pytest.mark.anyio
async def test_a_step_locks_its_cases_and_later_steps_cannot_change_them(
    tmp_path: Path,
    beagle: Path,
    fake_beagle: Path,
    fake_tau: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    project = _pursuit_project(tmp_path)
    monkeypatch.chdir(project)
    (project / "cases.json").write_text('[{"in": 1, "out": 2}]')
    _ready_task(fake_beagle)
    runtime, _ = _bound(tmp_path)
    step = _tool(runtime, "pursuit_step")

    first = await step.execute(
        "c1",
        {
            "task": "T0002",
            "criteria": "the cases are written",
            "done_when": "grep -q done done.txt",
            "locks": ["cases.json", "missing.json"],
        },
    )

    assert "Locked: cases.json" in first.text
    assert "missing.json: not a file in the project" in first.text
    assert (project / ".beagle" / "locked" / "cases.json").read_text() == '[{"in": 1, "out": 2}]'

    # A later worker that rewrites the cases has them put back before the check.
    (project / "done.txt").unlink()
    monkeypatch.setenv("FAKE_TAU_TAMPERS", "cases.json")
    second = await step.execute(
        "c2", {"task": "T0002", "criteria": "the code passes", "done_when": "grep -q done done.txt"}
    )

    assert (project / "cases.json").read_text() == '[{"in": 1, "out": 2}]'
    assert "changed locked files (cases.json)" in second.text
    assert "Locked files:" in _runs(fake_tau)[-1]["stdin"]
    assert "- cases.json" in _runs(fake_tau)[-1]["stdin"]


@pytest.mark.anyio
async def test_locks_asked_for_on_opening_hold_until_the_task_closes(
    tmp_path: Path,
    beagle: Path,
    fake_beagle: Path,
    fake_tau: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    project = _pursuit_project(tmp_path)
    monkeypatch.chdir(project)
    (project / "cases.json").write_text("[]")
    monkeypatch.setenv("FAKE_TAU_SUCCEEDS_ON", "99")
    _ready_task(fake_beagle)
    runtime, _ = _bound(tmp_path)
    step = _tool(runtime, "pursuit_step")

    await step.execute(
        "c1",
        {
            "task": "T0002",
            "criteria": "c",
            "done_when": "grep -q done done.txt",
            "locks": ["cases.json"],
            "attempts": 1,
        },
    )
    assert not (project / ".beagle" / "locked").exists()

    # Sent again without `locks`: the ones asked for at opening still apply.
    (fake_beagle / "next.out").write_text(json.dumps({"open": ["T0002"], "ready": []}))
    monkeypatch.setenv("FAKE_TAU_SUCCEEDS_ON", "1")
    result = await step.execute("c2", {"task": "T0002"})

    assert "Locked: cases.json" in result.text
    assert (project / ".beagle" / "locked" / "cases.json").is_file()


@pytest.mark.anyio
async def test_pursuit_step_says_why_a_measured_spend_overran(
    tmp_path: Path,
    beagle: Path,
    fake_beagle: Path,
    fake_tau: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(_pursuit_project(tmp_path))
    monkeypatch.setenv("FAKE_TAU_SUCCEEDS_ON", "1")
    _ready_task(fake_beagle)
    (fake_beagle / "next.out").write_text(json.dumps({"open": ["T0002"], "ready": []}))
    (fake_beagle / "close.out").write_text(
        "beagle: T0002 spent 226760 tokens against a budget of 100000 (2.3x). Say what "
        'the estimate missed with --spent 226760 --spent-because "...", then close.'
    )
    (fake_beagle / "close.rc").write_text("4")
    runtime, _ = _bound(tmp_path)

    await _tool(runtime, "pursuit_step").execute("c1", {})

    first, second = _pursuit_calls(fake_beagle, "close")
    assert "--spent-because" not in first
    assert second[: len(first)] == first
    assert "peak context" in second[second.index("--spent-because") + 1]


@pytest.mark.anyio
async def test_pursuit_step_keeps_a_task_open_while_its_check_fails(
    tmp_path: Path,
    beagle: Path,
    fake_beagle: Path,
    fake_tau: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(_pursuit_project(tmp_path))
    monkeypatch.setenv("FAKE_TAU_SUCCEEDS_ON", "99")
    _ready_task(fake_beagle)
    open_task = {"open": ["T0002"], "ready": [], "ready_total": 0}
    (fake_beagle / "next.out").write_text(json.dumps(open_task))
    runtime, _ = _bound(tmp_path)

    # An open task needs no criteria: they were bound when it opened.
    result = await _tool(runtime, "pursuit_step").execute("c1", {"attempts": 1})

    assert len(_runs(fake_tau)) == 1
    assert _pursuit_calls(fake_beagle, "open") == []
    # A done close the check refuses would block the task for good.
    assert _pursuit_calls(fake_beagle, "close") == []
    assert "stays open" in result.text and "new_route=true" in result.text


@pytest.mark.anyio
async def test_pursuit_step_amends_an_open_task_whose_check_cannot_judge(
    tmp_path: Path,
    beagle: Path,
    fake_beagle: Path,
    fake_tau: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # A 9B driver bound prose as the check; beagle runs it as words, so it
    # failed whatever the work did, and the old done_when was all it could send.
    monkeypatch.chdir(_pursuit_project(tmp_path))
    monkeypatch.setenv("FAKE_TAU_SUCCEEDS_ON", "1")
    _ready_task(fake_beagle, check="grep -q done done.txt exits 0 and is good")
    open_task = {"open": ["T0002"], "ready": [], "ready_total": 0}
    (fake_beagle / "next.out").write_text(json.dumps(open_task))
    runtime, _ = _bound(tmp_path)

    stuck = await _tool(runtime, "pursuit_step").execute("c0", {"task": "T0002"})
    assert "cannot pass" in stuck.text and len(_runs(fake_tau)) == 0

    result = await _tool(runtime, "pursuit_step").execute(
        "c1", {"task": "T0002", "done_when": "grep -q done done.txt"}
    )

    [amend] = _pursuit_calls(fake_beagle, "amend")
    assert amend[:3] == ["T0002", "--done-when", "grep -q done done.txt"] and "--reason" in amend
    assert "closed done" in result.text


@pytest.mark.anyio
async def test_pursuit_step_refuses_a_check_written_as_a_sentence(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(_pursuit_project(tmp_path))
    _ready_task(fake_beagle)
    runtime, _ = _bound(tmp_path)
    step = _tool(runtime, "pursuit_step")
    args = {"task": "T0002", "criteria": "greets"}

    prose = await step.execute(
        "c1", {**args, "done_when": 'python3 -m pytest -q exits 0 and a test asserts "x"'}
    )
    beagle_check = await step.execute("c3", {**args, "done_when": "beagle pursuit close T0002"})
    quoted = await step.execute(
        "c2", {**args, "done_when": "python3 -c 'import sys; sys.exit(1 and 1)'"}
    )

    assert "reads as a sentence" in prose.text and "'exits'" in prose.text
    assert "runs beagle itself" in beagle_check.text
    [opened] = _pursuit_calls(fake_beagle, "open")
    assert opened[opened.index("--done-when") + 1].startswith("python3 -c")
    assert "reads as a sentence" not in quoted.text


@pytest.mark.anyio
async def test_pursuit_step_refuses_a_bound_check_with_a_bare_operator(
    tmp_path: Path,
    beagle: Path,
    fake_beagle: Path,
    fake_tau: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Under `bash -c` this passes once done.txt exists; beagle's close would
    # hand `&&` to `test` and refuse it, blocking the task for good. No
    # sub-agent is spent on it.
    monkeypatch.chdir(_pursuit_project(tmp_path))
    monkeypatch.setenv("FAKE_TAU_SUCCEEDS_ON", "1")
    _ready_task(fake_beagle, check="grep -q done done.txt && true")
    open_task = {"open": ["T0002"], "ready": [], "ready_total": 0}
    (fake_beagle / "next.out").write_text(json.dumps(open_task))
    runtime, _ = _bound(tmp_path)

    result = await _tool(runtime, "pursuit_step").execute("c1", {"attempts": 1})

    assert _runs(fake_tau) == []
    assert _pursuit_calls(fake_beagle, "close") == []
    assert "bare '&&'" in result.text and "corrected done_when" in result.text


@pytest.mark.anyio
async def test_pursuit_step_will_not_open_a_task_whose_check_already_passes(
    tmp_path: Path,
    beagle: Path,
    fake_beagle: Path,
    fake_tau: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Run 9 bound a test an earlier task had already made pass: the task
    # closed done on whatever its worker did, or nothing.
    project = _pursuit_project(tmp_path)
    monkeypatch.chdir(project)
    (project / "done.txt").write_text("done by T0001")
    _ready_task(fake_beagle)
    runtime, _ = _bound(tmp_path)

    result = await _tool(runtime, "pursuit_step").execute(
        "c1", {"task": "T0002", "criteria": "done.txt exists", "done_when": "grep -q done done.txt"}
    )

    assert "already passes" in result.text and "abandon=" in result.text
    assert "do not write it yourself" in result.text
    assert _pursuit_calls(fake_beagle, "open") == [] and _runs(fake_tau) == []


def _part_on_a_passing_check(fake: Path, project: Path, container: str) -> None:
    """T0010 ready under `container`, beside T0009 done on the same check."""
    (project / "done.txt").write_text("done by T0009")
    nodes = [
        {"id": "T0001", "status": "open", "container": True},
        {"id": "T0007", "parent": "T0001", "status": "open", "container": True},
        {
            "id": "T0009",
            "parent": container,
            "status": "done",
            "done_when": "grep -q  done\tdone.txt",
        },
        {"id": "T0010", "parent": container, "status": "pending", "done_when": ""},
    ]
    (fake / "tree.out").write_text(json.dumps({"goal": "Ship it", "nodes": nodes}))
    ready = {"open": [], "ready": [{"id": "T0010", "title": "Re-run"}], "ready_total": 1}
    (fake / "next.out").write_text(json.dumps(ready))
    record = {"id": "T0010", "title": "Re-run", "intent": "confirm", "status": "pending"}
    (fake / "show.out").write_text(json.dumps({**record, "done_when": ""}))


@pytest.mark.anyio
async def test_already_passes_on_a_container_part_names_the_done_sibling(
    tmp_path: Path,
    beagle: Path,
    fake_beagle: Path,
    fake_tau: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Run R09: T0010 sat beside T0009, done on the same check, and was told to
    # abandon itself as a duplicate, which T0058 refuses for a container's part.
    project = _pursuit_project(tmp_path)
    monkeypatch.chdir(project)
    _part_on_a_passing_check(fake_beagle, project, "T0007")
    runtime, _ = _bound(tmp_path)

    result = await _tool(runtime, "pursuit_step").execute(
        "c1", {"task": "T0010", "criteria": "it runs", "done_when": "grep -q done done.txt"}
    )

    assert "already passes" in result.text and "abandon=" not in result.text
    assert "T0009 closed done on this same check" in result.text
    assert "pursuit_step {} for other work" in result.text
    assert _pursuit_calls(fake_beagle, "open") == [] and _runs(fake_tau) == []


@pytest.mark.anyio
async def test_already_passes_on_a_root_child_keeps_the_abandon_hint(
    tmp_path: Path,
    beagle: Path,
    fake_beagle: Path,
    fake_tau: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    project = _pursuit_project(tmp_path)
    monkeypatch.chdir(project)
    _part_on_a_passing_check(fake_beagle, project, "T0001")
    runtime, _ = _bound(tmp_path)

    result = await _tool(runtime, "pursuit_step").execute(
        "c1", {"task": "T0010", "criteria": "it runs", "done_when": "grep -q done done.txt"}
    )

    assert "already passes" in result.text and "abandon=" in result.text
    assert "closed done on this same check" not in result.text
    assert _pursuit_calls(fake_beagle, "open") == [] and _runs(fake_tau) == []


def _audit_due(fake: Path) -> None:
    ready = {"open": [], "ready": [{"id": "T0005", "title": "Impl"}], "ready_total": 1}
    (fake / "next.out").write_text(json.dumps({**ready, "audit_due": {"closes": ["T0002"]}}))
    (fake / "audit.out").write_text(
        "# Audit of 16 close(s)\nReport MEETS or SHORT per task.\n\n"
        "For the driver: `beagle pursuit audit --record --verdict sound|defects`\n"
    )


@pytest.mark.anyio
@pytest.mark.parametrize(
    ("report", "verdict"),
    [
        ("T0002 MEETS.\nT0003 MEETS.\nSOUND", "sound"),
        ("T0002 MEETS.\nT0003 SHORT: no test of join.\nDEFECTS 1", "defects"),
    ],
)
async def test_pursuit_step_has_a_sub_agent_do_a_due_audit(
    tmp_path: Path,
    beagle: Path,
    fake_beagle: Path,
    fake_tau: Path,
    monkeypatch: pytest.MonkeyPatch,
    report: str,
    verdict: str,
) -> None:
    # Run 9: with an audit due, open was refused with bash advice; the
    # driver recorded a verdict by hand, read nothing, and lost the thread.
    monkeypatch.chdir(_pursuit_project(tmp_path))
    monkeypatch.setenv("FAKE_TAU_REPORT", report)
    _audit_due(fake_beagle)
    runtime, _ = _bound(tmp_path)

    result = await _tool(runtime, "pursuit_step").execute("c1", {"task": "T0005"})

    [run] = _runs(fake_tau)
    assert "Audit of 16" in run["stdin"] and "For the driver" not in run["stdin"]
    assert _pursuit_calls(fake_beagle, "audit") == [
        [],
        ["--record", "--verdict", verdict, "--note", report],
    ]
    assert _pursuit_calls(fake_beagle, "open") == []
    assert f": {verdict}." in result.text and "pursuit_step" in result.text


@pytest.mark.anyio
async def test_a_due_audit_with_no_report_is_not_recorded(
    tmp_path: Path,
    beagle: Path,
    fake_beagle: Path,
    fake_tau: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(_pursuit_project(tmp_path))
    monkeypatch.setenv("FAKE_TAU_REPORT", " ")
    _audit_due(fake_beagle)
    runtime, _ = _bound(tmp_path)

    result = await _tool(runtime, "pursuit_step").execute("c1", {})

    assert _pursuit_calls(fake_beagle, "audit") == [[]]
    assert "did not finish" in result.text and "send it again" in result.text


@pytest.mark.parametrize(
    ("check", "problem"),
    [
        # Checks a 9B driver bound in runs 7 and 8.
        ('grep -q "interval tree clocks" .beagle/tree/T0008.md', "reads .beagle/"),
        # Run 11b's summary went into .beagle/memory/, so its check read it there.
        ("test -f .beagle/memory/reference-summary.md", "in the project, not in .beagle/"),
        ("bash -c 'beagle doctor && test -d tests'", "runs beagle itself"),
        ("/home/u/.tau/beagle-plugin/bin/beagle pursuit close T0002", "runs beagle itself"),
        ("test -d src/itc && test -f pyproject.toml", "bare '&&'"),
        ("python3 -m pytest -q tests/ | tail -1", "bare '|'"),
        ("python3 -m pytest -q exits 0 and passes", "reads as a sentence"),
        # Checks it bound in run 9, each passing whatever the work said.
        ("true", "exits 0 whatever"),
        ("cat docs/design.md", "as soon as the file is there"),
        ("python3 -m json.tool tests/cases.json", "as soon as the file is there"),
        ("python3 -m pytest -q tests/test_itc.py", None),
        ("grep -q 'join' docs/design.md", None),
        ("bash -c 'test -d tests && python3 -m pytest -q'", None),
        ("grep -q '&&' notes.txt", None),
    ],
)
def test_a_check_that_cannot_judge_the_work_is_refused(check: str, problem: str | None) -> None:
    found = _module()._check_problem(check)

    assert found is None if problem is None else problem in found


@pytest.mark.anyio
async def test_founding_seeds_milestones_from_criteria_when_every_one_is_setup(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    project = tmp_path / "project"
    project.mkdir()
    monkeypatch.chdir(project)
    (fake_beagle / "add.out").write_text("T0001  Implement interval tree clocks\n")
    runtime, _ = _bound(tmp_path)
    long = "Every public function of the itc package has a docstring and a test " * 2
    args = {
        "statement": "Implement interval tree clocks",
        "criteria": ["`python3 -m pytest -q` exits 0", long.strip(), "set up beagle"],
        "user_confirmed": True,
    }

    # Only with every criterion setup too is nothing written.
    named = await _tool(runtime, "pursuit_found").execute(
        "c1",
        {
            **args,
            "criteria": ["set up beagle"],
            "milestones": ["configure beagle::doctor and skills.toml"],
        },
    )

    assert "nothing written" in named.text and "'configure beagle'" in named.text
    assert _calls(fake_beagle) == [] and not (project / ".beagle").exists()

    # With every milestone a setup one, the criteria become the milestones.
    setup = await _tool(runtime, "pursuit_found").execute(
        "c2", {**args, "milestones": ["setup", "init project"]}
    )

    assert "Founded the pursuit" in setup.text
    assert "Dropped the setup milestone 'setup', 'init project'" in setup.text
    assert "one per criterion" in setup.text
    module = _module()
    [split] = _pursuit_calls(fake_beagle, "split")
    assert split == [
        "T0001",
        "`python3 -m pytest -q` exits 0::`python3 -m pytest -q` exits 0",
        f"{module._task_title(long)}::{long.strip()}",
        "--ordered",
    ]
    assert all(len(p.split("::")[0]) <= module.MAX_TASK_TITLE for p in split[1:-1])

    assert _module()._setup_milestone(["package layout::pyproject.toml and src/"]) is None
    # Run 11 wrote `title: purpose`, and the purpose's words hid the title.
    run_11 = "setup beagle pursuit: configure gates, cadences, skills, and dispatch"
    assert _module()._setup_milestone([run_11]) is not None


R07_FOUND = {
    "statement": (
        "Implement interval tree clocks — a logical clock for dynamic distributed systems "
        "where cluster membership changes constantly — in modern Python, per the 2008 ACM "
        "paper by Almeida, Baquero and Fonte and the ferd.ca reference notes."
    ),
    "criteria": [
        "The package imports and exposes the interval tree clock API (create, join, leave, "
        "tick, send, receive, compare, merge) and the underlying interval tree data structure."
    ],
    "milestones": [
        "setup::Beagle pursuit setup and modern Python toolchain (uv/ruff/pytest) per "
        "python-coding skill"
    ],
}


@pytest.mark.anyio
async def test_r07_setup_only_milestone_founds_from_its_criterion(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # R07: mimo's only milestone was setup; founding refused it twelve times
    # and the breaker ended the run at 44 s.
    project = tmp_path / "project"
    project.mkdir()
    monkeypatch.chdir(project)
    (fake_beagle / "add.out").write_text("T0001  Implement interval tree clocks\n")
    runtime, _ = _bound(tmp_path, ui=False)
    found = _tool(runtime, "pursuit_found")

    asked = await found.execute("c1", {**R07_FOUND, "user_confirmed": False})

    assert "nothing written —" not in asked.text
    assert "print mode" in asked.text and "user_delegated=true" in asked.text
    assert "one per criterion" in asked.text
    assert _calls(fake_beagle) == [] and not (project / ".beagle").exists()

    founded = await found.execute("c2", {**R07_FOUND, "user_delegated": True})

    assert "Founded the pursuit" in founded.text
    assert "Dropped the setup milestone 'setup'" in founded.text
    [criterion] = R07_FOUND["criteria"]
    title = _module()._task_title(criterion)
    adds = _pursuit_calls(fake_beagle, "add")
    assert adds[1:] == [[title, "--parent", "T0001", "--intent", criterion]]
    assert _pursuit_calls(fake_beagle, "split") == []


@pytest.mark.anyio
async def test_found_drops_setup_milestone_and_says_so(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Run R03's driver was refused for a `setup::` first milestone and sent
    # the same call fourteen times; founding drops it instead.
    project = tmp_path / "project"
    project.mkdir()
    monkeypatch.chdir(project)
    (fake_beagle / "add.out").write_text("T0001  Implement interval tree clocks\n")
    runtime, _ = _bound(tmp_path)

    result = await _tool(runtime, "pursuit_found").execute(
        "c1",
        {
            "statement": "Implement interval tree clocks",
            "criteria": ["`python3 -m pytest -q` exits 0"],
            "milestones": ["setup::project layout for beagle", "reference::", "impl::itc.py"],
            "user_confirmed": True,
        },
    )

    assert "Founded the pursuit" in result.text
    assert "Dropped the setup milestone 'setup'" in result.text
    assert _pursuit_calls(fake_beagle, "split") == [
        ["T0001", "reference::", "impl::itc.py", "--ordered"]
    ]


@pytest.mark.anyio
async def test_founding_drops_a_rerun_only_milestone_with_a_note(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    project = tmp_path / "project"
    project.mkdir()
    monkeypatch.chdir(project)
    (fake_beagle / "add.out").write_text("T0001  Implement interval tree clocks\n")
    runtime, _ = _bound(tmp_path)

    result = await _tool(runtime, "pursuit_found").execute(
        "c1",
        {
            "statement": "Implement interval tree clocks",
            "criteria": ["`python3 -m pytest -q` exits 0"],
            "milestones": [
                "reference::",
                "Run all tests and confirm they pass",
                "impl::itc.py",
                "tests::tests/test_itc.py",
            ],
            "user_confirmed": True,
        },
    )

    assert "Founded the pursuit" in result.text
    assert "Dropped a milestone: 'Run all tests and confirm they pass' only re-runs" in result.text
    assert _pursuit_calls(fake_beagle, "split") == [
        ["T0001", "reference::", "impl::itc.py", "tests::tests/test_itc.py", "--ordered"]
    ]


R10_MILESTONES = [
    "Setup beagle pursuit infrastructure - configure project for beagle workflows",
    "Read and understand reference materials - analyze the ITC2008 paper and ferd.ca notes",
    "Design the interval tree clock architecture - plan data structures and operations",
    "Implement core clock operations - create, increment, merge, and compare clocks",
    "Implement dynamic node management - join, leave, and key space subdivision",
    "Write comprehensive tests - cover all operations and edge cases",
]


def test_setup_milestone_titled_with_a_dash_and_naming_beagle_is_dropped() -> None:
    # R10: the title ran on past ' - ', and 'infrastructure' hid it from the
    # all-setup-words rule; every later task waited on it.
    setup = _module()._setup_milestone
    assert setup([R10_MILESTONES[0]]) is not None
    assert setup(["Configure the pursuit — gates and cadences"]) is not None
    assert setup(["M1::Setup beagle pursuit infrastructure"]) is not None
    assert (
        setup(["Implement core clock operations - create, increment, merge, and compare clocks"])
        is None
    )
    assert setup(["Set up the project layout"]) is None
    assert setup(["Implement the beagle exporter - write the output files"]) is None
    assert setup(["Implement the beagle exporter - configure its output paths"]) is None


@pytest.mark.anyio
async def test_founding_r10_milestones_drops_only_the_setup_one(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    project = tmp_path / "project"
    project.mkdir()
    monkeypatch.chdir(project)
    (fake_beagle / "add.out").write_text("T0001  Implement interval tree clocks\n")
    runtime, _ = _bound(tmp_path)

    result = await _tool(runtime, "pursuit_found").execute(
        "c1",
        {
            "statement": "Implement interval tree clocks",
            "criteria": ["`python3 -m pytest -q` exits 0"],
            "milestones": R10_MILESTONES,
            "user_confirmed": True,
        },
    )

    assert "Founded the pursuit" in result.text
    assert f"Dropped the setup milestone {R10_MILESTONES[0]!r}" in result.text
    [split] = _pursuit_calls(fake_beagle, "split")
    assert split[0] == "T0001" and split[-1] == "--ordered"
    kept = split[1:-1]
    assert len(kept) == 5
    for milestone, part in zip(R10_MILESTONES[1:], kept, strict=True):
        assert milestone in part
    assert not any("beagle" in part for part in kept)


@pytest.mark.anyio
async def test_founding_milestone_with_a_bare_label_takes_its_title_from_the_intent(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Run R09 founded with milestones 'M1::…'..'M4::…', titled 'M1'..'M4'.
    project = tmp_path / "project"
    project.mkdir()
    monkeypatch.chdir(project)
    (fake_beagle / "add.out").write_text("T0001  Implement interval tree clocks\n")
    runtime, _ = _bound(tmp_path)

    result = await _tool(runtime, "pursuit_found").execute(
        "c1",
        {
            "statement": "Implement interval tree clocks",
            "criteria": ["`python3 -m pytest -q` exits 0"],
            "milestones": [
                "M1::Read the paper and extract the operations",
                "Parser::reads input",
            ],
            "user_confirmed": True,
        },
    )

    assert "Founded the pursuit" in result.text
    split = _pursuit_calls(fake_beagle, "split")
    assert len(split) == 1
    title, sep, intent = split[0][1].partition("::")
    assert title.startswith("Read the paper")
    assert sep and intent == "Read the paper and extract the operations"
    assert split[0][2] == "Parser::reads input"


@pytest.mark.anyio
async def test_plan_part_with_a_bare_label_takes_its_title_from_the_intent(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Run R09 planned 'P1::…'..'P5::…', and commits read "T0009: P4".
    monkeypatch.chdir(_pursuit_project(tmp_path))
    runtime, _ = _bound(tmp_path)

    await _tool(runtime, "pursuit_plan").execute(
        "c1", {"task": "T0001", "parts": ["P4::Move the code to src/itc"]}
    )

    assert _pursuit_calls(fake_beagle, "add") == [
        ["Move the code to src/itc", "--parent", "T0001", "--intent", "Move the code to src/itc"]
    ]


@pytest.mark.anyio
async def test_founding_drops_a_criterion_about_beagle_setup_with_a_note(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Run R09 kept this criterion, and a step then named .beagle/ in scope.
    project = tmp_path / "project"
    project.mkdir()
    monkeypatch.chdir(project)
    (fake_beagle / "add.out").write_text("T0001  Implement interval tree clocks\n")
    runtime, _ = _bound(tmp_path)
    setup = "Packaged as a Beagle Pursuit project (.beagle/ present, tracked)"

    result = await _tool(runtime, "pursuit_found").execute(
        "c1",
        {
            "statement": "Implement interval tree clocks",
            "criteria": ["`python3 -m pytest -q` exits 0", setup],
            "milestones": ["impl::itc.py"],
            "user_confirmed": True,
        },
    )

    assert "Founded the pursuit" in result.text
    assert f"Dropped the setup criterion {setup!r}" in result.text
    goal = (project / ".beagle" / "pursuit.toml").read_text()
    assert "exits 0" in goal and "Packaged as" not in goal


@pytest.mark.anyio
async def test_planning_refuses_a_setup_part_and_a_step_its_store_scope(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(_pursuit_project(tmp_path))
    _ready_task(fake_beagle)
    runtime, _ = _bound(tmp_path)

    plan = await _tool(runtime, "pursuit_plan").execute(
        "c1", {"task": "T0001", "parts": ["project setup", "impl"]}
    )
    step = await _tool(runtime, "pursuit_step").execute(
        "c2",
        {
            "task": "T0002",
            "criteria": "beagle is configured",
            "done_when": "python3 -m pytest -q",
            "scope": [".beagle/"],
        },
    )

    assert "nothing added" in plan.text and "'project setup'" in plan.text
    assert "not opened" in step.text and "scope names .beagle/" in step.text
    assert _pursuit_calls(fake_beagle, "split") == []
    assert _pursuit_calls(fake_beagle, "open") == []


@pytest.mark.anyio
async def test_plan_refuses_a_part_that_only_reruns_a_check(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # R09 class 2b: P5 had nothing to change; the check runs at every close.
    monkeypatch.chdir(_pursuit_project(tmp_path))
    _ready_task(fake_beagle)
    runtime, _ = _bound(tmp_path)

    plan = await _tool(runtime, "pursuit_plan").execute(
        "c1",
        {
            "task": "T0001",
            "parts": [
                "P4::Move the code into src/itc",
                "P5::Re-run the case-data test and confirm exit 0",
            ],
        },
    )

    assert "nothing added" in plan.text and "'P5'" in plan.text
    assert "must change something" in plan.text and "every close" in plan.text
    assert "'P4'" not in plan.text
    assert _pursuit_calls(fake_beagle, "split") == []
    assert _pursuit_calls(fake_beagle, "add") == []


@pytest.mark.anyio
async def test_plan_accepts_a_part_that_verifies_by_writing_a_test(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(_pursuit_project(tmp_path))
    _ready_task(fake_beagle)
    (fake_beagle / "split.out").write_text("T0001 split into 2:\n  T0009  Join\n  T0010  Test\n")
    runtime, _ = _bound(tmp_path)
    parts = [
        "Join::implement join of two stamps",
        "Test::Add a test that verifies join restores the seed",
    ]

    plan = await _tool(runtime, "pursuit_plan").execute("c1", {"task": "T0001", "parts": parts})

    assert "nothing added" not in plan.text and "only re-runs" not in plan.text
    calls = _pursuit_calls(fake_beagle, "split") + _pursuit_calls(fake_beagle, "add")
    assert calls and calls[0][1:3] == parts
    assert _module()._rerun_only_part(["Verify::confirm the tests pass"]) is not None
    assert _module()._rerun_only_part(["Check::check the stamp is normalised"]) is None


def _split_open_task_with_cases(tmp_path: Path, fake_beagle: Path, *, commit: bool) -> Path:
    project = _pursuit_project(tmp_path)
    _git(project, "init", "-q")
    (project / "tests").mkdir()
    (project / "tests" / "cases.json").write_text("[]\n")
    (project / "notes.txt").write_text("outside the scope\n")
    if commit:
        _git(project, "add", "tests/cases.json", "notes.txt")
        _git(project, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "seed")
    record = {
        "id": "T0007",
        "title": "Cases",
        "status": "open",
        "scope": ["tests/", "src/itc"],
        "done_when": "pytest -q",
    }
    (fake_beagle / "show.out").write_text(json.dumps(record))
    (fake_beagle / "split.out").write_text("T0007 split into 2:\n  T0008  Data\n  T0009  Code\n")
    return project


@pytest.mark.anyio
async def test_plan_names_uncommitted_files_in_the_split_tasks_scope(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # R09 class 4b: T0007 was split with tests/cases.json uncommitted, and
    # T0009's commit took it beside src/itc/*.py, unlocked.
    monkeypatch.chdir(_split_open_task_with_cases(tmp_path, fake_beagle, commit=False))
    runtime, _ = _bound(tmp_path)

    plan = await _tool(runtime, "pursuit_plan").execute(
        "c1", {"task": "T0007", "parts": ["Data::write the cases", "Code::the clock"]}
    )

    assert "beagle refused" not in plan.text
    assert "Uncommitted in T0007's scope: tests/cases.json." in plan.text
    assert "with locks when it is data" in plan.text
    assert "a later part's commit" in plan.text
    assert "notes.txt" not in plan.text
    assert _pursuit_calls(fake_beagle, "split")


@pytest.mark.anyio
async def test_plan_says_nothing_of_a_clean_scope(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(_split_open_task_with_cases(tmp_path, fake_beagle, commit=True))
    runtime, _ = _bound(tmp_path)

    plan = await _tool(runtime, "pursuit_plan").execute(
        "c1", {"task": "T0007", "parts": ["Data::write the cases", "Code::the clock"]}
    )

    assert "beagle refused" not in plan.text and _pursuit_calls(fake_beagle, "split")
    assert "Uncommitted" not in plan.text


FAKE_BEAGLE_GIT_COMMIT = """\
import os, subprocess, sys
argv = sys.argv[1:]
if argv[:2] == ["pursuit", "commit"]:
    paths = argv[3 : argv.index("--subject")]
    subject = argv[argv.index("--subject") + 1]
    subprocess.run(["git", "add", "--", *paths], check=True)
    subprocess.run(["git", "commit", "-q", "-m", subject, "--", *paths], check=True)
    with open(os.path.join(os.environ["FAKE_BEAGLE_DIR"], "commit.out"), "w") as out:
        out.write(f"{argv[2]}: committed {len(paths)} file(s): {subject}\\n")
"""


def _split_with_a_check_that_last_exited(
    tmp_path: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch, exit_status: int
) -> tuple[Path, Any]:
    """T0007 open over tests/ with tests/test_x.py uncommitted; the pending plan's result."""
    project = _split_open_task_with_cases(tmp_path, fake_beagle, commit=True)
    (project / "tests" / "test_x.py").write_text("def test_x():\n    assert True\n")
    script = fake_beagle / "beagle"
    script.write_text(
        f"#!{sys.executable}\n{FAKE_BEAGLE_GIT_COMMIT}{FAKE_BEAGLE}", encoding="utf-8"
    )
    for var in ("GIT_AUTHOR", "GIT_COMMITTER"):
        monkeypatch.setenv(f"{var}_NAME", "t")
        monkeypatch.setenv(f"{var}_EMAIL", "t@t")
    monkeypatch.chdir(project)
    runtime, _ = _bound(tmp_path)
    _loaded_module()._LAST_CHECK_EXIT[(str(project), "T0007")] = exit_status
    plan = _tool(runtime, "pursuit_plan").execute(
        "c1", {"task": "T0007", "parts": ["Data::write the cases", "Code::the clock"]}
    )
    return project, plan


@pytest.mark.anyio
async def test_split_commits_passing_uncommitted_work_before_the_parts(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # R12 class 4: test_comprehensive.py passed under T0007 and was left to the
    # last part, so the workspace-clean gate stayed red for every part before it.
    project, pending = _split_with_a_check_that_last_exited(tmp_path, fake_beagle, monkeypatch, 0)
    plan = await pending

    assert "beagle refused" not in plan.text
    assert "was committed as 'T0007: work in progress before split'" in plan.text
    assert "tests/test_x.py" in plan.text
    assert "Give each to the part" not in plan.text
    assert _git(project, "status", "--porcelain", "--untracked-files=all", "--", "tests") == ""
    assert _git(project, "log", "-1", "--format=%s") == "T0007: work in progress before split\n"
    verbs = [c["argv"][1] for c in _calls(fake_beagle) if c["argv"][0] == "pursuit"]
    assert verbs.index("commit") < verbs.index("split")
    [commit] = _pursuit_calls(fake_beagle, "commit")
    assert commit[:2] == ["T0007", "tests/test_x.py"]


@pytest.mark.anyio
async def test_split_keeps_the_note_for_uncommitted_work_whose_check_failed(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    project, pending = _split_with_a_check_that_last_exited(tmp_path, fake_beagle, monkeypatch, 1)
    plan = await pending

    assert "beagle refused" not in plan.text and _pursuit_calls(fake_beagle, "split")
    assert "Uncommitted in T0007's scope: tests/test_x.py. Give each to the part" in plan.text
    assert "work in progress before split" not in plan.text
    assert _pursuit_calls(fake_beagle, "commit") == []
    assert "?? tests/test_x.py" in _git(project, "status", "--porcelain", "-uall")


R08_SCOPE = ["itc/tests/cases.json", "itc/tests/test_cases.py", "itc/interval_tree_clocks.py"]


@pytest.mark.anyio
async def test_step_refuses_a_scope_mixing_known_answer_data_with_source(
    tmp_path: Path,
    beagle: Path,
    fake_beagle: Path,
    fake_tau: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    project = _pursuit_project(tmp_path)
    monkeypatch.chdir(project)
    _ready_task(fake_beagle)
    runtime, _ = _bound(tmp_path)
    arguments = {
        "task": "T0002",
        "criteria": "the clocks pass the cases",
        "done_when": "grep -q done done.txt",
        "scope": R08_SCOPE,
    }

    refused = await _tool(runtime, "pursuit_step").execute("c1", arguments)

    assert "not opened" in refused.text
    assert "itc/tests/cases.json" in refused.text
    assert "itc/interval_tree_clocks.py" in refused.text
    assert "locks=[itc/tests/cases.json]" in refused.text and "later task" in refused.text
    assert _pursuit_calls(fake_beagle, "open") == []
    assert _runs(fake_tau) == []

    # Locked by an earlier task, the data is restored before every check.
    store = project / ".beagle" / "locked" / "itc" / "tests"
    store.mkdir(parents=True)
    (store / "cases.json").write_text("[]")
    passed = await _tool(runtime, "pursuit_step").execute("c2", arguments)

    assert "known-answer data" not in passed.text
    assert len(_pursuit_calls(fake_beagle, "open")) == 1


def _r09_project(tmp_path: Path) -> Path:
    project = _pursuit_project(tmp_path)
    (project / "src" / "itc").mkdir(parents=True)
    (project / "src" / "itc" / "clock.py").write_text("")
    (project / "tests").mkdir(exist_ok=True)
    (project / "tests" / "cases.json").write_text("[]")
    return project


@pytest.mark.anyio
async def test_step_refuses_directory_scopes_holding_unlocked_data_and_source(
    tmp_path: Path,
    beagle: Path,
    fake_beagle: Path,
    fake_tau: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    project = _r09_project(tmp_path)
    monkeypatch.chdir(project)
    _ready_task(fake_beagle)
    runtime, _ = _bound(tmp_path)
    arguments = {
        "task": "T0002",
        "criteria": "the clocks pass the cases",
        "done_when": "grep -q done done.txt",
        "scope": ["src/", "tests/"],
    }

    refused = await _tool(runtime, "pursuit_step").execute("c1", arguments)

    assert "not opened" in refused.text
    assert "tests/cases.json" in refused.text
    assert "src/itc/clock.py" in refused.text
    assert _pursuit_calls(fake_beagle, "open") == []
    assert _runs(fake_tau) == []

    store = project / ".beagle" / "locked" / "tests"
    store.mkdir(parents=True)
    (store / "cases.json").write_text("[]")
    passed = await _tool(runtime, "pursuit_step").execute("c2", arguments)

    assert "known-answer data" not in passed.text
    assert len(_pursuit_calls(fake_beagle, "open")) == 1


def _r12_project(tmp_path: Path, *, references: bool = True) -> Path:
    project = _pursuit_project(tmp_path)
    if references:
        (project / "references").mkdir()
        (project / "references" / "itc2008.txt").write_text("Interval Tree Clocks\n")
    return project


def _lock_cases_test(project: Path, imports: str) -> None:
    store = project / ".beagle" / "locked" / "tests"
    store.mkdir(parents=True)
    (store / "cases.json").write_text("[]")
    (store / "test_cases.py").write_text(f"import json\n\nimport pytest\n\n{imports}\n")


def _open_args(scope: list[str]) -> dict[str, Any]:
    return {
        "task": "T0002",
        "criteria": "the clocks pass the cases",
        "done_when": "grep -q done done.txt",
        "scope": scope,
    }


@pytest.mark.anyio
async def test_opening_a_new_source_module_before_a_locked_cases_test_is_refused(
    tmp_path: Path,
    beagle: Path,
    fake_beagle: Path,
    fake_tau: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # R12's T0004: scope src/, with no cases locked yet.
    project = _r12_project(tmp_path)
    monkeypatch.chdir(project)
    _ready_task(fake_beagle)
    runtime, _ = _bound(tmp_path)

    refused = await _tool(runtime, "pursuit_step").execute("c1", _open_args(["src/"]))

    assert "not opened" in refused.text and "Cases first" in refused.text
    assert "known-answers milestone" in refused.text
    assert 'pursuit_plan task="T0002" parts=["Known answers::' in refused.text
    assert '"Parser::the code, judged by the locked cases"' in refused.text
    assert _pursuit_calls(fake_beagle, "open") == []
    assert _runs(fake_tau) == []

    # A locked test imports another module: it is named, to scope instead.
    _lock_cases_test(project, "from itc import Stamp")
    other = await _tool(runtime, "pursuit_step").execute(
        "c2", _open_args(["src/interval_tree_clock.py"])
    )

    assert "Cases first" in other.text and "src/interval_tree_clock.py" in other.text
    assert "imports `itc`" in other.text and "in this task's scope instead" in other.text
    assert _pursuit_calls(fake_beagle, "open") == []

    # The known-answers task itself, data and tests only, is never gated.
    cases = await _tool(runtime, "pursuit_step").execute(
        "c3", _open_args(["tests/cases.json", "tests/test_cases.py"])
    )

    assert "Cases first" not in cases.text
    assert len(_pursuit_calls(fake_beagle, "open")) == 1


@pytest.mark.anyio
async def test_opening_the_module_a_locked_cases_test_imports_is_allowed(
    tmp_path: Path,
    beagle: Path,
    fake_beagle: Path,
    fake_tau: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    project = _r12_project(tmp_path)
    _git(project, "init", "-q")
    (project / "src").mkdir()
    (project / "src" / "old.py").write_text("")
    _git(project, "add", "src/old.py")
    _git(project, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "seed")
    _lock_cases_test(project, "import interval_tree_clock")
    monkeypatch.chdir(project)
    _ready_task(fake_beagle)
    runtime, _ = _bound(tmp_path)

    opened = await _tool(runtime, "pursuit_step").execute(
        "c1", _open_args(["src/interval_tree_clock.py"])
    )

    assert "Cases first" not in opened.text
    assert len(_pursuit_calls(fake_beagle, "open")) == 1

    # A file already at HEAD is no new module, and docs are no module at all.
    module = _module()
    goal = project / ".beagle" / "pursuit.toml"
    assert module._cases_first_problem(["src/old.py", "docs/"], "T0002", "Parser", goal) is None
    found = module._cases_first_problem(["src/itc/"], "T0002", "Parser", goal)
    assert found is not None and "imports `interval_tree_clock`" in found


@pytest.mark.anyio
async def test_cases_first_gate_is_off_without_references(
    tmp_path: Path,
    beagle: Path,
    fake_beagle: Path,
    fake_tau: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    project = _r12_project(tmp_path, references=False)
    monkeypatch.chdir(project)
    _ready_task(fake_beagle)
    runtime, _ = _bound(tmp_path)

    opened = await _tool(runtime, "pursuit_step").execute("c1", _open_args(["src/"]))

    assert "Cases first" not in opened.text
    assert len(_pursuit_calls(fake_beagle, "open")) == 1


def test_key_only_json_done_when_is_refused() -> None:
    module = _module()
    # R12's T0002 done_when (E11), read from its record.
    r12 = (
        "python3 -c \"import json; data=json.load(open('reference-summary.json')); "
        "assert 'title' in data and 'abstract' in data and 'core_concepts' in data "
        "and 'operations' in data\""
    )
    every = (
        "python3 -c \"import json; cases=json.load(open('tests/cases.json')); "
        "assert all('expected' in c for c in cases)\""
    )
    values = (
        "python3 -c \"import json; data=json.load(open('tests/cases.json')); "
        "assert data[0]['expected'] == [1, 0]\""
    )

    for check in (r12, every):
        found = module._check_problem(check)
        assert found is not None and "a key check passes on any content" in found
        assert "compares values to the reference" in found
    assert module._check_problem(values) is None


def test_scope_dir_walk_skips_cache_directories(tmp_path: Path) -> None:
    (tmp_path / "pkg" / "src").mkdir(parents=True)
    (tmp_path / "pkg" / "src" / "x.py").write_text("")
    cache = tmp_path / "pkg" / ".pytest_cache" / "v" / "cache"
    cache.mkdir(parents=True)
    (cache / "lastfailed").write_text("{}")

    assert _module()._scope_dir_files(tmp_path, "pkg") == ["pkg/src/x.py"]


@pytest.mark.anyio
async def test_step_accepts_a_source_directory_alone(
    tmp_path: Path,
    beagle: Path,
    fake_beagle: Path,
    fake_tau: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    project = _r09_project(tmp_path)
    monkeypatch.chdir(project)
    _ready_task(fake_beagle)
    runtime, _ = _bound(tmp_path)
    arguments = {
        "task": "T0002",
        "criteria": "the clocks tick",
        "done_when": "grep -q done done.txt",
        "scope": ["src/"],
    }

    passed = await _tool(runtime, "pursuit_step").execute("c1", arguments)

    assert "known-answer data" not in passed.text
    assert len(_pursuit_calls(fake_beagle, "open")) == 1


R08_IMPORT = 'python3 -c "from itc.interval_tree_clocks import IntervalTreeClock"'


@pytest.mark.anyio
async def test_check_importing_a_module_outside_scope_and_disk_is_refused(
    tmp_path: Path,
    beagle: Path,
    fake_beagle: Path,
    fake_tau: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    project = _pursuit_project(tmp_path)
    (project / "itc" / "src").mkdir(parents=True)
    scope = ["itc/src/interval_tree_clocks.py"]
    found = _module()._import_scope_problem(R08_IMPORT, scope, project)
    assert found is not None and "itc/interval_tree_clocks.py" in found
    assert "in scope" in found and "change the import" in found
    wrapped = f"bash -c '{R08_IMPORT}'"
    assert _module()._import_scope_problem(wrapped, scope, project) is not None

    monkeypatch.chdir(project)
    _ready_task(fake_beagle)
    runtime, _ = _bound(tmp_path)
    refused = await _tool(runtime, "pursuit_step").execute(
        "c1",
        {
            "task": "T0002",
            "criteria": "the clock is importable",
            "done_when": R08_IMPORT[:-1] + '; assert IntervalTreeClock().fork()"',
            "scope": scope,
        },
    )

    assert "not opened" in refused.text and "itc/interval_tree_clocks.py" in refused.text
    assert "only imports" not in refused.text
    assert _pursuit_calls(fake_beagle, "open") == []
    assert _runs(fake_tau) == []


def test_check_importing_stdlib_or_an_existing_module_is_accepted(tmp_path: Path) -> None:
    (tmp_path / "itc" / "src").mkdir(parents=True)
    (tmp_path / "itc" / "src" / "clocks.py").write_text("")
    problem = _module()._import_scope_problem
    scope = ["itc/interval_tree_clocks.py"]

    assert problem('python3 -c "import json, os.path"', [], tmp_path) is None
    assert problem(R08_IMPORT, scope, tmp_path) is None
    assert problem(R08_IMPORT, ["itc/"], tmp_path) is None
    assert problem('python3 -c "from itc.src.clocks import Clock"', [], tmp_path) is None
    assert problem('python3 -c "from itc.src import clocks"', [], tmp_path) is None
    assert problem("python3 -c 'import (('", [], tmp_path) is None
    assert problem("python3 -m pytest -q", [], tmp_path) is None


@pytest.mark.anyio
async def test_step_accepts_known_answer_data_with_its_tests_only(
    tmp_path: Path,
    beagle: Path,
    fake_beagle: Path,
    fake_tau: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(_pursuit_project(tmp_path))
    _ready_task(fake_beagle)
    runtime, _ = _bound(tmp_path)

    result = await _tool(runtime, "pursuit_step").execute(
        "c1",
        {
            "task": "T0002",
            "criteria": "the cases are written",
            "done_when": "grep -q done done.txt",
            "scope": ["itc/tests/cases.json", "itc/tests/test_cases.py"],
        },
    )

    assert "known-answer data" not in result.text
    assert len(_pursuit_calls(fake_beagle, "open")) == 1


@pytest.mark.anyio
async def test_pursuit_step_drops_a_setup_task_instead_of_working_it(
    tmp_path: Path,
    beagle: Path,
    fake_beagle: Path,
    fake_tau: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Run 11's setup milestone got past founding, and every check the driver
    # wrote for it ran beagle or read .beagle/, so each was refused.
    monkeypatch.chdir(_pursuit_project(tmp_path))
    _ready_task(fake_beagle)
    setup = {"id": "T0002", "title": "setup beagle pursuit", "status": "pending"}
    (fake_beagle / "show.out").write_text(json.dumps(setup))
    (fake_beagle / "close.out").write_text("T0002 abandoned\n")
    runtime, _ = _bound(tmp_path)

    result = await _tool(runtime, "pursuit_step").execute("c1", {})

    assert _pursuit_calls(fake_beagle, "close") == [
        ["T0002", "--outcome", "abandoned", "--reason", "founding set the pursuit up"]
    ]
    assert _pursuit_calls(fake_beagle, "open") == [] and _runs(fake_tau) == []
    assert "pursuit_found already did" in result.text
    assert "call pursuit_step with no arguments" in result.text


def _blocked_task(fake: Path, **record: Any) -> None:
    """T0002, closed as done but refused by its own check: nothing is ready."""
    (fake / "next.out").write_text(json.dumps({"open": [], "ready": [], "ready_total": 0}))
    blocked = {
        "id": "T0002",
        "title": "Parser",
        "intent": "reads input",
        "status": "blocked",
        "criteria": "the parser reads input",
        "done_when": "grep -q done done.txt",
        "scope": ["src/parser.py"],
        "check_refused": "exit 1",
        "reason": "closed as done, but `grep -q done done.txt` exit 1",
        "retries": 0,
        **record,
    }
    (fake / "show-T0002.out").write_text(json.dumps(blocked))
    nodes = [{"id": "T0001", "status": "pending", "container": True}, blocked]
    (fake / "tree.out").write_text(json.dumps({"goal": "Ship it", "nodes": nodes}))


@pytest.mark.anyio
async def test_pursuit_step_offers_the_routes_for_a_blocked_task(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(_pursuit_project(tmp_path))
    _blocked_task(fake_beagle)
    runtime, _ = _bound(tmp_path)

    result = await _tool(runtime, "pursuit_step").execute("c1", {})

    assert "Nothing is ready" in result.text and "- T0002 — Parser" in result.text
    assert "new_route=true" in result.text and "beagle pursuit" not in result.text


@pytest.mark.anyio
async def test_pursuit_step_reworks_a_blocked_task_and_retries_it(
    tmp_path: Path,
    beagle: Path,
    fake_beagle: Path,
    fake_tau: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(_pursuit_project(tmp_path))
    _blocked_task(fake_beagle)
    runtime, _ = _bound(tmp_path)

    result = await _tool(runtime, "pursuit_step").execute(
        "c1", {"task": "T0002", "notes": "the parser never wrote done.txt"}
    )

    [run] = _runs(fake_tau)
    # beagle briefs only an open task; this one is briefed from its record.
    assert "refused it" in run["stdin"] and "the parser never wrote done.txt" in run["stdin"]
    assert _pursuit_calls(fake_beagle, "brief") == []
    [retry] = _pursuit_calls(fake_beagle, "retry")
    assert retry[0] == "T0002" and "--because" in retry and "--spent" in retry
    assert _pursuit_calls(fake_beagle, "close") == [] == _pursuit_calls(fake_beagle, "spawn")
    assert "T0002 — Parser: closed done" in result.text


@pytest.mark.anyio
async def test_pursuit_step_retries_a_blocked_task_whose_check_now_passes(
    tmp_path: Path,
    beagle: Path,
    fake_beagle: Path,
    fake_tau: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    project = _pursuit_project(tmp_path)
    monkeypatch.chdir(project)
    _blocked_task(fake_beagle)
    (project / "done.txt").write_text("done under another task")
    runtime, _ = _bound(tmp_path)

    await _tool(runtime, "pursuit_step").execute("c1", {"task": "T0002"})

    assert _runs(fake_tau) == []
    [retry] = _pursuit_calls(fake_beagle, "retry")
    assert retry[retry.index("--spent") + 1] == "0" and "--spent-because" in retry


@pytest.mark.anyio
async def test_pursuit_step_spawns_a_new_route_for_a_blocked_task(
    tmp_path: Path,
    beagle: Path,
    fake_beagle: Path,
    fake_tau: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(_pursuit_project(tmp_path))
    # Run 8's T0003: bound to a grep of its own task file, which no rework fixes.
    _blocked_task(fake_beagle, done_when="grep -q parser .beagle/tree/T0002.md")
    successor = {"id": "T0003", "title": "Parser", "status": "pending", "done_when": ""}
    (fake_beagle / "show-T0003.out").write_text(json.dumps(successor))
    (fake_beagle / "spawn.out").write_text("T0002 superseded by T0003\n")
    (fake_beagle / "brief.out").write_text("# T0003: Parser\n")
    runtime, _ = _bound(tmp_path)
    step = _tool(runtime, "pursuit_step")
    new_check = {"task": "T0002", "done_when": "grep -q done done.txt"}

    no_notes = await step.execute("c1", new_check)
    no_check = await step.execute("c0", {"task": "T0002", "notes": "x"})
    new_end = await step.execute("c2", {**new_check, "notes": "x", "criteria": "it parses"})
    result = await step.execute("c3", {**new_check, "notes": "check the file it writes"})

    assert "needs notes" in no_notes.text and "keeps the criteria" in new_end.text
    # Not retried on the grep, and no successor left behind with it.
    assert "cannot judge the work" in no_check.text and "reads .beagle/" in no_check.text
    [spawn] = _pursuit_calls(fake_beagle, "spawn")
    assert spawn[0] == "T0002" and "--check-defect" in spawn
    assert spawn[spawn.index("--approach-delta") + 1] == "check the file it writes"
    [opened] = _pursuit_calls(fake_beagle, "open")
    assert opened[0] == "T0003"
    assert opened[opened.index("--criteria") + 1] == "the parser reads input"
    assert opened[opened.index("--done-when") + 1] == "grep -q done done.txt"
    assert opened[opened.index("--scope") + 1] == "src/parser.py"
    [close] = _pursuit_calls(fake_beagle, "close")
    assert close[0] == "T0003" and _pursuit_calls(fake_beagle, "retry") == []
    assert "superseded by T0003" in result.text and "T0003 — Parser: closed done" in result.text


@pytest.mark.anyio
async def test_pursuit_step_spawns_from_a_blocked_task_out_of_retries(
    tmp_path: Path,
    beagle: Path,
    fake_beagle: Path,
    fake_tau: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(_pursuit_project(tmp_path))
    _blocked_task(fake_beagle, retries=3)
    (fake_beagle / "spawn.out").write_text("T0002 superseded by T0003\n")
    runtime, _ = _bound(tmp_path)

    await _tool(runtime, "pursuit_step").execute("c1", {"task": "T0002", "notes": "smaller"})

    [spawn] = _pursuit_calls(fake_beagle, "spawn")
    assert "--check-defect" not in spawn and _pursuit_calls(fake_beagle, "retry") == []


@pytest.mark.anyio
async def test_driving_session_edits_only_the_pursuit_store(
    tmp_path: Path, beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    project = _pursuit_project(tmp_path)
    monkeypatch.chdir(project)
    runtime, session = _bound(tmp_path)
    write = _tool_with_hooks(runtime, "write")
    before_start = await write.execute("c0", {"path": "src/app.py", "content": "x"})
    await runtime.emit_session_start("startup")

    blocked = await write.execute("c1", {"path": "src/app.py", "content": "x"})
    store = await write.execute("c2", {"path": ".beagle/notes.md", "content": "x"})
    session.session_id = "subagent-session"  # an in-process subagent's own runtime
    subagent = await write.execute("c3", {"path": "src/app.py", "content": "x"})
    session.session_id = "session-1"
    monkeypatch.setenv("BEAGLE_TAU_DRIVER_EDITS", "1")
    opted_out = await write.execute("c4", {"path": "src/app.py", "content": "x"})

    assert "from the driving session" in blocked.text and "pursuit_step" in blocked.text
    assert "the pursuit tools own .beagle/" in store.text
    assert [before_start.text, subagent.text, opted_out.text] == ["ran"] * 3


@pytest.mark.anyio
async def test_driver_write_or_edit_under_dot_beagle_is_refused(
    tmp_path: Path, beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Run 10, E45: the driver's own edit of gates.toml left it failing to load.
    project = _pursuit_project(tmp_path)
    monkeypatch.chdir(project)
    runtime, session = _bound(tmp_path)
    edit = _tool_with_hooks(runtime, "edit")
    write = _tool_with_hooks(runtime, "write")
    await runtime.emit_session_start("startup")
    gate_edit = {
        "path": ".beagle/gates.toml",
        "edits": [{"oldText": 'name = "prose-volume"', "newText": 'name = "ruff"'}],
    }

    edited = await edit.execute("c1", gate_edit)
    written = await write.execute("c2", {"path": str(project / ".beagle" / "skills.toml")})
    session.session_id = "subagent-session"
    worker = await edit.execute("c3", gate_edit)

    for refused in (edited, written):
        assert "the pursuit tools own .beagle/" in refused.text
        assert "pursuit_step" in refused.text
    assert worker.text == "ran"


@pytest.mark.anyio
async def test_driver_bash_writing_dot_beagle_toml_is_refused(
    tmp_path: Path, beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Run 10, E45 as a shell edit: the ruff gate appended to gates.toml by hand.
    monkeypatch.chdir(_pursuit_project(tmp_path))
    runtime, _ = _bound(tmp_path)
    bash = _tool_with_hooks(runtime, "bash")
    await runtime.emit_session_start("startup")
    commands = [
        "cat >> .beagle/gates.toml <<'EOF'\n[[gate]]\nname = \"ruff\"\n"
        'command = "ruff check src/ || true"\nEOF',
        "printf '[[gate]]\\n' > .beagle/gates.toml",
        "echo '[[gate]]' | tee -a .beagle/gates.toml",
        "sed -i 's/prose-volume/ruff/' .beagle/gates.toml",
        "cp /tmp/gates.toml .beagle/gates.toml",
        "mv /tmp/gates.toml .beagle/",
        "python3 -c \"open('.beagle/gates.toml', 'a').write('[[gate]]')\"",
        "python3 - <<'EOF'\nimport tomllib\nopen('.beagle/skills.toml', 'w')\nEOF",
    ]

    for i, command in enumerate(commands):
        refused = await bash.execute(f"c{i}", {"command": command})
        assert "the pursuit tools own .beagle/" in refused.text, command
        assert "pursuit_step" in refused.text


@pytest.mark.anyio
async def test_driver_reading_dot_beagle_is_allowed(
    tmp_path: Path, beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(_pursuit_project(tmp_path))
    runtime, _ = _bound(tmp_path)
    bash = _tool_with_hooks(runtime, "bash")
    read = _tool_with_hooks(runtime, "read")
    await runtime.emit_session_start("startup")
    commands = [
        "cat .beagle/gates.toml",
        "ls .beagle",
        "beagle pursuit status",
        'grep -q "ruff" .beagle/gates.toml && echo "OK" || echo "FAIL"',
        "grep -A5 ruff .beagle/gates.toml 2>&1 | head -5 > /tmp/out",
        "cp .beagle/gates.toml /tmp/gates.toml",
    ]

    ran = [(await bash.execute(f"c{i}", {"command": c})).text for i, c in enumerate(commands)]
    ran.append((await read.execute("r", {"path": ".beagle/gates.toml"})).text)

    assert ran == ["ran"] * (len(commands) + 1)


@pytest.mark.anyio
async def test_driver_non_pursuit_streak_after_founding_is_refused(
    tmp_path: Path, beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Run 10: 59 calls after founding, 4 of them pursuit_step.
    monkeypatch.chdir(_pursuit_project(tmp_path))
    runtime, session = _bound(tmp_path)
    read = _tool_with_hooks(runtime, "read")
    step = _tool(runtime, "pursuit_step")
    await runtime.emit_session_start("startup")
    limit = _loaded_module().DRIVER_OFF_PURSUIT_CALLS
    assert limit == 8

    allowed = [(await read.execute(f"a{i}", {"path": "README"})).text for i in range(limit)]
    ninth = await read.execute("a9", {"path": "README"})
    tenth = await read.execute("a10", {"path": "README"})
    stepped = await step.execute("s1", {"task": "T0002"})
    after_step = await read.execute("b1", {"path": "README"})
    session.session_id = "subagent-session"
    worker = [(await read.execute(f"w{i}", {"path": "README"})).text for i in range(limit + 2)]
    session.session_id = "session-1"
    await runtime.emit_session_start("startup")
    restarted = [(await read.execute(f"n{i}", {"path": "README"})).text for i in range(limit)]

    assert allowed == ["ran"] * limit
    assert "9 tool calls in a row" in ninth.text and "pursuit_step" in ninth.text
    assert "10 tool calls in a row" in tenth.text
    assert "Tool call blocked" not in stepped.text and after_step.text == "ran"
    assert worker == ["ran"] * (limit + 2)
    assert restarted == ["ran"] * limit


@pytest.mark.anyio
async def test_driving_session_spawns_no_sub_agent_of_its_own(
    tmp_path: Path, beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Run 10: refused its own writes, the driver had an `agent` sub-agent,
    # whose session the edit guard does not hold, write the file instead.
    monkeypatch.chdir(_pursuit_project(tmp_path))
    runtime, session = _bound(tmp_path)
    agent = _tool_with_hooks(runtime, "agent")
    await runtime.emit_session_start("startup")

    blocked = await agent.execute("c1", {"prompt": "Write tests/test_gate.py"})
    session.session_id = "subagent-session"
    nested = await agent.execute("c2", {"prompt": "Write tests/test_gate.py"})

    assert "refusing to spawn a sub-agent" in blocked.text and "pursuit_step" in blocked.text
    assert nested.text == "ran"


@pytest.mark.parametrize(
    ("command", "found"),
    [
        # What the run 9 driver did to the project through bash.
        ("sed -i 's/a/b/' interval_tree_clocks.py", "change interval_tree_clocks.py"),
        ("cat > justfile << 'EOF'\ntest:\n\tpytest\nEOF", "change justfile"),
        ("git add justfile && git status", "run `git add`"),
        ("git -C . commit -m wip", "run `git commit`"),
        ("ruff check . --fix", "run `ruff check . --fix`, whose `--fix` flag"),
        ("uv run ruff format .", "run `ruff format .`"),
        (
            "python3 << 'EOF'\nwith open('x.py', 'w') as f:\n    f.write('')\nEOF",
            "run a python3 script that writes files",
        ),
        ("python3 -c \"open('x.py','a').write('')\"", "run a python3 script that writes"),
        # Reading, running, and what is not the project's work.
        ("ruff check .", None),
        ("uv run pytest tests/ -v 2>&1 | head -50", None),
        ("python3 -c \"print(open('x.py').read())\"", None),
        ("git status --short && git log --oneline", None),
        ("rm -rf __pycache__ tests/__pycache__ .pytest_cache", None),
        ("python3 -m pytest -q > /tmp/out.txt", None),
        ("cat .beagle/notes.txt", None),
    ],
)
@pytest.mark.anyio
async def test_driving_session_changes_no_project_file_through_bash(
    tmp_path: Path, beagle: Path, monkeypatch: pytest.MonkeyPatch, command: str, found: str | None
) -> None:
    project = _pursuit_project(tmp_path)
    monkeypatch.chdir(project)
    runtime, session = _bound(tmp_path)
    bash = _tool_with_hooks(runtime, "bash")
    await runtime.emit_session_start("startup")

    result = await bash.execute("c1", {"command": command})
    session.session_id = "subagent-session"
    worker = await bash.execute("c2", {"command": command})

    if found is None:
        assert result.text == "ran"
    else:
        assert f"refusing to {found}" in result.text and "pursuit_plan" in result.text
    assert worker.text == "ran"


@pytest.mark.parametrize(
    ("command", "found"),
    [
        ("git reset --hard 781924a", "reset --hard"),
        ("cd sub && git -C .. reset --keep HEAD~1", "reset --hard"),
        ("git clean -xdf", "clean"),
        ("git checkout -- .", "checkout ."),
        ("git stash", "stash"),
        ("git commit --amend --no-edit", "commit --amend"),
        ("git push -f origin main", "push --force"),
        ("bash -c 'git rebase -i HEAD~3'", "rebase"),
        ("git status --short && git diff", None),
        ("git reset HEAD greet.py", None),
        ("git restore greet.py", None),
        ("git stash list", None),
        ("git rebase --abort", None),
        ("echo 'git reset --hard'", None),
    ],
)
@pytest.mark.anyio
async def test_history_guard_names_what_discards_work(
    tmp_path: Path, beagle: Path, command: str, found: str | None
) -> None:
    _pursuit_project(tmp_path)
    runtime, _ = _bound(tmp_path)

    result = await _tool_with_hooks(runtime, "bash").execute("c1", {"command": command})

    if found is None:
        assert result.text == "ran"
    else:
        assert f"refusing `git {found}` in a pursuit" in result.text


@pytest.mark.anyio
async def test_history_guard_holds_every_session_in_a_pursuit(
    tmp_path: Path, beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    project = _pursuit_project(tmp_path)
    monkeypatch.chdir(project)
    runtime, session = _bound(tmp_path)
    bash = _tool_with_hooks(runtime, "bash")

    blocked = await bash.execute("c1", {"command": "git reset --hard 781924a"})
    session.session_id = "subagent-session"
    worker = await bash.execute("c2", {"command": "git clean -fd"})
    fine = await bash.execute("c3", {"command": "git rm --cached -r __pycache__"})
    (tmp_path / "bare" / "project").mkdir(parents=True)
    bare, _ = _bound(tmp_path / "bare")  # a project with no pursuit
    unfounded = await _tool_with_hooks(bare, "bash").execute("c4", {"command": "git stash"})

    assert "refusing `git reset --hard`" in blocked.text and "Fix forward" in blocked.text
    assert "refusing `git clean`" in worker.text
    assert [fine.text, unfounded.text] == ["ran"] * 2


@pytest.mark.parametrize(
    ("command", "verb"),
    [
        ("beagle pursuit close T0003 --done", "close"),
        ("beagle pursuit open T0004", "open"),
        ("beagle --root /p pursuit add 'Next piece'", "add"),
        ("cd /p && bash -c 'beagle pursuit retry T0002'", "retry"),
        ("BEAGLE_ROOT=/p beagle pursuit split T0003 a b", "split"),
        ("beagle pursuit brief T0003", None),
        ("beagle pursuit show T0003 && beagle pursuit tree", None),
        ("beagle --root /p pursuit status", None),
        ("beagle doctor", None),
        ("echo 'beagle pursuit close T0003'", None),
    ],
)
@pytest.mark.anyio
async def test_a_worker_may_read_the_pursuit_but_not_change_it(
    tmp_path: Path,
    beagle: Path,
    monkeypatch: pytest.MonkeyPatch,
    command: str,
    verb: str | None,
) -> None:
    monkeypatch.setenv("BEAGLE_TAU_WORKER", "1")
    runtime, _ = _bound(tmp_path)

    result = await _tool_with_hooks(runtime, "bash").execute("c1", {"command": command})

    if verb is None:
        assert result.text == "ran"
    else:
        assert f"refusing to run `beagle pursuit {verb}` in a sub-agent" in result.text


@pytest.mark.parametrize(
    ("command", "tool"),
    [
        # Run 8's driver, steering T0002 and T0003 by hand.
        ("cd /home/choong/itc && beagle pursuit spawn T0002", "new_route=true"),
        ('beagle pursuit retry T0002 --because "fixed"', "on the blocked task"),
        ("/home/u/.tau/beagle-plugin/bin/beagle pursuit close T0003 --outcome done", "closes"),
        ("beagle pursuit add --parent T0001 --sibling-of T0002 x", "pursuit_plan"),
        ("bash -c 'beagle pursuit split T0003 a b'", "pursuit_plan"),
        ("beagle pursuit show T0003 && beagle pursuit tree", None),
        ("beagle pursuit retire T0002 --reason 'not part of the goal'", None),
    ],
)
@pytest.mark.anyio
async def test_the_driver_steers_through_its_tools_not_bash_verbs(
    tmp_path: Path,
    beagle: Path,
    monkeypatch: pytest.MonkeyPatch,
    command: str,
    tool: str | None,
) -> None:
    monkeypatch.chdir(_pursuit_project(tmp_path))
    runtime, _ = _bound(tmp_path)
    bash = _tool_with_hooks(runtime, "bash")
    await runtime.emit_session_start("startup")

    result = await bash.execute("c1", {"command": command})
    monkeypatch.setenv("BEAGLE_TAU_DRIVER_EDITS", "1")
    opted_out = await bash.execute("c2", {"command": command})

    if tool is None:
        assert result.text == "ran"
    else:
        assert "refusing `beagle pursuit" in result.text and tool in result.text
    assert opted_out.text == "ran"


@pytest.mark.anyio
async def test_the_driver_runs_pursuit_verbs_outside_a_pursuit(
    tmp_path: Path, beagle: Path
) -> None:
    runtime, _ = _bound(tmp_path)
    await runtime.emit_session_start("startup")

    result = await _tool_with_hooks(runtime, "bash").execute(
        "c1", {"command": "beagle pursuit open T0004"}
    )

    assert result.text == "ran"


@pytest.mark.parametrize(
    ("tool", "arguments", "refused"),
    [
        # Run 8's driver, rewriting a check into the task file and the log.
        (
            "bash",
            {"command": "sed -i '/^done_when/a metric_command = x' .beagle/tree/T0002.md"},
            "tree/T0002.md",
        ),
        (
            "bash",
            {"command": "sed -i '/^metric/d' .beagle/log/000000-000499/000007-note.md"},
            "log/000000-000499/000007-note.md",
        ),
        ("write", {"path": ".beagle/state.json", "content": "{}"}, "state.json"),
        ("edit", {"path": ".beagle/locked/tests/cases.json"}, "locked/tests/cases.json"),
        ("bash", {"command": "cat >> .beagle/skills.toml << 'EOF'\n[x]\nEOF"}, None),
        ("bash", {"command": "cat .beagle/tree/T0002.md > notes.md"}, None),
        ("write", {"path": ".beagle/notes.md", "content": "x"}, None),
    ],
)
@pytest.mark.anyio
async def test_no_session_writes_beagles_records(
    tmp_path: Path,
    beagle: Path,
    monkeypatch: pytest.MonkeyPatch,
    tool: str,
    arguments: dict[str, Any],
    refused: str | None,
) -> None:
    monkeypatch.chdir(_pursuit_project(tmp_path))
    monkeypatch.setenv("BEAGLE_TAU_WORKER", "1")  # a worker too, not only the driver
    runtime, _ = _bound(tmp_path)

    result = await _tool_with_hooks(runtime, tool).execute("c1", arguments)

    if refused is None:
        assert result.text == "ran"
    else:
        assert f"refusing to change .beagle/{refused}" in result.text


def test_the_memory_cap_wraps_a_command_in_a_systemd_scope(
    beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    ext = _module()
    monkeypatch.setattr(ext, "_scopes_work", lambda: True)
    monkeypatch.setenv("BEAGLE_TAU_MEMORY_MAX", "2G")
    capped = ext._capped(["pytest", "-q"], ext._memory_max())
    monkeypatch.setenv("BEAGLE_TAU_MEMORY_MAX", "off")
    off = ext._memory_max()
    monkeypatch.setattr(ext, "_scopes_work", lambda: False)
    monkeypatch.setenv("BEAGLE_TAU_MEMORY_MAX", "2G")
    unavailable = ext._memory_max()

    assert capped[:4] == ["systemd-run", "--user", "--scope", "-q"]
    assert "MemoryMax=2G" in capped and "MemorySwapMax=0" in capped
    assert capped[-3:] == ["--", "pytest", "-q"]
    assert off is None and unavailable is None
    assert ext._capped(["pytest"], None) == ["pytest"]


@pytest.mark.anyio
async def test_a_check_over_the_memory_cap_is_killed_and_says_why(
    tmp_path: Path, beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    ext = _module()
    if not ext._scopes_work():
        pytest.skip("no systemd user scopes here")
    monkeypatch.setenv("BEAGLE_TAU_MEMORY_MAX", "64M")
    hog = f"{sys.executable} -c 'x = bytearray(512 << 20); print(len(x))'"

    rc, out = await ext._run_check(hog, tmp_path, timeout=60)
    monkeypatch.setenv("BEAGLE_TAU_MEMORY_MAX", "1G")
    ok_rc, ok_out = await ext._run_check(hog, tmp_path, timeout=60)

    assert rc == -9 and "64M memory cap" in out
    assert (ok_rc, ok_out) == (0, str(512 << 20))


@pytest.mark.anyio
async def test_a_long_goal_statement_is_cut_to_a_root_task_title(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # beagle refuses a title over 200 characters; the statement is not one.
    project = tmp_path / "project"
    project.mkdir()
    monkeypatch.chdir(project)
    (fake_beagle / "add.out").write_text("T0001  Implement\n")
    runtime, _ = _bound(tmp_path)
    statement = "Implement interval tree clocks " + "in modern Python " * 20

    await _tool(runtime, "pursuit_found").execute(
        "c1",
        {
            "statement": statement,
            "criteria": ["`uv run pytest` exits 0"],
            "milestones": ["Core::fork, join, event"],
            "user_delegated": True,
        },
    )

    [add] = [c["argv"] for c in _calls(fake_beagle) if c["argv"][:2] == ["pursuit", "add"]][:1]
    title = add[2]
    assert len(title) <= 200 and title.endswith("…")
    assert add[add.index("--intent") + 1] == statement.strip()


# -- R01: a founded driver steps, and leaves references to its workers ---------


@pytest.mark.anyio
async def test_founded_driver_dispatch_refused(
    tmp_path: Path,
    beagle: Path,
    fake_beagle: Path,
    fake_tau: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # R01: founded, the 9B driver dispatched twice instead of stepping, and
    # neither dispatch opened or closed a task.
    monkeypatch.chdir(_pursuit_project(tmp_path))
    (fake_beagle / "next.out").write_text(json.dumps({"open": [], "ready": ["T0003"]}))
    runtime, _ = _bound(tmp_path)

    result = await _tool(runtime, "pursuit_dispatch").execute(
        "c1", {"brief": "Implement the interval tree clock"}
    )

    assert _runs(fake_tau) == []
    assert "refused, nothing was spawned" in result.text
    assert "pursuit_step with task=T0003" in result.text


@pytest.mark.anyio
async def test_unfounded_dispatch_runs(
    tmp_path: Path, beagle: Path, fake_tau: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    project = tmp_path / "project"
    project.mkdir()
    monkeypatch.chdir(project)
    runtime, _ = _bound(tmp_path)

    result = await _tool(runtime, "pursuit_dispatch").execute("c1", {"brief": "Write notes"})

    assert len(_runs(fake_tau)) == 1
    assert "[pursuit_dispatch] step-executor" in result.text and "refused" not in result.text


@pytest.mark.anyio
async def test_founded_driver_reference_read_refused(
    tmp_path: Path, beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    project = _pursuit_project(tmp_path)
    monkeypatch.chdir(project)
    paper = tmp_path / "refs" / "itc.pdf"
    runtime, session = _bound(tmp_path)
    bash, read = _tool_with_hooks(runtime, "bash"), _tool_with_hooks(runtime, "read")
    fetch = _tool_with_hooks(runtime, "web_fetch")
    await runtime.emit_session_start("startup")

    refused = [
        await bash.execute("c1", {"command": "curl -sL https://example.org/itc.pdf -o itc.pdf"}),
        await bash.execute("c2", {"command": "cd /tmp && wget http://example.org/itc"}),
        await bash.execute(
            "c3", {"command": "python3 -c 'import urllib.request as u; u.urlopen(\"https://x\")'"}
        ),
        await bash.execute(
            "c4", {"command": "python3 - <<'EOF'\nimport requests\nrequests.get('https://x')\nEOF"}
        ),
        await read.execute("c5", {"path": str(paper)}),
        await read.execute("c6", {"path": "../refs/itc.pdf"}),
        await fetch.execute("c7", {"url": "https://example.org/itc"}),
    ]
    _loaded_module()._OFF_PURSUIT_CALLS = 0  # these calls pin other guards, not the streak
    allowed = [
        await read.execute("c8", {"path": "src/itc.py"}),
        await read.execute("c9", {"path": str(project / ".beagle" / "pursuit.toml")}),
        await read.execute("c10", {"path": str(beagle / "plugins")}),
        await read.execute("c11", {"path": str(tmp_path / "agents" / "x.md")}),
        await bash.execute("c12", {"command": "curl --version && echo https://x"}),
        await bash.execute("c13", {"command": "uv run pytest -q"}),
    ]
    session.session_id = "subagent-session"  # an in-process subagent's own runtime
    nested = await read.execute("c14", {"path": str(paper)})
    session.session_id = "session-1"
    monkeypatch.setenv("BEAGLE_TAU_DRIVER_EDITS", "1")
    opted_out = await read.execute("c15", {"path": str(paper)})

    for result in refused:
        assert "from the driving session" in result.text
        assert "references are read by the worker that a pursuit_step dispatches" in result.text
    assert [r.text for r in allowed] == ["ran"] * len(allowed)
    assert [nested.text, opted_out.text] == ["ran"] * 2


@pytest.mark.anyio
async def test_worker_reference_read_allowed(
    tmp_path: Path, beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(_pursuit_project(tmp_path))
    monkeypatch.setenv("BEAGLE_TAU_WORKER", "1")
    runtime, _ = _bound(tmp_path)
    await runtime.emit_session_start("startup")

    fetched = await _tool_with_hooks(runtime, "bash").execute(
        "c1", {"command": "curl -sL https://example.org/itc.pdf -o itc.pdf"}
    )
    read = await _tool_with_hooks(runtime, "read").execute(
        "c2", {"path": str(tmp_path / "refs" / "itc.pdf")}
    )

    assert [fetched.text, read.text] == ["ran"] * 2


@pytest.mark.anyio
async def test_unfounded_driver_may_fetch_references(
    tmp_path: Path, beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    project = tmp_path / "project"
    project.mkdir()
    monkeypatch.chdir(project)
    runtime, _ = _bound(tmp_path)
    await runtime.emit_session_start("startup")

    fetched = await _tool_with_hooks(runtime, "bash").execute(
        "c1", {"command": "curl -sL https://example.org/itc.pdf"}
    )
    read = await _tool_with_hooks(runtime, "read").execute(
        "c2", {"path": str(tmp_path / "refs" / "itc.pdf")}
    )

    assert [fetched.text, read.text] == ["ran"] * 2


# -- R01: workers stop by turn count, with a bounded timeout and thinking off --


@pytest.mark.anyio
async def test_worker_argv_caps_turns(
    tmp_path: Path, beagle: Path, fake_tau: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # R01: two 9B workers ran 43 and 51 turns into the kill and handed back nothing.
    project = tmp_path / "project"
    project.mkdir()
    monkeypatch.chdir(project)
    monkeypatch.delenv("BEAGLE_TAU_WORKER_MAX_TURNS", raising=False)
    runtime, _ = _bound(tmp_path)
    dispatch = _tool(runtime, "pursuit_dispatch")

    await dispatch.execute("c1", {"brief": "Write notes"})
    monkeypatch.setenv("BEAGLE_TAU_WORKER_MAX_TURNS", "12")
    await dispatch.execute("c2", {"brief": "Write notes"})

    default, pinned = (run["argv"] for run in _runs(fake_tau))
    assert default[default.index("--max-turns") + 1] == "30"
    assert pinned[pinned.index("--max-turns") + 1] == "12"


@pytest.mark.anyio
async def test_worker_argv_thinking_off(
    tmp_path: Path, beagle: Path, fake_tau: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    project = tmp_path / "project"
    project.mkdir()
    monkeypatch.chdir(project)
    monkeypatch.delenv("BEAGLE_TAU_DISPATCH_THINKING", raising=False)
    runtime, _ = _bound(tmp_path)
    dispatch = _tool(runtime, "pursuit_dispatch")

    await dispatch.execute("c1", {"brief": "Write notes"})
    monkeypatch.setenv("BEAGLE_TAU_DISPATCH_THINKING", "low")
    await dispatch.execute("c2", {"brief": "Write notes"})

    default, pinned = (run["argv"] for run in _runs(fake_tau))
    assert default[default.index("--thinking") + 1] == "off"
    assert pinned[pinned.index("--thinking") + 1] == "low"


@pytest.mark.anyio
async def test_step_and_dispatch_timeout_clamped(
    tmp_path: Path,
    beagle: Path,
    fake_beagle: Path,
    fake_tau: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # R01: the driver raised a worker's timeout to 1800 s, which bought only a longer spiral.
    module = _module()
    timeout, note = module._worker_timeout(1800)
    assert timeout == module.DEFAULT_DISPATCH_TIMEOUT == 900.0
    assert "clamped to 900s" in note
    assert module._worker_timeout(300) == (300.0, "")
    assert module._worker_timeout(None) == (module.DEFAULT_DISPATCH_TIMEOUT, "")
    assert module._worker_timeout("soon") == (module.DEFAULT_DISPATCH_TIMEOUT, "")

    monkeypatch.chdir(_pursuit_project(tmp_path))
    _ready_task(fake_beagle)
    runtime, _ = _bound(tmp_path)
    stepped = await _tool(runtime, "pursuit_step").execute(
        "c1",
        {
            "task": "T0002",
            "criteria": "done.txt exists",
            "done_when": "grep -q done done.txt",
            "scope": ["done.txt"],
            "timeout": 3600,
        },
    )
    assert stepped.text.startswith("(timeout 3600s was clamped to 900s")
    assert "closed done" in stepped.text

    bare = tmp_path / "bare"
    bare.mkdir()
    dispatch = _tool(runtime, "pursuit_dispatch")
    dispatched = await dispatch.execute(
        "c2", {"brief": "Write notes", "cwd": str(bare), "timeout": 1800}
    )
    assert dispatched.text.startswith("(timeout 1800s was clamped to 900s")
    assert "[pursuit_dispatch] step-executor" in dispatched.text
    unclamped = await dispatch.execute(
        "c3", {"brief": "Write notes", "cwd": str(bare), "timeout": 600}
    )
    assert "clamped" not in unclamped.text


# --------------------------------------------------------------------------- #
# run R02: an unprovable task re-stepped, milestones abandoned, a stalled stop
# --------------------------------------------------------------------------- #


def _witnessed_pursuit(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    project = _git_project(tmp_path, monkeypatch)
    with (project / ".beagle" / "pursuit.toml").open("a", encoding="utf-8") as goal:
        goal.write('\n[close]\nrequire = "witness"\n')
    return project


@pytest.mark.anyio
async def test_unprovable_restep_spawns_no_worker(
    tmp_path: Path,
    beagle: Path,
    fake_beagle: Path,
    fake_tau: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # R02: T0003's scope held tests only, so `prove` had no source file to take
    # away; six steps sent two workers each at the same passing check.
    monkeypatch.chdir(_witnessed_pursuit(tmp_path, monkeypatch))
    _ready_task(fake_beagle)
    runtime, _ = _bound(tmp_path)
    step = _tool(runtime, "pursuit_step")
    args = {
        "task": "T0002",
        "criteria": "c",
        "done_when": "grep -q done done.txt",
        "scope": ["tests"],
    }

    first = await step.execute("c1", args)
    record = {"id": "T0002", "title": "Parser", "status": "open"}
    record |= {"done_when": "grep -q done done.txt", "scope": ["tests"]}
    (fake_beagle / "show.out").write_text(json.dumps(record))
    (fake_beagle / "next.out").write_text(json.dumps({"open": [{"id": "T0002"}], "ready": []}))
    again = await step.execute("c2", {"task": "T0002"})
    same = await step.execute("c3", {"task": "T0002", "done_when": "grep -q done done.txt"})

    assert len(_runs(fake_tau)) == 1
    assert "no defect could be put back" in first.text and "stays open" in first.text
    for refused in (again, same):
        assert "not run: this check already passes and cannot be shown to refuse" in refused.text
        # R12: a tests-only scope with no data file proves through the module it imports.
        assert "mutate the module the test imports" in refused.text
        assert "the data file's absence is the proof" not in refused.text
        assert "import the code" not in refused.text
    assert _pursuit_calls(fake_beagle, "close") == []


@pytest.mark.anyio
async def test_unprovable_first_verdict_stops_attempts(
    tmp_path: Path,
    beagle: Path,
    fake_beagle: Path,
    fake_tau: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # R02 ran the second worker of a step after its check already passed.
    monkeypatch.chdir(_git_project(tmp_path, monkeypatch))
    monkeypatch.setenv("FAKE_TAU_REPORT", WITNESSED_REPORT)
    _ready_task(fake_beagle)
    (fake_beagle / "prove.out").write_text("T0002: NOT PROVEN — src/clock.py is not there\n")
    (fake_beagle / "prove.rc").write_text("9")
    runtime, _ = _bound(tmp_path)

    result = await _tool(runtime, "pursuit_step").execute(
        "c1",
        {
            "task": "T0002",
            "criteria": "c",
            "done_when": "grep -q done done.txt",
            "scope": ["done.txt"],
            "attempts": 3,
        },
    )

    assert len(_runs(fake_tau)) == 1
    # One verdict: the witness, then the changed source taken away.
    assert [p[1] for p in _pursuit_calls(fake_beagle, "prove")] == ["--mutate", "--absent"]
    assert _pursuit_calls(fake_beagle, "close") == []
    assert "no defect could be put back" in result.text
    assert "must import the code this task tests" in result.text


def _milestones(fake: Path, *nodes: dict[str, Any]) -> None:
    """A tree: root T0001, milestone T0002 under it, and `nodes` besides."""
    tree = [
        {"id": "T0001", "parent": "", "title": "Goal", "status": "pending", "container": True},
        {"id": "T0002", "parent": "T0001", "title": "Clock", "status": "pending"},
        *nodes,
    ]
    (fake / "tree.out").write_text(json.dumps({"nodes": tree}))


@pytest.mark.anyio
async def test_abandon_already_done_refused(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # R02 abandoned four of five milestones as "already exists / passes".
    monkeypatch.chdir(_pursuit_project(tmp_path))
    _ready_task(fake_beagle)
    _milestones(fake_beagle, {"id": "T0003", "parent": "T0002", "status": "pending"})
    runtime, _ = _bound(tmp_path)
    step = _tool(runtime, "pursuit_step")

    done = await step.execute("c1", {"task": "T0003", "abandon": "already done"})
    unknown = await step.execute("c2", {"task": "T0003", "abandon": "duplicate of T0099"})

    assert _pursuit_calls(fake_beagle, "close") == []
    for refused in (done, unknown):
        assert "T0003 not abandoned" in refused.text
        assert "bind the goal criterion's test" in refused.text
    hint = _module().ABANDON_HINT
    assert "already done" not in hint and "duplicate of Tnnnn" in hint


@pytest.mark.anyio
async def test_abandon_duplicate_of_done_task_closes(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(_pursuit_project(tmp_path))
    _ready_task(fake_beagle)
    _milestones(
        fake_beagle,
        {"id": "T0003", "parent": "T0002", "status": "done"},
        # T0058: a container's part is refused; a superseded milestone's successor goes.
        {"id": "T0005", "parent": "T0001", "status": "superseded"},
        {"id": "T0004", "parent": "T0001", "status": "pending", "sibling_of": "T0005"},
    )
    (fake_beagle / "close.out").write_text("T0004 abandoned — duplicate of T0003\n")
    runtime, _ = _bound(tmp_path)

    result = await _tool(runtime, "pursuit_step").execute(
        "c1", {"task": "T0004", "abandon": "duplicate of T0003"}
    )

    assert _pursuit_calls(fake_beagle, "close") == [
        ["T0004", "--outcome", "abandoned", "--reason", "duplicate of T0003"]
    ]
    assert "T0004 abandoned" in result.text


@pytest.mark.anyio
async def test_abandon_milestone_refused(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(_pursuit_project(tmp_path))
    _ready_task(fake_beagle)
    _milestones(fake_beagle, {"id": "T0003", "parent": "T0001", "status": "done"})
    runtime, _ = _bound(tmp_path)

    result = await _tool(runtime, "pursuit_step").execute(
        "c1", {"task": "T0002", "abandon": "duplicate of T0003"}
    )

    assert _pursuit_calls(fake_beagle, "close") == []
    assert "T0002 not abandoned — it is a milestone" in result.text
    assert "pursuit_plan" in result.text and "new_route=true" in result.text


STALLED_TREE = [
    {"id": "T0001", "parent": "", "title": "Goal", "status": "pending", "container": True},
    {"id": "T0002", "parent": "T0001", "title": "Cases", "status": "done"},
    {
        "id": "T0003",
        "parent": "T0001",
        "title": "Clock",
        "status": "abandoned",
        "reason": "already exists",
    },
    # Handed on: its successor holds the work.
    {"id": "T0004", "parent": "T0001", "title": "Old route", "status": "superseded"},
    {
        "id": "T0005",
        "parent": "T0001",
        "title": "New route",
        "status": "done",
        "sibling_of": "T0004",
    },
    {
        "id": "T0006",
        "parent": "T0001",
        "title": "Twin",
        "status": "abandoned",
        "reason": "duplicate of T0002",
    },
]


@pytest.mark.anyio
async def test_nothing_ready_with_stalled_root_says_not_done(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # R02 L107: "tell the user the pursuit is done", with the root stalled.
    monkeypatch.chdir(_pursuit_project(tmp_path))
    (fake_beagle / "next.out").write_text(json.dumps({"open": [], "ready": []}))
    (fake_beagle / "next.rc").write_text("3")
    (fake_beagle / "tree.out").write_text(json.dumps({"nodes": STALLED_TREE}))
    runtime, _ = _bound(tmp_path)

    result = await _tool(runtime, "pursuit_step").execute("c1", {})

    assert "The pursuit is NOT done" in result.text
    assert "tell the user the pursuit is done" not in result.text
    assert "- T0003 — Clock (abandoned: already exists)" in result.text
    for settled in ("T0004 —", "T0005 —", "T0006 —"):
        assert settled not in result.text.split("NOT done", 1)[1]


#: Run R06's tree after L73, cut down: T0003 waits on T0002, superseded by
#: T0008, and the driver's bash `depend` made T0008 wait on T0003.
CYCLE_TREE: list[dict[str, Any]] = [
    {"id": "T0001", "parent": "", "title": "ITC", "status": "pending", "container": True},
    {"id": "T0002", "parent": "T0001", "title": "Reference study", "status": "superseded"},
    {
        "id": "T0003",
        "parent": "T0001",
        "title": "Design",
        "status": "pending",
        "container": True,
        "waiting_on": ["T0002"],
    },
    {"id": "T0012", "parent": "T0003", "title": "Plan structure", "status": "pending"},
    {
        "id": "T0004",
        "parent": "T0001",
        "title": "Impl",
        "status": "pending",
        "waiting_on": ["T0003"],
    },
    {
        "id": "T0008",
        "parent": "T0001",
        "title": "Reference study",
        "status": "pending",
        "container": True,
        "sibling_of": "T0002",
        "waiting_on": ["T0003"],
    },
    {"id": "T0009", "parent": "T0008", "title": "Read the paper", "status": "pending"},
]


def _nothing_ready(fake: Path, nodes: list[dict[str, Any]]) -> None:
    (fake / "next.out").write_text(json.dumps({"open": [], "ready": []}))
    (fake / "next.rc").write_text("3")
    (fake / "tree.out").write_text(json.dumps({"nodes": nodes}))


@pytest.mark.anyio
async def test_driver_guard_steers_a_hard_depend_to_the_tools(
    tmp_path: Path, beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # R06 L72: the driver's bash `depend T0008 --hard T0003` closed the cycle.
    monkeypatch.chdir(_pursuit_project(tmp_path))
    runtime, _ = _bound(tmp_path)
    bash = _tool_with_hooks(runtime, "bash")
    await runtime.emit_session_start("startup")

    hard = await bash.execute("c1", {"command": "beagle pursuit depend T0008 --hard T0003"})
    soft = await bash.execute(
        "c2", {"command": "cd /x && beagle pursuit depend T0004 T0003 --reason 'order'"}
    )
    drop = await bash.execute(
        "c3", {"command": 'beagle pursuit depend T0008 T0003 --drop --reason "breaks it"'}
    )

    for added in (hard.text, soft.text):
        assert "refusing `beagle pursuit depend`" in added
        assert "pursuit_step with no arguments" in added and "--drop" in added
    assert drop.text == "ran"


@pytest.mark.anyio
async def test_step_names_the_drop_for_a_cycle_when_nothing_is_ready(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # R06 L77-L169: every step said "Nothing is ready" and offered plan or
    # new_route; the one call that broke the cycle was never named.
    monkeypatch.chdir(_pursuit_project(tmp_path))
    _nothing_ready(fake_beagle, CYCLE_TREE)
    runtime, _ = _bound(tmp_path)
    step = _tool(runtime, "pursuit_step")

    bare = await step.execute("c1", {})
    named = await step.execute("c2", {"task": "T0003"})

    for text in (bare.text, named.text):
        assert "Nothing is ready" in text and "form a cycle" in text
        assert "- T0003 waits on T0002 (superseded, handed to T0008: pending)" in text
        assert "- T0008 waits on T0003 (pending)" in text
        # The edge the driver added, not the plan's order through the heir.
        assert 'beagle pursuit depend T0008 T0003 --drop --reason "breaks the cycle' in text
        assert "beagle pursuit depend T0003 T0002" not in text
        assert "pursuit_plan" not in text and "new_route" not in text
        assert "new route" not in text
    assert _pursuit_calls(fake_beagle, "depend") == []


@pytest.mark.anyio
async def test_nothing_ready_names_each_blocking_edge(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # R06 L77: the nothing-ready text listed no task's wait. Each unfinished
    # task names what holds it, a part through the container that waits.
    monkeypatch.chdir(_pursuit_project(tmp_path))
    no_cycle = [{**n, "waiting_on": []} if n["id"] == "T0008" else n for n in CYCLE_TREE]
    lines = {
        "T0012": "- T0012 — Plan structure (pending); waits on T0002 (superseded, handed "
        "to T0008: pending) through T0003",
        "T0004": "- T0004 — Impl (pending); waits on T0003 (pending)",
    }
    for nodes, waits_on_t0003 in ((CYCLE_TREE, True), (no_cycle, False)):
        _nothing_ready(fake_beagle, nodes)
        runtime, _ = _bound(tmp_path)

        text = (await _tool(runtime, "pursuit_step").execute("c1", {})).text
        listed = _module()._unfinished(nodes)

        assert lines["T0012"] in listed and lines["T0004"] in listed
        t0009 = "- T0009 — Read the paper (pending)"
        assert (t0009 + "; waits on T0003 (pending) through T0008" in listed) is waits_on_t0003
        assert t0009 in "\n".join(listed)
        if waits_on_t0003:
            assert "form a cycle" in text
        else:
            assert "form a cycle" not in text and "The pursuit is NOT done" in text
            assert all(line in text for line in lines.values())


#: Run R08's tree at L99, cut down: T0007 waits on T0006, superseded by
#: T0011, a container stalled on two abandoned parts.
STALLED_HEIR_TREE: list[dict[str, Any]] = [
    {"id": "T0001", "parent": "", "title": "ITC", "status": "pending", "container": True},
    {
        "id": "T0004",
        "parent": "T0001",
        "title": "Impl",
        "status": "pending",
        "container": True,
        "subtree": "idle",
    },
    {"id": "T0006", "parent": "T0004", "title": "fix-id-usage", "status": "superseded"},
    {
        "id": "T0007",
        "parent": "T0004",
        "title": "implement-fill",
        "status": "pending",
        "waiting_on": ["T0006"],
        "waiting_heirs": {"T0006": "T0011"},
    },
    {
        "id": "T0011",
        "parent": "T0004",
        "title": "fix-id-usage",
        "status": "pending",
        "container": True,
        "subtree": "stalled",
        "sibling_of": "T0006",
    },
    {"id": "T0013", "parent": "T0011", "title": "fix-normalization", "status": "abandoned"},
    {"id": "T0014", "parent": "T0011", "title": "fix-grow", "status": "abandoned"},
    {"id": "T0015", "parent": "T0011", "title": "fix-event", "status": "done"},
]


@pytest.mark.anyio
async def test_abandon_releases_a_wait_routed_through_its_heir(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # R08 L306: abandoning T0011 left T0007's wait on T0006, handed to T0011.
    monkeypatch.chdir(_pursuit_project(tmp_path))
    _ready_task(fake_beagle)
    # T0058: abandoning a part of T0004 is refused, so T0006 and its heir
    # T0011 are lifted to milestones, where the successor may go.
    lifted = [
        {**n, "parent": "T0001"} if n["id"] in ("T0006", "T0011") else n for n in STALLED_HEIR_TREE
    ]
    (fake_beagle / "tree.out").write_text(json.dumps({"nodes": lifted}))
    (fake_beagle / "close.out").write_text("T0011 abandoned\n")
    runtime, _ = _bound(tmp_path)
    step = _tool(runtime, "pursuit_step")

    result = await step.execute("c1", {"task": "T0011", "abandon": "duplicate of T0015"})

    assert _pursuit_calls(fake_beagle, "close") == [
        ["T0011", "--outcome", "abandoned", "--reason", "duplicate of T0015"]
    ]
    assert _pursuit_calls(fake_beagle, "depend") == [
        ["T0007", "T0006", "--drop", "--reason", "T0011 abandoned: duplicate of T0015"]
    ]
    assert "No longer waiting on it: T0007." in result.text


@pytest.mark.anyio
async def test_duplicate_abandon_of_a_part_is_refused_because_it_stalls_its_container(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # R08: T0013 abandoned as a duplicate of done T0015 left T0011 stalled for good.
    monkeypatch.chdir(_pursuit_project(tmp_path))
    _ready_task(fake_beagle)
    tree = [
        {"id": "T0001", "parent": "", "title": "ITC", "status": "pending", "container": True},
        {"id": "T0004", "parent": "T0001", "title": "Impl", "status": "pending", "container": True},
        {"id": "T0011", "parent": "T0004", "title": "fix", "status": "pending", "container": True},
        {"id": "T0013", "parent": "T0011", "title": "fix-normalization", "status": "pending"},
        {"id": "T0015", "parent": "T0011", "title": "fix-event", "status": "done"},
    ]
    (fake_beagle / "tree.out").write_text(json.dumps({"nodes": tree}))
    runtime, _ = _bound(tmp_path)

    result = await _tool(runtime, "pursuit_step").execute(
        "c1", {"task": "T0013", "abandon": "duplicate of T0015"}
    )

    assert _pursuit_calls(fake_beagle, "close") == []
    assert "T0013 not abandoned" in result.text
    assert "T0011" in result.text and "stall" in result.text
    assert 'pursuit_step task="T0013"' in result.text and "done_when" in result.text


@pytest.mark.anyio
async def test_nothing_ready_names_the_drop_for_a_wait_on_a_stalled_heir(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # R08 L107: the text said "handed to T0011: pending" and offered plan or
    # new_route; `depend T0007 T0006 --drop` was never named.
    monkeypatch.chdir(_pursuit_project(tmp_path))
    abandoned = [
        {**n, "status": "abandoned"} if n["id"] == "T0011" else n for n in STALLED_HEIR_TREE
    ]
    live = [{**n, "subtree": "active"} if n["id"] == "T0011" else n for n in STALLED_HEIR_TREE]
    for nodes, state in ((STALLED_HEIR_TREE, "stalled"), (abandoned, "stalled"), (live, None)):
        _nothing_ready(fake_beagle, nodes)
        runtime, _ = _bound(tmp_path)

        text = (await _tool(runtime, "pursuit_step").execute("c1", {})).text

        assert "Nothing is ready" in text
        if state is None:
            assert "--drop" not in text and "can never be met" not in text
            assert "waits on T0006 (superseded, handed to T0011: pending)" in text
            continue
        assert "can never be met" in text
        assert f"- T0007 waits on T0006 (superseded, handed to T0011: {state})" in text
        assert "handed to T0011: pending" not in text
        assert (
            "beagle pursuit depend T0007 T0006 --drop --reason "
            f'"T0006 was handed to T0011, which is {state} and will never be done"'
        ) in text
        assert "pursuit_plan" not in text and "new_route" not in text
    assert _pursuit_calls(fake_beagle, "depend") == []


def _r08_shape(*parts: dict[str, Any]) -> list[dict[str, Any]]:
    """R08's frame: root T0001 holding containers, T0007 a part of non-root T0004."""
    return [
        {"id": "T0001", "parent": "", "title": "ITC", "status": "pending", "container": True},
        {
            "id": "T0002",
            "parent": "T0001",
            "title": "Design",
            "status": "done",
            "container": True,
            "subtree": "done",
        },
        {
            "id": "T0004",
            "parent": "T0001",
            "title": "Impl",
            "status": "pending",
            "container": True,
            "subtree": "idle",
        },
        *parts,
    ]


async def _assert_dead_wait_named(
    nodes: list[dict[str, Any]],
    wait: tuple[str, str, str],
    line: str,
    reason: str,
    tmp_path: Path,
    fake_beagle: Path,
) -> None:
    assert _module()._dead_waits(nodes) == [wait]
    _nothing_ready(fake_beagle, nodes)
    runtime, _ = _bound(tmp_path)

    text = (await _tool(runtime, "pursuit_step").execute("c1", {})).text

    assert "Nothing is ready" in text
    assert "can never be met" in text
    assert line in text
    assert f'beagle pursuit depend T0007 {wait[1]} --drop --reason "{reason}"' in text
    assert "The pursuit is NOT done" not in text
    assert _pursuit_calls(fake_beagle, "depend") == []


@pytest.mark.anyio
async def test_dead_wait_on_an_abandoned_leaf_in_r08_shape(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(_pursuit_project(tmp_path))
    nodes = _r08_shape(
        {
            "id": "T0007",
            "parent": "T0004",
            "title": "implement-fill",
            "status": "pending",
            "waiting_on": ["T0011"],
        },
        {"id": "T0011", "parent": "T0004", "title": "fix-id-usage", "status": "abandoned"},
    )
    await _assert_dead_wait_named(
        nodes,
        ("T0007", "T0011", "T0011"),
        "- T0007 waits on T0011 (abandoned)",
        "T0011 is abandoned and will never be done",
        tmp_path,
        fake_beagle,
    )


@pytest.mark.anyio
async def test_dead_wait_on_an_abandoned_non_container_heir_in_r08_shape(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(_pursuit_project(tmp_path))
    nodes = _r08_shape(
        {"id": "T0006", "parent": "T0004", "title": "fix-id-usage", "status": "superseded"},
        {
            "id": "T0007",
            "parent": "T0004",
            "title": "implement-fill",
            "status": "pending",
            "waiting_on": ["T0006"],
            "waiting_heirs": {"T0006": "T0011"},
        },
        {
            "id": "T0011",
            "parent": "T0004",
            "title": "fix-id-usage",
            "status": "abandoned",
            "sibling_of": "T0006",
        },
    )
    await _assert_dead_wait_named(
        nodes,
        ("T0007", "T0006", "T0011"),
        "- T0007 waits on T0006 (superseded, handed to T0011: abandoned)",
        "T0006 was handed to T0011, which is abandoned and will never be done",
        tmp_path,
        fake_beagle,
    )


def _say(text: str) -> list[Any]:
    from pi_event_helpers import assistant_done, assistant_start

    return [assistant_start(model="fake"), assistant_done(message=AssistantMessage(content=text))]


async def _print_run(tmp_path: Path, project: Path, stops: int) -> tuple[Any, bool]:
    from tau_ai import FakeProvider
    from tau_coding.cli import run_print_mode

    provider = FakeProvider([_say(f"complete {n}") for n in range(stops)])
    ok = await run_print_mode(
        prompt="Drive the pursuit.",
        model="fake",
        cwd=project,
        provider=provider,
        resource_paths=TauResourcePaths(root=tmp_path / "home-tau", agents_root=None),
        extension_paths=(EXTENSION,),
    )
    return provider, ok


def _sent(provider: Any) -> list[str]:
    """The user messages of each request after the first, past the prompt."""
    return [
        message.text
        for message in provider.calls[-1][2]
        if isinstance(message, UserMessage) and message.text.startswith("[beagle]")
    ]


@pytest.mark.anyio
async def test_print_mode_stop_gate_queues_followup_twice(
    tmp_path: Path,
    beagle: Path,
    fake_beagle: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    # R02 ended `tau -p` on "complete" with the root stalled: the Stop hooks
    # skip print mode. Through the real print-mode loop, each queued follow-up
    # is one more request, and the third stop goes through.
    project = _pursuit_project(tmp_path)
    (fake_beagle / "tree.out").write_text(json.dumps({"nodes": STALLED_TREE}))

    provider, ok = await _print_run(tmp_path, project, stops=4)

    assert ok is True
    assert len(provider.calls) == 3
    nudges = _sent(provider)
    assert len(nudges) == 2
    assert all("The pursuit is not done" in n and "- T0003 — Clock" in n for n in nudges)
    assert "complete 2" in capsys.readouterr().out


@pytest.mark.anyio
async def test_stop_gate_lets_a_finished_pursuit_and_a_worker_stop(
    tmp_path: Path,
    beagle: Path,
    fake_beagle: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    project = _pursuit_project(tmp_path)
    done = [{**node, "status": "done"} if node["id"] == "T0001" else node for node in STALLED_TREE]
    (fake_beagle / "tree.out").write_text(json.dumps({"nodes": done}))
    finished, _ = await _print_run(tmp_path, project, stops=2)
    leaves_done = [n for n in STALLED_TREE if n["id"] != "T0003"]
    (fake_beagle / "tree.out").write_text(json.dumps({"nodes": leaves_done}))
    all_leaves, _ = await _print_run(tmp_path, project, stops=2)
    (fake_beagle / "tree.out").write_text(json.dumps({"nodes": STALLED_TREE}))
    monkeypatch.setenv("BEAGLE_TAU_WORKER", "1")
    worker, _ = await _print_run(tmp_path, project, stops=2)

    assert len(finished.calls) == len(all_leaves.calls) == len(worker.calls) == 1


DELEGATING_PROMPT = (
    "set this project up for beagle pursuit, and then implement it. use your judgement "
    "to do the setup without further discussion."
)


def test_found_refusal_in_print_mode_quotes_the_prompt_and_leads_with_delegation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # R05: mimo took "ask the user to confirm" from a refusal whose delegation
    # branch came last, in `tau -p`, and the run ended after 18 s.
    module = _module()
    monkeypatch.setattr(module, "_LAST_PROMPT", DELEGATING_PROMPT + " x" * 400)
    text = module._unconfirmed_refusal("Build ITC", ["tests pass"], interactive=False)

    assert "print mode" in text and "without further discussion" in text
    assert text.index("user_delegated=true") < text.index("Goal: Build ITC")
    assert "Do not ask the user to confirm" in text and "- tests pass" in text
    assert len(text) < 1200 and "…" in text


R11_PROMPT = (
    "set this project up for beagle pursuit, and then implement a modern python (see "
    "skill) implementation of interval tree clocks. use your judgement to do the setup "
    "without further discussion, and use beagle's pursuit-run to structure and "
    "orchestrate the work."
)
UNDELEGATING_PROMPT = "set this project up for beagle pursuit and implement interval tree clocks."
UNFLAGGED_FOUND = {
    "statement": "Build ITC",
    "criteria": ["`uv run pytest` exits 0"],
    "milestones": ["Core::fork, join, event"],
    "user_confirmed": False,
}


def _found_in(
    tmp_path: Path,
    fake_beagle: Path,
    monkeypatch: pytest.MonkeyPatch,
    prompt: str,
    *,
    interactive: bool,
) -> tuple[Any, Path]:
    """A `pursuit_found` for a fresh project, after `prompt` started the session."""
    project = _setup_project(tmp_path, monkeypatch)
    (fake_beagle / "add.out").write_text("T0001  Build ITC\n")
    module = _module()
    monkeypatch.setattr(module, "_LAST_PROMPT", prompt)
    monkeypatch.setattr(module, "_FOUND_REFUSED_STATEMENT", None)
    monkeypatch.setattr(module, "_FOUND_AWAITS_USER", False)
    return module.make_found_tool(interactive=lambda: interactive), project


@pytest.mark.anyio
async def test_print_mode_found_infers_delegation_from_a_delegating_prompt(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # R11: mimo sent this call eleven times without user_delegated, under a
    # prompt that said "use your judgement ... without further discussion".
    found, project = _found_in(tmp_path, fake_beagle, monkeypatch, R11_PROMPT, interactive=False)

    result = await found("c1", UNFLAGGED_FOUND)

    assert (project / ".beagle" / "pursuit.toml").is_file()
    assert "Founded the pursuit" in result.text
    assert "Delegation was inferred" in result.text and "use your judgement" in result.text
    assert "criteria you chose" in result.text
    assert _module()._FOUND_AWAITS_USER is False


@pytest.mark.anyio
async def test_print_mode_found_takes_a_resend_after_its_refusal_as_delegation(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Told "call pursuit_found again", a 9B model calls it again unchanged:
    # with nobody to confirm, that repeat is the delegation.
    found, project = _found_in(
        tmp_path, fake_beagle, monkeypatch, UNDELEGATING_PROMPT, interactive=False
    )
    goal = project / ".beagle" / "pursuit.toml"

    other = await found("c1", {**UNFLAGGED_FOUND, "statement": "Build something else"})
    assert "print mode" in other.text and not goal.exists()
    refused = await found("c2", UNFLAGGED_FOUND)
    assert "print mode" in refused.text and not goal.exists()
    again = await found("c3", {**UNFLAGGED_FOUND, "statement": "build  ITC"})

    assert goal.is_file() and "Founded the pursuit" in again.text
    assert "Delegation was inferred" in again.text and "same goal again" in again.text

    from types import SimpleNamespace

    module = _module()
    for name in ("_SEEN_CWD", "_STARTED_SESSION", "_OFF_PURSUIT_CALLS"):
        monkeypatch.setattr(module, name, getattr(module, name))
    for key in ("CLAUDE_CODE_SESSION_ID", "CLAUDE_PID"):
        monkeypatch.delenv(key, raising=False)
    assert module._FOUND_REFUSED_STATEMENT == "build itc"
    module._on_session_start(None, SimpleNamespace(cwd=str(project), session_id="s2"))
    assert module._FOUND_REFUSED_STATEMENT is None


@pytest.mark.anyio
async def test_print_mode_found_without_a_delegating_prompt_refuses_first(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    found, project = _found_in(
        tmp_path, fake_beagle, monkeypatch, UNDELEGATING_PROMPT, interactive=False
    )

    refused = await found("c1", UNFLAGGED_FOUND)

    assert not (project / ".beagle" / "pursuit.toml").exists()
    assert "print mode" in refused.text and "user_delegated=true" in refused.text
    assert "Founded" not in refused.text
    assert _module()._FOUND_AWAITS_USER is True


@pytest.mark.anyio
async def test_interactive_found_never_infers_delegation(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # A user is there to ask, so neither the prompt nor a repeat stands in for them.
    found, project = _found_in(tmp_path, fake_beagle, monkeypatch, R11_PROMPT, interactive=True)

    for i in range(3):
        result = await found(f"c{i}", UNFLAGGED_FOUND)
        assert "ask the user to confirm" in result.text
        assert "Delegation was inferred" not in result.text
    assert not (project / ".beagle" / "pursuit.toml").exists()


@pytest.mark.anyio
async def test_print_mode_stop_gate_objects_once_to_an_unfounded_stop_after_a_confirmation_refusal(
    tmp_path: Path, beagle: Path, fake_beagle: Path
) -> None:
    from pi_event_helpers import assistant_done, assistant_start, tool_call_end
    from tau_agent.messages import ToolCall
    from tau_ai import FakeProvider
    from tau_coding.cli import run_print_mode

    project = tmp_path / "project"
    project.mkdir()
    call = ToolCall(
        id="f1",
        name="pursuit_found",
        arguments={
            "statement": "Build ITC",
            "criteria": ["`uv run pytest` exits 0"],
            "milestones": ["Core::fork, join, event"],
        },
    )
    asked = AssistantMessage(content=[call])
    provider = FakeProvider(
        [
            [assistant_start(), tool_call_end(call), assistant_done(asked, "toolUse")],
            _say("Please confirm or correct the goal."),
            _say("Please confirm."),
            _say("Please confirm, again."),
        ]
    )
    ok = await run_print_mode(
        prompt=UNDELEGATING_PROMPT,  # a delegating one now founds unasked (R11)
        model="fake",
        cwd=project,
        provider=provider,
        resource_paths=TauResourcePaths(root=tmp_path / "home-tau", agents_root=None),
        extension_paths=(EXTENSION,),
    )

    assert ok is True
    assert len(provider.calls) == 3
    refusal = [m for m in provider.calls[1][2] if getattr(m, "tool_call_id", None) == "f1"]
    assert refusal and "print mode" in str(refusal[0].content)
    nudges = _sent(provider)
    assert len(nudges) == 1 and nudges[0].startswith("[beagle] Nothing is founded")
    assert "user_delegated=true" in nudges[0]


def test_cases_first_note_recommends_a_check_beagle_accepts() -> None:
    import re

    module = _module()
    checks = re.findall(r"`(python3 [^`]+)`", module.CASES_FIRST_NOTE)
    recommended = [c for c in checks if "json.tool" not in c]
    assert recommended and all(module._check_problem(c) is None for c in recommended)
    assert module._check_problem("python3 -m json.tool tests/cases.json") is not None


BEAGLE_COMMIT_STEPS = """# T0002: Parser
Do the parser.

Before you report back, commit T0002 in the two steps
below. beagle writes the commit message from the task's record.

1. Record each fact:

     beagle pursuit claim T0002 "<fact>" --at <path>:<line> --quote "<text>"

2. Commit, naming each file you changed:

     beagle pursuit commit T0002 <path> --subject "<area>: <what>"

Beagle's own state under .beagle/ and __pycache__ are never part of the
change: name only the files you changed.

Working habits: keep it small.
"""


@pytest.mark.anyio
async def test_step_brief_has_no_commit_steps(
    tmp_path: Path,
    beagle: Path,
    fake_beagle: Path,
    fake_tau: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Run R02: every brief ordered `beagle pursuit commit`/`claim`, which the
    # worker guard refuses; pursuit_step commits on close instead.
    monkeypatch.chdir(_git_project(tmp_path, monkeypatch))
    _ready_task(fake_beagle)
    (fake_beagle / "brief.out").write_text(BEAGLE_COMMIT_STEPS)
    (fake_beagle / "prove.out").write_text("T0002: PROVEN — refuses with done.txt gone\n")
    runtime, _ = _bound(tmp_path)

    await _tool(runtime, "pursuit_step").execute(
        "c1",
        {
            "task": "T0002",
            "criteria": "done.txt exists",
            "done_when": "grep -q done done.txt",
            "scope": ["done.txt", "tests/test_parser.py"],
        },
    )

    [run] = _runs(fake_tau)
    brief = run["stdin"]
    assert "beagle pursuit commit" not in brief and "beagle pursuit claim" not in brief
    assert "Before you report back" not in brief
    assert "Do not commit or claim; pursuit_step commits on close." in brief
    assert "Do the parser." in brief and "Working habits: keep it small." in brief
    assert run["scope"] == "done.txt\ntests/test_parser.py"
    [commit] = _pursuit_calls(fake_beagle, "commit")
    assert commit[:2] == ["T0002", "done.txt"]


@pytest.mark.anyio
async def test_worker_guard_refuses_git_commit(
    tmp_path: Path, beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(_pursuit_project(tmp_path))
    monkeypatch.setenv("BEAGLE_TAU_WORKER", "1")
    runtime, _ = _bound(tmp_path)
    bash = _tool_with_hooks(runtime, "bash")
    commands = [
        "git add x",
        "git -C . commit -m wip",
        "cd src && git stage x",
        "beagle pursuit commit T1 x",
    ]

    refused = [(await bash.execute("c1", {"command": c})).text for c in commands]
    agent = await _tool_with_hooks(runtime, "agent").execute("c2", {"prompt": "record claims"})
    status = await bash.execute("c3", {"command": "git status"})

    assert all("in a sub-agent" in r and "Do not commit or claim" in r for r in refused)
    assert "refusing to spawn a sub-agent with the agent tool" in agent.text
    assert status.text == "ran"
    # The driver is told pursuit_step commits, not to run the verb itself.
    monkeypatch.delenv("BEAGLE_TAU_WORKER")
    driver, _ = _bound(tmp_path)
    await driver.emit_session_start("startup")
    by_hand = await _tool_with_hooks(driver, "bash").execute(
        "c4", {"command": "beagle pursuit commit T1 x"}
    )
    assert "refusing `beagle pursuit commit`" in by_hand.text
    assert "pursuit_step commits" in by_hand.text


def _scoped_worker(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, scope: str = "tests/x.py"
) -> ExtensionRuntime:
    monkeypatch.chdir(_pursuit_project(tmp_path))
    monkeypatch.setenv("BEAGLE_TAU_WORKER", "1")
    monkeypatch.setenv("BEAGLE_TAU_WORKER_TASK", "T0003")
    monkeypatch.setenv("BEAGLE_TAU_WORKER_SCOPE", scope)
    runtime, _ = _bound(tmp_path)
    return runtime


@pytest.mark.anyio
async def test_worker_write_outside_scope_refused(
    tmp_path: Path, beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Run R02: a worker wrote `tests/` over .gitignore with two turns left.
    runtime = _scoped_worker(tmp_path, monkeypatch)
    calls = [
        ("write", {"path": ".gitignore", "content": "tests/\n"}),
        ("edit", {"path": "src/clock.py", "old": "a", "new": "b"}),
        ("bash", {"command": "echo 'tests/' > .gitignore"}),
        ("bash", {"command": "cd tests && printf x >> ../src/clock.py"}),
    ]

    for tool, arguments in calls:
        result = await _tool_with_hooks(runtime, tool).execute("c1", arguments)

        assert "outside T0003's scope (tests/x.py)" in result.text, (tool, arguments)
        assert "name it in your report as follow-up" in result.text


@pytest.mark.anyio
async def test_worker_write_in_scope_or_tmp_allowed(
    tmp_path: Path, beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    runtime = _scoped_worker(tmp_path, monkeypatch)
    calls = [
        ("write", {"path": "tests/x.py", "content": "def test_x(): pass\n"}),
        ("edit", {"path": "tests/x.py", "old": "a", "new": "b"}),
        ("write", {"path": "/tmp/y", "content": "scratch"}),
        ("bash", {"command": "python3 -m pytest -q > /tmp/out.txt 2>&1"}),
        ("bash", {"command": "cat .gitignore > tests/x.py"}),
        ("bash", {"command": "pytest -q > .git/beagle/logs/T0003.log 2>&1"}),
        ("bash", {"command": "rm -rf tests/__pycache__"}),
        ("bash", {"command": "ls src > /dev/null"}),
    ]

    for tool, arguments in calls:
        result = await _tool_with_hooks(runtime, tool).execute("c1", arguments)

        assert result.text == "ran", (tool, arguments)
    # A worker sent on a task with no scope is not held to one.
    monkeypatch.delenv("BEAGLE_TAU_WORKER_SCOPE")
    unscoped, _ = _bound(tmp_path)
    outside = {"path": ".gitignore", "content": "x"}
    assert (await _tool_with_hooks(unscoped, "write").execute("c2", outside)).text == "ran"


def test_check_refuses_test_dash_f() -> None:
    # Run R02 closed its reference task on `test -f src/design.md`.
    for check in ("test -f src/design.md", "[ -e docs/itc.md ]", "test -s src/design.md"):
        found = _module()._check_problem(check)

        assert found is not None and "only tests that a file exists" in found, check
        assert "grep -q '<a term the reference uses>' <doc>" in found
    assert _module()._check_problem("test -d tests") is None


@pytest.mark.anyio
async def test_worker_raw_tool_call_report_falls_back(
    tmp_path: Path,
    beagle: Path,
    fake_beagle: Path,
    fake_tau: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Run R02: turn-capped workers ended on tool-call markup, handed back as the report.
    project = _git_project(tmp_path, monkeypatch)
    monkeypatch.chdir(project)
    markup = "<tool_call>\n<function=bash>\n<parameter=command>ls</parameter>\n</function>"
    monkeypatch.setenv("FAKE_TAU_REPORT", markup)
    _ready_task(fake_beagle)
    (fake_beagle / "prove.out").write_text("T0002: PROVEN — refuses with done.txt gone\n")
    runtime, _ = _bound(tmp_path)

    result = await _tool(runtime, "pursuit_step").execute(
        "c1",
        {
            "task": "T0002",
            "criteria": "c",
            "done_when": "grep -q done done.txt",
            "scope": ["done.txt"],
        },
    )

    assert "<function=" not in result.text and "<tool_call>" not in result.text
    assert "the sub-agent ended without a report" in result.text
    assert "Changed or new in its scope: done.txt" in result.text
    [close] = _pursuit_calls(fake_beagle, "close")
    assert "<tool_call>" not in close[close.index("--body") + 1]


@pytest.mark.anyio
async def test_ruff_fix_refusal_names_flag(
    tmp_path: Path, beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Run R02 quoted `ruff check src/ --fix` as `ruff check …`, beside "ruff check is fine".
    monkeypatch.chdir(_pursuit_project(tmp_path))
    runtime, _ = _bound(tmp_path)
    await runtime.emit_session_start("startup")
    bash = _tool_with_hooks(runtime, "bash")

    fixing = await bash.execute("c1", {"command": "ruff check src/ tests/ --fix"})
    reading = await bash.execute("c2", {"command": "ruff check src/ tests/"})

    assert "refusing to run `ruff check src/ tests/ --fix`" in fixing.text
    assert "whose `--fix` flag rewrites files" in fixing.text
    assert reading.text == "ran"


# --------------------------------------------------------------------------- #
# run R04: no escalation after 14 stays-open; the driver debugs worker files
# --------------------------------------------------------------------------- #

STAYS_OPEN_SCOPE = ["done.txt", "src/clock.py", "tests"]


def _failing_open_task(fake_beagle: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """T0002, whose worker never makes its check pass, opened by the first step."""
    monkeypatch.setenv("FAKE_TAU_SUCCEEDS_ON", "99")
    _ready_task(fake_beagle)


def _now_open(fake_beagle: Path) -> None:
    record = {"id": "T0002", "title": "Parser", "status": "open"}
    record |= {"done_when": "grep -q done done.txt", "scope": STAYS_OPEN_SCOPE}
    (fake_beagle / "show.out").write_text(json.dumps(record))
    (fake_beagle / "next.out").write_text(json.dumps({"open": ["T0002"], "ready": []}))


async def _stays_open(step: Any, fake_beagle: Path, times: int) -> list[Any]:
    results = []
    for n in range(times):
        args: dict[str, Any] = {"task": "T0002", "attempts": 1}
        if not results:
            args |= {"criteria": "c", "done_when": "grep -q done done.txt"}
            args |= {"scope": STAYS_OPEN_SCOPE}
        results.append(await step.execute(f"s{n}", args))
        _now_open(fake_beagle)
    return results


@pytest.mark.anyio
async def test_fourth_step_after_three_not_done_is_refused_with_choices(
    tmp_path: Path,
    beagle: Path,
    fake_beagle: Path,
    fake_tau: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # R04: 14 results left T0002 not done, and none offered another way.
    monkeypatch.chdir(_pursuit_project(tmp_path))
    _failing_open_task(fake_beagle, monkeypatch)
    runtime, _ = _bound(tmp_path)
    step = _tool(runtime, "pursuit_step")

    results = await _stays_open(step, fake_beagle, 3)
    fourth = await step.execute(
        "s4", {"task": "T0002", "scope": ["src/other.py"], "notes": "look harder"}
    )
    fifth = await step.execute("s5", {})

    assert len(_runs(fake_tau)) == 3
    assert all("stays open" in r.text for r in results)
    assert "The next step on it runs no sub-agent" in results[2].text
    for refused in (fourth, fifth):
        assert refused.text.startswith("pursuit_step: T0002 not run: 3 steps on it")
        assert 'pursuit_plan task="T0002"' in refused.text
        assert 'pursuit_step task="T0002", new_route=true' in refused.text
        assert "tell the user what blocks it" in refused.text
    assert _pursuit_calls(fake_beagle, "close") == []


@pytest.mark.anyio
async def test_new_route_resets_the_not_done_count(
    tmp_path: Path,
    beagle: Path,
    fake_beagle: Path,
    fake_tau: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(_pursuit_project(tmp_path))
    _failing_open_task(fake_beagle, monkeypatch)
    runtime, _ = _bound(tmp_path)
    step = _tool(runtime, "pursuit_step")
    await _stays_open(step, fake_beagle, 3)
    (fake_beagle / "spawn.out").write_text("T0002 superseded by T0003\n")
    successor = {"id": "T0003", "title": "Parser", "status": "open"}
    successor |= {"done_when": "grep -q done done.txt", "scope": STAYS_OPEN_SCOPE}
    (fake_beagle / "show-T0003.out").write_text(json.dumps(successor))

    rerouted = await step.execute(
        "r1",
        {"task": "T0002", "new_route": True, "notes": "write done.txt first", "attempts": 1},
    )

    assert len(_runs(fake_tau)) == 4
    assert "T0003" in rerouted.text and "stays open" in rerouted.text
    assert "not run" not in rerouted.text
    module = _loaded_module()
    assert [key[1] for key in module._NOT_DONE] == ["T0003"]


@pytest.mark.anyio
async def test_plan_of_a_task_resets_its_not_done_count(
    tmp_path: Path,
    beagle: Path,
    fake_beagle: Path,
    fake_tau: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(_pursuit_project(tmp_path))
    _failing_open_task(fake_beagle, monkeypatch)
    runtime, _ = _bound(tmp_path)
    step = _tool(runtime, "pursuit_step")
    await _stays_open(step, fake_beagle, 3)

    planned = await _tool(runtime, "pursuit_plan").execute(
        "p1", {"task": "T0002", "parts": ["Lexer::tokens", "Grammar::the tree"]}
    )
    again = await step.execute("s4", {"task": "T0002", "attempts": 1})

    assert "refused" not in planned.text
    assert len(_runs(fake_tau)) == 4
    assert "not run" not in again.text


@pytest.mark.anyio
async def test_unproven_memory_keyed_by_task_survives_scope_change(
    tmp_path: Path,
    beagle: Path,
    fake_beagle: Path,
    fake_tau: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # R04 L100: the driver got past a (check, scope) key by changing the scope.
    monkeypatch.chdir(_witnessed_pursuit(tmp_path, monkeypatch))
    _ready_task(fake_beagle)
    runtime, _ = _bound(tmp_path)
    step = _tool(runtime, "pursuit_step")
    args = {"task": "T0002", "criteria": "c", "done_when": "grep -q done done.txt"}

    first = await step.execute("c1", {**args, "scope": ["tests"]})
    record = {"id": "T0002", "title": "Parser", "status": "open"}
    record |= {"done_when": "grep -q done done.txt", "scope": ["tests"]}
    (fake_beagle / "show.out").write_text(json.dumps(record))
    (fake_beagle / "next.out").write_text(json.dumps({"open": ["T0002"], "ready": []}))
    rescoped = await step.execute("c2", {"task": "T0002", "scope": ["tests", "src/clock.py"]})

    assert len(_runs(fake_tau)) == 1
    assert "no defect could be put back" in first.text
    assert "new_route=true" in first.text
    assert "not run: this check already passes and cannot be shown to refuse" in rescoped.text
    assert "whatever check or scope" in rescoped.text
    assert 'pursuit_step task="T0002", new_route=true' in rescoped.text


@pytest.mark.anyio
async def test_driver_read_of_open_task_file_refused_after_two_stays_open(
    tmp_path: Path,
    beagle: Path,
    fake_beagle: Path,
    fake_tau: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # R04: ~60 driver bash/read calls on the workers' test files, 4 compactions.
    project = _pursuit_project(tmp_path)
    monkeypatch.chdir(project)
    _failing_open_task(fake_beagle, monkeypatch)
    runtime, session = _bound(tmp_path)
    await runtime.emit_session_start("startup")
    step = _tool(runtime, "pursuit_step")
    bash, read = _tool_with_hooks(runtime, "bash"), _tool_with_hooks(runtime, "read")

    await _stays_open(step, fake_beagle, 1)
    after_one = await read.execute("r0", {"path": "src/clock.py"})
    [second] = await _stays_open(step, fake_beagle, 1)
    refused = [
        await read.execute("r1", {"path": "src/clock.py"}),
        await read.execute("r2", {"path": str(project / "tests" / "test_clock.py")}),
        await bash.execute("r3", {"command": "cat tests/test_clock.py"}),
        await bash.execute("r4", {"command": "head -n 40 src/clock.py | tail -5"}),
        await bash.execute("r5", {"command": "sed -n 1,20p src/clock.py"}),
        await bash.execute("r6", {"command": "cd . && grep -n join tests/test_clock.py"}),
    ]
    _loaded_module()._OFF_PURSUIT_CALLS = 0  # these calls pin other guards, not the streak
    allowed = [
        await read.execute("a1", {"path": "README.md"}),
        await bash.execute("a2", {"command": "ls src tests"}),
        await bash.execute("a3", {"command": "grep -rn tests docs/"}),
    ]
    session.session_id = "subagent-session"
    nested = await read.execute("a5", {"path": "src/clock.py"})
    session.session_id = "session-1"
    monkeypatch.setenv("BEAGLE_TAU_WORKER", "1")
    worker = await read.execute("a6", {"path": "src/clock.py"})
    monkeypatch.delenv("BEAGLE_TAU_WORKER")
    monkeypatch.setenv("FAKE_TAU_SUCCEEDS_ON", "1")
    closed = await step.execute("s3", {"task": "T0002", "attempts": 1})
    after_close = await read.execute("a7", {"path": "src/clock.py"})

    assert after_one.text == "ran"
    assert "reading them yourself is refused" in second.text
    for result in refused:
        assert "from the driving session" in result.text
        assert "in the scope of T0002" in result.text
        assert "pursuit_step's notes" in result.text and "new_route=true" in result.text
    assert [r.text for r in allowed] == ["ran"] * len(allowed)
    assert [nested.text, worker.text] == ["ran"] * 2
    assert "closed done" in closed.text
    assert after_close.text == "ran"


# run R04: workers orienting on beagle, a one-liner write, guard holes


@pytest.mark.anyio
async def test_worker_guard_refuses_beagle_commands_and_beagle_reads(
    tmp_path: Path, beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # R04: 20 of 25 workers capped, W1 ten turns on .beagle/, doctor and the tree.
    runtime = _scoped_worker(tmp_path, monkeypatch, scope="tests/")
    calls = [
        ("bash", {"command": "beagle pursuit tree"}),
        ("bash", {"command": "beagle doctor"}),
        ("bash", {"command": "cd . && cat .beagle/tree/T0003.md"}),
        ("read", {"path": ".beagle/pursuit.toml"}),
    ]

    for tool, arguments in calls:
        result = await _tool_with_hooks(runtime, tool).execute("c1", arguments)

        assert "the brief has everything; do the task" in result.text, (tool, arguments)
    # Its own test runs and its check script still run.
    allowed = [
        ("bash", {"command": "python3 -m pytest -q tests/test_beagle.py"}),
        ("bash", {"command": "bash .beagle/checks/T0003/check.sh"}),
        ("read", {"path": "tests/x.py"}),
    ]
    for tool, arguments in allowed:
        result = await _tool_with_hooks(runtime, tool).execute("c2", arguments)

        assert result.text == "ran", (tool, arguments)
    # A worker sent with no scope is still kept from beagle.
    monkeypatch.delenv("BEAGLE_TAU_WORKER_SCOPE")
    unscoped, _ = _bound(tmp_path)
    tree = await _tool_with_hooks(unscoped, "bash").execute("c3", {"command": "beagle status"})
    assert "the brief has everything" in tree.text
    # One sent with no task (pursuit_dispatch, an audit) still reads the pursuit.
    monkeypatch.delenv("BEAGLE_TAU_WORKER_TASK")
    taskless, _ = _bound(tmp_path)
    brief = await _tool_with_hooks(taskless, "bash").execute(
        "c4", {"command": "beagle pursuit brief T0003"}
    )
    assert brief.text == "ran"
    assert _module().NO_BEAGLE_NOTE == "Do not inspect .beagle/ or run beagle."


@pytest.mark.anyio
async def test_worker_guard_refuses_python_one_liner_write_out_of_scope(
    tmp_path: Path, beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # R04: W9, refused a write to src/__init__.py, wrote it with python3 -c.
    runtime = _scoped_worker(tmp_path, monkeypatch, scope="tests/")
    bash = _tool_with_hooks(runtime, "bash")

    outside = await bash.execute("c1", {"command": "python3 -c \"open('src/x.py','w').write('')\""})
    write_text = "from pathlib import Path; Path('src/x.py').write_text('')"
    path = await bash.execute("c2", {"command": f'python3 -c "{write_text}"'})
    inside = await bash.execute(
        "c3", {"command": "python3 -c \"open('tests/cases.json','w').write('[]')\""}
    )
    reading = await bash.execute("c4", {"command": "python3 -c \"print(open('src/x.py').read())\""})

    for refused in (outside, path):
        assert "refusing to write src/x.py: it is outside T0003's scope (tests/)" in refused.text
    assert [inside.text, reading.text] == ["ran", "ran"]


#: R12 W10 E48, verbatim: it deleted create_node from T0004's committed src.
R12_OS_SYSTEM_SED = (
    'python3 -c "import os; os.system(\'sed -i \\"184,194d\\" src/interval_tree_clock.py\')"'
)


@pytest.mark.anyio
async def test_worker_guard_blocks_sed_through_os_system_in_inline_python(
    tmp_path: Path, beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # R12: W10, refused ~10 writes to src/, ran sed -i on it through os.system.
    runtime = _scoped_worker(tmp_path, monkeypatch, scope="tests/test_cases.py")
    bash = _tool_with_hooks(runtime, "bash")

    result = await bash.execute("c1", {"command": R12_OS_SYSTEM_SED})
    popen = await bash.execute(
        "c2", {"command": "python3 -c 'import os; os.popen(\"echo x > src/a.py\")'"}
    )
    heredoc = await bash.execute(
        "c3",
        {"command": "python3 - <<'EOF'\nimport os\nos.system('rm src/a.py')\nEOF"},
    )

    assert "refusing to write src/interval_tree_clock.py: it is outside T0003's scope" in (
        result.text
    )
    assert "(tests/test_cases.py)" in result.text
    assert "refusing to write src/a.py" in popen.text
    assert "refusing to write src/a.py" in heredoc.text


@pytest.mark.anyio
async def test_worker_guard_blocks_subprocess_write_outside_scope(
    tmp_path: Path, beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    runtime = _scoped_worker(tmp_path, monkeypatch, scope="tests/test_cases.py")
    bash = _tool_with_hooks(runtime, "bash")

    shell = await bash.execute(
        "c1",
        {
            "command": 'python3 -c "import subprocess; '
            "subprocess.run('sed -i 1d src/a.py', shell=True)\""
        },
    )
    # A list argument has no command line to read: a path literal stands for it.
    listed = await bash.execute(
        "c2",
        {
            "command": 'python3 -c "import subprocess; '
            "subprocess.run(['sed', '-i', '1d', 'src/a.py'])\""
        },
    )
    reads = await bash.execute(
        "c3", {"command": "python3 -c \"import os; os.system('cat src/a.py')\""}
    )
    runs = await bash.execute(
        "c4", {"command": "python3 -c \"import subprocess; subprocess.run(['pytest', '-q'])\""}
    )

    for refused in (shell, listed):
        assert "refusing to write src/a.py: it is outside T0003's scope" in refused.text
    assert [reads.text, runs.text] == ["ran", "ran"]


@pytest.mark.anyio
async def test_worker_guard_allows_os_system_write_inside_scope(
    tmp_path: Path, beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    runtime = _scoped_worker(tmp_path, monkeypatch, scope="src/interval_tree_clock.py")
    bash = _tool_with_hooks(runtime, "bash")

    sed = await bash.execute("c1", {"command": R12_OS_SYSTEM_SED})
    listed = await bash.execute(
        "c2",
        {
            "command": 'python3 -c "import subprocess; '
            "subprocess.run(['sed', '-i', '1d', 'src/interval_tree_clock.py'])\""
        },
    )
    scratch = await bash.execute(
        "c3", {"command": "python3 -c \"import os; os.system('echo x > /tmp/scratch.txt')\""}
    )

    assert [sed.text, listed.text, scratch.text] == ["ran", "ran", "ran"]


def test_check_problem_refuses_import_only_python_c() -> None:
    # R04 L178: bound, and W23 was dispatched on it.
    check = "python3 -c \"from tests.test_case_data import validate_fork_seed; print('OK')\""

    found = _module()._check_problem(check)

    assert found is not None and "only imports and prints" in found
    assert "passes as soon as the file is there" in found
    runs = 'python3 -c "from src.itc import Stamp; assert Stamp().fork()"'
    assert _module()._check_problem(runs) is None


@pytest.mark.anyio
async def test_prove_skips_witness_in_test_file(
    tmp_path: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # R04 L189: W24's witness was in tests/test_case_data.py.
    project = _git_project(tmp_path, monkeypatch)
    report = (
        "wrote the test\n\nWITNESS: tests/test_x.py\nNEEDLE:\n    assert x == 1\n"
        "REPLACEMENT:\n    assert x == 2\nEND WITNESS"
    )

    proof = await _module()._prove("T0002", report, ["tests/"], project, 60)

    assert proof is not None and not proof.proven
    assert "the WITNESS is in a test file; name a defect in the code the test runs" in proof.text
    assert _pursuit_calls(fake_beagle, "prove") == []


@pytest.mark.anyio
async def test_abandon_problem_refuses_root(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # R04 L142: abandon="duplicate of T0002" on T0001, the root, reached beagle.
    monkeypatch.chdir(_pursuit_project(tmp_path))
    _ready_task(fake_beagle)
    _milestones(fake_beagle)
    runtime, _ = _bound(tmp_path)

    result = await _tool(runtime, "pursuit_step").execute(
        "c1", {"task": "T0001", "abandon": "duplicate of T0002"}
    )

    assert _pursuit_calls(fake_beagle, "close") == []
    assert "T0001 not abandoned — it is the root" in result.text


#: Run R10's founding: a setup milestone T0002 every later milestone waits on.
R10_SETUP = "Setup beagle pursuit infrastructure - configure gates and checks"


def _r10_nodes(
    status: str = "pending", title: str = R10_SETUP, *children: str
) -> list[dict[str, Any]]:
    return [
        {"id": "T0001", "parent": "", "title": "ITC", "status": "pending"},
        {"id": "T0002", "parent": "T0001", "title": title, "status": status},
        {"id": "T0003", "parent": "T0001", "title": "Implement core clock", "status": "pending"},
        *(
            {"id": f"T00{10 + i}", "parent": "T0002", "title": "part", "status": child}
            for i, child in enumerate(children)
        ),
    ]


@pytest.mark.anyio
async def test_never_opened_setup_milestone_can_be_abandoned(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # R10: T0002 was refused at every step, and its abandon as "a milestone".
    problem = _module()._abandon_problem
    assert problem("T0002", "setup: founding did it", _r10_nodes()) is None
    assert (
        problem("T0002", "setup: founding did it", _r10_nodes("pending", R10_SETUP, "pending"))
        is None
    )

    monkeypatch.chdir(_pursuit_project(tmp_path))
    _ready_task(fake_beagle)
    (fake_beagle / "tree.out").write_text(json.dumps({"nodes": _r10_nodes()}))
    runtime, _ = _bound(tmp_path)

    result = await _tool(runtime, "pursuit_step").execute(
        "c1", {"task": "T0002", "abandon": "setup: founding did it"}
    )

    assert "not abandoned" not in result.text
    assert [c[0] for c in _pursuit_calls(fake_beagle, "close")] == ["T0002"]


def test_worked_or_goal_milestone_abandon_is_still_refused() -> None:
    problem = _module()._abandon_problem
    why = "setup: founding did it"
    refused = {
        "opened": _r10_nodes("open"),
        "done": _r10_nodes("done"),
        "worked child": _r10_nodes("pending", R10_SETUP, "pending", "open"),
        "done child": _r10_nodes("pending", R10_SETUP, "done"),
        "goal work": _r10_nodes("pending", "Implement core clock operations"),
    }
    for case, nodes in refused.items():
        text = problem("T0002", why, nodes)
        assert text is not None and "it is a milestone" in text, case
    assert "it is the root" in (problem("T0001", why, _r10_nodes()) or "")


def test_dot_beagle_scope_refusal_names_the_abandon_route() -> None:
    scope_problem = _module()._scope_problem
    route = 'pursuit_step task="T0002", abandon="setup: founding did it"'

    setup = scope_problem([".beagle/gates.toml"], "T0002", _r10_nodes())
    opened = scope_problem([".beagle/gates.toml"], "T0002", _r10_nodes("open"))
    goal = scope_problem(
        [".beagle/gates.toml"], "T0002", _r10_nodes("pending", "Implement core clock operations")
    )

    assert setup is not None and route in setup and "scope names .beagle/gates.toml" in setup
    for other in (opened, goal, scope_problem([".beagle/gates.toml"])):
        assert other is not None and "abandon" not in other
    assert scope_problem(["src/itc.py"], "T0002", _r10_nodes()) is None


#: Run R06's T0002 and its successor T0008, as `pursuit show` gives them.
R06_PREDECESSOR = {
    "id": "T0002",
    "parent": "T0001",
    "title": "Reference study",
    "status": "superseded",
    "criteria": "tests/cases.json holds cases from the reference, each citing its source",
    "done_when": "grep -q done done.txt",
    "scope": ["done.txt"],
}
R06_SUCCESSOR = {
    "id": "T0008",
    "parent": "T0001",
    "title": "Reference study",
    "status": "pending",
    "criteria": "",
    "done_when": "",
    "sibling_of": "T0002",
}


@pytest.mark.anyio
async def test_new_route_checks_done_when_before_spawning(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # R06 L28-29: T0008 was spawned, then not opened on a check that already
    # passed, and T0002 was superseded by a successor with no criteria.
    project = _pursuit_project(tmp_path)
    monkeypatch.chdir(project)
    (project / "done.txt").write_text("done")
    (fake_beagle / "next.out").write_text(json.dumps({"open": [{"id": "T0002"}], "ready": []}))
    opened = {**R06_PREDECESSOR, "status": "open", "done_when": "grep -q nothing done.txt"}
    (fake_beagle / "show-T0002.out").write_text(json.dumps(opened))
    (fake_beagle / "spawn.out").write_text("T0002 superseded by T0008\n")
    runtime, _ = _bound(tmp_path)
    step = _tool(runtime, "pursuit_step")
    route = {"task": "T0002", "new_route": True, "notes": "check only the data file"}

    passing = await step.execute("c1", {**route, "done_when": "grep -q done done.txt"})
    out_of_scope = await step.execute(
        "c2", {**route, "done_when": "grep -q x done.txt", "scope": [".beagle/tree"]}
    )

    assert "no new route for T0002" in passing.text and "already passes" in passing.text
    assert "no new route for T0002" in out_of_scope.text
    assert _pursuit_calls(fake_beagle, "spawn") == [] == _pursuit_calls(fake_beagle, "open")


@pytest.mark.anyio
async def test_new_route_successor_opens_with_the_predecessors_criteria(
    tmp_path: Path,
    beagle: Path,
    fake_beagle: Path,
    fake_tau: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # R06 L33-69: the successor's Next text asked for criteria, and beagle
    # refused each new set as drift from T0002's.
    monkeypatch.chdir(_pursuit_project(tmp_path))
    ready = {"open": [], "ready": [{"id": "T0008", "title": "Reference study"}]}
    (fake_beagle / "next.out").write_text(json.dumps(ready))
    (fake_beagle / "show-T0002.out").write_text(json.dumps(R06_PREDECESSOR))
    (fake_beagle / "show-T0008.out").write_text(json.dumps(R06_SUCCESSOR))
    (fake_beagle / "brief.out").write_text("# T0008: Reference study\n")
    runtime, _ = _bound(tmp_path)
    step = _tool(runtime, "pursuit_step")

    asked = await step.execute("c1", {"task": "T0008"})
    result = await step.execute(
        "c2",
        {
            "task": "T0008",
            "criteria": "A test file validates that cases.json exists",
            "done_when": "grep -q done done.txt",
            "scope": ["done.txt"],
        },
    )

    assert "carried over from T0002" in asked.text
    assert "criteria: what will be true" not in asked.text
    [opened] = _pursuit_calls(fake_beagle, "open")
    assert opened[0] == "T0008"
    assert opened[opened.index("--criteria") + 1] == R06_PREDECESSOR["criteria"]
    assert "refused" not in result.text and "Criteria kept from T0002" in result.text
    assert "T0008 — Reference study: closed done" in result.text


@pytest.mark.anyio
async def test_superseded_task_is_named_superseded_not_a_container(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # R06 L31: "T0002 is not a task to work now: it is a container", for a
    # T0002 that T0008 had superseded.
    monkeypatch.chdir(_pursuit_project(tmp_path))
    ready = {"open": [], "ready": [{"id": "T0008", "title": "Reference study"}]}
    (fake_beagle / "next.out").write_text(json.dumps(ready))
    root = {"id": "T0001", "parent": "", "status": "pending", "container": True}
    tree = [root, R06_PREDECESSOR, R06_SUCCESSOR]
    (fake_beagle / "tree.out").write_text(json.dumps({"nodes": tree}))
    runtime, _ = _bound(tmp_path)
    step = _tool(runtime, "pursuit_step")

    workable = await step.execute("c1", {"task": "T0002"})
    _nothing_ready(fake_beagle, CYCLE_TREE)
    stuck = await step.execute("c2", {"task": "T0002"})

    assert "T0002 was superseded by T0008" in workable.text
    assert 'pursuit_step task="T0008"' in workable.text
    assert "T0002 was superseded by T0008" in stuck.text and "not ready" in stuck.text
    for text in (workable.text, stuck.text):
        assert "it is a container" not in text
    assert _pursuit_calls(fake_beagle, "open") == []


@pytest.mark.anyio
async def test_plan_on_an_open_leaf_splits_into_two_or_more_parts(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # R06 L21-27: the escalation offered pursuit_plan, and a one-part plan of
    # open T0002 came back as beagle's raw refusal.
    monkeypatch.chdir(_pursuit_project(tmp_path))
    (fake_beagle / "add.out").write_text(
        "beagle: T0002 is a open leaf with work of its own. A child makes it a container: "
        "its own work stops being offered. To decompose T0002, `split` it. To make it a "
        "container on purpose, --make-container."
    )
    (fake_beagle / "add.rc").write_text("4")
    (fake_beagle / "split.out").write_text("T0002 split into 2:\n  T0009  Data\n  T0010  Test\n")
    runtime, _ = _bound(tmp_path)
    plan = _tool(runtime, "pursuit_plan")

    one = await plan.execute("c1", {"task": "T0002", "parts": ["Data::the cases"]})
    two = await plan.execute(
        "c2", {"task": "T0002", "parts": ["Data::the cases", "Test::runs them"]}
    )

    assert "two or more parts" in one.text and "beagle refused" not in one.text
    assert "beagle refused" not in two.text
    assert _pursuit_calls(fake_beagle, "split") == [
        ["T0002", "Data::the cases", "Test::runs them", "--ordered"]
    ]
    escalation = _module()._escalation("T0002", 3)
    assert 'pursuit_plan task="T0002" with two or more parts' in escalation


@pytest.mark.anyio
async def test_abandon_a_superseded_milestones_successor_with_a_reason(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # R06 L109-157: abandoning T0008, the successor of milestone T0002, was
    # refused as "a milestone" four times.
    monkeypatch.chdir(_pursuit_project(tmp_path))
    _ready_task(fake_beagle)
    root = {"id": "T0001", "parent": "", "status": "pending", "container": True}
    milestone = {"id": "T0003", "parent": "T0001", "status": "pending"}
    tree = [root, R06_PREDECESSOR, R06_SUCCESSOR, milestone]
    (fake_beagle / "tree.out").write_text(json.dumps({"nodes": tree}))
    (fake_beagle / "close.out").write_text("T0008 abandoned\n")
    runtime, _ = _bound(tmp_path)
    step = _tool(runtime, "pursuit_step")

    successor = await step.execute("c1", {"task": "T0008", "abandon": "it closes a cycle"})
    plain = await step.execute("c2", {"task": "T0003", "abandon": "it closes a cycle"})

    assert _pursuit_calls(fake_beagle, "close") == [
        ["T0008", "--outcome", "abandoned", "--reason", "it closes a cycle"]
    ]
    assert "T0008 abandoned" in successor.text
    assert "T0003 not abandoned — it is a milestone" in plain.text


@pytest.mark.anyio
async def test_worker_brief_drops_beagle_contain_run(
    tmp_path: Path,
    beagle: Path,
    fake_beagle: Path,
    fake_tau: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # R06: W2 L49 and W4 L41 ran the habit line's `beagle contain run` and were refused.
    log = "/repo/.git/beagle/logs/T0002.log"
    beagle_brief = (
        "# T0002: Parser\nDo the parser.\n"
        "Finished beside this task (context, not a contract; `beagle pursuit show <id>` "
        "has the whole record):\n"
        "29 done task(s) keep a standing check over this tree; `beagle pursuit recheck` "
        "runs them all and files nothing. Once your check passes, run it.\n"
        "Working habits:\n"
        "- Run every test, build and check contained, capped and redirected: "
        "`RUN_CONTAINED_FOREGROUND=1 beagle contain run heavy -- timeout 540 <cmd> > "
        f'{log} 2>&1; echo "exit $?"`, then read the tail.\n'
        "- Read files by the range you need.\n"
    )
    monkeypatch.chdir(_pursuit_project(tmp_path))
    _ready_task(fake_beagle)
    (fake_beagle / "brief.out").write_text(beagle_brief)
    runtime, _ = _bound(tmp_path)

    await _tool(runtime, "pursuit_step").execute(
        "c1",
        {
            "task": "T0002",
            "criteria": "done.txt exists",
            "done_when": "grep -q done done.txt",
            "scope": ["done.txt"],
        },
    )

    sent = _runs(fake_tau)[0]["stdin"]
    told = sent.replace(_module().NO_BEAGLE_NOTE, "")
    assert "beagle contain" not in told and "RUN_CONTAINED" not in told
    assert "beagle pursuit" not in told
    assert "- Run every test, build and check capped and redirected, as a plain command: " in told
    assert f"`timeout 540 <cmd> > {log} 2>&1" in told
    assert "- Read files by the range you need." in told
    assert "(context, not a contract):" in told
    assert re.search(r"\bbeagle\s+\w", told) is None


@pytest.mark.anyio
async def test_worker_guard_refuses_touch_and_mkdir_out_of_scope(
    tmp_path: Path, beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # R06: W4 L47 `touch src/itc/__init__.py` went through; W2 L64 `mkdir -p src/itc`.
    targets = _module()._bash_write_targets
    assert targets("touch a/b.py", tmp_path) == [tmp_path / "a" / "b.py"]
    assert targets("touch -d 2020-01-01 a.py", tmp_path) == [tmp_path / "a.py"]
    assert targets("mkdir -p -m 755 src/itc", tmp_path) == [tmp_path / "src" / "itc"]
    runtime = _scoped_worker(tmp_path, monkeypatch, scope="tests/")
    bash = _tool_with_hooks(runtime, "bash")

    touched = await bash.execute("c1", {"command": "touch src/itc/__init__.py"})
    made = await bash.execute("c2", {"command": "mkdir -p src/itc"})
    inside = await bash.execute("c3", {"command": "mkdir -p tests/data && touch tests/x.py"})

    assert "refusing to write src/itc/__init__.py: it is outside T0003's scope" in touched.text
    assert "refusing to write src/itc: it is outside T0003's scope" in made.text
    assert inside.text == "ran"


@pytest.mark.anyio
async def test_tests_only_unproven_next_names_no_import(
    tmp_path: Path,
    beagle: Path,
    fake_beagle: Path,
    fake_tau: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # R06 L13: the Next text also asked for an import of unwritten code; W3 put it in the check.
    _cases_task(tmp_path, fake_beagle, monkeypatch, CASES_DATA_TEST)
    (fake_beagle / "prove.out").write_text("T0002: NOT PROVEN — the file predates the task\n")
    (fake_beagle / "prove.rc").write_text("9")

    result = await _step_cases(tmp_path)

    assert "stays open" in result.text
    next_text = result.text[result.text.index("Next:") :]
    assert "tests/test_case_data.py must fail when tests/cases.json is removed" in next_text
    for word in ("ImportError", "import the module", "from <package>", "test_cases.py"):
        assert word not in next_text, word


M_TEST = "from src.m import f\n\n\ndef test_f():\n    assert f() == 1\n"


def _imports_m_task(
    tmp_path: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch, witness: str
) -> Path:
    """A tests-only task whose worker writes tests/test_m.py, which imports src/m.py."""
    project = _git_project(tmp_path, monkeypatch)
    monkeypatch.chdir(project)
    (project / "src").mkdir()
    (project / "src" / "m.py").write_text("def f():\n    return 1\n")
    monkeypatch.setenv("FAKE_TAU_WRITES", json.dumps({"tests/test_m.py": M_TEST}))
    monkeypatch.setenv(
        "FAKE_TAU_REPORT",
        f"wrote the test\n\nWITNESS: {witness}\nNEEDLE:\n    return 1\n"
        "REPLACEMENT:\n    return 2\nEND WITNESS",
    )
    _ready_task(fake_beagle, "grep -q test_f tests/test_m.py")
    (fake_beagle / "prove.out").write_text(
        "T0002: PROVEN — refuses when `return 1` is `return 2`\n"
    )
    return project


async def _step_m(tmp_path: Path) -> Any:
    runtime, _ = _bound(tmp_path)
    return await _tool(runtime, "pursuit_step").execute(
        "c1",
        {
            "task": "T0002",
            "criteria": "the tests of m are written",
            "done_when": "grep -q test_f tests/test_m.py",
            "scope": ["tests/test_m.py"],
        },
    )


@pytest.mark.anyio
async def test_tests_only_task_proves_by_mutating_the_imported_module(
    tmp_path: Path,
    beagle: Path,
    fake_beagle: Path,
    fake_tau: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # R12 E41-E42: T0008's check passed and its tests imported the module.
    _imports_m_task(tmp_path, fake_beagle, monkeypatch, "src/m.py")

    result = await _step_m(tmp_path)

    [prove] = _pursuit_calls(fake_beagle, "prove")
    assert prove[:3] == ["T0002", "--mutate", "src/m.py"]
    assert _pursuit_calls(fake_beagle, "close")[0][:3] == ["T0002", "--outcome", "done"]
    assert "closed done" in result.text


@pytest.mark.anyio
async def test_tests_only_witness_in_test_file_names_the_imported_module_and_is_not_unproven(
    tmp_path: Path,
    beagle: Path,
    fake_beagle: Path,
    fake_tau: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # R12 E41-E48: the witness in the test was refused, the task went unproven at
    # once, and the next text pointed at T0007's locked tests/cases.json.
    project = _imports_m_task(tmp_path, fake_beagle, monkeypatch, "tests/test_m.py")

    result = await _step_m(tmp_path)

    first, second = _runs(fake_tau)
    assert "Give a WITNESS in src/m.py" in second["stdin"]
    assert "Give a WITNESS in src/m.py" in result.text
    assert "stays open" in result.text and "new_route=true" not in result.text
    assert "the data file's absence is the proof" not in result.text
    assert (str(project), "T0002") not in _module()._UNPROVEN
    assert _pursuit_calls(fake_beagle, "prove") == []
    assert _pursuit_calls(fake_beagle, "close") == []
    assert _module()._scope_has_data(["tests/cases.json", "tests/test_m.py"])
    assert not _module()._scope_has_data(["tests/test_m.py", "tests/"])


@pytest.mark.anyio
async def test_new_route_passing_only_on_own_uncommitted_work_is_opened(
    tmp_path: Path,
    beagle: Path,
    fake_beagle: Path,
    fake_tau: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # R12 E44-E96: T0008's new route was refused as "already passes" five times,
    # on a check that passed only on its own uncommitted tests/test_cases.py.
    project = _git_project(tmp_path, monkeypatch)
    monkeypatch.chdir(project)
    (project / "tests").mkdir()
    (project / "tests" / "test_m.py").write_text(M_TEST)
    (fake_beagle / "next.out").write_text(json.dumps({"open": [{"id": "T0002"}], "ready": []}))
    opened = {
        **R06_PREDECESSOR,
        "status": "open",
        "done_when": "grep -q nothing tests/test_m.py",
        "scope": ["tests/test_m.py"],
    }
    (fake_beagle / "show-T0002.out").write_text(json.dumps(opened))
    (fake_beagle / "spawn.out").write_text("T0002 superseded by T0008\n")
    runtime, _ = _bound(tmp_path)

    result = await _tool(runtime, "pursuit_step").execute(
        "c1",
        {
            "task": "T0002",
            "new_route": True,
            "notes": "run the test that imports src/m.py",
            "done_when": "grep -q test_f tests/test_m.py",
        },
    )

    assert "already passes" not in result.text
    assert len(_pursuit_calls(fake_beagle, "spawn")) == 1
    assert (project / "tests" / "test_m.py").read_text() == M_TEST


@pytest.mark.anyio
async def test_implementation_in_tests_lets_small_helpers_through(
    tmp_path: Path,
    beagle: Path,
    fake_beagle: Path,
    fake_tau: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # R06 L21: the check passed, but T0002 stayed open over `load_cases` and `get_module_path`.
    data_test = (
        "import json\n\n\ndef load_cases():\n    with open('tests/cases.json') as f:\n"
        "        return json.load(f)\n\n\ndef get_module_path():\n    return 'src/itc'\n\n\n"
        "def test_cases():\n    assert load_cases()\n"
    )
    _cases_task(tmp_path, fake_beagle, monkeypatch, data_test)

    result = await _step_cases(tmp_path)

    assert "implementation belongs in the module" not in result.text
    assert "stays open" not in result.text
    assert _pursuit_calls(fake_beagle, "close") != []
    found = _module()._implementation_in_tests
    large = "def fork(s):\n" + "    s = s\n" * 15 + "    return s\n"
    (tmp_path / "test_big.py").write_text(f"class Stamp:\n    pass\n\n\n{large}")
    assert found(tmp_path, ["test_big.py"]) == ["test_big.py: class Stamp", "test_big.py: def fork"]


@pytest.mark.anyio
async def test_not_done_step_names_implementation_written_under_tests(
    tmp_path: Path,
    beagle: Path,
    fake_beagle: Path,
    fake_tau: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # R09 W4: refused src/, it wrote the library to tests/itc/; nothing said so.
    project = _git_project(tmp_path, monkeypatch)
    monkeypatch.chdir(project)
    writes = {"tests/pkg/clock.py": "class Clock:\n    pass\n"}
    monkeypatch.setenv("FAKE_TAU_WRITES", json.dumps(writes))
    _ready_task(fake_beagle, "grep -q out tests/cases.json")
    runtime, _ = _bound(tmp_path)

    result = await _tool(runtime, "pursuit_step").execute(
        "c1",
        {
            "task": "T0002",
            "criteria": "the known answers are written",
            "done_when": "grep -q out tests/cases.json",
            "scope": ["tests/"],
        },
    )

    assert "stays open" in result.text
    assert result.text.startswith(
        "The sub-agent wrote implementation into tests/ (tests/pkg/clock.py: class Clock), "
        "which is not this task's work."
    )


@pytest.mark.anyio
async def test_worker_problem_step_names_implementation_written_under_tests(
    tmp_path: Path,
    beagle: Path,
    fake_beagle: Path,
    fake_tau: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # A worker that came back with a problem may still have left code under tests/.
    project = _git_project(tmp_path, monkeypatch)
    monkeypatch.chdir(project)
    (project / "tests" / "pkg").mkdir(parents=True)
    (project / "tests" / "pkg" / "clock.py").write_text("class Clock:\n    pass\n")
    monkeypatch.setenv("TAU_BIN", str(tmp_path / "no-such-tau"))
    _ready_task(fake_beagle, "grep -q out tests/cases.json")
    runtime, _ = _bound(tmp_path)

    result = await _tool(runtime, "pursuit_step").execute(
        "c1",
        {
            "task": "T0002",
            "criteria": "the known answers are written",
            "done_when": "grep -q out tests/cases.json",
            "scope": ["tests/"],
        },
    )

    assert "stays open — " in result.text and "not found on PATH" in result.text
    assert result.text.startswith(
        "The sub-agent wrote implementation into tests/ (tests/pkg/clock.py: class Clock), "
        "which is not this task's work."
    )


@pytest.mark.anyio
async def test_prove_refused_step_names_implementation_written_under_tests(
    tmp_path: Path,
    beagle: Path,
    fake_beagle: Path,
    fake_tau: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # The check passes but `prove` refuses it; code under tests/ is still named first.
    monkeypatch.chdir(_git_project(tmp_path, monkeypatch))
    monkeypatch.setenv("FAKE_TAU_REPORT", WITNESSED_REPORT)
    writes = {"tests/pkg/clock.py": "class Clock:\n    pass\n"}
    monkeypatch.setenv("FAKE_TAU_WRITES", json.dumps(writes))
    _ready_task(fake_beagle)
    (fake_beagle / "prove.out").write_text("T0002: NOT PROVEN — src/clock.py is not there\n")
    (fake_beagle / "prove.rc").write_text("9")
    runtime, _ = _bound(tmp_path)

    result = await _tool(runtime, "pursuit_step").execute(
        "c1",
        {
            "task": "T0002",
            "criteria": "c",
            "done_when": "grep -q done done.txt",
            "scope": ["done.txt", "tests/"],
        },
    )

    assert "the check passes, but no defect could be put back" in result.text
    assert "stays open" in result.text
    assert result.text.startswith(
        "The sub-agent wrote implementation into tests/ (tests/pkg/clock.py: class Clock), "
        "which is not this task's work."
    )


@pytest.mark.anyio
async def test_worker_scope_refusal_of_source_says_not_under_tests_either(
    tmp_path: Path, beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    runtime = _scoped_worker(tmp_path, monkeypatch, scope="tests/")
    write = _tool_with_hooks(runtime, "write")

    source = await write.execute("c1", {"path": "src/x.py", "content": "class X: ...\n"})
    doc = await write.execute("c2", {"path": "docs/x.md", "content": "x\n"})

    either = "The implementation does not go under tests/ either: it is a later task's work"
    assert "refusing to write src/x.py: it is outside T0003's scope (tests/)" in source.text
    assert either in source.text
    assert "refusing to write docs/x.md" in doc.text and either not in doc.text


@pytest.mark.anyio
async def test_brief_for_a_data_task_gives_the_request_as_context_only(
    tmp_path: Path,
    beagle: Path,
    fake_beagle: Path,
    fake_tau: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # R09 T0002: a cases task's brief ended on the request, and its worker implemented it.
    project = _pursuit_project(tmp_path)
    monkeypatch.chdir(project)
    _fake_web(monkeypatch, {})
    _module()._fetch_references(project, ITC_PROMPT)
    _ready_task(fake_beagle, "grep -q out tests/cases.json")
    runtime, _ = _bound(tmp_path)

    await _tool(runtime, "pursuit_step").execute(
        "c1",
        {
            "task": "T0002",
            "criteria": "the known answers are written",
            "done_when": "grep -q out tests/cases.json",
            "scope": CASES_SCOPE,
        },
    )

    brief = _runs(fake_tau)[0]["stdin"]
    assert (
        "The user's original request, as context only; your task is the one above, not "
        f"this request:\n<<<\n{ITC_PROMPT}\n>>>"
    ) in brief
    assert "The user's original request, verbatim" not in brief


@pytest.mark.anyio
async def test_task_worker_brief_carries_the_no_beagle_note(
    tmp_path: Path,
    beagle: Path,
    fake_beagle: Path,
    fake_tau: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(_pursuit_project(tmp_path))
    _ready_task(fake_beagle)
    (fake_beagle / "brief.out").write_text("# T0002: Parser\nDo the parser.\n")
    runtime, _ = _bound(tmp_path)

    await _tool(runtime, "pursuit_step").execute(
        "c1",
        {
            "task": "T0002",
            "criteria": "done.txt exists",
            "done_when": "grep -q done done.txt",
            "scope": ["done.txt"],
        },
    )

    sent = _runs(fake_tau)[0]["stdin"]
    assert "Do the parser." in sent
    assert _module().NO_BEAGLE_NOTE in sent


def _stop_gate_sends(monkeypatch: pytest.MonkeyPatch, cwd: Path, *, has_ui: bool) -> list[str]:
    from types import SimpleNamespace

    module = _module()
    monkeypatch.setattr(module, "_FOUND_AWAITS_USER", True)
    monkeypatch.setattr(module, "_STOP_GATE_SENT", 0)
    sent: list[str] = []
    gate = module.make_stop_gate(SimpleNamespace(send_user_message=sent.append))
    stop = SimpleNamespace(
        message=SimpleNamespace(role="assistant", tool_calls=[], stop_reason="stop")
    )
    asyncio.run(gate(stop, SimpleNamespace(cwd=str(cwd), has_ui=has_ui)))
    return sent


def test_stop_gate_says_nothing_unfounded_in_an_interactive_session(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # T0044: a user is there to answer, so an unfounded stop awaiting them is left alone.
    project = tmp_path / "project"
    project.mkdir()

    assert _stop_gate_sends(monkeypatch, project, has_ui=True) == []
    assert _module()._FOUND_AWAITS_USER is True
    printed = _stop_gate_sends(monkeypatch, project, has_ui=False)
    assert len(printed) == 1 and printed[0].startswith("[beagle] Nothing is founded")


def test_stop_gate_founded_session_gets_no_unfounded_followup(
    tmp_path: Path, beagle: Path, fake_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # T0044: once founded, a stop hears what is not done, never "Nothing is founded".
    project = _pursuit_project(tmp_path)
    root = {"id": "T0001", "parent": "", "status": "pending", "container": True}
    leaf = {"id": "T0002", "parent": "T0001", "status": "pending"}
    (fake_beagle / "tree.out").write_text(json.dumps({"nodes": [root, leaf]}))

    sent = _stop_gate_sends(monkeypatch, project, has_ui=False)

    assert len(sent) == 1
    assert sent[0].startswith("[beagle] The pursuit is not done") and "T0002" in sent[0]
    assert not any("Nothing is founded" in s for s in sent)


def _event_line(message: dict[str, Any]) -> bytes:
    return json.dumps({"type": "message_end", "message": message}).encode()


def _tool_result(text: str) -> dict[str, Any]:
    return {
        "role": "toolResult",
        "toolCallId": "call-1",
        "toolName": "bash",
        "content": [{"type": "text", "text": text}],
        "isError": True,
    }


_PROVIDER_ERROR = {
    "role": "assistant",
    "content": [],
    "stopReason": "error",
    "errorMessage": "Provider stream ended without a final response",
}


def test_worker_stopped_by_the_breaker_reports_the_refused_call() -> None:
    problem = "this exact call already ran; its result has not changed."
    events = _module()._WorkerEvents()
    events.feed(
        _event_line(_tool_result(f"Not run: {problem} 1 more refused calls in a row stop the run."))
    )
    events.feed(
        _event_line(
            _tool_result("Not run, and the run is stopped: 3 tool calls in a row were refused.")
        )
    )
    events.feed(_event_line(_PROVIDER_ERROR))

    report = events.final_report("")

    assert "stopped by tau after repeated refused calls" in report
    assert f"the last refusal: {problem})" in report
    assert "more refused calls" not in report
    assert "worker error" not in report

    unstopped = _module()._WorkerEvents()
    unstopped.feed(
        _event_line(_tool_result(f"Not run: {problem} 2 more refused calls in a row stop the run."))
    )
    unstopped.feed(_event_line(_PROVIDER_ERROR))
    assert "(worker error: Provider stream ended" in unstopped.final_report("")
