import json
import tempfile
import unittest
from pathlib import Path

from engine.math_engine import compound_balance, population_growth, validate_answer
from engine.state import GameState, load_state, save_state


class WeekOneMathTests(unittest.TestCase):
    def test_week_one_answers(self) -> None:
        self.assertTrue(validate_answer("feed_cost", 135))
        self.assertAlmostEqual(compound_balance(1200, 0.05, 12, 1), 1261.39, places=2)
        self.assertAlmostEqual(population_growth(1000, 0.02, 5), 1105.17, places=2)
        self.assertTrue(validate_answer("price", 30))

    def test_wrong_answer_is_rejected(self) -> None:
        self.assertFalse(validate_answer("feed_cost", 136))


class StatePersistenceTests(unittest.TestCase):
    def test_state_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "state.json"
            original = GameState(cash=4321.5, reputation=8)
            save_state(original, path)
            restored = load_state(path)
            self.assertEqual(restored.to_dict(), original.to_dict())
            self.assertEqual(json.loads(path.read_text())["cash"], 4321.5)


if __name__ == "__main__":
    unittest.main()
