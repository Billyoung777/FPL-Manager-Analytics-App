
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from database.schema import create_tables


class TestSyncHistoryMigration(unittest.TestCase):

    def test_existing_sync_history_survives_migration(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = Path(temp_dir) / "test_fpl.db"

            connection = sqlite3.connect(db_path)

            try:
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

                connection.execute("""
                    INSERT INTO sync_history (
                        season,
                        status,
                        successful_managers,
                        failed_managers,
                        started_at,
                        finished_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    "2026/27",
                    "success",
                    12,
                    0,
                    "2026-10-14 12:00:00",
                    "2026-10-14 12:01:00"
                ))

                connection.commit()

            finally:
                connection.close()

            def test_connection():
                return sqlite3.connect(db_path)

            with patch(
                "database.schema.get_connection",
                side_effect=test_connection
            ):
                create_tables()
                create_tables()

            connection = sqlite3.connect(db_path)

            try:
                columns = {
                    row[1]
                    for row in connection.execute(
                        "PRAGMA table_info(sync_history)"
                    ).fetchall()
                }

                self.assertTrue({
                    "stage",
                    "error_message",
                    "failed_manager_ids"
                }.issubset(columns))

                record = connection.execute("""
                    SELECT
                        season,
                        status,
                        successful_managers,
                        failed_managers,
                        stage,
                        error_message,
                        failed_manager_ids
                    FROM sync_history
                    WHERE sync_id = 1
                """).fetchone()

                self.assertEqual(
                    record,
                    (
                        "2026/27",
                        "success",
                        12,
                        0,
                        None,
                        None,
                        None
                    )
                )

            finally:
                connection.close()


if __name__ == "__main__":
    unittest.main()
