
import unittest
from unittest.mock import patch

from database.multi_league_sync import sync_selected_leagues


class TestMultiLeagueSync(unittest.TestCase):

    @patch("database.multi_league_sync.sync_gameweeks")
    @patch("database.multi_league_sync.get_league_members")
    @patch("database.multi_league_sync.get_league")
    def test_shared_manager_synchronized_once(
        self,
        mock_league,
        mock_members,
        mock_sync
    ):
        mock_league.side_effect = [
            {"league_name": "League One"},
            {"league_name": "League Two"}
        ]

        mock_members.side_effect = [
            [{"manager_id": 1}, {"manager_id": 2}],
            [{"manager_id": 2}, {"manager_id": 3}]
        ]

        mock_sync.return_value = [
            {"gameweek": 1}
        ]

        result = sync_selected_leagues(
            league_ids=[100, 200]
        )

        self.assertEqual(result["total_leagues"], 2)
        self.assertEqual(result["total_unique_managers"], 3)
        self.assertEqual(result["successful"], 3)
        self.assertEqual(result["failed"], 0)
        self.assertEqual(mock_sync.call_count, 3)

    @patch("database.multi_league_sync.sync_gameweeks")
    @patch("database.multi_league_sync.get_league_members")
    @patch("database.multi_league_sync.get_league")
    def test_continues_after_manager_failure(
        self,
        mock_league,
        mock_members,
        mock_sync
    ):
        mock_league.return_value = {
            "league_name": "League One"
        }

        mock_members.return_value = [
            {"manager_id": 1},
            {"manager_id": 2}
        ]

        mock_sync.side_effect = [
            RuntimeError("API unavailable"),
            [{"gameweek": 1}]
        ]

        result = sync_selected_leagues(
            league_ids=[100]
        )

        self.assertEqual(result["successful"], 1)
        self.assertEqual(result["failed"], 1)
        self.assertEqual(mock_sync.call_count, 2)

    @patch("database.multi_league_sync.get_league")
    def test_unregistered_league_rejected(
        self,
        mock_league
    ):
        mock_league.return_value = None

        with self.assertRaises(ValueError):
            sync_selected_leagues(
                league_ids=[999]
            )

    @patch("database.multi_league_sync.sync_gameweeks")
    @patch("database.multi_league_sync.get_league_members")
    @patch("database.multi_league_sync.get_league")
    def test_request_pacing(
        self,
        mock_league,
        mock_members,
        mock_sync
    ):
        from unittest.mock import Mock

        mock_league.return_value = {
            "league_name": "Test League"
        }

        mock_members.return_value = [
            {"manager_id": 1},
            {"manager_id": 2},
            {"manager_id": 3}
        ]

        mock_sync.return_value = [
            {"gameweek": 1}
        ]

        sleep = Mock()

        result = sync_selected_leagues(
            league_ids=[100],
            request_delay=0.5,
            sleep_func=sleep
        )

        self.assertEqual(result["successful"], 3)
        self.assertEqual(mock_sync.call_count, 3)

        # Three managers require two delays.
        self.assertEqual(sleep.call_count, 2)
        sleep.assert_any_call(0.5)


if __name__ == "__main__":
    unittest.main()
