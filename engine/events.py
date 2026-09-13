"""Small deterministic event surface for the first playable turn."""

from dataclasses import dataclass

from .state import GameState


@dataclass(frozen=True)
class WeeklyEvent:
    title: str
    message: str
    cash_change: float = 0.0


def weekly_event(state: GameState) -> WeeklyEvent:
    if state.market_volatility == "high":
        return WeeklyEvent("Supply squeeze", "Feeder prices rose this week.", -35.0)
    if state.market_volatility == "med":
        return WeeklyEvent("Steady market", "Demand stayed close to forecast.")
    return WeeklyEvent("Quiet market", "Your supplier honored the usual rates.")
