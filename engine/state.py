"""Persistence and progression state for the simulation."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class GameState:
    week: int = 1
    cash: float = 5000.0
    debt: float = 1200.0
    reputation: int = 0
    unlocked_modules: list[str] = field(default_factory=lambda: ["operations"])
    math_complexity_level: int = 1
    market_volatility: str = "low"
    penalty_multiplier: float = 1.0
    assessment_passed_weeks: list[int] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "GameState":
        defaults = asdict(cls())
        defaults.update(data)
        return cls(**defaults)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def load_state(path: Path) -> GameState:
    if not path.exists():
        return GameState()
    with path.open(encoding="utf-8") as state_file:
        return GameState.from_dict(json.load(state_file))


def save_state(state: GameState, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_suffix(path.suffix + ".tmp")
    with temporary_path.open("w", encoding="utf-8") as state_file:
        json.dump(state.to_dict(), state_file, indent=2)
        state_file.write("\n")
    temporary_path.replace(path)
