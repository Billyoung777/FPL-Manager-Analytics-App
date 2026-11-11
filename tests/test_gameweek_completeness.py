
import unittest

from database.gameweek_completeness import (
    check_gameweek_completeness
)


class TestGameweekCompleteness(unittest.TestCase):

    def test_complete_history(self):
        result = check_gameweek_completeness(
            [1, 2, 3, 4],
            [1, 2, 3, 4]
        )

        self.assertEqual(result["status"], "complete")
        self.assertEqual(result["missing_gameweeks"], [])

    def test_incomplete_history(self):
        result = check_gameweek_completeness(
            [1, 2, 4],
            [1, 2, 3, 4]
        )

        self.assertEqual(result["status"], "incomplete")
        self.assertEqual(result["missing_gameweeks"], [3])

    def test_not_synchronized(self):
        result = check_gameweek_completeness(
            [],
            [1, 2, 3]
        )

        self.assertEqual(
            result["status"],
            "not_synchronized"
        )

    def test_unknown_verification(self):
        result = check_gameweek_completeness(
            [1, 2],
            None
        )

        self.assertEqual(result["status"], "unknown")

    def test_duplicate_gameweeks(self):
        result = check_gameweek_completeness(
            [1, 1, 2],
            [1, 2]
        )

        self.assertEqual(result["status"], "complete")
        self.assertEqual(result["stored_count"], 2)


if __name__ == "__main__":
    unittest.main()
