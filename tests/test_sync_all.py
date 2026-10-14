import unittest
from unittest.mock import patch

from database.sync_all import sync_all


class TestSyncAll(unittest.TestCase):

    @patch("database.sync_all.sync_all_gameweeks")
    @patch("database.sync_all.sync_league_memberships")
    @patch("database.sync_all.create_tables")
    def test_successful_sync(
        self,
        mock_create_tables,
        mock_memberships,
        mock_gameweeks
    ):
        sync_all()

        mock_create_tables.assert_called_once()
        self.assertEqual(mock_memberships.call_count, 2)
        mock_gameweeks.assert_called_once_with("2026/27")

    @patch("database.sync_all.sync_all_gameweeks")
    @patch("database.sync_all.sync_league_memberships")
    @patch("database.sync_all.create_tables")
    def test_league_failure_stops_gameweek_sync(
        self,
        mock_create_tables,
        mock_memberships,
        mock_gameweeks
    ):
        mock_memberships.side_effect = RuntimeError(
            "Simulated API failure"
        )

        sync_all()

        mock_create_tables.assert_called_once()
        self.assertEqual(mock_memberships.call_count, 2)
        mock_gameweeks.assert_not_called()

    @patch("database.sync_all.sync_all_gameweeks")
    @patch("database.sync_all.sync_league_memberships")
    @patch("database.sync_all.create_tables")
    def test_gameweek_failure_is_handled(
        self,
        mock_create_tables,
        mock_memberships,
        mock_gameweeks
    ):
        mock_gameweeks.side_effect = RuntimeError(
            "Simulated gameweek API failure"
        )

        sync_all()

        mock_create_tables.assert_called_once()
        self.assertEqual(mock_memberships.call_count, 2)
        mock_gameweeks.assert_called_once_with("2026/27")


if __name__ == "__main__":
    unittest.main()
