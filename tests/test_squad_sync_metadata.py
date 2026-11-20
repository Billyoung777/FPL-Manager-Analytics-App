
from multiprocessing import connection
import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path
from unittest.mock import patch

from database import schema
from database import squad_repository


MANAGER_ID = 1053858
SEASON = "2026/27"
GAMEWEEK = 10


def make_picks(start_id=100):
    """Generate a valid 15-player FPL squad."""

    return [
        {
            "element": start_id + position,
            "position": position,
            "multiplier": 2 if position == 1 else (
                1 if position <= 11 else 0
            ),
            "is_captain": position == 1,
            "is_vice_captain": position == 2,
        }
        for position in range(1, 16)
    ]


class TestSquadSyncMetadata(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)

        self.db_path = (
            Path(self.temp_dir.name) / "test_squads.db"
        )

        def connect():
            connection = sqlite3.connect(self.db_path)
            connection.execute("PRAGMA foreign_keys = ON")
            return connection

        self.connect = connect

        patcher_schema = patch.object(
            schema, "get_connection", connect
        )
        patcher_repo = patch.object(
            squad_repository, "get_connection", connect
        )

        patcher_schema.start()
        patcher_repo.start()

        self.addCleanup(patcher_schema.stop)
        self.addCleanup(patcher_repo.stop)

        schema.create_tables()

        with closing(self.connect()) as connection:
            with connection:
                connection.execute(
                """
                INSERT INTO managers (
                    manager_id,
                    manager_name,
                    team_name
                )
                VALUES (?, ?, ?)
                """,
                (MANAGER_ID, "Test Manager", "Test FC"),
            )

    def test_save_picks_and_final_status(self):
        picks = make_picks()

        squad_repository.save_manager_picks_with_status(
            MANAGER_ID,
            SEASON,
            GAMEWEEK,
            picks,
            True,
        )

        saved = squad_repository.get_manager_picks(
            MANAGER_ID, SEASON, GAMEWEEK
        )
        status = squad_repository.get_squad_sync_status(
            MANAGER_ID, SEASON, GAMEWEEK
        )

        self.assertEqual(saved, picks)
        self.assertTrue(status["is_final"])
        self.assertIsNotNone(status["last_synced_at"])

    def test_provisional_to_final_transition(self):
        picks = make_picks()

        squad_repository.save_manager_picks_with_status(
            MANAGER_ID, SEASON, GAMEWEEK, picks, False
        )

        provisional = squad_repository.get_squad_sync_status(
            MANAGER_ID, SEASON, GAMEWEEK
        )
        self.assertFalse(provisional["is_final"])

        squad_repository.save_manager_picks_with_status(
            MANAGER_ID, SEASON, GAMEWEEK, picks, True
        )

        final = squad_repository.get_squad_sync_status(
            MANAGER_ID, SEASON, GAMEWEEK
        )
        self.assertTrue(final["is_final"])

    def test_repeated_sync_does_not_duplicate_metadata(self):
        picks = make_picks()

        for _ in range(3):
            squad_repository.save_manager_picks_with_status(
                MANAGER_ID, SEASON, GAMEWEEK, picks, True
            )

        with closing(self.connect()) as connection:
            with connection:
              count = connection.execute(
                """
                SELECT COUNT(*)
                FROM manager_squad_sync_status
                WHERE manager_id = ?
                  AND season = ?
                  AND gameweek = ?
                """,
                (MANAGER_ID, SEASON, GAMEWEEK),
            ).fetchone()[0]

        self.assertEqual(count, 1)

    def test_invalid_squad_preserves_existing_data(self):
        original = make_picks()

        squad_repository.save_manager_picks_with_status(
            MANAGER_ID, SEASON, GAMEWEEK, original, True
        )

        invalid = make_picks(start_id=500)
        invalid[1]["element"] = invalid[0]["element"]

        with self.assertRaises(ValueError):
            squad_repository.save_manager_picks_with_status(
                MANAGER_ID, SEASON, GAMEWEEK, invalid, False
            )

        saved = squad_repository.get_manager_picks(
            MANAGER_ID, SEASON, GAMEWEEK
        )
        status = squad_repository.get_squad_sync_status(
            MANAGER_ID, SEASON, GAMEWEEK
        )

        self.assertEqual(saved, original)
        self.assertTrue(status["is_final"])

    def test_database_failure_rolls_back_both_tables(self):
        original = make_picks()

        squad_repository.save_manager_picks_with_status(
            MANAGER_ID, SEASON, GAMEWEEK, original, True
        )

        # Abort metadata updates after squad replacement has begun.
        # The entire transaction must roll back.
        with closing(self.connect()) as connection:
            with connection:
                connection.execute(
                """
                CREATE TRIGGER block_squad_metadata_update
                BEFORE UPDATE ON manager_squad_sync_status
                BEGIN
                    SELECT RAISE(ABORT, 'Simulated metadata failure');
                END
                """
            )

        replacement = make_picks(start_id=500)

        with self.assertRaises(sqlite3.DatabaseError):
            squad_repository.save_manager_picks_with_status(
                MANAGER_ID, SEASON, GAMEWEEK, replacement, False
            )

        saved = squad_repository.get_manager_picks(
            MANAGER_ID, SEASON, GAMEWEEK
        )
        status = squad_repository.get_squad_sync_status(
            MANAGER_ID, SEASON, GAMEWEEK
        )

        self.assertEqual(saved, original)
        self.assertTrue(status["is_final"])


if __name__ == "__main__":
    unittest.main()

