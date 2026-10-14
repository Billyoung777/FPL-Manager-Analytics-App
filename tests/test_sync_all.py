import unittest
from unittest.mock import patch
import io
from contextlib import redirect_stdout
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
        mock_gameweeks.return_value = (12, [])

        output = io.StringIO()

        with redirect_stdout(output):
            sync_all()

        result = output.getvalue()

        self.assertIn(
            "All tracked managers synchronized successfully.",
            result
        )

        self.assertNotIn(
            "WARNING: PARTIAL SYNCHRONIZATION",
            result
        )

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



    @patch("database.sync_all.sync_all_gameweeks")
    @patch("database.sync_all.sync_league_memberships")
    @patch("database.sync_all.create_tables")
    def test_partial_gameweek_sync(
        self,
        mock_create_tables,
        mock_memberships,
        mock_gameweeks
    ):
        # Simulate 10 successful managers and 2 failures.
        mock_gameweeks.return_value = (
            10,
            [953118, 1053858]
        )

        output = io.StringIO()

        with redirect_stdout(output):
            sync_all()

        result = output.getvalue()

        self.assertIn(
            "WARNING: PARTIAL SYNCHRONIZATION",
            result
        )

        self.assertIn(
            "Successful managers: 10",
            result
        )

        self.assertIn(
            "Failed managers: 2",
            result
        )

        self.assertIn(
            "Failed manager IDs: [953118, 1053858]",
            result
        )

        self.assertNotIn(
            "All tracked managers synchronized successfully.",
            result
        )

        mock_create_tables.assert_called_once()
        self.assertEqual(mock_memberships.call_count, 2)
        mock_gameweeks.assert_called_once_with("2026/27")



if __name__ == "__main__":
    unittest.main()
