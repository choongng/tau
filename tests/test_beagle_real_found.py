"""Founding and planning a pursuit against the real, pinned beagle CLI (beagle_real_cli)."""

from __future__ import annotations

import tomllib
from pathlib import Path

import pytest

from beagle_real_cli import (
    GOAL,
    beagle_json,
    founded,
    pinned_beagle,
    task_node,
)
from test_beagle_example_extension import _tool

pytestmark = [pytest.mark.real_beagle, pytest.mark.anyio]


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture
def real_beagle(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    return pinned_beagle(tmp_path, monkeypatch)


async def test_real_found_writes_a_goal_and_a_tree_beagle_accepts(
    tmp_path: Path, real_beagle: Path
) -> None:
    _, tree = await founded(tmp_path)

    goal = tomllib.loads((real_beagle / ".beagle" / "pursuit.toml").read_text())
    assert goal["goal"]["statement"] == GOAL["statement"]
    assert goal["goal"]["criteria"] == GOAL["criteria"]
    hello, bye = task_node(tree, "Hello"), task_node(tree, "Bye")
    assert hello["status"] == bye["status"] == "pending"
    ready = beagle_json(real_beagle, "pursuit", "next", "--json")
    assert [row["id"] for row in ready["ready"]] == [hello["id"]]


async def test_real_plan_splits_a_milestone_into_steps_beagle_files(
    tmp_path: Path, real_beagle: Path
) -> None:
    runtime, tree = await founded(tmp_path)
    hello, bye = task_node(tree, "Hello")["id"], task_node(tree, "Bye")["id"]

    result = await _tool(runtime, "pursuit_plan").execute(
        "c2", {"task": bye, "parts": ["Draft::write bye.txt", "Check::read it back"]}
    )

    tree = beagle_json(real_beagle, "pursuit", "tree", "--json")
    parts = [node for node in tree["nodes"] if node.get("parent") == bye]
    assert [node["title"] for node in parts] == ["Draft", "Check"], result.text
    ready = beagle_json(real_beagle, "pursuit", "next", "--json")
    assert [row["id"] for row in ready["ready"]] == [hello]
