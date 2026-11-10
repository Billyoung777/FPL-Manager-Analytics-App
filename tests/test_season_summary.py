import unittest
from unittest.mock import patch

from tracker.season_summary import generate_season_summary


class TestSeasonSummary(unittest.TestCase):

    def test_unified_season_summary(self):
        mock_leaderboard = [
            {
                "manager_id": 101,
                "team_name": "Team A",
                "total_points": 150,
                "average_points": 75.0
            }
        ]

        mock_winners = {
            1: [
                {"team_name": "Team A", "points": 80}
            ]
        }

        mock_movements = {
            2: [
                {
                    "manager_id": 101,
                    "team_name": "Team A",
                    "rank": 1,
                    "change": 1
                }
            ]
        }

        mock_consistency = [
            {
                "manager_id": 101,
                "team_name": "Team A",
                "average_points": 75.0,
                "best_gw": 80,
                "worst_gw": 70,
                "standard_deviation": 5.0
            }
        ]

        with (
            patch(
                "tracker.season_summary.build_leaderboard",
                return_value=("Test League", mock_leaderboard)
            ),
            patch(
                "tracker.season_summary.find_gameweek_winners",
                return_value=("Test League", mock_winners)
            ),
            patch(
                "tracker.season_summary.calculate_rank_movements",
                return_value=("Test League", mock_movements)
            ),
            patch(
                "tracker.season_summary.calculate_manager_consistency",
                return_value=("Test League", mock_consistency)
            )
        ):
            summary = generate_season_summary(123456)

        self.assertEqual(summary["league_id"], 123456)
        self.assertEqual(summary["league_name"], "Test League")

        self.assertEqual(summary["leaderboard"], mock_leaderboard)
        self.assertEqual(summary["gameweek_winners"], mock_winners)
        self.assertEqual(summary["rank_movements"], mock_movements)
        self.assertEqual(summary["consistency"], mock_consistency)

        self.assertEqual(
            summary["leaderboard"][0]["total_points"],
            150
        )
        self.assertEqual(
            summary["gameweek_winners"][1][0]["points"],
            80
        )
        self.assertEqual(
            summary["rank_movements"][2][0]["change"],
            1
        )
        self.assertEqual(
            summary["consistency"][0]["standard_deviation"],
            5.0
        )


if __name__ == "__main__":
    unittest.main()
