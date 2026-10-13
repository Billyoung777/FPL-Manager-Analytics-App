
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from database import db
from database.schema import create_tables
from database.manager_repository import save_manager
from database.league_repository import save_league
from database.membership_repository import save_membership
from database.gameweek_repository import save_gameweek_performance
from database.league_analytics import get_database_leaderboard


class TestDatabaseLeagueAnalytics(unittest.TestCase):

    def setUp(self):
        # Use a temporary database for every test.
        self.temp_dir = TemporaryDirectory()

        self.db_patch = patch.object(
            db,
            "DATABASE_PATH",
            Path(self.temp_dir.name) / "test.db"
        )

        self.db_patch.start()
        create_tables()

        # Create test leagues.
        save_league(100, "Test League")
        save_league(200, "Second League")

        # Create test managers.
        save_manager(1, "Manager One", "Team One")
        save_manager(2, "Manager Two", "Team Two")

        # Both managers belong to Test League.
        save_membership(100, 1)
        save_membership(100, 2)

        # Manager One also belongs to Second League.
        save_membership(200, 1)

        # Manager One: 60 + (50 - 4) = 106
        save_gameweek_performance(
            1, "2026/27", 1, 60, 0, 60
        )
        save_gameweek_performance(
            1, "2026/27", 2, 50, 4, 106
        )

        # Manager Two: 55 + 65 = 120
        save_gameweek_performance(
            2, "2026/27", 1, 55, 0, 55
        )
        save_gameweek_performance(
            2, "2026/27", 2, 65, 0, 120
        )

    def tearDown(self):
        self.db_patch.stop()
        self.temp_dir.cleanup()

    def test_leaderboard_ranking(self):
        league_name, leaderboard = get_database_leaderboard(
            100, "2026/27"
        )

        self.assertEqual(league_name, "Test League")
        self.assertEqual(len(leaderboard), 2)

        self.assertEqual(leaderboard[0]["manager_id"], 2)
        self.assertEqual(leaderboard[0]["rank"], 1)
        self.assertEqual(leaderboard[0]["total_points"], 120)

        self.assertEqual(leaderboard[1]["manager_id"], 1)
        self.assertEqual(leaderboard[1]["rank"], 2)
        self.assertEqual(leaderboard[1]["total_points"], 106)

    def test_transfer_deductions(self):
        _, leaderboard = get_database_leaderboard(
            100, "2026/27"
        )

        manager_one = next(
            manager for manager in leaderboard
            if manager["manager_id"] == 1
        )

        self.assertEqual(manager_one["total_points"], 106)
        self.assertEqual(manager_one["average_points"], 53.0)

    def test_multiple_league_membership(self):
        _, leaderboard = get_database_leaderboard(
            200, "2026/27"
        )

        self.assertEqual(len(leaderboard), 1)
        self.assertEqual(leaderboard[0]["manager_id"], 1)
        self.assertEqual(leaderboard[0]["total_points"], 106)

    def test_unknown_league(self):
        with self.assertRaises(ValueError):
            get_database_leaderboard(
                999999, "2026/27"
            )


if __name__ == "__main__":
    unittest.main()
