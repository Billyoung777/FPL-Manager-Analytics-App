
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from database.schema import create_tables
from database.squad_repository import (
    save_manager_picks,
    get_manager_picks,
)


class TestSquadRepository(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test_fpl.db"

        def test_connection():
            connection = sqlite3.connect(self.db_path)
            connection.execute("PRAGMA foreign_keys = ON")
            return connection

        self.connection_patch = patch(
            "database.db.get_connection",
            side_effect=test_connection
        )
        self.schema_patch = patch(
            "database.schema.get_connection",
            side_effect=test_connection
        )
        self.repository_patch = patch(
            "database.squad_repository.get_connection",
            side_effect=test_connection
        )

        self.connection_patch.start()
        self.schema_patch.start()
        self.repository_patch.start()

        create_tables()

        connection = test_connection()
        try:
            connection.execute(
                """
                INSERT INTO managers (
                    manager_id, manager_name, team_name
                ) VALUES (?, ?, ?)
                """,
                (1053858, "Test Manager", "Test FC")
            )
            connection.commit()
        finally:
            connection.close()

        self.manager_id = 1053858
        self.season = "2026/27"
        self.gameweek = 10

        self.picks = [
            {
                "element": 1000 + position,
                "position": position,
                "multiplier": 2 if position == 1 else (
                    1 if position <= 11 else 0
                ),
                "is_captain": position == 1,
                "is_vice_captain": position == 2,
            }
            for position in range(1, 16)
        ]

    def tearDown(self):
        self.repository_patch.stop()
        self.schema_patch.stop()
        self.connection_patch.stop()
        self.temp_dir.cleanup()

    def test_save_and_retrieve_fifteen_picks(self):
        save_manager_picks(
            self.manager_id,
            self.season,
            self.gameweek,
            self.picks
        )

        saved = get_manager_picks(
            self.manager_id,
            self.season,
            self.gameweek
        )

        self.assertEqual(len(saved), 15)
        self.assertEqual(saved, self.picks)
        self.assertTrue(saved[0]["is_captain"])
        self.assertTrue(saved[1]["is_vice_captain"])

    def test_replacing_existing_squad(self):
        save_manager_picks(
            self.manager_id,
            self.season,
            self.gameweek,
            self.picks
        )

        updated = [pick.copy() for pick in self.picks]
        updated[0]["element"] = 9999

        save_manager_picks(
            self.manager_id,
            self.season,
            self.gameweek,
            updated
        )

        saved = get_manager_picks(
            self.manager_id,
            self.season,
            self.gameweek
        )

        self.assertEqual(len(saved), 15)
        self.assertEqual(saved[0]["element"], 9999)

    def test_reject_duplicate_positions(self):
        invalid = [pick.copy() for pick in self.picks]
        invalid[1]["position"] = 1

        with self.assertRaises(ValueError):
            save_manager_picks(
                self.manager_id,
                self.season,
                self.gameweek,
                invalid
            )

    def test_reject_duplicate_players(self):
        invalid = [pick.copy() for pick in self.picks]
        invalid[1]["element"] = invalid[0]["element"]

        with self.assertRaises(ValueError):
            save_manager_picks(
                self.manager_id,
                self.season,
                self.gameweek,
                invalid
            )

    def test_reject_incomplete_squad(self):
        with self.assertRaises(ValueError):
            save_manager_picks(
                self.manager_id,
                self.season,
                self.gameweek,
                self.picks[:14]
            )

    def test_reject_missing_captain(self):
        invalid = [pick.copy() for pick in self.picks]
        invalid[0]["is_captain"] = False

        with self.assertRaises(ValueError):
            save_manager_picks(
                self.manager_id,
                self.season,
                self.gameweek,
                invalid
            )

    def test_failed_write_preserves_existing_squad(self):
        save_manager_picks(
            self.manager_id,
            self.season,
            self.gameweek,
            self.picks
        )

        original = get_manager_picks(
            self.manager_id,
            self.season,
            self.gameweek
        )

        invalid = [pick.copy() for pick in self.picks]
        invalid[0]["element"] = 9999

        # Trigger a database constraint failure after DELETE.
        # This verifies that the transaction rolls back.
        with patch(
            "database.squad_repository.get_connection"
        ) as mocked_connection:

            real_connection = sqlite3.connect(self.db_path)
            real_connection.execute("PRAGMA foreign_keys = ON")

            real_connection.execute("""
                CREATE TRIGGER reject_player
                BEFORE INSERT ON manager_gameweek_picks
                WHEN NEW.player_id = 9999
                BEGIN
                    SELECT RAISE(ABORT, 'Rejected test player');
                END
            """)
            real_connection.commit()
            real_connection.close()

            def connection_factory():
                connection = sqlite3.connect(self.db_path)
                connection.execute("PRAGMA foreign_keys = ON")
                return connection

            mocked_connection.side_effect = connection_factory

            with self.assertRaises(sqlite3.IntegrityError):
                save_manager_picks(
                    self.manager_id,
                    self.season,
                    self.gameweek,
                    invalid
                )

        saved = get_manager_picks(
            self.manager_id,
            self.season,
            self.gameweek
        )

        self.assertEqual(saved, original)

    def test_missing_gameweek_returns_empty_list(self):
        saved = get_manager_picks(
            self.manager_id,
            self.season,
            38
        )

        self.assertEqual(saved, [])


if __name__ == "__main__":
    unittest.main()
