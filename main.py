"""Command-line entry point for Herp & Rodent Haven."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from engine.admin import load_demo_state, preview_week
from engine.events import weekly_event
from engine.math_engine import validate_answer
from engine.state import GameState, load_state, save_state


ROOT = Path(__file__).parent
STATE_PATH = ROOT / "data" / "game_state.json"
ARTIFACTS_PATH = ROOT / "artifacts"


def ask_number(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a number, such as 135 or 1260.60.")


def run_turn(state: GameState) -> None:
    event = weekly_event(state)
    state.cash += event.cash_change
    print(f"\nWeek {state.week} dashboard")
    print(f"Cash: ${state.cash:,.2f} | Debt: ${state.debt:,.2f} | Reputation: {state.reputation}")
    print(f"Market event: {event.title} - {event.message}")
    print("Read docs/week_01_guide.md before entering your ledger answers.\n")

    tasks = [
        ("feed_cost", "Operations: 18 feeder orders cost $7.50 each. Total cost? "),
        ("loan_balance", "Finance: $1,200 at 5% annual interest, compounded monthly for one year. Balance? "),
        ("population", "Biology: 1,000 insects grow continuously at 2% per week for five weeks. Population? "),
        ("price", "Market: Revenue is R(p) = -2p^2 + 120p. Price that maximizes revenue? "),
    ]
    correct = 0
    for key, prompt in tasks:
        answer = ask_number(prompt)
        if validate_answer(key, answer):
            correct += 1
            state.reputation += 2
            print("Correct. +2 reputation.")
        else:
            state.cash -= 10 * state.penalty_multiplier
            print("Not quite. A $10 ledger correction was charged.")

    reflection = input("Reflection: What will you monitor most closely next week, and why?\n> ")
    ARTIFACTS_PATH.mkdir(parents=True, exist_ok=True)
    artifact_path = ARTIFACTS_PATH / f"week_{state.week:02d}_reflection.json"
    artifact_path.write_text(
        json.dumps(
            {
                "week": state.week,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "reflection": reflection,
                "correct_answers": correct,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    state.week += 1
    save_state(state, STATE_PATH)
    display_path = artifact_path.relative_to(ROOT) if artifact_path.is_relative_to(ROOT) else artifact_path
    print(f"Saved reflection to {display_path}")
    print(f"Turn complete. Reputation: {state.reputation}; Cash: ${state.cash:,.2f}")


def run_admin(demo: bool) -> None:
    state = load_demo_state(STATE_PATH) if demo else load_state(STATE_PATH)
    print("Instructor Console")
    print(preview_week(1))
    print(f"Preview settings: complexity {state.math_complexity_level}, market {state.market_volatility}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Herp & Rodent Haven business simulation")
    parser.add_argument("--demo", action="store_true", help="open the instructor preview console")
    parser.add_argument("--admin", action="store_true", help="open the instructor console")
    args = parser.parse_args()
    if args.demo or args.admin:
        run_admin(args.demo)
        return
    run_turn(load_state(STATE_PATH))


if __name__ == "__main__":
    main()
