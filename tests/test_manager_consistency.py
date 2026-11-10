import statistics
import unittest
from unittest.mock import patch

from tracker.manager_consistency import calculate_manager_consistency


class TestManagerConsistency(unittest.TestCase):

    def test_manager_consistency(self):
        mock_league = {
            "league": {"name": "Test League"},
            "standings": {
                "results": [
                    {"entry": 101, "entry_name": "Team A"},
                    {"entry": 102, "entry_name": "Team B"},
                    {"entry": 103, "entry_name": "Team C"},
                ]
            }
        }

        mock_histories = {
            101: [
                {"event": 1, "points": 50, "event_transfers_cost": 0},
                {"event": 2, "points": 70, "event_transfers_cost": 4},
                {"event": 3, "points": 40, "event_transfers_cost": 0},
            ],
            102: [
                {"event": 1, "points": 55, "event_transfers_cost": 0},
                {"event": 2, "points": 55, "event_transfers_cost": 0},
                {"event": 3, "points": 55, "event_transfers_cost": 0},
            ],
            103: []
        }

        with patch(
            "tracker.manager_consistency.get_mini_league",
            return_value=mock_league
        ), patch(
            "tracker.manager_consistency.get_manager_history",
            side_effect=lambda manager_id: mock_histories[manager_id]
        ):
            league_name, results = calculate_manager_consistency(123456)

        self.assertEqual(league_name, "Test League")

        # Managers with no completed gameweeks are excluded.
        self.assertEqual(len(results), 2)
        self.assertEqual(
            {manager["manager_id"] for manager in results},
            {101, 102}
        )

        # Team B has identical scores every gameweek.
        self.assertEqual(results[0]["team_name"], "Team B")
        self.assertEqual(results[0]["standard_deviation"], 0)

        # Team A's net scores are 50, 66 and 40.
        team_a = next(
            manager for manager in results
            if manager["manager_id"] == 101
        )

        self.assertEqual(team_a["gameweeks"], 3)
        self.assertEqual(team_a["average_points"], 52)
        self.assertEqual(team_a["best_gw"], 66)
        self.assertEqual(team_a["worst_gw"], 40)

        expected_std = statistics.pstdev([50, 66, 40])

        self.assertAlmostEqual(
            team_a["standard_deviation"],
            expected_std,
            delta=0.000001
        )


if __name__ == "__main__":
    unittest.main()
