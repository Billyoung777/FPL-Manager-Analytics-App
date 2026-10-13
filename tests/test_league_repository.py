import unittest
from unittest.mock import patch
from tempfile import TemporaryDirectory
from pathlib import Path

from database import db
from database.schema import create_tables
from database.league_repository import save_league, get_league


class TestLeagueRepository(unittest.TestCase):

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

    def test_save_and_update_league(self):
        save_league(1701837, "Original League")

        league = get_league(1701837)
        self.assertEqual(league["league_name"], "Original League")

        save_league(1701837, "Updated League")

        updated = get_league(1701837)
        self.assertEqual(updated["league_name"], "Updated League")

    def test_missing_league(self):
        self.assertIsNone(get_league(99999999))


if __name__ == "__main__":
    unittest.main()
