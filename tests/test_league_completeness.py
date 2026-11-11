
import unittest
from unittest.mock import patch

from database.league_completeness import get_manager_completeness


class TestLeagueCompleteness(unittest.TestCase):

    @patch("database.league_completeness.get_manager_gameweeks")
    def test_complete_manager(self, mock_history):
        mock_history.return_value = [
            {"gameweek": 1},
            {"gameweek": 2},
            {"gameweek": 3}
        ]

        result = get_manager_completeness(
            1053858,
            "2026/27",
            [1, 2, 3]
        )

        self.assertEqual(result["status"], "complete")
        self.assertEqual(result["missing_gameweeks"], [])

    @patch("database.league_completeness.get_manager_gameweeks")
    def test_missing_gameweek(self, mock_history):
        mock_history.return_value = [
            {"gameweek": 1},
            {"gameweek": 3}
        ]

        result = get_manager_completeness(
            1053858,
            "2026/27",
            [1, 2, 3]
        )

        self.assertEqual(result["status"], "incomplete")
        self.assertEqual(result["missing_gameweeks"], [2])

    @patch("database.league_completeness.get_manager_gameweeks")
    def test_no_stored_history(self, mock_history):
        mock_history.return_value = []

        result = get_manager_completeness(
            1053858,
            "2026/27",
            [1, 2, 3]
        )

        self.assertEqual(
            result["status"],
            "not_synchronized"
        )

    @patch("database.league_completeness.get_manager_gameweeks")
    def test_verification_unavailable(self, mock_history):
        mock_history.return_value = [
            {"gameweek": 1}
        ]

        result = get_manager_completeness(
            1053858,
            "2026/27",
            None
        )

        self.assertEqual(result["status"], "unknown")


if __name__ == "__main__":
    unittest.main()
