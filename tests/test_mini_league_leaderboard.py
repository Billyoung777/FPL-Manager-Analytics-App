import unittest
from unittest.mock import patch

from tracker.mini_league_leaderboard import build_leaderboard


def make_history(points, costs):
    history = []

    for gw, (score, cost) in enumerate(zip(points, costs), start=1):
        history.append({
            "event": gw,
            "points": score,
            "event_transfers_cost": cost
        })

    return history


class TestMiniLeagueLeaderboard(unittest.TestCase):

    def test_leaderboard_ranking_and_scoring(self):
        mock_league = {
            "league": {"name": "Test League"},
            "standings": {
                "results": [
                    {
                        "entry": 101,
                        "entry_name": "Team A",
                        "player_name": "Manager A"
                    },
                    {
                        "entry": 102,
                        "entry_name": "Team B",
                        "player_name": "Manager B"
                    }
                ]
            }
        }

        mock_histories = {
            101: make_history([50, 60, 70], [0, 4, 0]),
            102: make_history([55, 65, 75], [0, 0, 0])
        }

        with patch(
            "tracker.mini_league_leaderboard.get_mini_league",
            return_value=mock_league
        ), patch(
            "tracker.mini_league_leaderboard.get_manager_history",
            side_effect=lambda manager_id: mock_histories[manager_id]
        ):
            league_name, leaderboard = build_leaderboard(123456)

        self.assertEqual(league_name, "Test League")
        self.assertEqual(len(leaderboard), 2)

        # Team B: 55 + 65 + 75 = 195.
        self.assertEqual(leaderboard[0]["team_name"], "Team B")
        self.assertEqual(leaderboard[0]["total_points"], 195)
        self.assertEqual(leaderboard[0]["average_points"], 65.0)

        # Team A: 50 + (60 - 4) + 70 = 176.
        self.assertEqual(leaderboard[1]["team_name"], "Team A")
        self.assertEqual(leaderboard[1]["total_points"], 176)
        self.assertEqual(
            leaderboard[1]["average_points"],
            round(176 / 3, 2)
        )


if __name__ == "__main__":
    unittest.main()
