
import unittest
from unittest.mock import patch

from database.manager_analytics import calculate_manager_analytics


class TestDatabaseManagerAnalytics(unittest.TestCase):

    def setUp(self):
        self.manager = {
            "manager_id": 1053858,
            "manager_name": "Test Manager",
            "team_name": "Test FC"
        }

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
                "transfer_cost": 4,
                "total_points": 119
            },
            {
                "gameweek": 3,
                "points": 41,
                "transfer_cost": 0,
                "total_points": 160
            }
        ]

    @patch("database.manager_analytics.get_manager_gameweeks")
    @patch("database.manager_analytics.get_manager")
    def test_calculate_analytics(self, mock_manager, mock_history):
        mock_manager.return_value = self.manager
        mock_history.return_value = self.history

        result = calculate_manager_analytics(
            1053858, "2026/27"
        )

        self.assertEqual(result["gameweeks"], 3)
        self.assertEqual(result["total_net_points"], 160)
        self.assertEqual(result["average_points"], 53.33)
        self.assertEqual(
            result["best_gameweek"],
            {"gameweek": 2, "points": 64}
        )
        self.assertEqual(
            result["worst_gameweek"],
            {"gameweek": 3, "points": 41}
        )

    @patch("database.manager_analytics.get_manager")
    def test_missing_manager(self, mock_manager):
        mock_manager.return_value = None

        with self.assertRaises(ValueError):
            calculate_manager_analytics(999999, "2026/27")

    @patch("database.manager_analytics.get_manager_gameweeks")
    @patch("database.manager_analytics.get_manager")
    def test_missing_history(self, mock_manager, mock_history):
        mock_manager.return_value = self.manager
        mock_history.return_value = []

        with self.assertRaises(ValueError):
            calculate_manager_analytics(1053858, "2026/27")


if __name__ == "__main__":
    unittest.main()
