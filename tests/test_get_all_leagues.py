
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from database import db
from database.schema import create_tables
from database.league_repository import (
    save_league,
    get_all_leagues
)


class TestGetAllLeagues(unittest.TestCase):

    def setUp(self):
        self.temp_dir = TemporaryDirectory()

        self.db_patch = patch.object(
            db,
            "DATABASE_PATH",
            Path(self.temp_dir.name) / "test.db"
        )

        self.db_patch.start()
        create_tables()

    def tearDown(self):
        self.db_patch.stop()
        self.temp_dir.cleanup()

    def test_returns_registered_leagues(self):
        save_league(100, "League One")
        save_league(200, "League Two")

        leagues = get_all_leagues()

        self.assertEqual(len(leagues), 2)
        self.assertEqual(leagues[0]["league_id"], 100)
        self.assertEqual(leagues[1]["league_id"], 200)

    def test_returns_empty_list_when_no_leagues(self):
        leagues = get_all_leagues()

        self.assertEqual(leagues, [])


if __name__ == "__main__":
    unittest.main()
