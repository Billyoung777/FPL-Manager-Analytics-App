
import sqlite3
import unittest
from unittest.mock import patch

from database.schema import create_tables


class TestDatabaseConstraints(unittest.TestCase):

    def setUp(self):
        # Each test receives a fresh, isolated database.
        self.connection = sqlite3.connect(":memory:")
        self.connection.execute("PRAGMA foreign_keys = ON")

        # create_tables() normally closes its connection.
        # This wrapper keeps the test connection open.
        class ConnectionWrapper:
            def __init__(self, connection):
                self.connection = connection

            def execute(self, *args, **kwargs):
                return self.connection.execute(*args, **kwargs)

            def commit(self):
                return self.connection.commit()

            def close(self):
                pass

        wrapper = ConnectionWrapper(self.connection)

        try:
            with patch(
                "database.schema.get_connection",
                return_value=wrapper
            ):
                create_tables()

            self.connection.execute("""
                INSERT INTO managers (
                    manager_id, manager_name, team_name
                )
                VALUES (?, ?, ?)
            """, (-900001, "Test Manager", "Test FC"))

        except Exception:
            self.connection.close()
            raise

    def tearDown(self):
        self.connection.close()

    def test_duplicate_manager_id(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.connection.execute("""
                INSERT INTO managers (
                    manager_id, manager_name, team_name
                )
                VALUES (?, ?, ?)
            """, (-900001, "Duplicate", "Another FC"))

    def test_invalid_league_membership(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.connection.execute("""
                INSERT INTO league_memberships (
                    league_id, manager_id
                )
                VALUES (?, ?)
            """, (-999999, -900001))

    def test_invalid_gameweek(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.connection.execute("""
                INSERT INTO gameweek_performances (
                    manager_id, season, gameweek,
                    points, transfer_cost, total_points
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (-900001, "2026/27", 39, 50, 0, 50))


if __name__ == "__main__":
    unittest.main()
