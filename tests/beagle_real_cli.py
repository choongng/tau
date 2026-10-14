"""Helpers for the tests of tau's beagle extension against the real beagle CLI.

The extension's unit tests (test_beagle_example_extension.py) run against a
fake `beagle` that prints canned replies, so they kept passing against a beagle
with none of the verbs the extension called. These run the pinned beagle
(`BEAGLE_REAL_ROOT`, by default the 0.48 worktree at ~/beagle-wt/0.48) through
founding, planning and one step's open, worker and close, with a stub worker
standing in for `tau`: test_beagle_real_{found,step,close}.py. Marked
`real_beagle`; a missing CLI fails, never skips.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest

from tau_coding.extensions import ExtensionRuntime
from test_beagle_example_extension import _load, _module, _tool
from test_extensions import RecordingSession, RecordingUiBridge

#: Read before conftest points HOME at each test's tmp_path.
REAL_HOME = Path.home()
REAL_ROOT = Path(os.environ.get("BEAGLE_REAL_ROOT") or REAL_HOME / "beagle-wt/0.48")
REAL_BIN = REAL_ROOT / "plugins" / "beagle-pursuit" / "bin" / "beagle"
#: beagle's shim keeps its venv under the cache; the real one is already built.
REAL_CACHE = Path(os.environ.get("XDG_CACHE_HOME") or REAL_HOME / ".cache")

GIT_ID = {
    "GIT_AUTHOR_NAME": "t",
    "GIT_AUTHOR_EMAIL": "t@example.com",
    "GIT_COMMITTER_NAME": "t",
    "GIT_COMMITTER_EMAIL": "t@example.com",
}

#: A `tau -p --mode json` worker: makes `STUB_TAU_WRITES` (a JSON map of path
#: to text), commits it unless `STUB_TAU_COMMITS` is "0", and reports. With no
#: map it does nothing at all.
STUB_TAU = """\
import json, os, subprocess, sys
from pathlib import Path

brief = sys.stdin.read()
here = Path(os.environ["STUB_TAU_DIR"])
with (here / "runs.jsonl").open("a") as log:
    log.write(json.dumps({"argv": sys.argv[1:], "cwd": os.getcwd(), "stdin": brief}) + "\\n")
writes = json.loads(os.environ.get("STUB_TAU_WRITES") or "{}")
for rel, text in writes.items():
    Path(rel).write_text(text)
if writes and os.environ.get("STUB_TAU_COMMITS") != "0":
    subprocess.run(["git", "add", *writes], check=True)
    subprocess.run(["git", "commit", "--quiet", "-m", "stub worker"], check=True)
report = "made " + ", ".join(writes) if writes else "did nothing"
message = {
    "role": "assistant",
    "content": [{"type": "text", "text": report}],
    "usage": {"totalTokens": 1000},
    "stopReason": "stop",
}
print(json.dumps({"type": "message_end", "message": message}))
"""


def pinned_beagle(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Point the extension at the pinned beagle and a stub `tau` worker; the
    project, a git repo with one commit, made the cwd. Each test file's
    `real_beagle` fixture is this."""
    if not os.access(REAL_BIN, os.X_OK):
        pytest.fail(f"the pinned beagle CLI is missing: {REAL_BIN} (set BEAGLE_REAL_ROOT)")
    monkeypatch.setenv("BEAGLE_ROOT", str(REAL_ROOT))
    monkeypatch.setenv("BEAGLE_BIN", str(REAL_BIN))
    monkeypatch.setattr(_module(), "BEAGLE_BIN", str(REAL_BIN))
    monkeypatch.setenv("XDG_CACHE_HOME", str(REAL_CACHE))
    monkeypatch.setenv("BEAGLE_NO_USAGE_LOG", "1")
    monkeypatch.setenv("BEAGLE_TAU_AGENTS_DIR", str(tmp_path / "agents"))
    monkeypatch.setenv("BEAGLE_TAU_MEMORY_MAX", "off")
    monkeypatch.delenv("BEAGLE_TAU_WORKER", raising=False)
    # Recorded so teardown restores what setup overwrites.
    for name in ("PATH", "CLAUDE_PLUGIN_ROOT", "BEAGLE_HOST"):
        monkeypatch.setenv(name, os.environ.get(name, ""))
    for name, value in GIT_ID.items():
        monkeypatch.setenv(name, value)
    stub = tmp_path / "stub-tau"
    stub.mkdir()
    script = stub / "tau"
    script.write_text(f"#!{sys.executable}\n{STUB_TAU}", encoding="utf-8")
    script.chmod(0o755)
    monkeypatch.setenv("TAU_BIN", str(script))
    monkeypatch.setenv("STUB_TAU_DIR", str(stub))
    project = tmp_path / "project"
    project.mkdir()
    subprocess.run(["git", "init", "--quiet"], cwd=project, check=True)
    (project / "README.md").write_text("A test project.\n")
    subprocess.run(["git", "add", "README.md"], cwd=project, check=True)
    subprocess.run(["git", "commit", "--quiet", "-m", "start"], cwd=project, check=True)
    monkeypatch.chdir(project)
    return project


