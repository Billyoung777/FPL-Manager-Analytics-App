import unittest
from unittest.mock import patch

from tracker.historical_rankings import calculate_historical_rankings


class TestHistoricalRankings(unittest.TestCase):

    def test_historical_rankings(self):
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
            ],
            102: [
                {"event": 1, "points": 60, "event_transfers_cost": 0},
                {"event": 2, "points": 56, "event_transfers_cost": 0},
            ],
            103: [
                {"event": 1, "points": 40, "event_transfers_cost": 0},
                {"event": 2, "points": 65, "event_transfers_cost": 0},
            ],
        }

        with patch(
            "tracker.historical_rankings.get_mini_league",
            return_value=mock_league
        ), patch(
            "tracker.historical_rankings.get_manager_history",
            side_effect=lambda manager_id: mock_histories[manager_id]
        ):
            league_name, rankings = calculate_historical_rankings(123456)

        self.assertEqual(league_name, "Test League")
        self.assertEqual(sorted(rankings.keys()), [1, 2])

        self.assertEqual(
            [m["team_name"] for m in rankings[1]],
            ["Team B", "Team A", "Team C"]
        )

        self.assertEqual(
            [m["cumulative_points"] for m in rankings[2]],
            [116, 116, 105]
        )

        self.assertEqual(
            [m["rank"] for m in rankings[2]],
            [1, 2, 3]
        )


if __name__ == "__main__":
    unittest.main()
