
import unittest
from unittest.mock import patch

from database.manager_analytics import calculate_manager_analytics


class TestManagerAnalyticsIsolated(unittest.TestCase):

    @patch("database.manager_analytics.get_manager")
    @patch("database.manager_analytics.get_manager_gameweeks")
    def test_analytics_with_sample_data(
        self,
        mock_gameweeks,
        mock_manager
    ):
        mock_manager.return_value = {
            "manager_id": 12345,
            "team_name": "Test FC"
        }

        mock_gameweeks.return_value = [
            {
                "gameweek": 1,
                "points": 50,
                "transfer_cost": 0
            },
            {
                "gameweek": 2,
                "points": 70,
                "transfer_cost": 4
            },
            {
                "gameweek": 3,
                "points": 40,
                "transfer_cost": 0
            }
        ]

        result = calculate_manager_analytics(
            12345,
            "2026/27"
        )

        self.assertEqual(result["total_net_points"], 156)
        self.assertEqual(result["average_points"], 52.0)
        self.assertEqual(result["gameweeks"], 3)

        self.assertEqual(
            result["best_gameweek"],
            {"gameweek": 2, "points": 66}
        )

        self.assertEqual(
            result["worst_gameweek"],
            {"gameweek": 3, "points": 40}
        )

        # Verify consistency (population standard deviation)
        self.assertEqual(result["consistency_std"], 10.71)

        # Verify gameweek-to-gameweek changes
        self.assertEqual(
            result["performance_trends"],
            [
                {"gameweek": 1, "points": 50, "change": None},
                {"gameweek": 2, "points": 66, "change": 16},
                {"gameweek": 3, "points": 40, "change": -26}
            ]
        )
if __name__ == "__main__":
    unittest.main()
