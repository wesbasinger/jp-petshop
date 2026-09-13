"""Answer calculations and validation for the Week 1 lesson."""

from __future__ import annotations

import hashlib
import math


# Answers are stored as hashes, not plaintext, so a student browsing the shared
# repo can't read them directly. Comparison rounds to the cent before hashing.
WEEK_ONE_ANSWER_HASHES = {
    "feed_cost": "7bb9d03395c83bf7be72070a987605299c6d6538cfe025e1fa0a66c22ef8e340",
    "loan_balance": "022612ce92580cdb62b5428f546558224baf9144293b3a7d86cebd7c647776b8",
    "population": "3ae11572f0705d3161f936c86811c3e3940e74fa105d7d51f35d9e3bd01e8c48",
    "price": "8ff79d510e90a5e4e2fa5ca3430d0cec2c6d64bd53d29ac5e46cb15d7cc43120",
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


def _hash_answer(value: float) -> str:
    return hashlib.sha256(f"{value:.2f}".encode("utf-8")).hexdigest()


def validate_answer(task_key: str, answer: float) -> bool:
    return _hash_answer(round(answer, 2)) == WEEK_ONE_ANSWER_HASHES[task_key]
