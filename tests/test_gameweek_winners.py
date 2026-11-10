import unittest
from unittest.mock import patch

from tracker.gameweek_winners import find_gameweek_winners


class TestGameweekWinners(unittest.TestCase):

    def test_winner_selection_and_transfer_deductions(self):
        mock_league = {
            "league": {"name": "Test League"},
            "standings": {
                "results": [
                    {"entry": 101, "entry_name": "Team A"},
                    {"entry": 102, "entry_name": "Team B"},
                    {"entry": 103, "entry_name": "Team C"},
                ]
            },
        }

        mock_histories = {
            101: [
                {"event": 1, "points": 60, "event_transfers_cost": 0},
                {"event": 2, "points": 70, "event_transfers_cost": 4},
            ],
            102: [
                {"event": 1, "points": 55, "event_transfers_cost": 0},
                {"event": 2, "points": 66, "event_transfers_cost": 0},
            ],
            103: [
                {"event": 1, "points": 60, "event_transfers_cost": 4},
                {"event": 2, "points": 65, "event_transfers_cost": 0},
            ],
        }

        with patch(
            "tracker.gameweek_winners.get_mini_league",
            return_value=mock_league,
        ), patch(
            "tracker.gameweek_winners.get_manager_history",
            side_effect=lambda manager_id: mock_histories[manager_id],
        ):
            league_name, winners = find_gameweek_winners(123456)

        self.assertEqual(league_name, "Test League")

        self.assertEqual(len(winners[1]), 1)
        self.assertEqual(winners[1][0]["team_name"], "Team A")
        self.assertEqual(winners[1][0]["points"], 60)

        self.assertEqual(len(winners[2]), 2)
        self.assertEqual(
            {manager["team_name"] for manager in winners[2]},
            {"Team A", "Team B"},
        )
        self.assertTrue(
            all(manager["points"] == 66 for manager in winners[2])
        )


if __name__ == "__main__":
    unittest.main()
