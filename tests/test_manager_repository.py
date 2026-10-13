
import unittest
from unittest.mock import patch

from database.manager_repository import save_manager, get_manager
from database.db import get_connection


class TestManagerRepository(unittest.TestCase):

    def test_save_and_update_manager(self):
        manager_id = -900002

        try:
            save_manager(manager_id, "Test Manager", "Original FC")

            manager = get_manager(manager_id)

            self.assertIsNotNone(manager)
            self.assertEqual(manager["team_name"], "Original FC")

            save_manager(manager_id, "Test Manager", "Updated FC")

            updated = get_manager(manager_id)

            self.assertEqual(updated["team_name"], "Updated FC")

        finally:
            connection = get_connection()

            try:
                connection.execute(
                    "DELETE FROM managers WHERE manager_id = ?",
                    (manager_id,)
                )
                connection.commit()
            finally:
                connection.close()


if __name__ == "__main__":
    unittest.main()
