"""Answer calculations and validation for the Week 1 lesson."""

from __future__ import annotations

import math


WEEK_ONE_ANSWERS = {
    "feed_cost": 135.0,
    "loan_balance": 1261.39,
    "population": 1105.17,
    "price": 30.0,
}


def compound_balance(principal: float, annual_rate: float, compounds: int, years: float) -> float:
    return principal * (1 + annual_rate / compounds) ** (compounds * years)


def population_growth(initial: float, rate: float, weeks: float) -> float:
    return initial * math.exp(rate * weeks)


def accrue_debt_over_days(balance: float, annual_rate: float, elapsed_days: float, compounds_per_year: int = 12) -> float:
    """Applies real elapsed-time compounding to an outstanding balance."""
    if balance <= 0 or elapsed_days <= 0:
        return balance
    return compound_balance(balance, annual_rate, compounds_per_year, elapsed_days / 365)


def population_growth_over_days(initial: float, weekly_rate: float, elapsed_days: float) -> float:
    """Applies real elapsed-time continuous growth, expressed in a weekly rate."""
    return population_growth(initial, weekly_rate, elapsed_days / 7)


def validate_answer(task_key: str, answer: float, tolerance: float = 0.01) -> bool:
    expected = WEEK_ONE_ANSWERS[task_key]
    return math.isclose(answer, expected, rel_tol=0.0, abs_tol=tolerance)
