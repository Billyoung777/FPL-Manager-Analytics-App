
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from database import db
from database.schema import create_tables
from database.manager_repository import save_manager
from database.gameweek_repository import (
    save_gameweek_performance,
    get_manager_gameweeks
)


class TestGameweekRepository(unittest.TestCase):

    def setUp(self):
        self.temp_dir = TemporaryDirectory()

        self.db_patch = patch.object(
            db,
            "DATABASE_PATH",
            Path(self.temp_dir.name) / "test.db"
        )

        self.db_patch.start()
        create_tables()

        save_manager(
            1053858,
            "Test Manager",
            "Test FPL Team"
        )

    def tearDown(self):
        self.db_patch.stop()
        self.temp_dir.cleanup()

    def test_save_gameweek(self):
        save_gameweek_performance(
            1053858, "2026/27", 1, 55, 0, 55
        )

        history = get_manager_gameweeks(
            1053858, "2026/27"
        )

        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["points"], 55)

    def test_update_gameweek(self):
        save_gameweek_performance(
            1053858, "2026/27", 1, 55, 0, 55
        )

        save_gameweek_performance(
            1053858, "2026/27", 1, 60, 0, 60
        )

        history = get_manager_gameweeks(
            1053858, "2026/27"
        )

        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["points"], 60)

    def test_multiple_gameweeks(self):
        save_gameweek_performance(
            1053858, "2026/27", 1, 55, 0, 55
        )

        save_gameweek_performance(
            1053858, "2026/27", 2, 68, 0, 123
        )

        history = get_manager_gameweeks(
            1053858, "2026/27"
        )

        self.assertEqual(len(history), 2)
        self.assertEqual(
            [gw["gameweek"] for gw in history],
            [1, 2]
        )

    def test_season_isolation(self):
        save_gameweek_performance(
            1053858, "2026/27", 1, 55, 0, 55
        )

        save_gameweek_performance(
            1053858, "2027/28", 1, 70, 0, 70
        )

        history = get_manager_gameweeks(
            1053858, "2026/27"
        )

        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["points"], 55)


if __name__ == "__main__":
    unittest.main()
