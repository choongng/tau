"""Tests for the Beagle example extension (`examples/extensions/beagle.py`).

The extension is loaded through a real `ExtensionRuntime` against a fake beagle
checkout, so these exercise its wiring without a beagle install.
"""

from __future__ import annotations

import asyncio
import json
import os
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
from tau_coding.events import AgentSettledEvent
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
if len(sys.argv) > 2 and reply.exists():
    sys.stdout.write(reply.read_text())
status = here / (sys.argv[2] + ".rc")
if len(sys.argv) > 2 and status.exists():
    sys.exit(int(status.read_text()))
"""


@pytest.fixture
def fake_beagle(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """A `beagle` that logs each call, prints `<argv[2]>.out` when it exists and
    exits with `<argv[2]>.rc`'s status (else 0)."""
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


@pytest.mark.anyio
async def test_worker_runs_no_loop_and_keeps_parent_session(
    tmp_path: Path, beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("BEAGLE_TAU_WORKER", "1")
    runtime, _ = _bound(tmp_path)

    await runtime.emit_session_start("startup")

    assert runtime.build_command_registry().get("pursuit-run") is None
    assert [t.name for t in runtime.compose_tools([])] == ["pursuit_dispatch"]
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
    log.write(json.dumps({"argv": sys.argv[1:], "stdin": brief}) + "\\n")
attempt = len(runs.read_text().splitlines())
if attempt >= int(os.environ.get("FAKE_TAU_SUCCEEDS_ON", "1")):
    Path("done.txt").write_text("done")
message = {
    "role": "assistant",
    "content": [{"type": "text", "text": f"attempt {attempt}: wrote done.txt"}],
    "usage": {"totalTokens": 1000},
    "stopReason": "stop",
}
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


def _ready_task(fake: Path, check: str = "test -f done.txt") -> None:
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
            "done_when": "test -f done.txt",
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
            "test -f done.txt",
            "--scope",
            "done.txt",
        ]
    ]
    first, second = _runs(fake_tau)
    assert first["argv"][:3] == ["-p", "--mode", "json"]
    assert "Do the parser." in first["stdin"] and "Start in the project root." in first["stdin"]
    assert "the check still fails (exit 1)" in second["stdin"]
    [close] = _pursuit_calls(fake_beagle, "close")
    assert close[:3] == ["T0002", "--outcome", "done"]
    assert close[close.index("--spent") + 1] == "2000"
    assert close[close.index("--body") + 1] == "attempt 2: wrote done.txt"
    assert "closed done" in result.text and "pursuit_step with no arguments" in result.text


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
    assert "stays open" in result.text and "--outcome blocked" in result.text


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
    _ready_task(fake_beagle, check="test -f done.txt exits 0 and is good")
    open_task = {"open": ["T0002"], "ready": [], "ready_total": 0}
    (fake_beagle / "next.out").write_text(json.dumps(open_task))
    runtime, _ = _bound(tmp_path)

    stuck = await _tool(runtime, "pursuit_step").execute("c0", {"task": "T0002"})
    assert "cannot pass" in stuck.text and len(_runs(fake_tau)) == 0

    result = await _tool(runtime, "pursuit_step").execute(
        "c1", {"task": "T0002", "done_when": "test -f done.txt"}
    )

    [amend] = _pursuit_calls(fake_beagle, "amend")
    assert amend[:3] == ["T0002", "--done-when", "test -f done.txt"] and "--reason" in amend
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
        "c2", {**args, "done_when": "python3 -c 'import sys; sys.exit(0 and 1)'"}
    )

    assert "reads as a sentence" in prose.text and "'exits'" in prose.text
    assert "runs beagle itself" in beagle_check.text
    [opened] = _pursuit_calls(fake_beagle, "open")
    assert opened[opened.index("--done-when") + 1].startswith("python3 -c")
    assert "reads as a sentence" not in quoted.text


@pytest.mark.anyio
async def test_pursuit_step_runs_the_check_as_words_like_beagle(
    tmp_path: Path,
    beagle: Path,
    fake_beagle: Path,
    fake_tau: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Under `bash -c` this passes once done.txt exists; beagle's close would
    # hand `&&` to `test` and refuse it, blocking the task for good.
    monkeypatch.chdir(_pursuit_project(tmp_path))
    monkeypatch.setenv("FAKE_TAU_SUCCEEDS_ON", "1")
    _ready_task(fake_beagle, check="test -f done.txt && true")
    open_task = {"open": ["T0002"], "ready": [], "ready_total": 0}
    (fake_beagle / "next.out").write_text(json.dumps(open_task))
    runtime, _ = _bound(tmp_path)

    result = await _tool(runtime, "pursuit_step").execute("c1", {"attempts": 1})

    assert _pursuit_calls(fake_beagle, "close") == []
    assert "stays open" in result.text and "corrected done_when" in result.text


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
    assert [before_start.text, store.text, subagent.text, opted_out.text] == ["ran"] * 4


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
