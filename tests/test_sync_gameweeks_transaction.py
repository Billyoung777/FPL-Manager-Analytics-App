
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from database import db
from database.schema import create_tables
from database.manager_repository import save_manager
from database.gameweek_repository import get_manager_gameweeks
from database.sync_gameweeks import sync_gameweeks


class TestSyncGameweeksTransaction(unittest.TestCase):

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

    @patch("database.sync_gameweeks.FPLClient")
    def test_failed_gameweek_rolls_back_all_writes(
        self,
        mock_client_class
    ):
        mock_client = mock_client_class.return_value

        mock_client.get.return_value = {
            "current": [
                {
                    "event": 8,
                    "points": 50,
                    "event_transfers_cost": 0,
                    "total_points": 400
                },
                {
                    "event": 9,
                    "points": None,
                    "event_transfers_cost": 0,
                    "total_points": 450
                }
            ]
        }

        with self.assertRaises(Exception):
            sync_gameweeks(
                manager_id=1053858,
                season="2026/27",
                completed_gameweeks=[8, 9]
            )

        history = get_manager_gameweeks(
            1053858,
            "2026/27"
        )

        self.assertEqual(
            history,
            [],
            "A failed synchronization must roll back all writes"
        )


if __name__ == "__main__":
    unittest.main()
