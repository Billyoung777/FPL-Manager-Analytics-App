import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from database.sync_history_repository import (
    save_sync_history,
    get_latest_sync
)


class TestSyncHistoryRepository(unittest.TestCase):

    def test_save_sync_history(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = Path(temp_dir) / "test_fpl.db"

            connection = sqlite3.connect(db_path)

            connection.execute("""
                CREATE TABLE sync_history (
                    sync_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    season TEXT NOT NULL,
                    status TEXT NOT NULL,
                    successful_managers INTEGER DEFAULT 0,
                    failed_managers INTEGER DEFAULT 0,
                    started_at TEXT NOT NULL,
                    finished_at TEXT NOT NULL
                )
            """)

            connection.commit()
            connection.close()

            def test_connection():
                return sqlite3.connect(db_path)

            with patch(
                "database.sync_history_repository.get_connection",
                side_effect=test_connection
            ):
                sync_id = save_sync_history(
                    season="2026/27",
                    status="success",
                    successful_managers=12,
                    failed_managers=0,
                    started_at="2026-10-14 12:00:00",
                    finished_at="2026-10-14 12:01:00"
                )

            self.assertEqual(sync_id, 1)

            connection = sqlite3.connect(db_path)

            try:
                record = connection.execute("""
                    SELECT season, status,
                           successful_managers, failed_managers
                    FROM sync_history
                    WHERE sync_id = ?
                """, (sync_id,)).fetchone()

                self.assertEqual(
                    record,
                    ("2026/27", "success", 12, 0)
                )

            finally:
                connection.close()


    def get_latest_sync():
        """
        Retrieve the most recent synchronization record.
        """

        connection = get_connection()

        try:
            connection.row_factory = sqlite3.Row

            cursor = connection.execute("""
                SELECT
                    sync_id,
                    season,
                    status,
                    successful_managers,
                    failed_managers,
                    started_at,
                    finished_at
                FROM sync_history
                ORDER BY sync_id DESC
                LIMIT 1
            """)

            record = cursor.fetchone()

            if record is None:
                return None

            return dict(record)

        finally:
            connection.close()

    
    def test_get_latest_sync(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = Path(temp_dir) / "test_fpl.db"

            connection = sqlite3.connect(db_path)

            connection.execute("""
                CREATE TABLE sync_history (
                    sync_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    season TEXT NOT NULL,
                    status TEXT NOT NULL,
                    successful_managers INTEGER DEFAULT 0,
                    failed_managers INTEGER DEFAULT 0,
                    started_at TEXT NOT NULL,
                    finished_at TEXT NOT NULL
                )
            """)

            connection.executemany("""
                INSERT INTO sync_history (
                    season, status, successful_managers,
                    failed_managers, started_at, finished_at
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, [
                (
                    "2026/27", "failed", 0, 12,
                    "2026-10-14 10:00:00",
                    "2026-10-14 10:01:00"
                ),
                (
                    "2026/27", "success", 12, 0,
                    "2026-10-14 12:00:00",
                    "2026-10-14 12:01:00"
                )
            ])

            connection.commit()
            connection.close()

            def test_connection():
                return sqlite3.connect(db_path)

            with patch(
                "database.sync_history_repository.get_connection",
                side_effect=test_connection
            ):
                latest = get_latest_sync()

            self.assertIsNotNone(latest)
            self.assertEqual(latest["sync_id"], 2)
            self.assertEqual(latest["status"], "success")
            self.assertEqual(latest["successful_managers"], 12)
            self.assertEqual(latest["failed_managers"], 0)

    def test_get_latest_sync_when_empty(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = Path(temp_dir) / "test_fpl.db"

            connection = sqlite3.connect(db_path)

            connection.execute("""
                CREATE TABLE sync_history (
                    sync_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    season TEXT NOT NULL,
                    status TEXT NOT NULL,
                    successful_managers INTEGER DEFAULT 0,
                    failed_managers INTEGER DEFAULT 0,
                    started_at TEXT NOT NULL,
                    finished_at TEXT NOT NULL
                )
            """)

            connection.commit()
            connection.close()

            def test_connection():
                return sqlite3.connect(db_path)

            with patch(
                "database.sync_history_repository.get_connection",
                side_effect=test_connection
            ):
                latest = get_latest_sync()

            self.assertIsNone(latest)


if __name__ == "__main__":
    unittest.main()
