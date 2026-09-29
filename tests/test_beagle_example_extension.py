"""Tests for the Beagle example extension (`examples/extensions/beagle.py`).

The extension is loaded through a real `ExtensionRuntime` against a fake beagle
checkout, so these exercise its wiring without a beagle install.
"""

from __future__ import annotations

import asyncio
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Any

import pytest

from tau_agent.events import AgentEndEvent
from tau_agent.messages import AssistantMessage, TextContent
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


def _skill(plugins: Path, plugin: str, name: str) -> Path:
    skill = plugins / plugin / "skills" / name
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: {name} skill\n---\n\nBody.\n", encoding="utf-8"
    )
    return skill


@pytest.fixture
def beagle(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """A fake beagle checkout with the three plugins the extension reads."""
    root = tmp_path / "beagle"
    plugins = root / "plugins"
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
    monkeypatch.delenv("BEAGLE_TAU_WORKER", raising=False)
    monkeypatch.chdir(tmp_path)  # the process cwd is not a pursuit unless a test says so
    return root


FAKE_BEAGLE = """\
import json, os, sys
from pathlib import Path

here = Path(os.environ["FAKE_BEAGLE_DIR"])
stdin = sys.stdin.read()
with (here / "calls.jsonl").open("a") as log:
    log.write(json.dumps({"argv": sys.argv[1:], "cwd": os.getcwd(), "stdin": stdin}) + "\\n")
if json.loads(stdin or "{}").get("stop_hook_active"):
    sys.exit(0)  # as beagle's Stop hooks do
reply = here / (sys.argv[2] + ".out")
if len(sys.argv) > 2 and reply.exists():
    sys.stdout.write(reply.read_text())
"""


@pytest.fixture
def fake_beagle(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """A `beagle` that logs each call and prints `<hook>.out` when it exists."""
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


def test_merged_plugin_root_links_loaded_skills(tmp_path: Path, beagle: Path) -> None:
    runtime = _load(tmp_path)
    root = tmp_path / "home-tau" / "beagle-plugin"

    assert runtime.skill_dirs == (root / "skills",)
    linked = sorted(p.name for p in (root / "skills").iterdir())
    # Every beagle-dev / beagle-reference skill, but only the named pursuit ones.
    assert linked == ["containment", "offload", "pursuit-dispatch", "python-coding", "tilth-usage"]
    pursuit = beagle / "plugins" / "beagle-pursuit"
    assert (root / "skills" / "containment").resolve() == pursuit / "skills" / "containment"
    assert (root / "commands").resolve() == pursuit / "commands"
    assert (root / "agents").resolve() == beagle / "plugins" / "beagle-dev" / "agents"
    assert os.environ["CLAUDE_PLUGIN_ROOT"] == str(root)


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


def test_pre_rename_checkout_still_loads_from_campaign(tmp_path: Path, beagle: Path) -> None:
    plugins = beagle / "plugins"
    (plugins / "beagle-pursuit").rename(plugins / "beagle-campaign")

    runtime = _load(tmp_path)

    root = tmp_path / "home-tau" / "beagle-plugin"
    campaign = plugins / "beagle-campaign"
    assert (root / "skills" / "offload").resolve() == campaign / "skills" / "offload"
    assert (root / "commands").resolve() == campaign / "commands"
    registry = runtime.build_command_registry()
    assert registry.get("pursuit") is not None and registry.get("pursuit-run") is not None


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
    assert "Do not offer these commands" in section.body


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


@pytest.mark.anyio
async def test_wakeup_arms_replaces_fires_and_disarms(tmp_path: Path, beagle: Path) -> None:
    runtime, session = _bound(tmp_path)
    session.is_running = True
    wakeup = _tool(runtime, "pursuit_wakeup")

    armed = await wakeup.execute("c1", {"delay_minutes": 0.2})
    assert "armed" in armed.text and "--resuming-in 1" in armed.text
    again = await wakeup.execute("c2", {"delay_minutes": 90, "prompt": "/pursuit-run"})
    assert "replacing the previous wakeup" in again.text
    assert "--resuming-in 60" in again.text

    stopped = await wakeup.execute("c3", {"stop": True})
    assert stopped.text == "pursuit_wakeup: disarmed."
    assert (await wakeup.execute("c4", {"stop": True})).text == (
        "pursuit_wakeup: nothing was armed."
    )
    assert session.followed_up == []


@pytest.mark.anyio
async def test_wakeup_fire_expands_pursuit_run(
    tmp_path: Path, beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    runtime, session = _bound(tmp_path)
    session.is_running = True
    wakeup = _tool(runtime, "pursuit_wakeup")
    loop = asyncio.get_running_loop()
    fired: list[Any] = []

    def call_now(delay: float, callback: Any, *args: Any) -> Any:
        fired.append(delay)
        return loop.call_soon(callback, *args)

    monkeypatch.setattr(loop, "call_later", call_now)
    await wakeup.execute("c1", {"delay_minutes": 2})
    await asyncio.sleep(0)

    assert fired == [120]
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
    session.is_running = True
    loop = asyncio.get_running_loop()
    monkeypatch.setattr(loop, "call_later", lambda delay, cb, *a: loop.call_soon(cb, *a))
    await _tool(runtime, "pursuit_wakeup").execute("c1", {"prompt": "/pursuit next"})
    await asyncio.sleep(0)

    [turn] = session.followed_up
    invocation = parse_skill_invocation(turn)
    assert invocation is not None and invocation.name == "pursuit"
    assert invocation.additional_instructions == "next"


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


def _tool_with_hooks(runtime: ExtensionRuntime) -> Any:
    async def run(*_: Any, **__: Any) -> AgentToolResult:
        return AgentToolResult(content=[TextContent(text="ran")])

    bash = AgentTool(name="bash", label="bash", description="", parameters={}, execute_fn=run)
    [wrapped] = [t for t in runtime.compose_tools([bash]) if t.name == "bash"]
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
    headless, headless_session = _bound(tmp_path, ui=False)
    await headless.emit_event(_end())
    await headless.emit_event(AgentSettledEvent())

    assert session.followed_up == [] and headless_session.followed_up == []
    assert not [c for c in _calls(fake_beagle) if "loop-guard" in c["argv"]]


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
