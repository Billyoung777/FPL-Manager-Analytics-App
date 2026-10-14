import unittest
import io
from contextlib import redirect_stdout
from unittest.mock import patch
from database.sync_all import sync_all

class TestSyncAll(unittest.TestCase):

    def setUp(self):
        history_patcher = patch(
            "database.sync_all.save_sync_history"
        )

        self.mock_save_history = history_patcher.start()
        self.addCleanup(history_patcher.stop)

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
            sync_result = sync_all()

        result = output.getvalue()

        self.assertEqual(
            sync_result,
            {
                "status": "success",
                "season": "2026/27",
                "successful_leagues": 2,
                "successful_managers": 12,
                "failed_managers": []
            }
        )

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
        self.mock_save_history.assert_called_once()
        
        saved_data = self.mock_save_history.call_args.kwargs

        self.assertEqual(saved_data["season"], "2026/27")
        self.assertEqual(saved_data["status"], "success")
        self.assertEqual(saved_data["successful_managers"], 12)
        self.assertEqual(saved_data["failed_managers"], 0)

        self.assertTrue(saved_data["started_at"])
        self.assertTrue(saved_data["finished_at"])


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

        output = io.StringIO()

        with redirect_stdout(output):
            sync_result = sync_all()

        self.assertEqual(
            sync_result,
            {
                "status": "failed",
                "season": "2026/27",
                "stage": "leagues",
                "successful_leagues": 0,
                "failed_leagues": [1701837, 1840079]
            }
        )

        mock_create_tables.assert_called_once()
        self.assertEqual(mock_memberships.call_count, 2)
        mock_gameweeks.assert_not_called()
        self.mock_save_history.assert_called_once()
        
        saved_data = self.mock_save_history.call_args.kwargs

        self.assertEqual(saved_data["season"], "2026/27")
        self.assertEqual(saved_data["status"], "failed")
        self.assertEqual(saved_data["successful_managers"], 0)
        self.assertEqual(saved_data["failed_managers"], 0)

        self.assertTrue(saved_data["started_at"])
        self.assertTrue(saved_data["finished_at"])


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

        output = io.StringIO()

        with redirect_stdout(output):
            sync_result = sync_all()

        self.assertEqual(
            sync_result,
            {
                "status": "failed",
                "season": "2026/27",
                "stage": "gameweeks",
                "error": "Simulated gameweek API failure"
            }
        )

        mock_create_tables.assert_called_once()
        self.assertEqual(mock_memberships.call_count, 2)
        mock_gameweeks.assert_called_once_with("2026/27")
        self.mock_save_history.assert_called_once()
        
        saved_data = self.mock_save_history.call_args.kwargs

        self.assertEqual(saved_data["season"], "2026/27")
        self.assertEqual(saved_data["status"], "failed")
        self.assertEqual(saved_data["successful_managers"], 0)
        self.assertEqual(saved_data["failed_managers"], 0)

        self.assertTrue(saved_data["started_at"])
        self.assertTrue(saved_data["finished_at"])



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
            sync_result = sync_all()

        result = output.getvalue()

        self.assertEqual(
            sync_result,
            {
                "status": "partial",
                "season": "2026/27",
                "successful_managers": 10,
                "failed_managers": [953118, 1053858]
            }
        )

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
        self.mock_save_history.assert_called_once()
        
        saved_data = self.mock_save_history.call_args.kwargs

        self.assertEqual(saved_data["season"], "2026/27")
        self.assertEqual(saved_data["status"], "partial")
        self.assertEqual(saved_data["successful_managers"], 10)
        self.assertEqual(saved_data["failed_managers"], 2)

        self.assertTrue(saved_data["started_at"])
        self.assertTrue(saved_data["finished_at"])



if __name__ == "__main__":
    unittest.main()
