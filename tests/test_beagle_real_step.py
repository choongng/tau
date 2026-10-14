"""One pursuit_step's open, stub worker and close against the real, pinned beagle CLI."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from beagle_real_cli import (
    pinned_beagle,
    show,
    step_hello,
)

pytestmark = [pytest.mark.real_beagle, pytest.mark.anyio]


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture
def real_beagle(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    return pinned_beagle(tmp_path, monkeypatch)


async def test_real_step_opens_dispatches_the_worker_and_closes(
    tmp_path: Path, real_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    hello, _, result = await step_hello(tmp_path, monkeypatch, {"hello.txt": "hi\n"})

    [run] = [json.loads(line) for line in (tmp_path / "stub-tau" / "runs.jsonl").open()]
    assert run["argv"][:3] == ["-p", "--mode", "json"]
    assert hello in run["stdin"]
    record = show(real_beagle, hello)
    assert record["done_when"] == "grep -q hi hello.txt"
    assert record["status"] == "done", result.text
    assert "closed done" in result.text, result.text


async def test_real_step_commits_work_a_worker_left_uncommitted_then_closes(
    tmp_path: Path, real_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # A real worker is refused `git commit`: pursuit_step commits its scope.
    monkeypatch.setenv("STUB_TAU_COMMITS", "0")
    hello, _, result = await step_hello(tmp_path, monkeypatch, {"hello.txt": "hi\n"})

    assert "closed done" in result.text, result.text
    assert show(real_beagle, hello)["status"] == "done"
    tracked = subprocess.run(
        ["git", "log", "--format=%s", "--", "hello.txt"],
        cwd=real_beagle,
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    assert tracked.strip(), result.text
    assert not subprocess.run(
        ["git", "status", "--porcelain", "--", "hello.txt"],
        cwd=real_beagle,
        capture_output=True,
        text=True,
        check=True,
    ).stdout
