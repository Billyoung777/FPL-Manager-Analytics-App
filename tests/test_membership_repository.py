import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from database import db
from database.schema import create_tables
from database.manager_repository import save_manager
from database.league_repository import save_league
from database.membership_repository import (
    save_membership,
    get_league_members
)


class TestMembershipRepository(unittest.TestCase):

    def setUp(self):
        self.temp_dir = TemporaryDirectory()

        self.db_patch = patch.object(
            db,
            "DATABASE_PATH",
            Path(self.temp_dir.name) / "test.db"
        )

        self.db_patch.start()

        create_tables()

        save_manager(1001, "Manager One", "Team One")
        save_manager(1002, "Manager Two", "Team Two")

        save_league(2001, "Test League")

    def tearDown(self):
        self.db_patch.stop()
        self.temp_dir.cleanup()

    def test_save_membership(self):
        save_membership(2001, 1001)

        members = get_league_members(2001)

        self.assertEqual(len(members), 1)
        self.assertEqual(members[0]["manager_id"], 1001)

    def test_duplicate_membership(self):
        save_membership(2001, 1001)
        save_membership(2001, 1001)

        members = get_league_members(2001)

        self.assertEqual(len(members), 1)

    def test_multiple_members(self):
        save_membership(2001, 1001)
        save_membership(2001, 1002)

        members = get_league_members(2001)

        self.assertEqual(len(members), 2)


if __name__ == "__main__":
    unittest.main()
