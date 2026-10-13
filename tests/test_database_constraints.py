
import sqlite3
import unittest

from database.db import get_connection


class TestDatabaseConstraints(unittest.TestCase):

    def setUp(self):
        self.connection = get_connection()
        self.connection.execute("SAVEPOINT constraint_test")

        self.connection.execute("""
            INSERT INTO managers (
                manager_id, manager_name, team_name
            )
            VALUES (?, ?, ?)
        """, (-900001, "Test Manager", "Test FC"))

    def tearDown(self):
        self.connection.execute("ROLLBACK TO SAVEPOINT constraint_test")
        self.connection.execute("RELEASE SAVEPOINT constraint_test")
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
