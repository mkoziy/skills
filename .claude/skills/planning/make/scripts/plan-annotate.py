#!/usr/bin/env python3
"""plan-annotate.py - open a plan copy in $EDITOR via terminal overlay for annotation.

file mode (used by /planning:make interactive review):

    plan-annotate.py docs/plans/foo.md

opens a copy of the plan file in $EDITOR. if the user makes changes,
outputs a unified diff to stdout. claude reads the diff, revises the
plan file, and calls again — looping until no changes.

terminal priority: tmux display-popup → kitty overlay → wezterm split-pane → error
"""

import difflib
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path


def get_diff(original: str, edited: str) -> str:
    orig_lines = original.splitlines(keepends=True)
    edit_lines = edited.splitlines(keepends=True)
    diff = difflib.unified_diff(orig_lines, edit_lines, fromfile="original", tofile="annotated", n=2)
    return "".join(diff)


def open_editor(filepath: Path) -> int:
    editor = os.environ.get("EDITOR", "micro")
    editor_parts = shlex.split(editor)
    resolved = shutil.which(editor_parts[0])
    if resolved:
        editor_parts[0] = resolved
    editor_cmd = " ".join(shlex.quote(p) for p in editor_parts)

    if os.environ.get("TMUX") and shutil.which("tmux"):
        result = subprocess.run(
            ["tmux", "display-popup", "-E", "-w", "90%", "-h", "90%",
             "-T", "Plan Review", "--", "sh", "-c",
             f'{editor_cmd} {shlex.quote(str(filepath))}'],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        return result.returncode

    kitty_sock = os.environ.get("KITTY_LISTEN_ON")
    if kitty_sock and shutil.which("kitty"):
        fd, sentinel_path = tempfile.mkstemp(prefix="plan-done-")
        os.close(fd)
        os.unlink(sentinel_path)
        sentinel = Path(sentinel_path)
        wrapper = f'{editor_cmd} {shlex.quote(str(filepath))}; touch {shlex.quote(str(sentinel))}'
        cmd = ["kitty", "@", "--to", kitty_sock, "launch", "--type=overlay",
               f"--title=Plan Review: {filepath.name}"]
        cmd.extend(["sh", "-c", wrapper])
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        while not sentinel.exists():
            time.sleep(0.3)
        sentinel.unlink(missing_ok=True)
        return 0

    wezterm_pane = os.environ.get("WEZTERM_PANE")
    if wezterm_pane and shutil.which("wezterm"):
        fd, sentinel_path = tempfile.mkstemp(prefix="plan-done-")
        os.close(fd)
        os.unlink(sentinel_path)
        sentinel = Path(sentinel_path)
        wrapper = f'{editor_cmd} {shlex.quote(str(filepath))}; touch {shlex.quote(str(sentinel))}'
        subprocess.run(
            ["wezterm", "cli", "split-pane", "--bottom", "--percent", "80",
             "--pane-id", wezterm_pane, "--", "sh", "-c", wrapper],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        while not sentinel.exists():
            time.sleep(0.3)
        sentinel.unlink(missing_ok=True)
        return 0

    return 1


def main() -> None:
    if len(sys.argv) < 2:
        print("usage: plan-annotate.py <plan-file>", file=sys.stderr)
        sys.exit(1)

    plan_file = Path(sys.argv[1])
    if not plan_file.exists():
        print(f"error: file not found: {plan_file}", file=sys.stderr)
        sys.exit(1)

    plan_content = plan_file.read_text()

    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", prefix="plan-review-", delete=False) as tmp:
        tmp.write(plan_content)
        tmp_path = Path(tmp.name)

    try:
        if open_editor(tmp_path) != 0:
            print("error: no overlay terminal available (requires tmux, kitty, or wezterm)", file=sys.stderr)
            sys.exit(1)

        edited_content = tmp_path.read_text()
        diff = get_diff(plan_content, edited_content)

        if diff:
            print(diff)
    finally:
        tmp_path.unlink(missing_ok=True)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\r\033[K", end="")
        sys.exit(130)
