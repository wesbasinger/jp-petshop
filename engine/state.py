"""Persistence and progression state for the simulation."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
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
    # ISO timestamp of the last processed turn; None means no elapsed-time accrual yet.
    last_action_at: str | None = None
    # Safety valve: caps how many real days of accrual a single turn can apply,
    # so a save left untouched for a long break doesn't compound unrealistically.
    max_elapsed_days_per_action: float = 14.0

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "GameState":
        defaults = asdict(cls())
        defaults.update(data)
        return cls(**defaults)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def elapsed_days_since_last_action(state: GameState, now: datetime | None = None) -> float:
    """Real wall-clock days since the last processed turn, clamped by the state's cap."""
    now = now or datetime.now(timezone.utc)
    if state.last_action_at is None:
        return 0.0
    last = datetime.fromisoformat(state.last_action_at)
    elapsed = (now - last).total_seconds() / 86400
    elapsed = max(elapsed, 0.0)
    return min(elapsed, state.max_elapsed_days_per_action)


def mark_action_now(state: GameState, now: datetime | None = None) -> None:
    state.last_action_at = (now or datetime.now(timezone.utc)).isoformat()


# Fields the instructor controls via data/weekly_config.json, synced through git.
# Deliberately excludes cash/debt/reputation/week/last_action_at, which only ever
# change through local play.
WEEKLY_CONFIG_FIELDS = (
    "unlocked_modules",
    "math_complexity_level",
    "market_volatility",
    "penalty_multiplier",
    "max_elapsed_days_per_action",
)


def apply_weekly_config(state: GameState, config_path: Path) -> bool:
    """Merges instructor-controlled fields from weekly_config.json into state. Returns True if anything changed."""
    if not config_path.exists():
        return False
    config = json.loads(config_path.read_text(encoding="utf-8"))
    changed = False
    for field_name in WEEKLY_CONFIG_FIELDS:
        if field_name in config and getattr(state, field_name) != config[field_name]:
            setattr(state, field_name, config[field_name])
            changed = True
    return changed


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
