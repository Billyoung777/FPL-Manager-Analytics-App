
import unittest
from unittest.mock import patch

from database.sync_gameweeks import sync_gameweeks


class TestSyncGameweeksFilter(unittest.TestCase):


    @patch("database.sync_gameweeks.get_connection")
    @patch("database.sync_gameweeks.get_manager_gameweeks")
    @patch("database.sync_gameweeks.save_gameweek_performance")
    @patch("database.sync_gameweeks.get_manager")
    @patch("database.sync_gameweeks.FPLClient")
    def test_only_completed_gameweeks_are_saved(
        self,
        mock_client_class,
        mock_get_manager,
        mock_save,
        mock_get_gameweeks,
        mock_get_connection
    ):
        mock_get_manager.return_value = {"manager_id": 1053858}

        mock_client = mock_client_class.return_value
        mock_client.get.return_value = {
            "current": [
                {
                    "event": gw,
                    "points": 50,
                    "event_transfers_cost": 0,
                    "total_points": gw * 50
                }
                for gw in range(1, 6)
            ]
        }

        mock_get_gameweeks.return_value = []

        sync_gameweeks(
            manager_id=1053858,
            season="2026/27",
            completed_gameweeks=[1, 2, 3]
        )

        self.assertEqual(mock_save.call_count, 3)

        saved_gameweeks = [
            call.kwargs["gameweek"]
            for call in mock_save.call_args_list
        ]

        self.assertEqual(saved_gameweeks, [1, 2, 3])
        
        mock_get_connection.assert_called_once_with()

        connection = mock_get_connection.return_value

        connection.commit.assert_called_once_with()
        connection.rollback.assert_not_called()
        connection.close.assert_called_once_with()

        for call in mock_save.call_args_list:
            self.assertIs(
                call.kwargs["connection"],
                connection
            )



if __name__ == "__main__":
    unittest.main()
