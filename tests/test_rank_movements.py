import unittest
from unittest.mock import patch

from tracker.rank_movements import calculate_rank_movements


class TestRankMovements(unittest.TestCase):

    def test_rank_movements(self):
        mock_rankings = {
            1: [
                {"manager_id": 101, "team_name": "Team A", "rank": 1},
                {"manager_id": 102, "team_name": "Team B", "rank": 2},
                {"manager_id": 103, "team_name": "Team C", "rank": 3},
            ],
            2: [
                {"manager_id": 103, "team_name": "Team C", "rank": 1},
                {"manager_id": 101, "team_name": "Team A", "rank": 2},
                {"manager_id": 102, "team_name": "Team B", "rank": 3},
            ],
            3: [
                {"manager_id": 103, "team_name": "Team C", "rank": 1},
                {"manager_id": 102, "team_name": "Team B", "rank": 2},
                {"manager_id": 101, "team_name": "Team A", "rank": 3},
            ],
        }

        with patch(
            "tracker.rank_movements.calculate_historical_rankings",
            return_value=("Test League", mock_rankings)
        ):
            league_name, movements = calculate_rank_movements(123456)

        self.assertEqual(league_name, "Test League")
        self.assertEqual(sorted(movements.keys()), [1, 2, 3])

        # GW1: All managers appear for the first time.
        self.assertTrue(
            all(
                manager["change"] is None
                for manager in movements[1]
            )
        )

        # GW2: Team C climbs from 3rd to 1st.
        team_c_gw2 = next(
            manager for manager in movements[2]
            if manager["manager_id"] == 103
        )
        self.assertEqual(team_c_gw2["change"], 2)

        # GW3: Team C remains in 1st place.
        team_c_gw3 = next(
            manager for manager in movements[3]
            if manager["manager_id"] == 103
        )
        self.assertEqual(team_c_gw3["change"], 0)

        # GW3: Team A drops from 2nd to 3rd.
        team_a_gw3 = next(
            manager for manager in movements[3]
            if manager["manager_id"] == 101
        )
        self.assertEqual(team_a_gw3["change"], -1)


if __name__ == "__main__":
    unittest.main()
