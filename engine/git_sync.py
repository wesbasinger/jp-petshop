"""Optional git integration for pulling instructor content and pushing student artifacts.

Deliberately conservative: fast-forward-only pulls (no auto-merge), explicit
path staging (never `git add -A`), and no force operations. Any failure raises
GitSyncError with a message meant for a non-technical student to read.
"""

from __future__ import annotations

import subprocess
from pathlib import Path


class GitSyncError(RuntimeError):
    pass


def _run(args: list[str], cwd: Path) -> str:
    result = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        raise GitSyncError(result.stderr.strip() or result.stdout.strip() or f"git {' '.join(args)} failed")
    return result.stdout.strip()


def is_git_repo(root: Path) -> bool:
    try:
        _run(["rev-parse", "--is-inside-work-tree"], root)
        return True
    except GitSyncError:
        return False


def working_tree_is_clean(root: Path) -> bool:
    return _run(["status", "--porcelain"], root) == ""


def current_branch(root: Path) -> str:
    return _run(["rev-parse", "--abbrev-ref", "HEAD"], root)


def sync_content(root: Path) -> str:
    """Fast-forward-only pull of instructor-authored content (docs, engine, weekly_config.json)."""
    if not is_git_repo(root):
        raise GitSyncError("This folder isn't a git repository. Ask the instructor for the shared repo link.")
    if not working_tree_is_clean(root):
        raise GitSyncError("You have local changes outside of normal play. Ask the instructor before syncing.")
    branch = current_branch(root)
    try:
        _run(["fetch", "origin"], root)
        _run(["merge", "--ff-only", f"origin/{branch}"], root)
    except GitSyncError as error:
        raise GitSyncError(
            f"Couldn't fast-forward to the latest content ({error}). Ask the instructor for help "
            "instead of merging manually."
        ) from error
    return f"Synced '{branch}' with the latest instructor content."


def submit_artifacts(root: Path, message: str) -> str:
    """Commits and pushes only the artifacts/ folder."""
    if not is_git_repo(root):
        raise GitSyncError("This folder isn't a git repository. Ask the instructor for the shared repo link.")
    if not (root / "artifacts").exists():
        raise GitSyncError("No artifacts folder found yet. Play a turn first.")
    _run(["add", "--", "artifacts"], root)
    staged = _run(["diff", "--cached", "--name-only"], root)
    if not staged:
        return "Nothing new to submit."
    _run(["commit", "-m", message], root)
    branch = current_branch(root)
    try:
        _run(["push", "origin", branch], root)
    except GitSyncError as error:
        raise GitSyncError(
            f"Saved your artifacts locally, but the push failed ({error}). Ask the instructor to help "
            "push your work next time you're together."
        ) from error
    return f"Submitted artifacts to '{branch}'."