def beagle_cli(project: Path, *argv: str, ok: bool = True) -> subprocess.CompletedProcess[str]:
    """The real CLI, as a person would run it in the project."""
    done = subprocess.run(
        [str(REAL_BIN), *argv], cwd=project, capture_output=True, text=True, timeout=120
    )
    if ok:
        assert done.returncode == 0, f"beagle {' '.join(argv)}: {done.stdout}\n{done.stderr}"
    return done


def beagle_json(project: Path, *argv: str) -> Any:
    out = beagle_cli(project, *argv).stdout
    return json.loads(out[out.index("{") if out.lstrip()[:1] == "{" else out.index("[") :])


def bound(tmp_path: Path) -> ExtensionRuntime:
    runtime = _load(tmp_path)
    runtime.set_ui_bridge(RecordingUiBridge(has_ui=False))  # type: ignore[arg-type]
    runtime.bind(RecordingSession(tmp_path / "project", running=False))  # type: ignore[arg-type]
    return runtime


GOAL = {
    "statement": "Greet the reader",
    "criteria": ["hello.txt says hi", "bye.txt says bye"],
    "milestones": ["Hello::write hello.txt saying hi", "Bye::write bye.txt saying bye"],
    "user_confirmed": True,
}


async def founded(tmp_path: Path) -> tuple[ExtensionRuntime, dict[str, Any]]:
    runtime = bound(tmp_path)
    result = await _tool(runtime, "pursuit_found").execute("c1", dict(GOAL))
    assert "root task" in result.text, result.text
    project = tmp_path / "project"
    tree = beagle_json(project, "pursuit", "tree", "--json")
    return runtime, tree


def task_node(tree: dict[str, Any], title: str) -> dict[str, Any]:
    [node] = [node for node in tree["nodes"] if node.get("title") == title]
    return node


def show(project: Path, task: str) -> dict[str, Any]:
    return beagle_json(project, "pursuit", "show", task, "--json")


async def step_hello(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, writes: dict[str, str]
) -> tuple[str, str, Any]:
    """Found, then one pursuit_step on the Hello milestone; (its id, Bye's id, result)."""
    runtime, tree = await founded(tmp_path)
    hello, bye = task_node(tree, "Hello")["id"], task_node(tree, "Bye")["id"]
    monkeypatch.setenv("STUB_TAU_WRITES", json.dumps(writes))
    step = _tool(runtime, "pursuit_step")
    shown = await step.execute("c2", {})
    assert hello in shown.text, shown.text
    result = await step.execute(
        "c3",
        {
            "task": hello,
            "criteria": "hello.txt says hi",
            "done_when": "grep -q hi hello.txt",
            "scope": ["hello.txt"],
        },
    )
    return hello, bye, result
