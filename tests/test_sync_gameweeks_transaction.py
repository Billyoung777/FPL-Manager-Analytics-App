
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

    @patch("database.sync_gameweeks.FPLClient")
    def test_failed_sync_preserves_existing_gameweek(
        self,
        mock_client_class
    ):
        from database.gameweek_repository import (
            save_gameweek_performance
        )

        # Store an existing GW8 record.
        save_gameweek_performance(
            manager_id=1053858,
            season="2026/27",
            gameweek=8,
            points=50,
            transfer_cost=0,
            total_points=400
        )

        mock_client = mock_client_class.return_value

        mock_client.get.return_value = {
            "current": [
                {
                    "event": 8,
                    "points": 65,
                    "event_transfers_cost": 0,
                    "total_points": 415
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

        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["gameweek"], 8)
        self.assertEqual(history[0]["points"], 50)
        self.assertEqual(history[0]["total_points"], 400)

    @patch("database.sync_gameweeks.FPLClient")
    def test_failed_sync_can_be_retried_without_duplicates(
        self,
        mock_client_class
    ):
        mock_client = mock_client_class.return_value

        # First attempt: GW8 valid, GW9 invalid.
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

        self.assertEqual(
            get_manager_gameweeks(1053858, "2026/27"),
            []
        )

        # Second attempt: both gameweeks valid.
        mock_client.get.return_value["current"][1]["points"] = 50

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
            [gw["gameweek"] for gw in history],
            [8, 9]
        )

        # Third attempt: repeat synchronization with
        # an updated GW8 score.
        mock_client.get.return_value["current"][0]["points"] = 65

        sync_gameweeks(
            manager_id=1053858,
            season="2026/27",
            completed_gameweeks=[8, 9]
        )

        history = get_manager_gameweeks(
            1053858,
            "2026/27"
        )

        self.assertEqual(len(history), 2)
        self.assertEqual(
            [gw["gameweek"] for gw in history],
            [8, 9]
        )
        self.assertEqual(history[0]["points"], 65)
        self.assertEqual(history[1]["points"], 50)


if __name__ == "__main__":
    unittest.main()
