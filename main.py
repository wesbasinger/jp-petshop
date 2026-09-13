"""Command-line entry point for Herp & Rodent Haven."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from engine import ui
from engine.admin import load_demo_state, preview_week
from engine.assessment import consume_session, create_session
from engine.events import weekly_event
from engine.git_sync import GitSyncError, submit_artifacts, sync_content
from engine.math_engine import accrue_debt_over_days, validate_answer
from engine.state import (
    GameState,
    apply_weekly_config,
    elapsed_days_since_last_action,
    load_state,
    mark_action_now,
    save_state,
)


ROOT = Path(__file__).parent
STATE_PATH = ROOT / "data" / "game_state.json"
ARTIFACTS_PATH = ROOT / "artifacts"
ASSESSMENT_SESSION_PATH = ROOT / "data" / "assessment_session.json"
WEEKLY_CONFIG_PATH = ROOT / "data" / "weekly_config.json"
DEBT_ANNUAL_RATE = 0.05


def ask_number(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a number, such as 135 or 1260.60.")


def run_turn(state: GameState) -> None:
    now = datetime.now(timezone.utc)
    elapsed_days = elapsed_days_since_last_action(state, now)
    if elapsed_days > 0:
        state.debt = accrue_debt_over_days(state.debt, DEBT_ANNUAL_RATE, elapsed_days)
    event = weekly_event(state, elapsed_days or 7.0)
    state.cash += event.cash_change

    ui.heading(f"Week {state.week} Dashboard")
    if elapsed_days > 0:
        ui.warn(f"{elapsed_days:.1f} real day(s) elapsed since your last turn; debt and market effects were scaled accordingly.")
    ui.panel(
        "Herp & Rodent Haven",
        [
            ("Cash", f"${state.cash:,.2f}"),
            ("Debt", f"${state.debt:,.2f}"),
            ("Reputation", str(state.reputation)),
            ("Market event", f"{event.title} - {event.message}"),
        ],
    )
    print(ui.dim("Read docs/week_01_guide.md before entering your ledger answers."))

    tasks = [
        ("feed_cost", "Operations", "18 feeder orders cost $7.50 each. Total cost? "),
        ("loan_balance", "Finance", "$1,200 at 5% annual interest, compounded monthly for one year. Balance? "),
        ("population", "Biology", "1,000 insects grow continuously at 2% per week for five weeks. Population? "),
        ("price", "Market", "Revenue is R(p) = -2p^2 + 120p. Price that maximizes revenue? "),
    ]
    correct = 0
    for index, (key, category, prompt) in enumerate(tasks, start=1):
        ui.step_progress(index, len(tasks), category)
        answer = ask_number(prompt)
        if validate_answer(key, answer):
            correct += 1
            state.reputation += 2
            ui.success("Correct. +2 reputation.")
        else:
            state.cash -= 10 * state.penalty_multiplier
            ui.warn("Not quite. A $10 ledger correction was charged.")

    ui.heading("Reflection")
    reflection = input("What will you monitor most closely next week, and why?\n> ")
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
    mark_action_now(state, now)
    save_state(state, STATE_PATH)
    display_path = artifact_path.relative_to(ROOT) if artifact_path.is_relative_to(ROOT) else artifact_path
    ui.success(f"Saved reflection to {display_path}")
    ui.heading("Turn Complete")
    print(f"Reputation: {ui.bold(str(state.reputation))}  |  Cash: {ui.bold(f'${state.cash:,.2f}')}")


def assessment_tasks() -> list[tuple[str, str]]:
    return [
        ("feed_cost", "Operations: 18 feeder orders cost $7.50 each. Total cost? "),
        ("loan_balance", "Finance: $1,200 at 5% annual interest, compounded monthly for one year. Balance? "),
        ("population", "Biology: 1,000 insects grow continuously at 2% per week for five weeks. Population? "),
        ("price", "Market: Revenue is R(p) = -2p^2 + 120p. Price that maximizes revenue? "),
    ]


def run_assessment(state: GameState, code: str) -> None:
    session = consume_session(ASSESSMENT_SESSION_PATH, code, state.week)
    ui.heading(f"SUPERVISED ASSESSMENT - Week {session.week}")
    ui.warn("Instructor must remain present. No hints or correctness feedback will be shown.")
    answers = [ask_number(prompt) for _, prompt in assessment_tasks()]
    correct = sum(validate_answer(key, answer) for (key, _), answer in zip(assessment_tasks(), answers))
    passed = correct >= 3
    artifact_path = ARTIFACTS_PATH / f"assessments/week_{state.week:02d}_assessment.json"
    artifact_path.parent.mkdir(parents=True, exist_ok=True)
    artifact_path.write_text(
        json.dumps(
            {
                "week": state.week,
                "created_at": session.created_at,
                "submitted_at": datetime.now(timezone.utc).isoformat(),
                "correct_answers": correct,
                "total_questions": len(answers),
                "passed": passed,
                "supervised": True,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    if passed and state.week not in state.assessment_passed_weeks:
        state.assessment_passed_weeks.append(state.week)
        save_state(state, STATE_PATH)
    result = "passed" if passed else "not passed"
    ui.heading("Assessment Submitted")
    print(f"Result: {ui.bold(result)} ({correct}/{len(answers)}). The instructor can review the assessment artifact.")


def run_admin(demo: bool) -> None:
    state = load_demo_state(STATE_PATH) if demo else load_state(STATE_PATH)
    ui.heading("Instructor Console")
    print(preview_week(1))
    print(f"Preview settings: complexity {state.math_complexity_level}, market {state.market_volatility}")


def create_assessment() -> None:
    state = load_state(STATE_PATH)
    code = create_session(ASSESSMENT_SESSION_PATH, state.week)
    ui.success(f"Created Week {state.week} supervised assessment.")
    print(f"Share this one-time code with the student: {ui.bold(code)}")


def run_sync() -> None:
    try:
        message = sync_content(ROOT)
    except GitSyncError as sync_error:
        ui.error(f"Sync failed: {sync_error}")
        return
    ui.success(message)
    state = load_state(STATE_PATH)
    if apply_weekly_config(state, WEEKLY_CONFIG_PATH):
        save_state(state, STATE_PATH)
        ui.success("Updated your unlocked modules and difficulty settings from the instructor.")


def run_submit() -> None:
    state = load_state(STATE_PATH)
    message = f"Week {state.week} artifacts - {datetime.now(timezone.utc).isoformat()}"
    try:
        result = submit_artifacts(ROOT, message)
    except GitSyncError as submit_error:
        ui.error(f"Submit failed: {submit_error}")
        return
    ui.success(result)


def main() -> None:
    parser = argparse.ArgumentParser(description="Herp & Rodent Haven business simulation")
    parser.add_argument("--demo", action="store_true", help="open the instructor preview console")
    parser.add_argument("--admin", action="store_true", help="open the instructor console")
    parser.add_argument("--create-assessment", action="store_true", help="create a one-time supervised assessment code")
    parser.add_argument("--assessment", action="store_true", help="take the active supervised assessment")
    parser.add_argument("--sync", action="store_true", help="pull the latest instructor content from git")
    parser.add_argument("--submit", action="store_true", help="commit and push your artifacts/ folder to git")
    args = parser.parse_args()
    if args.demo or args.admin:
        run_admin(args.demo)
        return
    if args.create_assessment:
        create_assessment()
        return
    if args.assessment:
        run_assessment(load_state(STATE_PATH), input("Enter the instructor's assessment code: "))
        return
    if args.sync:
        run_sync()
        return
    if args.submit:
        run_submit()
        return
    run_turn(load_state(STATE_PATH))


if __name__ == "__main__":
    main()
