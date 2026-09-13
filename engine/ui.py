"""Small, dependency-free terminal presentation helpers.

Pure ANSI escapes with a plain-text fallback when the terminal doesn't look
like a TTY (e.g. piped input/output in tests or automation). No external
packages required, so a student only needs the Python that's already there.
"""

from __future__ import annotations

import sys
import time

_RESET = "\x1b[0m"
_BOLD = "\x1b[1m"
_DIM = "\x1b[2m"
_CYAN = "\x1b[36m"
_GREEN = "\x1b[32m"
_YELLOW = "\x1b[33m"
_RED = "\x1b[31m"
_MAGENTA = "\x1b[35m"


def _color_enabled() -> bool:
    return sys.stdout.isatty()


def _wrap(code: str, text: str) -> str:
    if not _color_enabled():
        return text
    return f"{code}{text}{_RESET}"


def bold(text: str) -> str:
    return _wrap(_BOLD, text)


def dim(text: str) -> str:
    return _wrap(_DIM, text)


def success(text: str) -> None:
    print(_wrap(_GREEN, f"✔ {text}"))


def warn(text: str) -> None:
    print(_wrap(_YELLOW, f"⚠ {text}"))


def error(text: str) -> None:
    print(_wrap(_RED, f"✘ {text}"))


def heading(text: str) -> None:
    print()
    print(_wrap(_BOLD + _CYAN, text))
    print(_wrap(_DIM, "-" * len(text)))


def panel(title: str, rows: list[tuple[str, str]]) -> None:
    """A simple bordered box for the weekly dashboard: label/value pairs."""
    label_width = max((len(label) for label, _ in rows), default=0)
    inner_width = max(len(title), max((label_width + 2 + len(value) for label, value in rows), default=0)) + 2
    top = "┌" + "─" * inner_width + "┐"
    bottom = "└" + "─" * inner_width + "┘"
    print(_wrap(_DIM, top))
    print(_wrap(_DIM, "│ ") + bold(title.ljust(inner_width - 1)) + _wrap(_DIM, "│"))
    print(_wrap(_DIM, "├" + "─" * inner_width + "┤"))
    for label, value in rows:
        line = f"{label.ljust(label_width)}  {value}"
        print(_wrap(_DIM, "│ ") + line.ljust(inner_width - 1) + _wrap(_DIM, "│"))
    print(_wrap(_DIM, bottom))


def step_progress(current: int, total: int, label: str) -> None:
    """Restrained step indicator between tasks, e.g. '● ● ○ ○  Task 2 of 4: Finance'."""
    dots = " ".join("●" if i < current else "○" for i in range(total))
    print(f"\n{_wrap(_MAGENTA, dots)}  {dim(f'Task {current} of {total}:')} {bold(label)}")
    if _color_enabled():
        for _ in range(2):
            time.sleep(0.06)
            print(".", end="", flush=True)
        print()
