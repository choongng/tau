"""Tests for the Beagle example extension (`examples/extensions/beagle.py`).

The extension is loaded through a real `ExtensionRuntime` against a fake beagle
checkout, so these exercise its wiring without a beagle install.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from tau_coding.commands import CommandContext
from tau_coding.extensions import ExtensionRuntime
from tau_coding.resources import TauResourcePaths
from test_extensions import RecordingSession

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
    for name in ("pursuit-dispatch", "offload", "containment", "campaign-planning"):
        _skill(plugins, "beagle-campaign", name)
    commands = plugins / "beagle-campaign" / "commands"
    commands.mkdir()
    (commands / "pursuit.md").write_text(
        "---\ndescription: driver\n---\n\nRead ${CLAUDE_PLUGIN_ROOT}/commands/pursuit.md\n",
        encoding="utf-8",
    )
    agents = plugins / "beagle-dev" / "agents"
    agents.mkdir()
    (agents / "step-executor.md").write_text("You execute one step.\n", encoding="utf-8")

    monkeypatch.setenv("BEAGLE_ROOT", str(root))
    # Recorded so teardown restores whatever the process had; setup overwrites it.
    monkeypatch.setenv("CLAUDE_PLUGIN_ROOT", "/inherited/beagle-dev")
    return root


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
    # Every beagle-dev / beagle-reference skill, but only the pursuit ones from campaign.
    assert linked == ["containment", "offload", "pursuit-dispatch", "python-coding", "tilth-usage"]
    campaign = beagle / "plugins" / "beagle-campaign"
    assert (root / "skills" / "containment").resolve() == campaign / "skills" / "containment"
    assert (root / "commands").resolve() == campaign / "commands"
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
    assert turn.startswith("User input to /pursuit:\ngo\n\n")
    assert f"Read {root}/commands/pursuit.md" in turn
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
