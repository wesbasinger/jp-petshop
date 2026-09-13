"""Instructor-facing preview helpers."""

from pathlib import Path

from .state import GameState, load_state


def preview_week(week: int) -> str:
    if week != 1:
        raise ValueError("Only Week 1 is available in this first slice.")
    return "Week 1: Operations, debt balance, population growth, pricing, and reflection."


def load_demo_state(state_path: Path) -> GameState:
    state = load_state(state_path)
    state.unlocked_modules = ["operations", "finance", "biology", "market"]
    state.math_complexity_level = 3
    state.market_volatility = "med"
    return state
