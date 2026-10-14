"""A step's close, done and refused, against the real, pinned beagle CLI (beagle_real_cli)."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from beagle_real_cli import (
    beagle_cli,
    beagle_json,
    bound,
    pinned_beagle,
    show,
    step_hello,
)
from test_beagle_example_extension import _module, _tool

pytestmark = [pytest.mark.real_beagle, pytest.mark.anyio]


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture
def real_beagle(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    return pinned_beagle(tmp_path, monkeypatch)


async def test_real_close_ends_done_and_offers_the_next_milestone(
    tmp_path: Path, real_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    hello, bye, result = await step_hello(tmp_path, monkeypatch, {"hello.txt": "hi\n"})
    assert "closed done" in result.text, result.text

    status = beagle_cli(real_beagle, "pursuit", "status").stdout
    counts = dict(line.split()[:2] for line in status.splitlines() if line.startswith("    "))
    # Done: Hello. Pending: the root and Bye, which alone is ready.
    assert counts["done"] == "1" and counts["open"] == "0", status
    assert re.search(r"pending\s+2 \(1 ready\)", status), status
    assert show(real_beagle, hello)["status"] == "done"
    ready = beagle_json(real_beagle, "pursuit", "next", "--json")
    assert [row["id"] for row in ready["ready"]] == [bye]
    runtime = bound(tmp_path)
    shown = await _tool(runtime, "pursuit_step").execute("c4", {})
    assert bye in shown.text, shown.text


async def test_real_close_is_refused_when_the_worker_does_nothing(
    tmp_path: Path, real_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    hello, _, result = await step_hello(tmp_path, monkeypatch, {})

    assert "the check still fails" in result.text and "stays open" in result.text, result.text
    assert "did nothing" in result.text
    assert show(real_beagle, hello)["status"] == "open"
    # beagle agrees: a done close over the failing check is refused, not taken.
    refused = beagle_cli(real_beagle, "pursuit", "close", hello, "--outcome", "done", ok=False)
    assert refused.returncode != 0, refused.stdout
    assert show(real_beagle, hello)["status"] != "done"


async def test_real_prove_runs_isolated_beside_a_live_worker_and_relays_next(
    tmp_path: Path, real_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # T0602: 0.48 refuses a prove in this checkout while another worker's wait is
    # live in the loop; the step proves in a scratch copy (--isolated) instead.
    beagle_cli(real_beagle, "loop", "start", "--by", "test")
    beagle_cli(
        real_beagle, "loop", "tick", "--awaiting", "W9 on T0999", "--wait-id", "W9", "--for", "30"
    )
    hello, _, result = await step_hello(tmp_path, monkeypatch, {"hello.txt": "hi\n"})

    assert "closed done" in result.text, result.text
    assert show(real_beagle, hello)["status"] == "done"
    # The close's `next: beagle pursuit next` comes as the tau call that makes it.
    assert "next: beagle pursuit next" not in result.text
    assert result.text.endswith("Next: call pursuit_step with no arguments for the next task.")
    # Proven, in a scratch copy: in this checkout beagle refuses, naming --isolated.
    assert "in a scratch copy" in show(real_beagle, hello)["refutes"]
    here = beagle_cli(real_beagle, "pursuit", "prove", hello, "--absent", "hello.txt", ok=False)
    assert here.returncode != 0 and "NOT RUN" in here.stderr, here.stderr
    assert f"next: beagle pursuit prove {hello} --isolated" in here.stderr
    # The wait the refusal counted, as the extension reads the loop record.
    record = _module()._json_out(["loop", "read", "--json"], real_beagle)
    assert [wait["id"] for wait in record["waits"]] == ["W9"], record
