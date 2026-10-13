
import unittest
from unittest.mock import patch

from database.verified_gameweeks import get_filtered_gameweeks


class TestVerifiedGameweeks(unittest.TestCase):

    def setUp(self):
        self.history = [
            {
                "gameweek": 1,
                "points": 55,
                "transfer_cost": 0,
                "total_points": 55
            },
            {
                "gameweek": 2,
                "points": 68,
                "transfer_cost": 0,
                "total_points": 123
            },
            {
                "gameweek": 3,
                "points": 41,
                "transfer_cost": 0,
                "total_points": 164
            }
        ]

        self.statuses = [
            {"gameweek": 1, "verified": True},
            {"gameweek": 2, "verified": True},
            {"gameweek": 3, "verified": False}
        ]

    @patch(
        "database.verified_gameweeks.get_gameweek_statuses"
    )
    @patch(
        "database.verified_gameweeks.get_manager_gameweeks"
    )
    def test_verified_mode(self, mock_history, mock_statuses):
        mock_history.return_value = self.history
        mock_statuses.return_value = self.statuses

        result = get_filtered_gameweeks(
            1053858, "2026/27", "verified"
        )

        self.assertEqual(len(result), 2)
        self.assertEqual(
            [gw["gameweek"] for gw in result],
            [1, 2]
        )

    @patch(
        "database.verified_gameweeks.get_gameweek_statuses"
    )
    @patch(
        "database.verified_gameweeks.get_manager_gameweeks"
    )
    def test_provisional_mode(
        self, mock_history, mock_statuses
    ):
        mock_history.return_value = self.history

        result = get_filtered_gameweeks(
            1053858, "2026/27", "provisional"
        )

        self.assertEqual(len(result), 3)
        mock_statuses.assert_not_called()

    def test_invalid_mode(self):
        with self.assertRaises(ValueError):
            get_filtered_gameweeks(
                1053858, "2026/27", "unknown"
            )


if __name__ == "__main__":
    unittest.main()
