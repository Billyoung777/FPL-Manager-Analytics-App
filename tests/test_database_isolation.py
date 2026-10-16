
import sqlite3
import unittest
from unittest.mock import patch

from database.schema import create_tables


class TestDatabaseIsolation(unittest.TestCase):

    def test_schema_creation_in_memory(self):
        connection = sqlite3.connect(":memory:")

        connection.execute("PRAGMA foreign_keys = ON")

        try:
            # Prevent create_tables() from closing
            # our in-memory connection.
            class ConnectionWrapper:
                def __init__(self, conn):
                    self.conn = conn

                def execute(self, *args, **kwargs):
                    return self.conn.execute(*args, **kwargs)

                def commit(self):
                    return self.conn.commit()

                def close(self):
                    pass

            wrapper = ConnectionWrapper(connection)

            with patch(
                "database.schema.get_connection",
                return_value=wrapper
            ):
                create_tables()

            tables = {
                row[0]
                for row in connection.execute(
                    """
                    SELECT name
                    FROM sqlite_master
                    WHERE type = 'table'
                    """
                ).fetchall()
            }

            expected_tables = {
                "managers",
                "leagues",
                "league_memberships",
                "gameweek_performances",
                "sync_history"
            }

            self.assertTrue(
                expected_tables.issubset(tables)
            )

        finally:
            connection.close()


if __name__ == "__main__":
    unittest.main()
