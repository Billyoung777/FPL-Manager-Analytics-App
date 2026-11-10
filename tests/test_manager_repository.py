
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from database.schema import create_tables
from database.manager_repository import save_manager, get_manager


class TestManagerRepository(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.database_path = (
            Path(self.temp_dir.name) / "test_managers.db"
        )

        def test_connection():
            connection = sqlite3.connect(self.database_path)
            connection.execute("PRAGMA foreign_keys = ON")
            return connection

        # Initialize the temporary database using the real schema.
        with patch(
            "database.schema.get_connection",
            side_effect=test_connection
        ):
            create_tables()

        # Redirect repository operations to the temporary database.
        self.connection_patch = patch(
            "database.manager_repository.get_connection",
            side_effect=test_connection
        )

        self.connection_patch.start()
        self.addCleanup(self.connection_patch.stop)
        self.addCleanup(self.temp_dir.cleanup)

    def test_save_and_update_manager(self):
        manager_id = -900002

        save_manager(
            manager_id,
            "Test Manager",
            "Original FC"
        )

        manager = get_manager(manager_id)

        self.assertIsNotNone(manager)
        self.assertEqual(
            manager["team_name"],
            "Original FC"
        )

        save_manager(
            manager_id,
            "Test Manager",
            "Updated FC"
        )

        updated = get_manager(manager_id)

        self.assertEqual(
            updated["team_name"],
            "Updated FC"
        )


if __name__ == "__main__":
    unittest.main()
