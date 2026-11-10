import unittest
from unittest.mock import patch

from tracker.performance_trends import calculate_performance_trend


class TestPerformanceTrends(unittest.TestCase):

    def test_performance_trend(self):
        mock_history = [
            {"event": 3, "points": 45, "event_transfers_cost": 4},
            {"event": 1, "points": 50, "event_transfers_cost": 0},
            {"event": 2, "points": 70, "event_transfers_cost": 4},
        ]

        with patch(
            "tracker.performance_trends.get_manager_history",
            return_value=mock_history
        ):
            trend = calculate_performance_trend(123456)

        self.assertEqual(len(trend), 3)

        # Confirm gameweeks are ordered correctly.
        self.assertEqual(
            [gw["gameweek"] for gw in trend],
            [1, 2, 3]
        )

        # Net points: 50, 66, 41.
        self.assertEqual(
            [gw["net_points"] for gw in trend],
            [50, 66, 41]
        )

        # Cumulative points: 50, 116, 157.
        self.assertEqual(
            [gw["cumulative_points"] for gw in trend],
            [50, 116, 157]
        )


if __name__ == "__main__":
    unittest.main()
